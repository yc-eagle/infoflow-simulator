import sqlite3
import pandas as pd

conn = sqlite3.connect("seed710_2000.db")
# 示例格式，替换成本机真实CSV位置
csv_path = r"d:/z.repos/infoflow-simulator/data/data_inquire/seed710_2000sample.csv"
df = pd.read_csv(csv_path)
# if_exists参数：replace覆盖表、append追加数据
df.to_sql("seed710_2000sample", conn, if_exists="replace", index=False)
conn.close()