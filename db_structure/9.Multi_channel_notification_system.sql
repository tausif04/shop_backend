-- =================================================================
-- Segment 9: Multi-Channel Notification System
-- =================================================================
-- This segment provides the infrastructure for a robust notification
-- system that can deliver messages across various channels like
-- email, SMS, and push notifications.

-- Table: notification_templates
-- Stores reusable templates for different types of notifications.
CREATE TABLE notification_templates (
    template_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    template_name VARCHAR(255) NOT NULL UNIQUE,
    template_type ENUM('email', 'sms', 'push', 'in_app') NOT NULL,
    -- For email templates, this would be the subject line. Can use placeholders.
    subject_template VARCHAR(512),
    -- The main content of the notification. Can use placeholders like {{username}}.
    body_template TEXT NOT NULL,
    -- A JSON array of variable names used in the template for validation. e.g., ["username", "order_id"]
    variables_json JSON,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Table: notifications
-- The central log of all notifications sent or scheduled to be sent.
CREATE TABLE notifications (
    notification_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    template_id BIGINT UNSIGNED,
    -- The general category of the notification, e.g., 'order_confirmation', 'new_review'.
    notification_type VARCHAR(100) NOT NULL,
    -- Final rendered title/subject.
    title VARCHAR(512),
    -- Final rendered message body.
    message TEXT NOT NULL,
    -- Any additional data to be sent, especially for push or in-app notifications (e.g., deep link URL).
    data_json JSON,
    -- The channels this notification should be sent through, e.g., ["email", "push"].
    channels_json JSON NOT NULL,
    priority ENUM('low', 'medium', 'high') NOT NULL DEFAULT 'medium',
    status ENUM('pending', 'sent', 'delivered', 'failed', 'read') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    read_at TIMESTAMP,

    CONSTRAINT fk_notifications_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_notifications_template
        FOREIGN KEY (template_id) REFERENCES notification_templates(template_id)
        ON DELETE SET NULL
);

-- Indexes for notifications
CREATE INDEX idx_notifications_user_id_status ON notifications(user_id, status);
CREATE INDEX idx_notifications_type ON notifications(notification_type);


-- Table: notification_preferences
-- Stores user-specific choices about which notifications they want to receive.
-- This is a duplicate of the user_preferences table in the first segment, but focused on notification types.
-- A more normalized approach would be to have a single table. This is provided as requested.
CREATE TABLE notification_preferences (
    preference_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    -- The type of notification, linking to notifications.notification_type.
    notification_type VARCHAR(100) NOT NULL,
    email_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    sms_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    push_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    in_app_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_notification_preferences_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_user_notification_type (user_id, notification_type)
);


-- Table: notification_logs
-- A detailed log for each delivery attempt on each channel for a notification.
CREATE TABLE notification_logs (
    log_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    notification_id BIGINT UNSIGNED NOT NULL,
    channel ENUM('email', 'sms', 'push', 'in_app') NOT NULL,
    status ENUM('success', 'failed', 'deferred') NOT NULL,
    -- Stores the response from the delivery service (e.g., SMTP server, push gateway).
    response_data_json JSON,
    attempted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP,

    CONSTRAINT fk_notification_logs_notification
        FOREIGN KEY (notification_id) REFERENCES notifications(notification_id)
        ON DELETE CASCADE
);

-- Indexes for notification_logs
CREATE INDEX idx_notification_logs_notification_id ON notification_logs(notification_id);


-- Table: push_subscriptions
-- Stores the necessary endpoints and keys for sending web push notifications.
CREATE TABLE push_subscriptions (
    subscription_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    -- The unique endpoint URL provided by the browser's push service.
    endpoint VARCHAR(2048) NOT NULL UNIQUE,
    p256dh_key VARCHAR(255) NOT NULL,
    auth_key VARCHAR(255) NOT NULL,
    user_agent VARCHAR(512),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_push_subscriptions_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE
);

-- Indexes for push_subscriptions
CREATE INDEX idx_push_subscriptions_user_id ON push_subscriptions(user_id);


-- Table: email_campaigns
-- Manages bulk email marketing campaigns.
CREATE TABLE email_campaigns (
    campaign_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    campaign_name VARCHAR(255) NOT NULL,
    template_id BIGINT UNSIGNED NOT NULL,
    -- JSON defining the target audience (e.g., all users in a country, or users who bought a specific product).
    target_audience_json JSON,
    scheduled_at TIMESTAMP,
    status ENUM('draft', 'scheduled', 'sending', 'sent', 'cancelled') NOT NULL DEFAULT 'draft',
    created_by VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_email_campaigns_template
        FOREIGN KEY (template_id) REFERENCES notification_templates(template_id)
        ON DELETE RESTRICT
);


-- Table: notification_queues
-- A dedicated queue table to manage the sending of notifications asynchronously.
CREATE TABLE notification_queues (
    queue_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    notification_id BIGINT UNSIGNED NOT NULL,
    channel ENUM('email', 'sms', 'push', 'in_app') NOT NULL,
    priority INT NOT NULL DEFAULT 10,
    scheduled_at TIMESTAMP NOT NULL,
    attempts INT UNSIGNED NOT NULL DEFAULT 0,
    max_attempts INT UNSIGNED NOT NULL DEFAULT 3,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_notification_queues_notification
        FOREIGN KEY (notification_id) REFERENCES notifications(notification_id)
        ON DELETE CASCADE
);

-- Indexes for notification_queues
-- Index to help the queue processor find the next job to run.
CREATE INDEX idx_notification_queues_scheduled_at_priority ON notification_queues(scheduled_at, priority);
