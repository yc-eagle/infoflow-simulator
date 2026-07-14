import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# ============ 图2：Density_Dropout（修复版） ============
print("\n📊 正在处理 Sheet 2：Density_Dropout")
df2 = pd.read_excel('dropout_tables_EN.xlsx', sheet_name='Density_Dropout')

# 🔧 修复：清理列名（转小写 + 去空格）
df2.columns = df2.columns.str.strip().str.lower()

print(f"  数据量：{len(df2)} 行，列名：{list(df2.columns)}")

if 'information_density' in df2.columns and 'dropout_flag' in df2.columns:
    summary2 = df2.groupby('information_density')['dropout_flag'].agg(
        total='count', dropped='sum'
    ).reset_index()
    summary2['dropout_rate'] = (summary2['dropped'] / summary2['total']) * 100

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=summary2, x='information_density', y='dropout_rate', s=120, color='#E67E22')
    sns.regplot(data=summary2, x='information_density', y='dropout_rate', scatter=False, color='#27AE60', line_kws={"linewidth": 2})
    plt.title('Figure 2: Information Density vs Dropout Rate', fontsize=14, pad=15)
    plt.xlabel('Information Density', fontsize=12)
    plt.ylabel('Dropout Rate (%)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.5)
    for i in range(len(summary2)):
        plt.text(summary2['information_density'][i], summary2['dropout_rate'][i] + 1,
                 f"{summary2['dropout_rate'][i]:.1f}%", ha='center', fontsize=10)
    plt.tight_layout()
    plt.savefig('chart_2_density_dropout.png', dpi=300)
    print("  ✅ 图2已保存：chart_2_density_dropout.png")
    plt.close()
else:
    print("  ⚠️ 找不到 information_density 或 dropout_flag 列，跳过图2")
    print(f"     当前列名：{list(df2.columns)}")  # 调试用，告诉你实际有哪些列
