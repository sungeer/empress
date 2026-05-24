


-- 会话表
CREATE TABLE `conversations` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `thread_id` CHAR(18) NOT NULL COMMENT '主题 ID',
    `title` VARCHAR(255) NOT NULL COMMENT '会话主题',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_thread_id` (`thread_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会话表';


-- 消息表
CREATE TABLE `messages` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '主键',
    `conversation_id` INT NOT NULL COMMENT '会话 ID',
    `role` VARCHAR(20) NOT NULL COMMENT '角色',  -- 'system', 'user', 'assistant'
    `content` TEXT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    INDEX `idx_conversation_i`d (`conversation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';
