import pandas as pd


# =========================
# 설정
# =========================

INPUT_FILE = "processed_dataset.csv"
OUTPUT_FILE = "processed_dataset_no_mac.csv"


# =========================
# CSV 읽기
# =========================

df = pd.read_csv(INPUT_FILE)


# =========================
# MAC 컬럼 제거
# =========================

remove_columns = [
    "MAC_dst",
    "MAC_src",
    "time_stamp",
    "ETher_type",
    "IP_src",
    "IP_dst",
    "sport",
    "dport"
]


df_no_mac = df.drop(
    columns=remove_columns
)



# =========================
# 저장
# =========================

df_no_mac.to_csv(
    OUTPUT_FILE,
    index=False
)


print("완료")
print(df_no_mac.head())
print(df_no_mac.columns)