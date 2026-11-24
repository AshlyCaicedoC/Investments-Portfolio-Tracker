CREATE TABLE cash_account (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    balance  NUMERIC(14, 2) NOT NULL,
    CONSTRAINT balance CHECK (balance >= 0)
);

-- One implicit account, so exactly one row.
INSERT INTO cash_account (id, balance) VALUES (1, 0);

CREATE TABLE portfolios (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    name     VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE assets (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10)  NOT NULL UNIQUE,
    issuer   VARCHAR(100) NOT NULL
);

CREATE TABLE transactions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    portfolio_id    INT NOT NULL,
    asset_id        INT NOT NULL,
    side            ENUM('buy', 'sell') NOT NULL,
    quantity        DECIMAL(14, 4) NOT NULL,
    price_per_share DECIMAL(14, 4) NOT NULL,
    trade_date      DATETIME NOT NULL,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios (id),
    FOREIGN KEY (asset_id) REFERENCES assets (id),
    CONSTRAINT ck_transaction_quantity_positive CHECK (quantity > 0),
    CONSTRAINT ck_transaction_price_not_negative CHECK (price_per_share >= 0)
);