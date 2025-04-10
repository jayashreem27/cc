USE logsdb;

CREATE TABLE IF NOT EXISTS logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    level VARCHAR(10),
    message TEXT,
    service VARCHAR(50)
);
