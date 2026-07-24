"""
Generate static analysis charts from behavioral telemetry data.

Produces:
  - chart_1_basic_CET.png:     Session completion / exit / time summary
  - chart_2_density_dropout.png:  Information density vs. dropout rate
  - chart_3_familiarity_dropout.png: User familiarity vs. dropout rate

Usage:
    python plot_chart.py
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = "seed710_2000sample.csv"


def plot_density_dropout(df: pd.DataFrame):
    """Scatter: information density vs. dropout rate with OLS trendline."""
    print("\n[Chart 2] Information Density vs. Dropout Rate")
    summary = df.groupby("information_density")["dropout_flag"].agg(
        total="count", dropped="sum"
    ).reset_index()
    summary["dropout_rate"] = (summary["dropped"] / summary["total"]) * 100

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=summary, x="information_density", y="dropout_rate",
                    s=120, color="#E67E22")
    sns.regplot(data=summary, x="information_density", y="dropout_rate",
                scatter=False, color="#27AE60", line_kws={"linewidth": 2})
    plt.title("Figure 2: Information Density vs Dropout Rate", fontsize=14, pad=15)
    plt.xlabel("Information Density", fontsize=12)
    plt.ylabel("Dropout Rate (%)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    for _, row in summary.iterrows():
        plt.text(row["information_density"], row["dropout_rate"] + 1,
                 f"{row['dropout_rate']:.1f}%", ha="center", fontsize=10)
    plt.tight_layout()
    plt.savefig("chart_2_density_dropout.png", dpi=300)
    print("  -> Saved chart_2_density_dropout.png")
    plt.close()


def plot_familiarity_dropout(df: pd.DataFrame):
    """Bar: user familiarity vs. dropout rate."""
    print("\n[Chart 3] User Familiarity vs. Dropout Rate")
    summary = df.groupby("user_familiarity")["dropout_flag"].agg(
        total="count", dropped="sum"
    ).reset_index()
    summary["dropout_rate"] = (summary["dropped"] / summary["total"]) * 100

    plt.figure(figsize=(10, 6))
    sns.barplot(data=summary, x="user_familiarity", y="dropout_rate",
                palette="RdYlGn_r")
    plt.title("Figure 3: User Familiarity vs Dropout Rate", fontsize=14, pad=15)
    plt.xlabel("User Familiarity", fontsize=12)
    plt.ylabel("Dropout Rate (%)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5, axis="y")
    for _, row in summary.iterrows():
        plt.text(row["user_familiarity"] - 1, row["dropout_rate"] + 1,
                 f"{row['dropout_rate']:.1f}%", fontsize=10)
    plt.tight_layout()
    plt.savefig("chart_3_familiarity_dropout.png", dpi=300)
    print("  -> Saved chart_3_familiarity_dropout.png")
    plt.close()


def main():
    print(f"Loading: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    print(f"  -> {len(df):,} rows, columns: {list(df.columns)}")

    # Filter to exit rows for dropout analysis
    exit_df = df[df["action_type"] == "exit"].copy() if "action_type" in df.columns else df

    plot_density_dropout(exit_df)
    plot_familiarity_dropout(exit_df)
    print("\nAll charts generated.")


if __name__ == "__main__":
    main()
