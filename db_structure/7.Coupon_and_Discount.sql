-- =================================================================
-- Segment 7: Flexible Coupon and Discount Management System
-- =================================================================
-- This segment provides a flexible system for creating and managing
-- various types of discounts, coupons, and promotional campaigns.
-- It includes robust tracking to prevent abuse and analyze performance.

-- Table: coupons
-- The central table for defining individual discount coupons.
CREATE TABLE coupons (
    coupon_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- A coupon can be platform-wide (shop_id is NULL) or shop-specific.
    shop_id BIGINT UNSIGNED,
    coupon_code VARCHAR(100) NOT NULL UNIQUE,
    coupon_name VARCHAR(255),
    description TEXT,
    discount_type ENUM('percentage', 'fixed_amount', 'free_shipping') NOT NULL,
    -- The value of the discount (e.g., 10.0 for 10%, or 25.00 for $25).
    discount_value DECIMAL(10, 2) NOT NULL,
    minimum_order_amount DECIMAL(12, 2),
    maximum_discount_amount DECIMAL(12, 2), -- Useful for percentage discounts.
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    starts_at TIMESTAMP,
    expires_at TIMESTAMP,
    -- Total number of times the coupon can be used across all customers.
    usage_limit INT UNSIGNED,
    -- How many times a single customer can use this coupon.
    usage_limit_per_customer INT UNSIGNED,
    created_by VARCHAR(255), -- Keycloak ID of the admin/shop owner who created it.
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_coupons_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE
);

-- Indexes for coupons
CREATE INDEX idx_coupons_shop_id ON coupons(shop_id);
CREATE INDEX idx_coupons_is_active_dates ON coupons(is_active, starts_at, expires_at);


-- Table: coupon_usage
-- Logs every instance a coupon is successfully used in an order.
CREATE TABLE coupon_usage (
    usage_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    coupon_id BIGINT UNSIGNED NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    order_id BIGINT UNSIGNED NOT NULL,
    discount_amount DECIMAL(12, 2) NOT NULL,
    used_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_coupon_usage_coupon
        FOREIGN KEY (coupon_id) REFERENCES coupons(coupon_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_coupon_usage_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_coupon_usage_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    -- An order can only have one usage record for a specific coupon.
    UNIQUE KEY uk_coupon_order (coupon_id, order_id)
);

-- Indexes for coupon_usage
CREATE INDEX idx_coupon_usage_user_id ON coupon_usage(user_id);


-- Table: discount_policies
-- For creating complex, rule-based discounts (e.g., "Buy 2, Get 1 Free").
CREATE TABLE discount_policies (
    policy_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    policy_name VARCHAR(255) NOT NULL,
    policy_type ENUM('bulk_purchase', 'category_wide', 'customer_group') NOT NULL,
    -- JSON to define the rules, e.g., {"min_quantity": 3, "category_id": 12}.
    conditions_json JSON NOT NULL,
    -- JSON to define the discount, e.g., {"type": "percentage", "value": 15}.
    discount_json JSON NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    -- Priority to resolve conflicts if multiple policies apply. Higher number = higher priority.
    priority INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_discount_policies_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE
);


-- Table: promotional_campaigns
-- Manages marketing campaigns that might include multiple coupons or discounts.
CREATE TABLE promotional_campaigns (
    campaign_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- Can be a platform-wide or shop-specific campaign.
    shop_id BIGINT UNSIGNED,
    campaign_name VARCHAR(255) NOT NULL,
    campaign_type VARCHAR(100), -- e.g., 'Summer Sale', 'New Customer Offer'
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15, 2),
    -- JSON to define the target audience, e.g., {"countries": ["US", "CA"], "min_purchase_history": 5}.
    target_audience_json JSON,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_promotional_campaigns_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE
);


-- Table: campaign_coupons
-- A junction table to link coupons to a promotional campaign.
CREATE TABLE campaign_coupons (
    campaign_coupon_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    campaign_id BIGINT UNSIGNED NOT NULL,
    coupon_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_campaign_coupons_campaign
        FOREIGN KEY (campaign_id) REFERENCES promotional_campaigns(campaign_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_campaign_coupons_coupon
        FOREIGN KEY (coupon_id) REFERENCES coupons(coupon_id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_campaign_coupon (campaign_id, coupon_id)
);


-- Table: customer_discount_eligibility
-- Stores pre-calculated eligibility for specific customers for complex discounts.
CREATE TABLE customer_discount_eligibility (
    eligibility_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(255) NOT NULL,
    discount_policy_id BIGINT UNSIGNED NOT NULL,
    is_eligible BOOLEAN NOT NULL DEFAULT FALSE,
    calculated_at TIMESTAMP NOT NULL,

    CONSTRAINT fk_customer_discount_eligibility_customer
        FOREIGN KEY (customer_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_customer_discount_eligibility_policy
        FOREIGN KEY (discount_policy_id) REFERENCES discount_policies(policy_id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_customer_policy (customer_id, discount_policy_id)
);


-- Table: discount_usage_analytics
-- Denormalized table for tracking the performance of coupons and discounts over time.
CREATE TABLE discount_usage_analytics (
    analytics_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    coupon_id BIGINT UNSIGNED,
    date DATE NOT NULL,
    usage_count INT UNSIGNED NOT NULL,
    total_discount_amount DECIMAL(15, 2) NOT NULL,
    -- A metric to estimate the sales generated by the discount.
    revenue_impact DECIMAL(15, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_discount_usage_analytics_coupon
        FOREIGN KEY (coupon_id) REFERENCES coupons(coupon_id)
        ON DELETE SET NULL,
    UNIQUE KEY uk_coupon_date (coupon_id, date)
);
