WITH session_marked AS (
    -- 标记每条日志所属的会话ID：每出现一次enter，会话序号+1
    SELECT 
        *,
        SUM(CASE WHEN action_type = 'enter' THEN 1 ELSE 0 END) 
            OVER (ORDER BY action_timestamp, user_id) AS session_id
    FROM seed710_2000sample
),
session_summary AS (
    -- 按会话聚合，提取每个会话的核心属性与最终结果
    SELECT 
        session_id,
        user_id,
        MAX(user_familiarity) AS user_familiarity,
        MAX(CASE WHEN action_type = 'enter' THEN level_id END) AS start_stage,
        MAX(level_id) AS max_reached_stage,
        MAX(CASE WHEN action_type = 'exit' THEN dropout_flag END) AS dropout_flag,
        ROUND(AVG(information_density), 2) AS avg_info_density,
        ROUND(SUM(dwell_time), 2) AS total_dwell_sec,
        COUNT(CASE WHEN action_type = 'click' THEN 1 END) AS total_clicks
    FROM session_marked
    GROUP BY session_id, user_id
)
-- 预览前10个会话数据，验证逻辑
SELECT * FROM session_summary LIMIT 10;