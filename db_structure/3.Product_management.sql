-- =================================================================
-- Segment 3: Comprehensive Product Management System
-- =================================================================
-- This segment covers everything related to products, including
-- categories, variants, attributes, inventory, and reviews.

-- Table: categories
-- Defines product categories in a hierarchical structure.
CREATE TABLE categories (
    category_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- Self-referencing foreign key for creating category trees (e.g., Electronics > Laptops).
    parent_category_id BIGINT UNSIGNED,
    category_name VARCHAR(255) NOT NULL,
    -- URL-friendly name, important for SEO and clean URLs.
    category_slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    image_url VARCHAR(2048),
    -- Optional commission rate that overrides shop or platform defaults for products in this category.
    commission_rate_override DECIMAL(5, 2),
    sort_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key to itself to establish the parent-child relationship.
    CONSTRAINT fk_categories_parent
        FOREIGN KEY (parent_category_id) REFERENCES categories(category_id)
        ON DELETE SET NULL -- If a parent is deleted, children become top-level categories.
);

-- Indexes for categories
-- Index for efficiently finding child categories.
CREATE INDEX idx_categories_parent_category_id ON categories(parent_category_id);
-- Index on is_active for quickly filtering active/inactive categories.
CREATE INDEX idx_categories_is_active ON categories(is_active);


-- Table: products
-- The main table for storing core product information.
CREATE TABLE products (
    product_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    shop_id BIGINT UNSIGNED NOT NULL,
    category_id BIGINT UNSIGNED NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    -- Slug should be unique within a shop for clean product URLs.
    product_slug VARCHAR(255) NOT NULL,
    description TEXT,
    short_description VARCHAR(512),
    -- Stock Keeping Unit, should be unique per shop.
    sku VARCHAR(100),
    brand VARCHAR(100),
    status ENUM('draft', 'active', 'inactive', 'archived') NOT NULL DEFAULT 'draft',
    featured BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- Foreign key to the shops table.
    CONSTRAINT fk_products_shop
        FOREIGN KEY (shop_id) REFERENCES shops(shop_id)
        ON DELETE CASCADE,
    -- Foreign key to the categories table.
    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE RESTRICT, -- Prevent deleting a category that still has products.
    -- Ensures a product slug is unique for a given shop.
    UNIQUE KEY uk_product_shop_slug (shop_id, product_slug),
    -- Ensures SKU is unique for a given shop.
    UNIQUE KEY uk_product_shop_sku (shop_id, sku)
);

-- Indexes for products
-- Indexes for filtering products by shop, category, and status.
CREATE INDEX idx_products_shop_id ON products(shop_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_status ON products(status);
-- Full-text index for powerful product search.
CREATE FULLTEXT INDEX ft_products_name_desc ON products(product_name, description, short_description);


-- Table: product_variants
-- Stores different versions of a product (e.g., size, color).
CREATE TABLE product_variants (
    variant_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT UNSIGNED NOT NULL,
    variant_name VARCHAR(255), -- e.g., "Red, Large"
    sku VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL,
    compare_price DECIMAL(10, 2), -- The "before" price for sales
    cost_price DECIMAL(10, 2), -- For internal profit calculation
    weight DECIMAL(10, 2), -- For shipping calculations
    dimensions_json JSON, -- e.g., {"height": 10, "width": 5, "depth": 2}
    barcode VARCHAR(100),
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign key to the products table.
    CONSTRAINT fk_product_variants_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE,
    -- Variant SKU should be unique for a given product.
    UNIQUE KEY uk_variant_product_sku (product_id, sku)
);

-- Indexes for product_variants
CREATE INDEX idx_product_variants_product_id ON product_variants(product_id);
CREATE INDEX idx_product_variants_sku ON product_variants(sku);


-- Table: product_attributes
-- Defines reusable attributes like 'Color', 'Size', 'Material'.
CREATE TABLE product_attributes (
    attribute_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    attribute_name VARCHAR(100) NOT NULL UNIQUE,
    attribute_type ENUM('text', 'number', 'boolean', 'select') NOT NULL DEFAULT 'text',
    is_required BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Table: product_attribute_values
-- Assigns specific attribute values to products.
CREATE TABLE product_attribute_values (
    value_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT UNSIGNED NOT NULL,
    attribute_id BIGINT UNSIGNED NOT NULL,
    attribute_value VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys to link values to products and attributes.
    CONSTRAINT fk_product_attribute_values_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_product_attribute_values_attribute
        FOREIGN KEY (attribute_id) REFERENCES product_attributes(attribute_id)
        ON DELETE CASCADE,
    -- A product should only have one value for a given attribute.
    UNIQUE KEY uk_product_attribute (product_id, attribute_id)
);


-- Table: product_images
-- Stores images for products and their variants.
CREATE TABLE product_images (
    image_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT UNSIGNED NOT NULL,
    -- An image can be linked to a specific variant (e.g., a red shirt).
    variant_id BIGINT UNSIGNED,
    image_url VARCHAR(2048) NOT NULL,
    alt_text VARCHAR(255),
    sort_order INT NOT NULL DEFAULT 0,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Foreign keys to products and variants.
    CONSTRAINT fk_product_images_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_product_images_variant
        FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id)
        ON DELETE SET NULL
);

-- Indexes for product_images
CREATE INDEX idx_product_images_product_id ON product_images(product_id);
CREATE INDEX idx_product_images_variant_id ON product_images(variant_id);


-- Table: product_inventory
-- Tracks stock levels for each product variant.
CREATE TABLE product_inventory (
    inventory_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    -- Each variant has its own inventory record.
    variant_id BIGINT UNSIGNED NOT NULL,
    quantity_available INT NOT NULL DEFAULT 0,
    -- Quantity reserved in open carts or pending orders.
    quantity_reserved INT NOT NULL DEFAULT 0,
    reorder_level INT,
    supplier_info_json JSON,
    last_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    -- A variant can only have one inventory record.
    UNIQUE KEY uk_product_inventory_variant_id (variant_id),
    CONSTRAINT fk_product_inventory_variant
        FOREIGN KEY (variant_id) REFERENCES product_variants(variant_id)
        ON DELETE CASCADE
);


-- Table: product_reviews_summary
-- Denormalized table to hold aggregated review data for fast retrieval on product pages.
CREATE TABLE product_reviews_summary (
    summary_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT UNSIGNED NOT NULL,
    average_rating DECIMAL(3, 2) NOT NULL DEFAULT 0.00,
    total_reviews INT UNSIGNED NOT NULL DEFAULT 0,
    -- e.g., {"1": 10, "2": 5, "3": 20, "4": 50, "5": 100}
    rating_distribution_json JSON,
    last_updated_at TIMESTAMP NOT NULL,

    -- A product can only have one review summary.
    UNIQUE KEY uk_product_reviews_summary_product_id (product_id),
    CONSTRAINT fk_product_reviews_summary_product
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);
