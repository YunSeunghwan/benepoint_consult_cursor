# 📊 로그 관리 및 모니터링 가이드

## 🎯 로그 시스템 개요

Benefit Station AI는 체계적인 로그 관리 시스템을 제공합니다. 모든 API 요청, 채팅 상호작용, 시스템 이벤트, 오류가 자동으로 기록됩니다.

## 📂 로그 파일 구조

```
backend/logs/
├── api_requests.log      # 모든 API 요청 기록
├── chat_interactions.log # 사용자-AI 채팅 상호작용
├── system.log           # 시스템 이벤트 및 성능 정보
└── errors.log           # 오류 및 예외 상황
```

## 🔍 로그 조회 방법

### 1️⃣ **웹 API를 통한 조회**

```bash
# 로그 파일 목록 확인
curl "https://successful-here-prospective-reaction.trycloudflare.com/api/logs"

# 특정 로그 파일 내용 보기 (최근 100줄)
curl "https://successful-here-prospective-reaction.trycloudflare.com/api/logs/chat_interactions?lines=50"

# 로그에서 키워드 검색
curl "https://successful-here-prospective-reaction.trycloudflare.com/api/logs/system/search?keyword=ERROR&lines=20"

# 구조화된 채팅 상호작용 데이터
curl "https://successful-here-prospective-reaction.trycloudflare.com/api/logs/chat/interactions"
```

### 2️⃣ **터미널에서 직접 조회**

```bash
# 백엔드 디렉토리로 이동
cd ~/benefit_recommender_20250729/backend

# 최근 채팅 로그 확인
tail -10 logs/chat_interactions.log

# 실시간 로그 모니터링
tail -f logs/system.log

# 오류 로그 확인
cat logs/errors.log

# 특정 키워드 검색
grep "건강" logs/chat_interactions.log
```

## 📈 로그 분석 예시

### 💬 **채팅 상호작용 분석**

```bash
# 가장 많이 요청된 키워드 찾기
grep "Message:" logs/chat_interactions.log | sort | uniq -c | sort -nr

# 특정 사용자의 활동 추적
grep "User: demo-user" logs/chat_interactions.log

# 추천 상품 개수별 통계
grep "Products:" logs/chat_interactions.log | cut -d':' -f4 | sort | uniq -c
```

### ⚡ **성능 모니터링**

```bash
# 응답 시간 분석
grep "process_time" logs/system.log | grep "api/chat"

# API 사용량 통계
grep "API_RESPONSE" logs/system.log | cut -d"'" -f4 | sort | uniq -c

# 오류율 계산
echo "총 요청: $(grep "API_RESPONSE" logs/system.log | wc -l)"
echo "오류 발생: $(grep "ERROR" logs/errors.log | wc -l)"
```

## 🔧 로그 설정 관리

### **로그 레벨 조정**

`backend/logger_config.py`에서 로그 레벨을 변경할 수 있습니다:

```python
# 개발 환경: DEBUG 레벨
setup_logger('API', 'api_requests.log', logging.DEBUG)

# 운영 환경: INFO 레벨 (권장)
setup_logger('API', 'api_requests.log', logging.INFO)

# 중요한 이벤트만: WARNING 레벨
setup_logger('API', 'api_requests.log', logging.WARNING)
```

### **로그 파일 크기 관리**

현재 설정:
- **최대 파일 크기**: 5MB
- **보관 파일 수**: 5개
- **총 저장 용량**: 약 25MB per 로그 타입

변경하려면 `logger_config.py` 수정:

```python
file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, log_file),
    maxBytes=10*1024*1024,  # 10MB로 증가
    backupCount=10          # 10개 파일 보관
)
```

## 📊 로그 모니터링 대시보드

### **실시간 모니터링 스크립트**

```bash
#!/bin/bash
# monitor_logs.sh

echo "=== Benefit Station AI 로그 모니터링 ==="
echo "시간: $(date)"
echo ""

echo "📊 로그 파일 현황:"
ls -lh ~/benefit_recommender_20250729/backend/logs/

echo ""
echo "💬 최근 채팅 활동 (최근 5건):"
tail -5 ~/benefit_recommender_20250729/backend/logs/chat_interactions.log

echo ""
echo "⚡ 시스템 상태 (최근 3건):"
tail -3 ~/benefit_recommender_20250729/backend/logs/system.log

echo ""
echo "🚨 오류 현황:"
if [ -s ~/benefit_recommender_20250729/backend/logs/errors.log ]; then
    echo "❌ 오류 발견!"
    tail -5 ~/benefit_recommender_20250729/backend/logs/errors.log
else
    echo "✅ 오류 없음"
fi
```

### **사용법**

```bash
# 스크립트에 실행 권한 부여
chmod +x monitor_logs.sh

# 실행
./monitor_logs.sh

# 주기적 모니터링 (10초마다)
watch -n 10 ./monitor_logs.sh
```

## 🔍 로그 검색 패턴

### **유용한 검색 쿼리들**

```bash
# 특정 시간대 활동 찾기
grep "2025-07-31 07:4" logs/chat_interactions.log

# 오류가 발생한 API 찾기
grep -B2 -A2 "ERROR" logs/api_requests.log

# 응답 시간이 긴 API 찾기
grep "process_time.*[0-9]\.[5-9]" logs/system.log

# 특정 상품이 추천된 횟수
grep "스타벅스" logs/chat_interactions.log | wc -l

# 사용자별 활동 통계
cut -d'|' -f2 logs/chat_interactions.log | sort | uniq -c
```

## 🚨 알림 및 경고 시스템

### **오류 알림 스크립트**

```bash
#!/bin/bash
# error_alert.sh

ERROR_LOG="~/benefit_recommender_20250729/backend/logs/errors.log"
LAST_CHECK_FILE="/tmp/last_error_check"

# 마지막 체크 시간 이후 새로운 오류가 있는지 확인
if [ -f "$LAST_CHECK_FILE" ]; then
    NEW_ERRORS=$(find "$ERROR_LOG" -newer "$LAST_CHECK_FILE" 2>/dev/null)
    if [ -n "$NEW_ERRORS" ]; then
        echo "🚨 새로운 오류 발견!"
        tail -5 "$ERROR_LOG"
        echo ""
        echo "즉시 확인이 필요합니다."
    fi
fi

# 현재 시간을 마지막 체크 시간으로 저장
touch "$LAST_CHECK_FILE"
```

## 📈 성능 분석

### **API 성능 리포트 생성**

```bash
# API별 평균 응답 시간 계산
grep "process_time" logs/system.log | \
awk -F"'" '{print $4, $8}' | \
awk -F's' '{sum[$1]+=$2; count[$1]++} END {for(api in sum) printf "%s: %.4fs\n", api, sum[api]/count[api]}' | \
sort -k2 -nr
```

### **사용자 활동 패턴 분석**

```bash
# 시간대별 활동 분석
grep "CHAT - INFO" logs/chat_interactions.log | \
cut -d' ' -f2 | cut -d':' -f1 | sort | uniq -c | \
awk '{printf "%02d시: %d건\n", $2, $1}'
```

## 💾 로그 백업 및 보관

### **자동 백업 스크립트**

```bash
#!/bin/bash
# backup_logs.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="~/log_backups"
SOURCE_DIR="~/benefit_recommender_20250729/backend/logs"

mkdir -p "$BACKUP_DIR"

# 로그 압축 백업
tar -czf "$BACKUP_DIR/logs_backup_$DATE.tar.gz" -C "$SOURCE_DIR" .

echo "✅ 로그 백업 완료: logs_backup_$DATE.tar.gz"

# 30일 이상 된 백업 파일 삭제
find "$BACKUP_DIR" -name "logs_backup_*.tar.gz" -mtime +30 -delete
```

### **정기 백업 설정 (crontab)**

```bash
# crontab 편집
crontab -e

# 매일 새벽 2시에 백업 실행
0 2 * * * /path/to/backup_logs.sh
```

## 🎯 로그 활용 팁

### **1. 문제 해결**
- 오류 발생 시 `errors.log`에서 상세 정보 확인
- API 응답 지연 시 `system.log`에서 `process_time` 확인
- 사용자 불만 시 `chat_interactions.log`에서 대화 내역 추적

### **2. 서비스 개선**
- 가장 많이 요청되는 키워드 분석 → 상품 추가
- 응답 시간 모니터링 → 성능 최적화
- 사용자 패턴 분석 → UX 개선

### **3. 비즈니스 인사이트**
- 인기 상품 카테고리 파악
- 사용자 활동 시간대 분석
- 추천 시스템 효과 측정

---

## 🚀 **완성된 로그 관리 시스템의 장점**

✅ **완전 자동화** - 모든 활동이 자동으로 기록됨
✅ **실시간 모니터링** - API로 언제든 조회 가능
✅ **장기 보관** - 파일 로테이션으로 오래된 로그도 안전하게 보관
✅ **검색 및 분석** - 키워드 검색과 통계 분석 가능
✅ **성능 추적** - API 응답 시간과 시스템 상태 모니터링
✅ **오류 추적** - 모든 오류가 상세하게 기록됨

**이제 서비스의 모든 활동을 추적하고 분석할 수 있습니다!** 🎉