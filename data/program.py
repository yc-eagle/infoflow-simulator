"""
InfoFlow Simulator — Simulation Engine.

Generates synthetic behavioral telemetry logs simulating virtual users
navigating through information structures of varying complexity.

Usage:
    python data/program.py                          # run with config.yaml defaults
    python data/program.py --seed 42 --logs 1000    # CLI overrides
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import argparse
import os
import sys

# Try to load YAML config; fall back to hardcoded defaults if unavailable
try:
    import yaml

    _CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    if os.path.exists(_CONFIG_PATH):
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            _CFG = yaml.safe_load(f)
    else:
        _CFG = {}
except ImportError:
    _CFG = {}


def _cfg(key, default):
    """Read config value with fallback."""
    return _CFG.get(key, default)


# ============================================================
# 1. Global configuration (overridable via run_simulation kwargs)
# ============================================================
def run_simulation(
    random_seed=None,
    target_logs=None,
    num_users=None,
    max_stage=None,
    base_dwell_time=None,
    base_accuracy=None,
    difficulty_penalty=None,
    difficulty_noise=None,
    error_dwell_multiplier=None,
    familiarity_acc_boost=None,
    density_acc_penalty=None,
    familiarity_speed_boost=None,
    density_dwell_penalty=None,
    base_enter_exit_rate=None,
    base_step_dropout_rate=None,
    stage_base_difficulty=None,
    stage_density_range=None,
    output_csv=None,
):
    """
    Run the simulation and return a DataFrame of behavioral logs.

    All parameters are optional — omitted values fall back to config.yaml,
    then to hardcoded defaults.
    """
    # --- Resolve parameters: explicit arg > config.yaml > hardcoded ---
    SEED = random_seed if random_seed is not None else _cfg("random_seed", 710)
    TARGET = target_logs if target_logs is not None else _cfg("target_logs", 2000)
    N_USERS = num_users if num_users is not None else _cfg("num_users", 130)
    MAX_STAGE = max_stage if max_stage is not None else _cfg("max_stage", 5)

    BASE_DWELL = base_dwell_time if base_dwell_time is not None else _cfg("base_dwell_time", 2.5)
    BASE_ACC = base_accuracy if base_accuracy is not None else _cfg("base_accuracy", 0.85)
    DIFF_PENALTY = difficulty_penalty if difficulty_penalty is not None else _cfg("difficulty_penalty", 0.55)
    DIFF_NOISE = difficulty_noise if difficulty_noise is not None else _cfg("difficulty_noise", 0.15)
    ERR_MULT = error_dwell_multiplier if error_dwell_multiplier is not None else _cfg("error_dwell_multiplier", 1.4)

    FAM_ACC = familiarity_acc_boost if familiarity_acc_boost is not None else _cfg("familiarity_acc_boost", 0.04)
    DEN_ACC = density_acc_penalty if density_acc_penalty is not None else _cfg("density_acc_penalty", 0.03)
    FAM_SPEED = familiarity_speed_boost if familiarity_speed_boost is not None else _cfg("familiarity_speed_boost", 0.08)
    DEN_DWELL = density_dwell_penalty if density_dwell_penalty is not None else _cfg("density_dwell_penalty", 0.06)

    ENTER_EXIT = base_enter_exit_rate if base_enter_exit_rate is not None else _cfg("base_enter_exit_rate", 0.1)
    STEP_DROP = base_step_dropout_rate if base_step_dropout_rate is not None else _cfg("base_step_dropout_rate", 0.04)

    STAGE_DIFF = stage_base_difficulty if stage_base_difficulty is not None else _cfg("stage_base_difficulty", {
        1: 0.2, 2: 0.35, 3: 0.5, 4: 0.65, 5: 0.8,
    })
    DENSITY_RANGE = stage_density_range if stage_density_range is not None else _cfg("stage_density_range", {
        1: [1, 10], 2: [1, 10], 3: [1, 10], 4: [1, 10], 5: [1, 10],
    })

    np.random.seed(SEED)

    # ============================================================
    # 2. User profile generation
    # ============================================================
    user_ids = [f"user_{i:03d}" for i in range(1, N_USERS + 1)]
    user_speed_factor = np.clip(np.random.normal(1.0, 0.2, N_USERS), 0.6, 1.7)
    user_ability_factor = np.clip(np.random.normal(1.0, 0.12, N_USERS), 0.75, 1.25)
    user_familiarity = np.random.randint(1, 6, size=N_USERS)

    # ============================================================
    # 3. Core simulation loop
    # ============================================================
    logs = []
    log_count = 0
    current_time = datetime(2026, 7, 10, 9, 0, 0)
    user_idx = 0

    while log_count < TARGET:
        uid = user_ids[user_idx % N_USERS]
        speed = user_speed_factor[user_idx % N_USERS]
        ability = user_ability_factor[user_idx % N_USERS]
        familiarity = user_familiarity[user_idx % N_USERS]

        start_stage = np.random.randint(1, MAX_STAGE + 1)

        # --- Enter ---
        d_min, d_max = DENSITY_RANGE[start_stage]
        enter_density = round((d_min + d_max) / 2, 0)

        dwell_enter = max(0.5, np.random.normal(
            loc=BASE_DWELL * (1 + STAGE_DIFF[start_stage] * 0.5) / speed, scale=0.6,
        ))
        logs.append({
            "user_id": uid,
            "level_id": start_stage,
            "action_timestamp": current_time,
            "action_type": "enter",
            "dwell_time": round(dwell_enter, 2),
            "dropout_flag": 0,
            "information_density": int(enter_density),
            "user_familiarity": familiarity,
        })
        log_count += 1
        current_time += timedelta(seconds=dwell_enter)

        # --- Early exit branch ---
        enter_exit_prob = ENTER_EXIT * (1 + (start_stage - 1) * 0.25)
        if np.random.random() < enter_exit_prob:
            dwell_exit = max(0.2, np.random.normal(loc=0.8 / speed, scale=0.2))
            logs.append({
                "user_id": uid, "level_id": start_stage,
                "action_timestamp": current_time, "action_type": "exit",
                "dwell_time": round(dwell_exit, 2), "dropout_flag": 1,
                "information_density": int(enter_density), "user_familiarity": familiarity,
            })
            log_count += 1
            current_time += timedelta(seconds=dwell_exit)
            current_time += timedelta(seconds=np.random.randint(15, 60))
            user_idx += 1
            continue

        # --- Click-loop progression ---
        current_stage = start_stage
        is_dropout = False

        while current_stage <= MAX_STAGE and not is_dropout and log_count < TARGET:
            base_diff = STAGE_DIFF[current_stage]
            actual_difficulty = np.clip(
                base_diff + np.random.uniform(-DIFF_NOISE, DIFF_NOISE), 0.1, 0.95,
            )
            d_min, d_max = DENSITY_RANGE[current_stage]
            information_density = np.random.randint(d_min, d_max + 1)
            last_density = information_density

            accuracy = BASE_ACC * ability - actual_difficulty * DIFF_PENALTY
            accuracy = accuracy + (familiarity - 3) * FAM_ACC - (information_density - 5) * DEN_ACC
            accuracy = np.clip(accuracy, 0.1, 0.95)

            dwell_click = max(0.3, np.random.normal(
                loc=BASE_DWELL * (1 + actual_difficulty * 0.8) / speed, scale=0.5,
            ))
            is_correct = np.random.random() < accuracy
            if not is_correct:
                dwell_click *= ERR_MULT

            logs.append({
                "user_id": uid, "level_id": current_stage,
                "action_timestamp": current_time, "action_type": "click",
                "dwell_time": round(dwell_click, 2), "dropout_flag": 0,
                "information_density": int(information_density), "user_familiarity": familiarity,
            })
            log_count += 1
            current_time += timedelta(seconds=dwell_click)

            if is_correct:
                current_stage += 1

            dropout_prob = STEP_DROP * (1 + (current_stage - 1) * 0.25)
            if np.random.random() < dropout_prob:
                is_dropout = True
                break

        # --- Exit ---
        dwell_exit = max(0.2, np.random.normal(loc=1.0 / speed, scale=0.3))
        is_clear = current_stage > MAX_STAGE
        dropout_flag = 0 if is_clear else 1

        logs.append({
            "user_id": uid, "level_id": min(current_stage, MAX_STAGE),
            "action_timestamp": current_time, "action_type": "exit",
            "dwell_time": round(dwell_exit, 2), "dropout_flag": dropout_flag,
            "information_density": int(last_density), "user_familiarity": familiarity,
        })
        log_count += 1
        current_time += timedelta(seconds=dwell_exit)
        current_time += timedelta(seconds=np.random.randint(15, 60))
        user_idx += 1

    # ============================================================
    # 4. Build and return DataFrame
    # ============================================================
    df = pd.DataFrame(logs)
    df = df.sort_values("action_timestamp").reset_index(drop=True)
    df["action_timestamp"] = df["action_timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df


# ============================================================
# 5. CLI entry point
# ============================================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="InfoFlow Simulation Engine")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--logs", type=int, help="Target log count")
    parser.add_argument("--users", type=int, help="Number of virtual users")
    parser.add_argument("--stages", type=int, help="Max stage count")
    parser.add_argument("--output", type=str, default="maze_stage_behavior_logs_seed710.csv",
                        help="Output CSV path")
    args = parser.parse_args()

    kwargs = {}
    if args.seed is not None:
        kwargs["random_seed"] = args.seed
    if args.logs is not None:
        kwargs["target_logs"] = args.logs
    if args.users is not None:
        kwargs["num_users"] = args.users
    if args.stages is not None:
        kwargs["max_stage"] = args.stages

    df = run_simulation(**kwargs)

    # --- Summary stats ---
    print("=" * 60)
    print(f"Logs generated : {len(df)}")
    print(f"Unique users   : {df['user_id'].nunique()}")
    print(f"Stages         : 1 ~ {df['level_id'].max()}")
    print(f"Density range  : {df['information_density'].min()} ~ {df['information_density'].max()}")
    print(f"Action dist    :\n{df['action_type'].value_counts().to_string()}")
    exit_df = df[df["action_type"] == "exit"]
    print(f"Clear rate     : {(exit_df['dropout_flag'] == 0).mean():.2%}")
    print(f"Dropout rate   : {exit_df['dropout_flag'].mean():.2%}")

    df.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"\nSaved → {args.output}")
