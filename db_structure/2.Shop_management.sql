-- =================================================================
-- Segment 2: Multi-Vendor Shop Management System
-- =================================================================
-- This segment defines the tables necessary for operating a
-- multi-vendor marketplace, where each shop is a distinct entity.

-- Table: shops
-- The central table for storing information about each vendor's shop.
CREATE TABLE shops (
    shop_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- The Keycloak user ID of the shop owner.
    owner_id VARCHAR(255) NOT NULL,
    shop_name VARCHAR(255) NOT NULL,
    -- A URL-friendly version of the shop name. Must be unique.
    shop_slug VARCHAR(255) NOT NULL UNIQUE,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    address TEXT,
    zip_code VARCHAR(20),
    phone VARCHAR(50),
    email VARCHAR(255),
    description TEXT,
    logo_url VARCHAR(2048),
    banner_url VARCHAR(2048),
    -- The approval status of the shop, controlled by platform admins.
    status ENUM('pending', 'approved', 'suspended', 'rejected') NOT NULL DEFAULT 'pending',
    approval_date TIMESTAMP NULL,
    approved_by VARCHAR(255), -- Keycloak ID of the admin who approved it
    -- Commission rate for sales from this shop. Can be overridden from a category default.
    commission_rate DECIMAL(5, 2) NOT NULL DEFAULT 10.00,
    minimum_payout_amount DECIMAL(10, 2) NOT NULL DEFAULT 50.00,
    shop_type VARCHAR(100), -- e.g., 'Retail', 'Handmade', 'Services'
    business_license VARCHAR(255),
    tax_id VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign key linking a shop to its owner in the user_profiles table.
    -- ON DELETE RESTRICT prevents deleting a user who owns a shop, ensuring business logic is handled first.
    CONSTRAINT fk_shops_owner
        FOREIGN KEY (owner_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE RESTRICT
);

-- Indexes for shops
-- Index on owner_id to quickly find all shops owned by a user.
CREATE INDEX idx_shops_owner_id ON shops(owner_id);
-- Index on shop_slug is created automatically by the UNIQUE constraint.
-- Index on status for efficient filtering of shops by their status (e.g., finding all pending shops).
CREATE INDEX idx_shops_status ON shops(status);
-- Full-text index for searching shop names and descriptions. Crucial for user-facing search functionality.
CREATE FULLTEXT INDEX ft_shops_name_description ON shops(shop_name, description);


-- Table: shop_categories
-- Defines the categories that shops can be assigned to.
CREATE TABLE shop_categories (
    category_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    -- Allows overriding the default platform commission rate for shops in this category.
    commission_rate_override DECIMAL(5, 2) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Table: shop_category_assignments
-- A junction table to link shops to one or more categories (many-to-many relationship).
CREATE TABLE shop_category_assignments (
    assignment_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    category_id BIGINT UNSIGNED NOT NULL,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key to the shops table.
    CONSTRAINT fk_shop_category_assignments_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE,
    -- Foreign key to the shop_categories table.
    CONSTRAINT fk_shop_category_assignments_category
        FOREIGN KEY (category_id) REFERENCES shop_categories(category_id)
        ON DELETE CASCADE,
    -- Ensures a shop cannot be assigned to the same category twice.
    UNIQUE KEY uk_shop_category (shop_id, category_id)
);


-- Table: shop_policies
-- Stores various policy documents for a shop.
CREATE TABLE shop_policies (
    policy_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    return_policy TEXT,
    shipping_policy TEXT,
    privacy_policy TEXT,
    terms_of_service TEXT,
    refund_policy TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- A shop should only have one set of policies.
    UNIQUE KEY uk_shop_policies_shop_id (shop_id),
    -- Foreign key to the shops table.
    CONSTRAINT fk_shop_policies_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE
);


-- Table: shop_settings
-- A key-value store for shop-specific settings.
CREATE TABLE shop_settings (
    setting_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    setting_key VARCHAR(100) NOT NULL,
    setting_value TEXT NOT NULL,
    setting_type VARCHAR(50), -- e.g., 'string', 'number', 'boolean', 'json'
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign key to the shops table.
    CONSTRAINT fk_shop_settings_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE,
    -- Ensures a setting key is unique for each shop.
    UNIQUE KEY uk_shop_setting (shop_id, setting_key)
);


-- Table: shop_staff
-- Manages staff members for a shop and their roles/permissions.
CREATE TABLE shop_staff (
    staff_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    -- The Keycloak user ID of the staff member.
    user_id VARCHAR(255) NOT NULL,
    role ENUM('manager', 'staff', 'viewer') NOT NULL,
    -- JSON field for granular permissions, offering flexibility beyond simple roles.
    permissions_json JSON,
    hired_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive') NOT NULL DEFAULT 'active',

    -- Foreign key to the shops table.
    CONSTRAINT fk_shop_staff_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE,
    -- Foreign key to the user_profiles table.
    CONSTRAINT fk_shop_staff_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    -- Ensures a user can only have one role per shop.
    UNIQUE KEY uk_shop_staff (shop_id, user_id)
);


-- Table: shop_statistics
-- Stores aggregated statistics for each shop to improve performance on dashboards.
-- This data would be updated periodically by a background job.
CREATE TABLE shop_statistics (
    stat_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    total_products INT UNSIGNED NOT NULL DEFAULT 0,
    total_orders INT UNSIGNED NOT NULL DEFAULT 0,
    total_revenue DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    average_rating DECIMAL(3, 2) NOT NULL DEFAULT 0.00,
    total_reviews INT UNSIGNED NOT NULL DEFAULT 0,
    last_calculated_at TIMESTAMP NOT NULL,

    -- A shop should only have one row of statistics.
    UNIQUE KEY uk_shop_statistics_shop_id (shop_id),
    -- Foreign key to the shops table.
    CONSTRAINT fk_shop_statistics_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE
);
