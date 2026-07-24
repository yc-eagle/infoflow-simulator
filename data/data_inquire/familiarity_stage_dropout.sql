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
        MAX(user_familiarity) AS user_familiarity,
        MAX(CASE WHEN action_type = 'enter' THEN level_id END) AS start_stage,
        MAX(CASE WHEN action_type = 'exit' THEN dropout_flag END) AS dropout_flag
    FROM session_marked
    GROUP BY session_id
)
SELECT
    user_familiarity,
    start_stage,
    COUNT(*) AS session_count,
    ROUND(AVG(dropout_flag) * 100, 2) AS dropout_rate_pct
FROM session_summary
GROUP BY user_familiarity, start_stage
ORDER BY user_familiarity, start_stage;