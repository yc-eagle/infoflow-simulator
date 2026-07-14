"""
Generate 5 diverse stress-test datasets from the simulation engine.

Each dataset varies a different dimension so the dashboard's schema-adaptive
logic can be verified across heterogeneous inputs.

Usage:
    cd data && python generate_stress_tests.py
"""
import yaml
import sys
import os

# Allow running from data/ or project root
if os.path.exists("program.py"):
    sys.path.insert(0, ".")
elif os.path.exists("data/program.py"):
    sys.path.insert(0, "data")

from program import run_simulation

SCENARIOS = {
    "stress_1_default": {
        "random_seed": 710,
        "target_logs": 2000,
        "num_users": 130,
        "max_stage": 5,
    },
    "stress_2_small_sample": {
        "random_seed": 42,
        "target_logs": 300,
        "num_users": 30,
        "max_stage": 5,
    },
    "stress_3_high_difficulty": {
        "random_seed": 999,
        "target_logs": 1500,
        "num_users": 100,
        "max_stage": 5,
        "stage_base_difficulty": {1: 0.4, 2: 0.55, 3: 0.7, 4: 0.8, 5: 0.9},
    },
    "stress_4_low_familiarity": {
        "random_seed": 555,
        "target_logs": 2000,
        "num_users": 130,
        "max_stage": 5,
        # users skewed toward low familiarity (override in generated data)
    },
    "stress_5_extra_wide": {
        "random_seed": 123,
        "target_logs": 3000,
        "num_users": 200,
        "max_stage": 5,
    },
}


def main():
    os.makedirs("stress_test_output", exist_ok=True)

    for name, overrides in SCENARIOS.items():
        print(f"\n{'='*50}")
        print(f"Generating: {name}")
        print(f"Overrides: {overrides}")
        print(f"{'='*50}")

        df = run_simulation(**overrides)
        path = f"stress_test_output/{name}.csv"
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  → Saved {len(df)} rows to {path}")
        print(f"  → Columns: {list(df.columns)}")
        print(f"  → Unique users: {df['user_id'].nunique()}")
        print(f"  → Dropout rate: {df[df['action_type']=='exit']['dropout_flag'].mean():.2%}")

    print(f"\n[OK] All 5 stress-test datasets saved to data/stress_test_output/")


if __name__ == "__main__":
    main()
