# ARP Spoofing Detection

작년에 정보보안을 공부하면서 네트워크 보안에 꽂혀서 시작한 프로젝트입니다.  
ARP Spoofing을 직접 구현해보고, 이걸 어떻게 탐지할 수 있을까 고민하다가 머신러닝을 활용한 탐지 모델을 만들어보았습니다.

## 프로젝트 배경

두 대의 노트북으로 ARP Spoofing을 실제로 돌려보면서 ping RTT가 어떻게 변하는지 관찰했습니다.  
Scapy로 패킷을 직접 조립도 해보고, Wireshark로 hex 값까지 뜯어보면서 공부했습니다.  
IP Forwarding을 켜고 끌 때 피해자 쪽 통신이 어떻게 되는지도 확인했고, nmap으로 호스트가 안 보이는 경우도 경험했습니다.

결국 “이걸 모델로 탐지할 수 있지 않을까?” 싶어서 본격적으로 데이터 모으고 모델을 만들기 시작했습니다.

## 데이터 수집

총 8가지 상황에서 IPv4 패킷을 각각 1만 개씩, **총 8만 개** 수집했습니다.

- ARP Spoofing 공격 전/후
- 유튜브 보기
- 일반 웹 서핑
- 파일 다운로드
- DNS Query
- 등...

처음에는 timestamp, MAC, IP, Port, Length 등 거의 다 수집했다가,  
ARP랑 크게 상관없는 부분은 빼고 `ttl`, `proto`, `length`, `interval`, `pps`, `jitter` 위주로 정리했습니다.

## 모델 및 결과

`DecisionTreeClassifier`를 사용해서 학습시켰습니다.  
현재 테스트 정확도는 **약 72.2%** 정도 나왔습니다.  
아직 많이 부족하지만, 첫 시도치고 나쁘지 않다고 생각합니다.

모델 파일은 `arp_detector_no_mac.pkl`에 저장해두었습니다.

## 파일 구성

- `pre.py`, `pre_nomac.py` : 데이터 전처리 스크립트
- `decision_tree.py` : 모델 학습 코드
- `processed_dataset*.csv` : 전처리된 데이터
- `DNS/`, `youtube/`, `download/`, `websuf/` : 원본 패킷 캡처 폴더

## 앞으로 하고 싶은 것

- ARP 패킷 발생 빈도 + 공유기(192.168.1.1) ping RTT 비교를 활용한 실시간 탐지
- 모델 정확도 더 올리기 (Random Forest, XGBoost 등)
- 실제 네트워크 환경에서 테스트해보기

부족한 점이 많지만, 공부하면서 재미있게 했던 프로젝트라서 올려둡니다.  
피드백이나 조언 있으시면 언제든지 Issues나 PR 남겨주세요!

---
