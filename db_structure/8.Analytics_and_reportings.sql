-- =================================================================
-- Segment 8: Comprehensive Analytics and Reporting
-- =================================================================
-- This segment focuses on collecting data for business intelligence.
-- It includes tables for raw event tracking and pre-aggregated
-- reports to ensure high performance for analytical queries.

-- Table: analytics_events
-- The raw event stream, capturing every significant user interaction.
CREATE TABLE analytics_events (
    event_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    session_id VARCHAR(255),
    event_type VARCHAR(100) NOT NULL, -- e.g., 'page_view', 'add_to_cart', 'search'
    -- Flexible JSON to store event-specific data.
    event_data_json JSON,
    product_id BIGINT UNSIGNED,
    shop_id BIGINT UNSIGNED,
    order_id BIGINT UNSIGNED,
    ip_address VARCHAR(45),
    user_agent VARCHAR(512),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys are nullable as not all events relate to these entities.
    CONSTRAINT fk_analytics_events_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE SET NULL,
    CONSTRAINT fk_analytics_events_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE SET NULL,
    CONSTRAINT fk_analytics_events_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE SET NULL,
    CONSTRAINT fk_analytics_events_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE SET NULL
);

-- Indexes for analytics_events
-- Time-series index is crucial for analytical queries.
CREATE INDEX idx_analytics_events_created_at ON analytics_events(created_at);
-- Index for filtering events by type.
CREATE INDEX idx_analytics_events_event_type ON analytics_events(event_type);
-- Index for tracing all events within a user session.
CREATE INDEX idx_analytics_events_session_id ON analytics_events(session_id);


-- Table: daily_sales_reports
-- Pre-aggregated daily sales data for fast reporting.
CREATE TABLE daily_sales_reports (
    report_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    report_date DATE NOT NULL,
    -- Can be for a specific shop or platform-wide (NULL).
    shop_id BIGINT UNSIGNED,
    total_orders INT UNSIGNED NOT NULL,
    total_revenue DECIMAL(15, 2) NOT NULL,
    total_commission DECIMAL(15, 2) NOT NULL,
    average_order_value DECIMAL(15, 2) NOT NULL,
    new_customers INT UNSIGNED NOT NULL,
    returning_customers INT UNSIGNED NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE KEY uk_daily_sales_report_date_shop (report_date, shop_id)
);


-- Table: product_analytics
-- Aggregated daily analytics for each product.
CREATE TABLE product_analytics (
    analytics_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT UNSIGNED NOT NULL,
    date DATE NOT NULL,
    views INT UNSIGNED NOT NULL DEFAULT 0,
    clicks INT UNSIGNED NOT NULL DEFAULT 0,
    add_to_cart INT UNSIGNED NOT NULL DEFAULT 0,
    purchases INT UNSIGNED NOT NULL DEFAULT 0,
    revenue DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_analytics_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_product_analytics_date (product_id, date)
);


-- Table: shop_performance
-- Aggregated daily performance metrics for each shop.
CREATE TABLE shop_performance (
    performance_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    date DATE NOT NULL,
    orders_count INT UNSIGNED NOT NULL,
    revenue DECIMAL(15, 2) NOT NULL,
    commission_paid DECIMAL(15, 2) NOT NULL,
    average_rating DECIMAL(3, 2) NOT NULL,
    -- Average time to respond to customer inquiries.
    response_time_hours DECIMAL(10, 2),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_shop_performance_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_shop_performance_date (shop_id, date)
);


-- Table: user_behavior_analytics
-- Aggregated daily analytics on user behavior.
CREATE TABLE user_behavior_analytics (
    behavior_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    pages_viewed INT UNSIGNED NOT NULL,
    time_spent_minutes INT UNSIGNED NOT NULL,
    products_viewed INT UNSIGNED NOT NULL,
    searches_made INT UNSIGNED NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_behavior_analytics_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_user_behavior_date (user_id, date)
);


-- Table: platform_metrics
-- High-level, platform-wide metrics aggregated daily.
CREATE TABLE platform_metrics (
    metric_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    metric_date DATE NOT NULL UNIQUE,
    total_users INT UNSIGNED NOT NULL,
    active_users INT UNSIGNED NOT NULL,
    total_shops INT UNSIGNED NOT NULL,
    active_shops INT UNSIGNED NOT NULL,
    total_orders INT UNSIGNED NOT NULL,
    total_revenue DECIMAL(18, 2) NOT NULL,
    platform_commission DECIMAL(18, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Table: custom_reports
-- Allows users to save the configuration for custom reports they build.
CREATE TABLE custom_reports (
    report_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    report_name VARCHAR(255) NOT NULL,
    report_type VARCHAR(100) NOT NULL,
    -- JSON defining the filters, dimensions, and metrics for the report.
    filters_json JSON NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_run_at TIMESTAMP,

    CONSTRAINT fk_custom_reports_user
        FOREIGN KEY (created_by) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE
);


-- Table: report_schedules
-- Schedules the automatic generation and delivery of reports.
CREATE TABLE report_schedules (
    schedule_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    report_id BIGINT UNSIGNED NOT NULL,
    frequency ENUM('daily', 'weekly', 'monthly') NOT NULL,
    -- JSON array of email addresses or user IDs to receive the report.
    recipients_json JSON NOT NULL,
    next_run_at TIMESTAMP NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_report_schedules_report
        FOREIGN KEY (report_id) REFERENCES custom_reports(report_id)
        ON DELETE CASCADE
);

-- =================================================================
-- Triggers for Automated Analytics Aggregation
-- =================================================================

DELIMITER $$

-- Trigger: trg_after_order_item_insert
-- Purpose: Updates product and shop analytics after a new order item is created.
CREATE TRIGGER trg_after_order_item_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    -- Update product analytics for the purchased product
    INSERT INTO product_analytics (product_id, date, purchases, revenue)
    VALUES (NEW.product_id, CURDATE(), NEW.quantity, NEW.total_price)
    ON DUPLICATE KEY UPDATE
        purchases = purchases + NEW.quantity,
        revenue = revenue + NEW.total_price;

    -- Update shop performance for the relevant shop
    INSERT INTO shop_performance (shop_id, date, orders_count, revenue, commission_paid, average_rating)
    VALUES (NEW.shop_id, CURDATE(), 1, NEW.total_price, NEW.commission_amount, 0)
    ON DUPLICATE KEY UPDATE
        orders_count = orders_count + 1,
        revenue = revenue + NEW.total_price,
        commission_paid = commission_paid + NEW.commission_amount;
END$$

-- Trigger: trg_after_order_insert
-- Purpose: Updates the platform-wide metrics after a new order is created.
CREATE TRIGGER trg_after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Update platform-wide metrics
    INSERT INTO platform_metrics (metric_date, total_users, active_users, total_shops, active_shops, total_orders, total_revenue, platform_commission)
    VALUES (CURDATE(), 0, 0, 0, 0, 1, NEW.total_amount, 0)
    ON DUPLICATE KEY UPDATE
        total_orders = total_orders + 1,
        total_revenue = total_revenue + NEW.total_amount;
END$$


-- Trigger: trg_after_user_profile_insert
-- Purpose: Updates platform metrics when a new user registers.
CREATE TRIGGER trg_after_user_profile_insert
AFTER INSERT ON user_profiles
FOR EACH ROW
BEGIN
    INSERT INTO platform_metrics (metric_date, total_users, active_users, total_shops, active_shops, total_orders, total_revenue, platform_commission)
    VALUES (CURDATE(), 1, 1, 0, 0, 0, 0, 0)
    ON DUPLICATE KEY UPDATE
        total_users = total_users + 1,
        active_users = active_users + 1; -- Assuming new user is active
END$$


-- Trigger: trg_after_shop_insert
-- Purpose: Updates platform metrics when a new shop is created.
CREATE TRIGGER trg_after_shop_insert
AFTER INSERT ON shops
FOR EACH ROW
BEGIN
    INSERT INTO platform_metrics (metric_date, total_users, active_users, total_shops, active_shops, total_orders, total_revenue, platform_commission)
    VALUES (CURDATE(), 0, 0, 1, IF(NEW.status = 'approved', 1, 0), 0, 0, 0)
    ON DUPLICATE KEY UPDATE
        total_shops = total_shops + 1,
        active_shops = active_shops + IF(NEW.status = 'approved', 1, 0);
END$$

DELIMITER ;
