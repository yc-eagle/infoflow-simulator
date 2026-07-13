WITH session_marked AS (
    SELECT 
        *,
        SUM(CASE WHEN action_type = 'enter' THEN 1 ELSE 0 END) 
            OVER (ORDER BY action_timestamp, user_id) AS session_id
    FROM seed710_2000sample
),
session_summary AS (
    SELECT 
        session_id,
        ROUND(AVG(information_density), 0) AS info_density_tier,
        MAX(CASE WHEN action_type = 'exit' THEN dropout_flag END) AS dropout_flag
    FROM session_marked
    GROUP BY session_id
)
SELECT 
    info_density_tier AS 信息密度等级,
    COUNT(*) AS 会话总数,
    ROUND(AVG(dropout_flag) * 100, 2) AS 放弃率_百分比
FROM session_summary
GROUP BY info_density_tier
ORDER BY info_density_tier;