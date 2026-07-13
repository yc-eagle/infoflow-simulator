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
        user_id,
        MAX(user_familiarity) AS user_familiarity,
        MAX(CASE WHEN action_type = 'exit' THEN dropout_flag END) AS dropout_flag
    FROM session_marked
    GROUP BY session_id, user_id
)
SELECT 
    user_familiarity AS 用户熟悉度,
    COUNT(*) AS 会话总数,
    SUM(dropout_flag) AS 放弃会话数,
    ROUND(AVG(dropout_flag) * 100, 2) AS 放弃率_百分比
FROM session_summary
GROUP BY user_familiarity
ORDER BY user_familiarity;