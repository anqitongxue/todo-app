-- 初始化脚本：建库 + 建表
-- 用法：mysql -P 8080 -u root -p < schema.sql
-- （如果你的 MySQL 是默认 3306 端口，把 -P 8080 去掉）

CREATE DATABASE IF NOT EXISTS todo_app DEFAULT CHARACTER SET utf8mb4;
USE todo_app;

-- 用户表：存账号和密码哈希
CREATE TABLE IF NOT EXISTS users (
    id            INT NOT NULL AUTO_INCREMENT,
    username      VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,   -- 存 bcrypt 哈希，绝不存明文
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY username (username)         -- 用户名唯一，防止重名
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 任务表：每条任务属于某个用户（user_id）
CREATE TABLE IF NOT EXISTS tasks (
    id         INT NOT NULL AUTO_INCREMENT,
    name       VARCHAR(255) NOT NULL,
    done       TINYINT(1) DEFAULT 0,       -- 0=未完成，1=已完成
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_deleted TINYINT(1) DEFAULT 0,       -- 软删除标记：1=已删除
    user_id    INT DEFAULT NULL,           -- 归属用户（逻辑上对应 users.id）
    category   VARCHAR(50) NOT NULL DEFAULT '',
    due_date   DATE DEFAULT NULL,          -- 截止日期，可空
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
