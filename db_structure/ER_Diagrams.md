1. User Profile Management System ER-Diagram
```mermaid
erDiagram
    user_profiles {
        BIGINT profile_id PK
        VARCHAR(255) keycloak_user_id UK "Unique Keycloak ID"
        VARCHAR(255) email "Indexed"
        VARCHAR(50) phone
        VARCHAR(100) first_name
        VARCHAR(100) last_name
        DATE date_of_birth
        ENUM gender
        VARCHAR(2048) avatar_url
        TEXT bio
        ENUM status "Indexed"
        TIMESTAMP created_at
        TIMESTAMP updated_at
        TIMESTAMP last_sync_at
    }

    user_addresses {
        BIGINT address_id PK
        VARCHAR(255) keycloak_user_id FK
        ENUM address_type
        VARCHAR(255) address_line1
        VARCHAR(255) address_line2
        VARCHAR(100) city
        VARCHAR(100) state
        VARCHAR(100) country
        VARCHAR(20) postal_code
        BOOLEAN is_default
        TIMESTAMP created_at
    }

    user_business_data {
        BIGINT business_id PK
        VARCHAR(255) keycloak_user_id FK
        ENUM kyc_status "Indexed"
        JSON kyc_documents_json
        VARCHAR(100) tax_id
        VARCHAR(255) business_license
        VARCHAR(100) business_type
        TEXT verification_notes
        TIMESTAMP verified_at
        VARCHAR(255) verified_by
    }

    keycloak_user_sync {
        BIGINT sync_id PK
        VARCHAR(255) keycloak_user_id
        TIMESTAMP last_sync_at
        ENUM sync_status "Indexed"
        TEXT error_message
        JSON attributes_synced_json
    }

    user_preferences {
        BIGINT preference_id PK
        VARCHAR(255) keycloak_user_id FK
        BOOLEAN notification_email
        BOOLEAN notification_sms
        BOOLEAN notification_push
        VARCHAR(10) language
        VARCHAR(10) currency
        VARCHAR(50) timezone
        ENUM theme
        BOOLEAN marketing_consent
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    shop_user_roles {
        BIGINT role_assignment_id PK
        BIGINT shop_id "FK (to shops)"
        VARCHAR(255) keycloak_user_id
        VARCHAR(100) keycloak_role_name
        TIMESTAMP assigned_at
        VARCHAR(255) assigned_by
        BOOLEAN is_active
    }

    user_activity_log {
        BIGINT activity_id PK
        VARCHAR(255) keycloak_user_id
        VARCHAR(100) activity_type "Indexed"
        VARCHAR(100) resource_type
        VARCHAR(255) resource_id
        VARCHAR(45) ip_address
        VARCHAR(512) user_agent
        TIMESTAMP created_at "Indexed"
    }

    user_profiles ||--o{ user_addresses : "has"
    user_profiles ||--|| user_business_data : "has"
    user_profiles ||--o{ user_preferences : "has"
    user_profiles ||--o{ keycloak_user_sync : "syncs"
    user_profiles ||--o{ shop_user_roles : "has roles in"
    user_profiles ||--o{ user_activity_log : "performs"
```
2. Multi-Vendor Shop Management System ER-Diagram
```mermaid
erDiagram

    user_profiles {
        VARCHAR(255) keycloak_user_id PK
        VARCHAR(255) email
    }

    shops {
        BIGINT shop_id PK
        VARCHAR(255) owner_id FK
        VARCHAR(255) shop_name
        VARCHAR(255) shop_slug UK
        ENUM status "Indexed"
        DECIMAL commission_rate
        TIMESTAMP created_at
    }

    shop_categories {
        BIGINT category_id PK
        VARCHAR(255) category_name UK
    }

    shop_category_assignments {
        BIGINT assignment_id PK
        BIGINT shop_id FK
        BIGINT category_id FK
    }

    shop_policies {
        BIGINT policy_id PK
        BIGINT shop_id FK
        TEXT return_policy
        TEXT shipping_policy
    }

    shop_settings {
        BIGINT setting_id PK
        BIGINT shop_id FK
        VARCHAR(100) setting_key
        TEXT setting_value
    }

    shop_staff {
        BIGINT staff_id PK
        BIGINT shop_id FK
        VARCHAR(255) user_id FK
        ENUM role
        JSON permissions_json
    }

    shop_statistics {
        BIGINT stat_id PK
        BIGINT shop_id FK
        INT total_orders
        DECIMAL total_revenue
    }

    user_profiles ||--|{ shops : "owns"
    shops ||--|{ shop_category_assignments : "is in"
    shop_categories ||--|{ shop_category_assignments : "has"
    shops ||--|| shop_policies : "defines"
    shops ||--|{ shop_settings : "has"
    shops ||--|{ shop_staff : "employs"
    user_profiles ||--|{ shop_staff : "is"
    shops ||--|| shop_statistics : "has"
```

3. Comprehensive Product Management System ER-Diagram
```mermaid
erDiagram

    shops { BIGINT shop_id PK }
    categories {
        BIGINT category_id PK
        BIGINT parent_category_id FK "Self-referencing"
        VARCHAR(255) category_name
        VARCHAR(255) category_slug UK
    }

    products {
        BIGINT product_id PK
        BIGINT shop_id FK
        BIGINT category_id FK
        VARCHAR(255) product_name
        VARCHAR(255) product_slug
        VARCHAR(100) sku
        ENUM status
    }

    product_variants {
        BIGINT variant_id PK
        BIGINT product_id FK
        VARCHAR(255) variant_name
        VARCHAR(100) sku
        DECIMAL price
    }

    product_attributes {
        BIGINT attribute_id PK
        VARCHAR(100) attribute_name UK
    }

    product_attribute_values {
        BIGINT value_id PK
        BIGINT product_id FK
        BIGINT attribute_id FK
        VARCHAR(255) attribute_value
    }

    product_images {
        BIGINT image_id PK
        BIGINT product_id FK
        BIGINT variant_id FK "Nullable"
        VARCHAR(2048) image_url
    }

    product_inventory {
        BIGINT inventory_id PK
        BIGINT variant_id FK
        INT quantity_available
    }

    product_reviews_summary {
        BIGINT summary_id PK
        BIGINT product_id FK
        DECIMAL average_rating
        INT total_reviews
    }

    shops ||--|{ products : "sells"
    categories ||--|{ products : "contains"
    categories }o--|| categories : "is child of"
    products ||--|{ product_variants : "has"
    products ||--|{ product_attribute_values : "has"
    product_attributes ||--|{ product_attribute_values : "defines"
    products ||--|{ product_images : "has"
    product_variants }o--|{ product_images : "has specific"
    product_variants ||--|| product_inventory : "has"
    products ||--|| product_reviews_summary : "is summarized by"

```

4. Comprehensive Order Management System ER-Diagram
```mermaid
erDiagram

    user_profiles { VARCHAR(255) keycloak_user_id PK }
    products { BIGINT product_id PK }
    product_variants { BIGINT variant_id PK }
    shops { BIGINT shop_id PK }

    orders {
        BIGINT order_id PK
        VARCHAR(255) customer_id FK
        VARCHAR(50) order_number UK
        ENUM status
        DECIMAL total_amount
        TIMESTAMP order_date
    }

    order_items {
        BIGINT item_id PK
        BIGINT order_id FK
        BIGINT product_id FK
        BIGINT variant_id FK
        BIGINT shop_id FK
        INT quantity
        DECIMAL total_price
    }

    order_addresses {
        BIGINT address_id PK
        BIGINT order_id FK
        ENUM address_type
        VARCHAR(255) address_line1
    }

    order_status_history {
        BIGINT history_id PK
        BIGINT order_id FK
        VARCHAR(50) status
        TIMESTAMP changed_at
    }

    order_tracking {
        BIGINT tracking_id PK
        BIGINT order_id FK
        VARCHAR(100) carrier
        VARCHAR(255) tracking_number
    }

    order_payments {
        BIGINT payment_id PK
        BIGINT order_id FK
        VARCHAR(100) payment_method
        VARCHAR(255) transaction_id
        DECIMAL amount
        ENUM status
    }

    order_refunds {
        BIGINT refund_id PK
        BIGINT order_id FK
        BIGINT item_id FK "Nullable"
        DECIMAL refund_amount
        ENUM status
    }

    shipping_zones {
        BIGINT zone_id PK
        VARCHAR(255) zone_name
        JSON shipping_rates_json
    }

    user_profiles ||--|{ orders : "places"
    orders ||--|{ order_items : "contains"
    products ||--o{ order_items : "is"
    product_variants ||--o{ order_items : "is"
    shops ||--o{ order_items : "fulfills"
    orders ||--|{ order_addresses : "ships to/bills to"
    orders ||--|{ order_status_history : "has history of"
    orders ||--|{ order_tracking : "is tracked by"
    orders ||--|{ order_payments : "is paid by"
    orders ||--|{ order_refunds : "can be"
    order_items }o--|{ order_refunds : "can be"

```
5. Financial Transaction & Commission System ER-Diagram
```mermaid
erDiagram

    user_profiles { VARCHAR(255) keycloak_user_id PK }
    orders { BIGINT order_id PK }
    shops { BIGINT shop_id PK }
    order_items { BIGINT item_id PK }

    transactions {
        BIGINT transaction_id PK
        BIGINT order_id FK "Nullable"
        VARCHAR(255) user_id FK "Nullable"
        ENUM transaction_type
        DECIMAL amount
        ENUM status
    }

    commissions {
        BIGINT commission_id PK
        BIGINT order_id FK
        BIGINT shop_id FK
        BIGINT item_id FK
        DECIMAL commission_amount
        ENUM status
    }

    payouts {
        BIGINT payout_id PK
        BIGINT shop_id FK
        DECIMAL payout_amount
        ENUM status
    }

    payout_transactions {
        BIGINT payout_transaction_id PK
        BIGINT payout_id FK
        BIGINT commission_id FK
    }

    wallet_transactions {
        BIGINT wallet_transaction_id PK
        VARCHAR(255) user_id FK
        ENUM transaction_type
        DECIMAL amount
    }

    orders }o--|| transactions : "generates"
    user_profiles }o--|{ transactions : "performs"
    order_items ||--|| commissions : "generates"
    shops ||--|{ payouts : "requests"
    payouts ||--|{ payout_transactions : "covers"
    commissions ||--|{ payout_transactions : "is covered by"
    user_profiles ||--|{ wallet_transactions : "has"

```
6. Comprehensive Review and Rating System ER-Diagram
```mermaid
erDiagram

    products { BIGINT product_id PK }
    order_items { BIGINT order_item_id PK }
    user_profiles { VARCHAR(255) keycloak_user_id PK }
    shops { BIGINT shop_id PK }

    reviews {
        BIGINT review_id PK
        BIGINT product_id FK
        BIGINT order_item_id FK
        VARCHAR(255) customer_id FK
        BIGINT shop_id FK
        TINYINT rating
        ENUM status
    }

    review_images {
        BIGINT image_id PK
        BIGINT review_id FK
        VARCHAR(2048) image_url
    }

    review_responses {
        BIGINT response_id PK
        BIGINT review_id FK
        VARCHAR(255) responder_id FK
        TEXT response_text
    }

    review_votes {
        BIGINT vote_id PK
        BIGINT review_id FK
        VARCHAR(255) user_id FK
        ENUM vote_type
    }

    review_moderation {
        BIGINT moderation_id PK
        BIGINT review_id FK
        VARCHAR(255) moderator_id FK
        ENUM action
    }

    order_items ||--|| reviews : "is reviewed by"
    reviews ||--|{ review_images : "has"
    reviews ||--|| review_responses : "is responded to by"
    user_profiles ||--o{ review_responses : "is"
    reviews ||--|{ review_votes : "is voted on by"
    user_profiles ||--o{ review_votes : "is"
    reviews ||--|{ review_moderation : "is moderated by"
    user_profiles ||--o{ review_moderation : "is"
```
7. Coupon and Discount Management System ER-Diagram
```mermaid
erDiagram

    shops { BIGINT shop_id PK }
    user_profiles { VARCHAR(255) keycloak_user_id PK }
    orders { BIGINT order_id PK }

    coupons {
        BIGINT coupon_id PK
        BIGINT shop_id FK "Nullable"
        VARCHAR(100) coupon_code UK
        ENUM discount_type
        DECIMAL discount_value
        TIMESTAMP expires_at
    }

    coupon_usage {
        BIGINT usage_id PK
        BIGINT coupon_id FK
        VARCHAR(255) user_id FK
        BIGINT order_id FK
        DECIMAL discount_amount
    }

    promotional_campaigns {
        BIGINT campaign_id PK
        VARCHAR(255) campaign_name
        DATE start_date
        DATE end_date
    }

    campaign_coupons {
        BIGINT campaign_coupon_id PK
        BIGINT campaign_id FK
        BIGINT coupon_id FK
    }

    shops }o--|{ coupons : "offers"
    coupons ||--|{ coupon_usage : "is used in"
    user_profiles ||--|{ coupon_usage : "uses"
    orders ||--|{ coupon_usage : "applies"
    promotional_campaigns ||--|{ campaign_coupons : "includes"
    coupons ||--|{ campaign_coupons : "is part of"
```
8. Analytics and Reporting System ER-Diagram
```mermaid
erDiagram
    user_profiles { VARCHAR(255) keycloak_user_id PK }
    products { BIGINT product_id PK }
    shops { BIGINT shop_id PK }
    orders { BIGINT order_id PK }

    analytics_events {
        BIGINT event_id PK
        VARCHAR(255) user_id FK
        BIGINT product_id FK
        BIGINT shop_id FK
        BIGINT order_id FK
        VARCHAR(100) event_type
        TIMESTAMP created_at
    }

    daily_sales_reports {
        BIGINT report_id PK
        DATE report_date
        BIGINT shop_id FK "Nullable"
        DECIMAL total_revenue
    }

    product_analytics {
        BIGINT analytics_id PK
        BIGINT product_id FK
        DATE date
        INT views
        INT purchases
    }

    custom_reports {
        BIGINT report_id PK
        VARCHAR(255) report_name
        VARCHAR(255) created_by FK
    }

    report_schedules {
        BIGINT schedule_id PK
        BIGINT report_id FK
        ENUM frequency
    }

    user_profiles }o--|{ analytics_events : "generates"
    products }o--|{ analytics_events : "relates to"
    shops }o--|{ analytics_events : "relates to"
    orders }o--|{ analytics_events : "relates to"
    shops }o--|{ daily_sales_reports : "has"
    products ||--|{ product_analytics : "has"
    user_profiles ||--|{ custom_reports : "creates"
    custom_reports ||--|{ report_schedules : "can be"

```

9. Notification System ER-Diagram
```mermaid
erDiagram

    user_profiles { VARCHAR(255) keycloak_user_id PK }

    notification_templates {
        BIGINT template_id PK
        VARCHAR(255) template_name UK
        ENUM template_type
    }

    notifications {
        BIGINT notification_id PK
        VARCHAR(255) user_id FK
        BIGINT template_id FK
        VARCHAR(100) notification_type
        ENUM status
    }

    notification_logs {
        BIGINT log_id PK
        BIGINT notification_id FK
        ENUM channel
        ENUM status
    }

    notification_queues {
        BIGINT queue_id PK
        BIGINT notification_id FK
        ENUM channel
        INT priority
    }

    push_subscriptions {
        BIGINT subscription_id PK
        VARCHAR(255) user_id FK
        VARCHAR(2048) endpoint UK
    }

    user_profiles ||--|{ notifications : "receives"
    notification_templates }o--|{ notifications : "uses"
    notifications ||--|{ notification_logs : "is logged by"
    notifications ||--|{ notification_queues : "is queued for"
    user_profiles ||--|{ push_subscriptions : "has"
```
10. Audit Logging and Security Monitoring System ER-Diagram
```mermaid
erDiagram

    user_profiles { VARCHAR(255) keycloak_user_id PK }

    audit_logs {
        BIGINT log_id PK
        VARCHAR(255) user_id FK "Nullable"
        VARCHAR(255) action
        VARCHAR(100) resource_type
        VARCHAR(255) resource_id
        TIMESTAMP timestamp
    }

    security_logs {
        BIGINT log_id PK
        VARCHAR(255) user_id FK "Nullable"
        ENUM event_type
        VARCHAR(45) ip_address
        BOOLEAN success
        TIMESTAMP timestamp
    }

    data_change_logs {
        BIGINT change_id PK
        VARCHAR(100) table_name
        VARCHAR(255) record_id
        ENUM operation
        JSON old_data_json
        JSON new_data_json
    }

    login_history {
        BIGINT login_id PK
        VARCHAR(255) user_id FK
        VARCHAR(45) ip_address
        BOOLEAN success
        TIMESTAMP attempted_at
    }

    security_incidents {
        BIGINT incident_id PK
        VARCHAR(100) incident_type
        ENUM severity
        TIMESTAMP detected_at
    }

    user_profiles }o--|{ audit_logs : "performs actions in"
    user_profiles }o--|{ security_logs : "generates"
    user_profiles ||--|{ login_history : "attempts"
```