WITH session_marked AS (
    -- Tag each log with its session ID: increment session counter on each 'enter'
    SELECT
        *,
        SUM(CASE WHEN action_type = 'enter' THEN 1 ELSE 0 END)
            OVER (ORDER BY action_timestamp, user_id) AS session_id
    FROM seed710_2000sample
),
session_summary AS (
    -- Aggregate by session: extract core attributes and final outcome
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
-- Preview first 10 sessions to verify logic
SELECT * FROM session_summary LIMIT 10;