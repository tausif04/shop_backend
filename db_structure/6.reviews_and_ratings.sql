-- =================================================================
-- Segment 6: Comprehensive Review and Rating System
-- =================================================================
-- This segment provides the tables needed for a robust system
-- where customers can review products and shops, with moderation
-- and response capabilities.

-- Table: reviews
-- The core table for storing customer reviews of products.
CREATE TABLE reviews (
    review_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT UNSIGNED NOT NULL,
    -- Linking to order_item_id ensures the review is for a specific purchased item.
    order_item_id BIGINT UNSIGNED NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    shop_id BIGINT UNSIGNED NOT NULL,
    rating TINYINT UNSIGNED NOT NULL, -- Rating from 1 to 5.
    title VARCHAR(255),
    review_text TEXT,
    -- A crucial flag to indicate if the reviewer actually purchased the item.
    is_verified_purchase BOOLEAN NOT NULL DEFAULT FALSE,
    status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- A customer should only be able to review a specific purchased item once.
    UNIQUE KEY uk_review_order_item (order_item_id),
    CONSTRAINT fk_reviews_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reviews_order_item
        FOREIGN KEY (order_item_id) REFERENCES order_items(item_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reviews_customer
        FOREIGN KEY (customer_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reviews_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE,
    -- Ensures the rating value is within the valid range.
    CONSTRAINT chk_rating CHECK (rating >= 1 AND rating <= 5)
);

-- Indexes for reviews
CREATE INDEX idx_reviews_product_id_status ON reviews(product_id, status);
CREATE INDEX idx_reviews_shop_id_status ON reviews(shop_id, status);
CREATE INDEX idx_reviews_customer_id ON reviews(customer_id);


-- Table: review_images
-- Allows users to attach images to their reviews.
CREATE TABLE review_images (
    image_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    review_id BIGINT UNSIGNED NOT NULL,
    image_url VARCHAR(2048) NOT NULL,
    alt_text VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_images_review
        FOREIGN KEY (review_id) REFERENCES reviews(review_id)
        ON DELETE CASCADE
);


-- Table: review_responses
-- Allows shop owners or admins to respond to customer reviews.
CREATE TABLE review_responses (
    response_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    review_id BIGINT UNSIGNED NOT NULL,
    -- The user (shop owner, staff, admin) who is responding.
    responder_id VARCHAR(255) NOT NULL,
    response_text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Only one response per review is allowed.
    UNIQUE KEY uk_review_response (review_id),
    CONSTRAINT fk_review_responses_review
        FOREIGN KEY (review_id) REFERENCES reviews(review_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_review_responses_responder
        FOREIGN KEY (responder_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE
);


-- Table: review_votes
-- Captures "helpful" or "not helpful" votes on reviews from other users.
CREATE TABLE review_votes (
    vote_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    review_id BIGINT UNSIGNED NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    vote_type ENUM('helpful', 'not_helpful') NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_votes_review
        FOREIGN KEY (review_id) REFERENCES reviews(review_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_review_votes_user
        FOREIGN KEY (user_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    -- A user can only vote once per review.
    UNIQUE KEY uk_review_user_vote (review_id, user_id)
);


-- Table: shop_reviews
-- For reviews about the shop itself, separate from product reviews.
CREATE TABLE shop_reviews (
    shop_review_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    customer_id VARCHAR(255) NOT NULL,
    -- Link to an order to verify the customer has experience with the shop.
    order_id BIGINT UNSIGNED NOT NULL,
    rating TINYINT UNSIGNED NOT NULL,
    title VARCHAR(255),
    review_text TEXT,
    status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_shop_reviews_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_shop_reviews_customer
        FOREIGN KEY (customer_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_shop_reviews_order
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    -- A customer can review a shop based on a specific order only once.
    UNIQUE KEY uk_shop_customer_order_review (shop_id, customer_id, order_id),
    CONSTRAINT chk_shop_rating CHECK (rating >= 1 AND rating <= 5)
);

-- Indexes for shop_reviews
CREATE INDEX idx_shop_reviews_shop_id_status ON shop_reviews(shop_id, status);


-- Table: rating_summaries
-- Denormalized table for high-performance retrieval of aggregated rating data.
CREATE TABLE rating_summaries (
    summary_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- Can be for a product or a shop.
    product_id BIGINT UNSIGNED,
    shop_id BIGINT UNSIGNED,
    average_rating DECIMAL(3, 2) NOT NULL DEFAULT 0.00,
    total_reviews INT UNSIGNED NOT NULL DEFAULT 0,
    rating_1_count INT UNSIGNED NOT NULL DEFAULT 0,
    rating_2_count INT UNSIGNED NOT NULL DEFAULT 0,
    rating_3_count INT UNSIGNED NOT NULL DEFAULT 0,
    rating_4_count INT UNSIGNED NOT NULL DEFAULT 0,
    rating_5_count INT UNSIGNED NOT NULL DEFAULT 0,
    last_updated_at TIMESTAMP NOT NULL,

    -- Ensure either product_id or shop_id is set, but not both.
    CONSTRAINT chk_summary_target CHECK (
        (product_id IS NOT NULL AND shop_id IS NULL) OR
        (product_id IS NULL AND shop_id IS NOT NULL)
    ),
    -- Create unique keys to ensure only one summary row per product or shop.
    UNIQUE KEY uk_rating_summary_product (product_id),
    UNIQUE KEY uk_rating_summary_shop (shop_id)
);


-- Table: review_moderation
-- Creates an audit trail for all moderation actions on reviews.
CREATE TABLE review_moderation (
    moderation_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    review_id BIGINT UNSIGNED NOT NULL,
    moderator_id VARCHAR(255) NOT NULL, -- Keycloak ID of the admin/moderator
    action ENUM('approve', 'reject', 'flag', 'edit') NOT NULL,
    reason TEXT,
    moderated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_review_moderation_review
        FOREIGN KEY (review_id) REFERENCES reviews(review_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_review_moderation_moderator
        FOREIGN KEY (moderator_id) REFERENCES user_profiles(keycloak_user_id)
        ON DELETE NO ACTION
);

-- Indexes for review_moderation
CREATE INDEX idx_review_moderation_review_id ON review_moderation(review_id);
CREATE INDEX idx_review_moderation_moderator_id ON review_moderation(moderator_id);
