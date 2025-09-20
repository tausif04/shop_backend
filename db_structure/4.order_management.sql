-- =================================================================
-- Segment 4: Comprehensive Order Management and Tracking System
-- =================================================================
-- This segment defines the tables for managing customer orders,
-- payments, shipping, and tracking from creation to delivery.

-- Table: orders
-- The primary table for storing order information.
CREATE TABLE orders (
    order_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- The Keycloak user ID of the customer who placed the order.
    customer_id VARCHAR(255) NOT NULL,
    -- A user-friendly, unique order identifier.
    order_number VARCHAR(50) NOT NULL UNIQUE,
    -- The current state of the order in the fulfillment pipeline.
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'refunded', 'failed') NOT NULL DEFAULT 'pending',
    -- Using DECIMAL for all financial values is crucial to avoid floating-point errors.
    subtotal DECIMAL(12, 2) NOT NULL,
    tax_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    shipping_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    discount_amount DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    total_amount DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    order_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    shipped_date TIMESTAMP NULL,
    delivered_date TIMESTAMP NULL,
    cancelled_date TIMESTAMP NULL,
    notes TEXT,

    -- Foreign key linking to the customer's profile.
    -- ON DELETE NO ACTION prevents deleting a customer with existing orders, forcing a manual review.
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE NO ACTION
);

-- Indexes for orders
-- Index for finding all orders by a specific customer.
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
-- Index on status for efficient querying of orders based on their current state (e.g., all 'processing' orders).
CREATE INDEX idx_orders_status ON orders(status);
-- Index on order_date for time-based reporting and analysis.
CREATE INDEX idx_orders_order_date ON orders(order_date);


-- Table: order_items
-- Stores the individual items included in an order.
CREATE TABLE order_items (
    item_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    product_id BIGINT UNSIGNED NOT NULL,
    variant_id BIGINT UNSIGNED NOT NULL,
    shop_id BIGINT UNSIGNED NOT NULL,
    quantity INT UNSIGNED NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(12, 2) NOT NULL,
    -- Commission details are stored at the time of sale for historical accuracy.
    commission_rate DECIMAL(5, 2) NOT NULL,
    commission_amount DECIMAL(10, 2) NOT NULL,
    -- Status of the individual item, which could differ from the main order status.
    status ENUM('pending', 'shipped', 'delivered', 'cancelled', 'refunded') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys linking the item to the order, product, variant, and shop.
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_order_items_variant
        FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_order_items_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE RESTRICT
);

-- Indexes for order_items
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_order_items_shop_id ON order_items(shop_id);


-- Table: order_addresses
-- Stores the billing and shipping addresses for an order.
CREATE TABLE order_addresses (
    address_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    address_type ENUM('billing', 'shipping') NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    company VARCHAR(255),
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    phone VARCHAR(50),

    -- An order should have only one of each address type.
    UNIQUE KEY uk_order_address_type (order_id, address_type),
    CONSTRAINT fk_order_addresses_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE
);


-- Table: order_status_history
-- Logs every status change for an order, providing a full audit trail.
CREATE TABLE order_status_history (
    history_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    status VARCHAR(50) NOT NULL,
    changed_by VARCHAR(255), -- User ID of who made the change (customer or admin)
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    notification_sent BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT fk_order_status_history_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE
);

-- Indexes for order_status_history
CREATE INDEX idx_order_status_history_order_id ON order_status_history(order_id);


-- Table: order_tracking
-- Stores shipping and tracking information for an order.
CREATE TABLE order_tracking (
    tracking_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    carrier VARCHAR(100),
    tracking_number VARCHAR(255),
    tracking_url VARCHAR(2048),
    status VARCHAR(100), -- Status from the carrier API
    location VARCHAR(255), -- Last known location from carrier
    estimated_delivery DATE,
    last_updated_at TIMESTAMP,

    -- An order can have multiple tracking numbers if items are shipped separately.
    UNIQUE KEY uk_order_tracking_number (order_id, tracking_number),
    CONSTRAINT fk_order_tracking_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE
);


-- Table: order_payments
-- Logs payment attempts and transactions for an order.
CREATE TABLE order_payments (
    payment_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    payment_method VARCHAR(100),
    transaction_id VARCHAR(255), -- From the payment gateway
    amount DECIMAL(12, 2) NOT NULL,
    status ENUM('pending', 'completed', 'failed', 'refunded') NOT NULL,
    -- Store the raw response from the gateway for auditing and debugging.
    gateway_response_json JSON,
    processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_order_payments_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE
);

-- Indexes for order_payments
CREATE INDEX idx_order_payments_transaction_id ON order_payments(transaction_id);


-- Table: order_refunds
-- Manages refund requests and processing.
CREATE TABLE order_refunds (
    refund_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    -- A refund can be for a specific item or the whole order (nullable).
    item_id BIGINT UNSIGNED,
    refund_amount DECIMAL(12, 2) NOT NULL,
    reason TEXT,
    status ENUM('pending', 'approved', 'processed', 'rejected') NOT NULL,
    processed_by VARCHAR(255), -- Admin user ID
    processed_at TIMESTAMP,
    notes TEXT,

    CONSTRAINT fk_order_refunds_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_order_refunds_item
        FOREIGN KEY (item_id) REFERENCES order_items(item_id)
        ON DELETE SET NULL
);

-- Indexes for order_refunds
CREATE INDEX idx_order_refunds_status ON order_refunds(status);


-- Table: shipping_zones
-- Defines shipping regions and their associated rates.
CREATE TABLE shipping_zones (
    zone_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    zone_name VARCHAR(255) NOT NULL,
    -- JSON array of country codes, e.g., ["US", "CA"].
    countries_json JSON,
    -- Flexible JSON structure to define different shipping rates (e.g., by weight, flat rate).
    shipping_rates_json JSON,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
