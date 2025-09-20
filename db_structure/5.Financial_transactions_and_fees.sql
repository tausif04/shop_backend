-- =================================================================
-- Segment 5: Financial Transaction Management and Commission Tracking
-- =================================================================
-- This segment handles all financial aspects, including transactions,
-- commission calculation, and payouts to vendors. Accuracy and
-- auditability are the highest priorities here.

-- Table: payment_methods
-- Defines the available payment methods and their configurations.
CREATE TABLE payment_methods (
    method_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    method_name VARCHAR(100) NOT NULL, -- e.g., 'Stripe', 'PayPal', 'Cash on Delivery'
    method_type ENUM('card', 'wallet', 'bank', 'cod') NOT NULL,
    gateway_name VARCHAR(100),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    -- For storing API keys, webhook secrets, etc.
    -- SECURITY NOTE: This data is highly sensitive and must be encrypted at rest.
    -- In a production environment, consider using a dedicated secrets manager.
    configuration_json JSON,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for payment_methods
CREATE INDEX idx_payment_methods_is_active ON payment_methods(is_active);


-- Table: transactions
-- A central ledger for every financial transaction on the platform.
CREATE TABLE transactions (
    transaction_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- Can be linked to an order, but not all transactions are (e.g., wallet top-up).
    order_id BIGINT UNSIGNED,
    -- The user initiating or receiving the transaction.
    user_id VARCHAR(255),
    transaction_type ENUM('payment', 'refund', 'commission', 'payout', 'wallet_deposit', 'wallet_withdrawal') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    status ENUM('pending', 'completed', 'failed', 'cancelled') NOT NULL,
    -- The unique ID from the payment gateway for external reference.
    gateway_transaction_id VARCHAR(255),
    -- Raw response from the gateway for auditing and dispute resolution.
    gateway_response_json JSON,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,

    -- Foreign keys to orders and users.
    CONSTRAINT fk_transactions_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE SET NULL,
    CONSTRAINT fk_transactions_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE SET NULL
);

-- Indexes for transactions
CREATE INDEX idx_transactions_order_id ON transactions(order_id);
CREATE INDEX idx_transactions_user_id ON transactions(user_id);
CREATE INDEX idx_transactions_type_status ON transactions(transaction_type, status);
CREATE INDEX idx_transactions_gateway_id ON transactions(gateway_transaction_id);


-- Table: commissions
-- Records the commission earned by the platform for each order item.
CREATE TABLE commissions (
    commission_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    order_id BIGINT UNSIGNED NOT NULL,
    shop_id BIGINT UNSIGNED NOT NULL,
    item_id BIGINT UNSIGNED NOT NULL,
    commission_rate DECIMAL(5, 2) NOT NULL,
    -- The base amount on which the commission is calculated.
    gross_amount DECIMAL(12, 2) NOT NULL,
    commission_amount DECIMAL(10, 2) NOT NULL,
    -- Any additional fixed fees for the platform.
    platform_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    -- The final amount due to the shop owner (gross - commission - fee).
    net_amount DECIMAL(12, 2) NOT NULL,
    -- Status indicating if the commission is available for payout.
    status ENUM('pending', 'cleared', 'paid_out', 'disputed') NOT NULL DEFAULT 'pending',
    calculated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_commissions_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_commissions_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_commissions_item
        FOREIGN KEY (item_id) REFERENCES order_items(item_id)
        ON DELETE CASCADE
);

-- Indexes for commissions
CREATE INDEX idx_commissions_shop_id_status ON commissions(shop_id, status);
CREATE INDEX idx_commissions_order_id ON commissions(order_id);


-- Table: payouts
-- Manages payout requests from shop owners.
CREATE TABLE payouts (
    payout_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    payout_amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    status ENUM('pending', 'processing', 'completed', 'failed') NOT NULL,
    payout_method VARCHAR(100),
    -- Stores bank account, PayPal email, etc.
    -- SECURITY NOTE: This data must be encrypted at rest.
    bank_details_json JSON,
    requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP,
    -- Reference number from the payment processor for the payout transaction.
    reference_number VARCHAR(255),

    CONSTRAINT fk_payouts_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE RESTRICT
);

-- Indexes for payouts
CREATE INDEX idx_payouts_shop_id_status ON payouts(shop_id, status);


-- Table: payout_transactions
-- A junction table linking a single payout to the multiple commissions it covers.
CREATE TABLE payout_transactions (
    payout_transaction_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    payout_id BIGINT UNSIGNED NOT NULL,
    commission_id BIGINT UNSIGNED NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payout_transactions_payout
        FOREIGN KEY (payout_id) REFERENCES payouts(payout_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_payout_transactions_commission
        FOREIGN KEY (commission_id) REFERENCES commissions(commission_id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_payout_commission (payout_id, commission_id)
);


-- Table: invoices
-- For generating invoices, typically for shop fees or subscriptions.
CREATE TABLE invoices (
    invoice_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    invoice_number VARCHAR(50) NOT NULL UNIQUE,
    billing_period_start DATE NOT NULL,
    billing_period_end DATE NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    tax_amount DECIMAL(12, 2) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    status ENUM('draft', 'sent', 'paid', 'overdue', 'void') NOT NULL,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date DATE,
    paid_at TIMESTAMP,

    CONSTRAINT fk_invoices_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE
);

-- Indexes for invoices
CREATE INDEX idx_invoices_shop_id_status ON invoices(shop_id, status);


-- Table: financial_reports
-- Stores pre-generated reports for performance.
CREATE TABLE financial_reports (
    report_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    report_type VARCHAR(100) NOT NULL, -- e.g., 'monthly_sales', 'tax_summary'
    -- Can be for a specific shop or platform-wide (nullable).
    shop_id BIGINT UNSIGNED,
    report_data_json JSON NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_financial_reports_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE SET NULL
);


-- Table: wallet_transactions
-- A ledger for a user's internal wallet.
CREATE TABLE wallet_transactions (
    wallet_transaction_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    transaction_type ENUM('deposit', 'withdrawal', 'payment', 'refund_credit') NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    balance_after DECIMAL(12, 2) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_wallet_transactions_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE
);

-- Indexes for wallet_transactions
CREATE INDEX idx_wallet_transactions_user_id ON wallet_transactions(user_id);
