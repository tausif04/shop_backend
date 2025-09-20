-- =================================================================
-- Segment 1: Keycloak-Integrated User Management System
-- =================================================================
-- This segment defines tables for storing user-related data that
-- complements the information managed by Keycloak.

-- Table: user_profiles
-- Stores extended profile information for users, linking back to Keycloak.
CREATE TABLE user_profiles (
    profile_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- The unique identifier from Keycloak. This is the core link.
    keycloak_user_id VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    date_of_birth DATE,
    gender ENUM('male', 'female', 'other', 'prefer_not_to_say'),
    avatar_url VARCHAR(2048),
    bio TEXT,
    -- User status, managed locally. E.g., for temporary deactivation.
    status ENUM('active', 'inactive', 'suspended') NOT NULL DEFAULT 'active',
    -- Timestamps for auditing and tracking record lifecycle.
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Tracks when the local profile was last synced with Keycloak data.
    last_sync_at TIMESTAMP NULL
);

-- Indexes for user_profiles
-- Index on keycloak_user_id is created automatically by the UNIQUE constraint.
-- Index on email for fast lookups, as it's a common login/search field.
CREATE INDEX idx_user_profiles_email ON user_profiles(email);
-- Index on status for quickly filtering users by their activity status.
CREATE INDEX idx_user_profiles_status ON user_profiles(status);


-- Table: user_addresses
-- Stores multiple physical addresses for each user.
CREATE TABLE user_addresses (
    address_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    keycloak_user_id VARCHAR(255) NOT NULL,
    address_type ENUM('home', 'work', 'billing', 'shipping') NOT NULL,
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100),
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Foreign key to link addresses to a user profile.
    -- ON DELETE CASCADE ensures that if a user is deleted, their addresses are also removed.
    CONSTRAINT fk_user_addresses_user_profiles
        FOREIGN KEY (keycloak_user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE
);

-- Indexes for user_addresses
-- Index on keycloak_user_id for efficient retrieval of all addresses for a user.
CREATE INDEX idx_user_addresses_keycloak_user_id ON user_addresses(keycloak_user_id);


-- Table: user_business_data
-- Stores business-related information, including KYC details for vendors/merchants.
CREATE TABLE user_business_data (
    business_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    keycloak_user_id VARCHAR(255) NOT NULL,
    kyc_status ENUM('pending', 'approved', 'rejected', 'resubmit_required') NOT NULL DEFAULT 'pending',
    -- Storing documents as JSON can include URLs, file paths, or metadata.
    -- For security, actual files should be in secure storage (like S3), not the DB.
    kyc_documents_json JSON,
    tax_id VARCHAR(100),
    business_license VARCHAR(255),
    business_type VARCHAR(100),
    -- Notes for internal review during the verification process.
    verification_notes TEXT,
    verified_at TIMESTAMP NULL,
    verified_by VARCHAR(255), -- Could be a Keycloak ID of an admin
    -- Foreign key to link business data to a user profile.
    CONSTRAINT fk_user_business_data_user_profiles
        FOREIGN KEY (keycloak_user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE
);

-- Indexes for user_business_data
-- Index on keycloak_user_id for quick access to a user's business info.
CREATE INDEX idx_user_business_data_keycloak_user_id ON user_business_data(keycloak_user_id);
-- Index on kyc_status to efficiently query users based on their verification status.
CREATE INDEX idx_user_business_data_kyc_status ON user_business_data(kyc_status);


-- Table: keycloak_user_sync
-- Logs synchronization attempts between the local database and Keycloak.
CREATE TABLE keycloak_user_sync (
    sync_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    keycloak_user_id VARCHAR(255) NOT NULL,
    last_sync_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sync_status ENUM('success', 'failed') NOT NULL,
    -- Store error messages for debugging failed syncs.
    error_message TEXT,
    -- A JSON object detailing which attributes were updated during the sync.
    attributes_synced_json JSON
);

-- Indexes for keycloak_user_sync
-- Index for finding sync history for a specific user.
CREATE INDEX idx_keycloak_user_sync_keycloak_user_id ON keycloak_user_sync(keycloak_user_id);
-- Index for querying syncs by status, useful for monitoring and alerts.
CREATE INDEX idx_keycloak_user_sync_status ON keycloak_user_sync(sync_status);


-- Table: user_preferences
-- Stores user-specific settings and preferences.
CREATE TABLE user_preferences (
    preference_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    keycloak_user_id VARCHAR(255) NOT NULL,
    notification_email BOOLEAN NOT NULL DEFAULT TRUE,
    notification_sms BOOLEAN NOT NULL DEFAULT FALSE,
    notification_push BOOLEAN NOT NULL DEFAULT TRUE,
    language VARCHAR(10) NOT NULL DEFAULT 'en-US',
    currency VARCHAR(10) NOT NULL DEFAULT 'USD',
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    theme ENUM('light', 'dark') NOT NULL DEFAULT 'light',
    marketing_consent BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    -- Foreign key to link preferences to a user profile.
    CONSTRAINT fk_user_preferences_user_profiles
        FOREIGN KEY (keycloak_user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE
);

-- Indexes for user_preferences
-- Index for retrieving a user's preferences quickly.
CREATE INDEX idx_user_preferences_keycloak_user_id ON user_preferences(keycloak_user_id);


-- Table: shop_user_roles
-- Maps users to roles within a specific shop (multi-vendor context).
-- This is separate from Keycloak's global roles.
CREATE TABLE shop_user_roles (
    role_assignment_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- Assumes a `shops` table will be created. This is a forward declaration.
    -- The actual foreign key will be added later if the shops table is in another script.
    shop_id BIGINT UNSIGNED NOT NULL,
    keycloak_user_id VARCHAR(255) NOT NULL,
    -- Role name specific to the shop context, e.g., 'Shop Manager', 'Staff'.
    keycloak_role_name VARCHAR(100) NOT NULL,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_by VARCHAR(255), -- Keycloak ID of the user who assigned the role
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    -- A composite unique key to prevent assigning the same role to the same user in the same shop more than once.
    UNIQUE KEY uk_shop_user_role (shop_id, keycloak_user_id, keycloak_role_name)
);

-- Indexes for shop_user_roles
-- Index for finding all roles for a user across all shops.
CREATE INDEX idx_shop_user_roles_keycloak_user_id ON shop_user_roles(keycloak_user_id);
-- Index for finding all users and their roles for a specific shop.
CREATE INDEX idx_shop_user_roles_shop_id ON shop_user_roles(shop_id);


-- Table: user_activity_log
-- A crucial table for security and auditing, tracking user actions.
CREATE TABLE user_activity_log (
    activity_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    keycloak_user_id VARCHAR(255),
    activity_type VARCHAR(100) NOT NULL, -- e.g., 'login', 'update_profile', 'create_product'
    resource_type VARCHAR(100), -- e.g., 'product', 'order'
    resource_id VARCHAR(255), -- The ID of the affected resource
    ip_address VARCHAR(45) NOT NULL, -- Supports both IPv4 and IPv6
    user_agent VARCHAR(512),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for user_activity_log
-- Index for retrieving all activities for a specific user.
CREATE INDEX idx_user_activity_log_keycloak_user_id ON user_activity_log(keycloak_user_id);
-- Index for searching activities by type, useful for monitoring specific actions.
CREATE INDEX idx_user_activity_log_activity_type ON user_activity_log(activity_type);
-- Index on timestamp for time-based queries and reports.
CREATE INDEX idx_user_activity_log_created_at ON user_activity_log(created_at);
