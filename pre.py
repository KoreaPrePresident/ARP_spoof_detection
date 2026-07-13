import pandas as pd
import os
from collections import deque


# =========================
# 설정
# =========================

ROOT_DIR = "."       # 현재 폴더
OUTPUT_FILE = "processed_dataset.csv"


# =========================
# CSV 모두 수집
# =========================

all_data = []


for root, dirs, files in os.walk(ROOT_DIR):

    for file in files:

        if file.endswith(".csv"):

            path = os.path.join(root, file)

            print("Loading:", path)

            df = pd.read_csv(path)


            # -------------------------
            # Label 지정
            # -------------------------

            if "attack" in file.lower():
                df["Label"] = 1

            elif "normal" in file.lower():
                df["Label"] = 0

            else:
                continue


            # # 어떤 환경인지 기록 (선택)
            # df["capture_type"] = os.path.basename(root)


            all_data.append(df)



# =========================
# 데이터 합치기
# =========================

data = pd.concat(
    all_data,
    ignore_index=True
)


# timestamp 기준 정렬
data = data.sort_values(
    by="time_stamp"
).reset_index(drop=True)



# =========================
# Interval
# =========================

data["interval"] = data["time_stamp"].diff()

data["interval"] = data["interval"].fillna(0)



# =========================
# PPS
# 최근 1초 패킷 개수
# =========================

timestamps = data["time_stamp"].values

pps = []

window = deque()


for t in timestamps:

    window.append(t)

    while window[0] < t - 1:
        window.popleft()

    pps.append(len(window))


data["pps"] = pps



# =========================
# Jitter
# =========================

data["jitter"] = (
    data["interval"]
    .diff()
    .abs()
)

data["jitter"] = data["jitter"].fillna(0)



# =========================
# 저장
# =========================

data.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\n완료")
print(data.head())
print(data["Label"].value_counts())



#------------------------------------------
#아래서부터는 실행결과
# Accuracy : 0.7024787585141493

# Classification Report
#               precision    recall  f1-score   support

#            0       0.75      0.71      0.73      7991
#            1       0.65      0.69      0.67      6250

#     accuracy                           0.70     14241
#    macro avg       0.70      0.70      0.70     14241
# weighted avg       0.71      0.70      0.70     14241


# Confusion Matrix
# [[5665 2326]
#  [1911 4339]]

# Feature Importance
# ttl: 0.11366
# proto: 0.19729
# Len: 0.16028
# interval: 0.19558
# pps: 0.27203
# jitter: 0.06116

# model saved
# PS C:\Users\bubbl\Desktop\subpcanal> ^C
# PS C:\Users\bubbl\Desktop\subpcanal> 
# PS C:\Users\bubbl\Desktop\subpcanal>  c:; cd 'c:\Users\bubbl\Desktop\subpcanal'; & 'C:\Users\bubbl\AppData\Local\Programs\Python\Python313\python.exe' 'c:\Users\bubbl\.vscode\extensions\ms-python.debugpy-2026.6.0-win32-x64\bundled\libs\debugpy\launcher' '50866' '--' 'C:\Users\bubbl\Desktop\subpcanal\decision_tree.py' 
# Accuracy : 0.7219296397724879

# Classification Report
#               precision    recall  f1-score   support

#            0       0.74      0.77      0.76      7991
#            1       0.69      0.66      0.68      6250

#     accuracy                           0.72     14241
#    macro avg       0.72      0.72      0.72     14241
# weighted avg       0.72      0.72      0.72     14241


# Confusion Matrix
# [[6151 1840]
#  [2120 4130]]

# Feature Importance
# ttl: 0.11967
# proto: 0.12440
# Len: 0.16588
# interval: 0.17675
# pps: 0.32389
# jitter: 0.08941

# model saved