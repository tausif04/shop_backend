-- =================================================================
-- Segment 10: Comprehensive Audit Logging and Security Monitoring
-- =================================================================
-- This final segment establishes a robust framework for security
-- and compliance. It includes detailed logging for all critical
-- actions, data changes, and security-related events, with
-- automated triggers to ensure a complete audit trail.

-- Table: audit_logs
-- A general-purpose log for high-level user actions.
CREATE TABLE audit_logs (
    log_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    action VARCHAR(255) NOT NULL, -- e.g., 'create_product', 'update_shop_policy'
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    -- Storing before and after states is crucial for forensic analysis.
    old_values_json JSON,
    new_values_json JSON,
    ip_address VARCHAR(45) NOT NULL,
    user_agent VARCHAR(512),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_logs_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE SET NULL
);

-- Indexes for audit_logs
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);


-- Table: security_logs
-- Specifically for security-sensitive events.
CREATE TABLE security_logs (
    log_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    event_type ENUM('login', 'logout', 'failed_login', 'password_change', 'suspicious_activity', 'permission_change') NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent VARCHAR(512),
    success BOOLEAN NOT NULL,
    failure_reason VARCHAR(255),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_security_logs_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE SET NULL
);

-- Indexes for security_logs
CREATE INDEX idx_security_logs_event_type_success ON security_logs(event_type, success);
CREATE INDEX idx_security_logs_user_id ON security_logs(user_id);
CREATE INDEX idx_security_logs_ip_address ON security_logs(ip_address);


-- Table: data_change_logs
-- A low-level, trigger-populated log of all changes to critical tables.
CREATE TABLE data_change_logs (
    change_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id VARCHAR(255) NOT NULL,
    operation ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    changed_by VARCHAR(255), -- User ID from the application context
    old_data_json JSON,
    new_data_json JSON,
    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for data_change_logs
CREATE INDEX idx_data_change_logs_table_record ON data_change_logs(table_name, record_id);


-- Table: login_history
-- A detailed history of all login attempts for forensic analysis.
CREATE TABLE login_history (
    login_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent VARCHAR(512),
    -- GeoIP lookup data stored for mapping login locations.
    location_json JSON,
    login_method VARCHAR(50), -- e.g., 'password', 'google_oauth', 'keycloak_sso'
    success BOOLEAN NOT NULL,
    failure_reason VARCHAR(255),
    attempted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_login_history_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE
);

-- Indexes for login_history
CREATE INDEX idx_login_history_user_id ON login_history(user_id);
CREATE INDEX idx_login_history_ip_address ON login_history(ip_address);


-- Table: api_access_logs
-- Logs all requests made to your platform's API.
CREATE TABLE api_access_logs (
    log_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    endpoint VARCHAR(512) NOT NULL,
    method VARCHAR(10) NOT NULL,
    request_data_json JSON,
    response_status INT,
    response_time_ms INT,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for api_access_logs
CREATE INDEX idx_api_access_logs_endpoint ON api_access_logs(endpoint);
CREATE INDEX idx_api_access_logs_user_id ON api_access_logs(user_id);


-- Table: security_incidents
-- A table for tracking and managing security incidents.
CREATE TABLE security_incidents (
    incident_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    incident_type VARCHAR(100) NOT NULL, -- e.g., 'data_breach', 'dos_attack', 'account_takeover'
    severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    description TEXT NOT NULL,
    affected_users_json JSON,
    detected_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    resolution_notes TEXT
);


-- Table: system_backups
-- Logs metadata about system backups for disaster recovery planning.
CREATE TABLE system_backups (
    backup_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    backup_type ENUM('full', 'incremental', 'database', 'filesystem') NOT NULL,
    file_path VARCHAR(2048) NOT NULL,
    file_size BIGINT UNSIGNED,
    backup_started_at TIMESTAMP NOT NULL,
    backup_completed_at TIMESTAMP,
    status ENUM('in_progress', 'completed', 'failed') NOT NULL,
    checksum VARCHAR(255) -- e.g., SHA256 hash to verify integrity
);


-- Table: compliance_reports
-- Stores generated reports for compliance audits (e.g., GDPR, PCI-DSS).
CREATE TABLE compliance_reports (
    report_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(100) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    report_data_json JSON NOT NULL,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =================================================================
-- Triggers for Automated Data Change Logging & Security Monitoring
-- =================================================================

DELIMITER $$

-- Trigger: trg_user_profiles_after_update
-- Purpose: Logs changes to the user_profiles table.
CREATE TRIGGER trg_user_profiles_after_update
AFTER UPDATE ON user_profiles
FOR EACH ROW
BEGIN
    INSERT INTO data_change_logs (table_name, record_id, operation, old_data_json, new_data_json)
    VALUES (
        'user_profiles',
        OLD.profile_id,
        'UPDATE',
        JSON_OBJECT(
            'email', OLD.email,
            'phone', OLD.phone,
            'first_name', OLD.first_name,
            'last_name', OLD.last_name,
            'status', OLD.status
        ),
        JSON_OBJECT(
            'email', NEW.email,
            'phone', NEW.phone,
            'first_name', NEW.first_name,
            'last_name', NEW.last_name,
            'status', NEW.status
        )
    );
END$$

-- Trigger: trg_shops_after_update
-- Purpose: Logs changes to sensitive fields in the shops table.
CREATE TRIGGER trg_shops_after_update
AFTER UPDATE ON shops
FOR EACH ROW
BEGIN
    -- Only log if sensitive data has changed
    IF OLD.status <> NEW.status OR OLD.commission_rate <> NEW.commission_rate OR OLD.owner_id <> NEW.owner_id THEN
        INSERT INTO data_change_logs (table_name, record_id, operation, old_data_json, new_data_json)
        VALUES (
            'shops',
            OLD.shop_id,
            'UPDATE',
            JSON_OBJECT(
                'status', OLD.status,
                'commission_rate', OLD.commission_rate,
                'owner_id', OLD.owner_id
            ),
            JSON_OBJECT(
                'status', NEW.status,
                'commission_rate', NEW.commission_rate,
                'owner_id', NEW.owner_id
            )
        );
    END IF;
END$$

-- Trigger: trg_products_after_insert
-- Purpose: Logs the creation of new products.
CREATE TRIGGER trg_products_after_insert
AFTER INSERT ON products
FOR EACH ROW
BEGIN
    INSERT INTO data_change_logs (table_name, record_id, operation, new_data_json)
    VALUES (
        'products',
        NEW.product_id,
        'INSERT',
        JSON_OBJECT(
            'product_name', NEW.product_name,
            'shop_id', NEW.shop_id,
            'category_id', NEW.category_id,
            'status', NEW.status
        )
    );
END$$

-- Trigger: trg_orders_after_update
-- Purpose: Logs significant status changes in orders to the main audit log.
CREATE TRIGGER trg_orders_after_update
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    -- Log only when the status changes, as this is a key event in the order lifecycle.
    IF OLD.status <> NEW.status THEN
        INSERT INTO audit_logs (user_id, action, resource_type, resource_id, old_values_json, new_values_json, ip_address)
        VALUES (
            NEW.customer_id,
            'update_order_status',
            'order',
            NEW.order_id,
            JSON_OBJECT('status', OLD.status),
            JSON_OBJECT('status', NEW.status),
            '::1' -- IP address should be captured from the application context
        );
    END IF;
END$$

-- Trigger: trg_payouts_after_update
-- Purpose: Logs changes to payout status, a critical financial event.
CREATE TRIGGER trg_payouts_after_update
AFTER UPDATE ON payouts
FOR EACH ROW
BEGIN
    IF OLD.status <> NEW.status THEN
        INSERT INTO data_change_logs (table_name, record_id, operation, old_data_json, new_data_json)
        VALUES (
            'payouts',
            OLD.payout_id,
            'UPDATE',
            JSON_OBJECT('status', OLD.status, 'amount', OLD.payout_amount),
            JSON_OBJECT('status', NEW.status, 'amount', NEW.payout_amount, 'processed_at', NEW.processed_at)
        );
    END IF;
END$$

-- Trigger: trg_after_failed_login
-- Purpose: Detects potential brute-force attacks by logging suspicious activity.
CREATE TRIGGER trg_after_failed_login
AFTER INSERT ON login_history
FOR EACH ROW
BEGIN
    DECLARE failed_count INT;
    -- Check for failed logins from the same IP in the last 5 minutes.
    IF NEW.success = 0 THEN
        SELECT COUNT(*)
        INTO failed_count
        FROM login_history
        WHERE ip_address = NEW.ip_address
          AND success = 0
          AND attempted_at > (NOW() - INTERVAL 5 MINUTE);

        -- If more than 5 failed attempts, log a security event.
        IF failed_count > 5 THEN
            INSERT INTO security_logs (user_id, event_type, ip_address, user_agent, success, failure_reason)
            VALUES (NEW.user_id, 'suspicious_activity', NEW.ip_address, NEW.user_agent, 0, 'Multiple failed login attempts detected.');
        END IF;
    END IF;
END$$

DELIMITER ;
