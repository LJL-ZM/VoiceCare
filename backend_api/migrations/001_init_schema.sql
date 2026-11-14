# 数据库建表 SQL
# 初版：创建用户表和分析记录表
# 执行方式：mysql -u root -p voicare < migrations/001_init_schema.sql

-- 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS voicare DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
USE voicare;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL UNIQUE COMMENT '用户ID',
    name VARCHAR(100) COMMENT '姓名',
    gender VARCHAR(10) COMMENT '性别',
    age INT COMMENT '年龄',
    phone VARCHAR(20) COMMENT '手机号',
    emergency_contact VARCHAR(100) COMMENT '紧急联系人',
    emergency_phone VARCHAR(20) COMMENT '紧急联系人电话',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 分析记录表
CREATE TABLE IF NOT EXISTS analysis_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    task_type VARCHAR(20) NOT NULL COMMENT '任务类型：picture/story/voicemail',
    audio_path VARCHAR(500) COMMENT '音频存储路径(OBS)',
    audio_duration FLOAT COMMENT '音频时长(秒)',
    text TEXT COMMENT '转写文本',
    psd FLOAT COMMENT '静默时间占比',
    ttr FLOAT COMMENT '词汇多样性',
    pause_count INT COMMENT '停顿次数',
    speech_rate FLOAT COMMENT '语速(字/秒)',
    semantic_coherence FLOAT COMMENT '语义连贯性',
    score FLOAT COMMENT '风险评分',
    deviation FLOAT COMMENT '相对基线偏离度',
    baseline_score FLOAT COMMENT '历史基线分数',
    risk_level VARCHAR(20) COMMENT '风险等级：low/medium/high',
    shap_values JSON COMMENT 'SHAP 特征归因',
    report_text TEXT COMMENT 'Agent 简报文本',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='分析记录表';

-- 历史数据表（用于趋势分析）
CREATE TABLE IF NOT EXISTS history_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL COMMENT '用户ID',
    record_id INT NOT NULL COMMENT '关联分析记录ID',
    metric_name VARCHAR(50) NOT NULL COMMENT '指标名称',
    metric_value FLOAT COMMENT '指标值',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_metric (metric_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='历史数据表';

-- 基线表（存储用户个人历史基线）
CREATE TABLE IF NOT EXISTS baselines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL UNIQUE COMMENT '用户ID',
    baseline_score FLOAT COMMENT '基线风险分',
    baseline_metrics JSON COMMENT '基线指标快照',
    sample_count INT DEFAULT 0 COMMENT '样本数量',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='基线表';