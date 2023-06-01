CREATE TABLE IF NOT EXISTS financial_data (
       symbol char(10),
       date DATE,
       open_price FLOAT8,
       close_price FLOAT8,
       volume INT,
       PRIMARY KEY(symbol, date)
);
