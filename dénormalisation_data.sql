T
CREATE TABLE crypto_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    timestamp DATETIME NOT NULL
);

CREATE TABLE traders_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    trade_id BIGINT NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    qty DECIMAL(18, 8) NOT NULL,
    quoteQty DECIMAL(18, 8) NOT NULL,
    time DATETIME NOT NULL,
    isBuyerMaker BOOLEAN NOT NULL,
    isBestMatch BOOLEAN NOT NULL
);