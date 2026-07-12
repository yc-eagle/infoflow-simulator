import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ============================================================
# 1. 全局配置（固定随机种子，保证100%可复现）
# ============================================================
RANDOM_SEED = 710
np.random.seed(RANDOM_SEED)

TARGET_LOGS = 2000       # 目标日志总量
NUM_USERS = 130          # 虚拟用户总数
MAX_STAGE = 5           # 最高阶段，完成阶段5视为通关

# 行为核心参数
BASE_DWELL_TIME = 2.5       # 单节点基础停留时间（秒）
BASE_ACCURACY = 0.85        # 基础答题正确率
DIFFICULTY_PENALTY = 0.55   # 难度对正确率的惩罚系数：难度越高，正确率越低
DIFFICULTY_NOISE = 0.15     # 每阶段困难度随机波动范围（±0.15）
ERROR_DWELL_MULTIPLIER = 1.4  # 答错时的停留时间倍率（答错思考更久）

# 信息密度和用户熟悉度影响权重参数 
FAMILIARITY_ACC_BOOST = 0.04    # 熟悉度每升1级，正确率提升4个百分点
DENSITY_ACC_PENALTY = 0.03     # 信息密度每升1点，正确下降3个百分点
FAMILIARITY_SPEED_BOOST = 0.08 # 熟悉度每升1级，停留时间减少8%
DENSITY_DWELL_PENALTY = 0.06   # 信息密度每升1点，停留时间增加6%

# 流失概率参数
BASE_ENTER_EXIT_RATE = 0.1   # 进入关卡后直接退出的基础概率
BASE_STEP_DROPOUT_RATE = 0.04 # 每完成一次点击后中途放弃的基础概率

# ============================================================
# 2. 阶段基础难度配置（1~5阶段难度递增）
# ============================================================
stage_base_difficulty = {
    1: 0.2,   # 阶段1基础难度
    2: 0.35,
    3: 0.5,
    4: 0.65,
    5: 0.8    # 阶段5基础难度
}

# ==========各阶段信息密度取值范围（1-10，阶段越高区间越高） ==========
stage_density_range = {
    1: (1, 10),   
    2: (1, 10),  
    3: (1, 10),  
    4: (1, 10), 
    5: (1, 10)   
}

# ============================================================
# 3. 用户个体属性（操作速度 + 答题能力的个体差异）
# ============================================================
user_ids = [f"user_{i:03d}" for i in range(1, NUM_USERS + 1)]

# 速度因子：<1 操作更快，>1 操作更慢
user_speed_factor = np.random.normal(loc=1.0, scale=0.2, size=NUM_USERS)
user_speed_factor = np.clip(user_speed_factor, 0.6, 1.7)

# 能力因子：>1 答题正确率更高，<1 正确率更低
user_ability_factor = np.random.normal(loc=1.0, scale=0.12, size=NUM_USERS)
user_ability_factor = np.clip(user_ability_factor, 0.75, 1.25)

# 用户熟悉度：1~5级固定属性
user_familiarity = np.random.randint(low=1, high=6, size=NUM_USERS)

# ============================================================
# 4. 核心模拟：正误判断 + 阶段递进 + 随机难度
# ============================================================
logs = []
log_count = 0
current_time = datetime(2026, 7, 10, 9, 0, 0)
user_idx = 0

while log_count < TARGET_LOGS:
    uid = user_ids[user_idx % NUM_USERS]
    speed = user_speed_factor[user_idx % NUM_USERS]
    ability = user_ability_factor[user_idx % NUM_USERS]
    familiarity = user_familiarity[user_idx % NUM_USERS]
    
    # 随机选择起始阶段（1~5任意阶段enter）
    start_stage = np.random.randint(1, MAX_STAGE + 1)

    # --------------------------
    # 第一步：enter 进入对应阶段
    # --------------------------
    # 进入阶段的信息密度取该阶段区间的中间值
    d_min, d_max = stage_density_range[start_stage]
    enter_density = round((d_min + d_max) / 2, 0)
            
    dwell_enter = max(0.5, np.random.normal(
        loc=BASE_DWELL_TIME * (1 + stage_base_difficulty[start_stage] * 0.5) / speed,
        scale=0.6
    ))
    logs.append({
        "user_id": uid,
        "level_id": start_stage,
        "action_timestamp": current_time,
        "action_type": "enter",
        "dwell_time": round(dwell_enter, 2),
        "dropout_flag": 0,
        "information_density": int(enter_density),
        "user_familiarity": familiarity
    })

    log_count += 1
    current_time += timedelta(seconds=dwell_enter)

    # --------------------------
    # 分支：enter后直接退出（未开始答题就放弃）
    # --------------------------
    enter_exit_prob = BASE_ENTER_EXIT_RATE * (1 + (start_stage - 1) * 0.25)
    if np.random.random() < enter_exit_prob:
        dwell_exit = max(0.2, np.random.normal(loc=0.8 / speed, scale=0.2))
        logs.append({
            "user_id": uid,
            "level_id": start_stage,
            "action_timestamp": current_time,
            "action_type": "exit",
            "dwell_time": round(dwell_exit, 2),
            "dropout_flag": 1,
            "information_density": int(enter_density),
            "user_familiarity": familiarity
        })
        log_count += 1
        current_time += timedelta(seconds=dwell_exit)
        current_time += timedelta(seconds=np.random.randint(15, 60))
        user_idx += 1
        continue

    # --------------------------
    # 第二步：循环点击答题，逐阶段推进
    # --------------------------
    current_stage = start_stage
    is_dropout = False

    while current_stage <= MAX_STAGE and not is_dropout and log_count < TARGET_LOGS:
        # 1. 为当前阶段生成随机困难度（基础难度 ± 随机波动）
        base_diff = stage_base_difficulty[current_stage]
        actual_difficulty = np.clip(
            base_diff + np.random.uniform(-DIFFICULTY_NOISE, DIFFICULTY_NOISE),
            0.1, 0.95
        )

        # ========== 生成当前节点的信息密度（该阶段范围内随机整数） ==========
        d_min, d_max = stage_density_range[current_stage]
        information_density = np.random.randint(d_min, d_max + 1)
        last_density = information_density

        # 2. 计算本次点击的实际正确率
        # 公式：基础正确率 × 用户能力 - 难度惩罚
        accuracy = BASE_ACCURACY * ability - actual_difficulty * DIFFICULTY_PENALTY
        accuracy = accuracy + (familiarity - 3) * FAMILIARITY_ACC_BOOST \
                            - (information_density - 5) * DENSITY_ACC_PENALTY
        accuracy = np.clip(accuracy, 0.1, 0.95)  # 限制在合理范围

        # 3. 计算停留时间：难度越高，思考越久；答错停留更久
        base_dwell = BASE_DWELL_TIME * (1 + actual_difficulty * 0.8) / speed
        # 熟悉度越高越快，信息密度越高越慢
        dwell_click = base_dwell * (1 - (familiarity - 3) * FAMILIARITY_SPEED_BOOST) \
                                * (1 + (information_density - 5) * DENSITY_DWELL_PENALTY)
        dwell_click = max(0.3, np.random.normal(
            loc=BASE_DWELL_TIME * (1 + actual_difficulty * 0.8) / speed,
            scale=0.5
        ))
        is_correct = np.random.random() < accuracy
        if not is_correct:
            dwell_click *= ERROR_DWELL_MULTIPLIER

        # 4. 记录click行为
        logs.append({
            "user_id": uid,
            "level_id": current_stage,
            "action_timestamp": current_time,
            "action_type": "click",
            "dwell_time": round(dwell_click, 2),
            "dropout_flag": 0,
            "information_density": int(information_density),
            "user_familiarity": familiarity
        })
        log_count += 1
        current_time += timedelta(seconds=dwell_click)

        # 5. 答对进入下一阶段，答错留在当前阶段
        if is_correct:
            current_stage += 1

        # 6. 判断是否中途放弃（难度越高，放弃概率越大）
        dropout_prob = BASE_STEP_DROPOUT_RATE * (1 + (current_stage - 1) * 0.25)
        if np.random.random() < dropout_prob:
            is_dropout = True
            break

    # --------------------------
    # 第三步：exit 退出关卡
    # --------------------------
    dwell_exit = max(0.2, np.random.normal(loc=1.0 / speed, scale=0.3))
    # 通关判定：current_stage > 5 说明完成了全部5个阶段
    is_clear = current_stage > MAX_STAGE
    dropout_flag = 0 if is_clear else 1

    logs.append({
        "user_id": uid,
        "level_id": min(current_stage, MAX_STAGE),
        "action_timestamp": current_time,
        "action_type": "exit",
        "dwell_time": round(dwell_exit, 2),
        "dropout_flag": dropout_flag,
        "information_density": int(last_density),
        "user_familiarity": familiarity
    })
    log_count += 1
    current_time += timedelta(seconds=dwell_exit)

    # 会话间随机时间间隔
    current_time += timedelta(seconds=np.random.randint(15, 60))
    user_idx += 1

# ============================================================
# 5. 数据整理与结果输出
# ============================================================
df = pd.DataFrame(logs)
df = df.sort_values("action_timestamp").reset_index(drop=True)
df["action_timestamp"] = df["action_timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

# 打印统计概览
print("=" * 60)
print(f"生成日志总数：{len(df)} 条（目标区间 500-1000）")
print(f"涉及用户数：{df['user_id'].nunique()} 人")
print(f"阶段范围：1 ~ {MAX_STAGE}")
print(f"信息密度范围：{df['information_density'].min()} ~ {df['information_density'].max()}")
print(f"用户熟悉度分布：")
print(df.drop_duplicates("user_id")["user_familiarity"].value_counts().sort_index().to_string())

print("\n行为类型分布：")
print(df["action_type"].value_counts().to_string())

exit_df = df[df["action_type"] == "exit"]
print(f"\n整体通关率：{(exit_df['dropout_flag'] == 0).mean():.2%}")
print(f"整体放弃率：{exit_df['dropout_flag'].mean():.2%}")

# ==========各起始阶段的本层通关率 ==========

temp_df = df.copy()
temp_df["session_id"] = (temp_df["action_type"] == "enter").cumsum()

# 提取每个会话的基础信息
session_start = temp_df[temp_df["action_type"] == "enter"][["session_id", "level_id"]].rename(
    columns={"level_id": "start_stage"}
)
session_max_stage = temp_df.groupby("session_id")["level_id"].max().reset_index().rename(
    columns={"level_id": "max_stage"}
)
session_final = temp_df[temp_df["action_type"] == "exit"][["session_id", "dropout_flag"]]

# 合并会话全量信息
session_info = session_start.merge(session_max_stage, on="session_id").merge(session_final, on="session_id")

# 定义单层通关规则
def judge_clear_current(row):
    if row["start_stage"] == MAX_STAGE:
        return row["dropout_flag"] == 0
    else:
        return row["max_stage"] > row["start_stage"]

session_info["clear_current_stage"] = session_info.apply(judge_clear_current, axis=1)

# 输出统计结果
print("\n各起始阶段的本层通关率：")
stage_clear_rate = (
    session_info.groupby("start_stage")["clear_current_stage"]
    .mean()
    .round(4)
    .mul(100)
    .astype(str) + " %"
)
print(stage_clear_rate.to_string())

# 保存CSV
df.to_csv("maze_stage_behavior_logs_seed710.csv", index=False, encoding="utf-8-sig")
print("\n数据集已保存为 maze_stage_behavior_logs_seed710.csv")
