# 🚀 Benefit Station AI 프로토타입 실행 가이드

## 📋 현재 상태
✅ **프로토타입 완성**: 기본 구조와 UI가 모두 구현되었습니다!

## 🛠️ 실행 준비

### 1. 환경변수 설정
`.env.example` 파일을 참고하여 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

`.env` 파일에서 다음 값들을 설정하세요:
- `SUPABASE_URL`: Supabase 프로젝트 URL
- `SUPABASE_KEY`: Supabase API 키  
- `OPENAI_API_KEY`: OpenAI API 키

### 2. 백엔드 실행

```bash
# 1. 백엔드 디렉토리로 이동
cd backend

# 2. Python 가상환경 생성
python -m venv venv

# 3. 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows

# 4. 패키지 설치
pip install -r ../requirements.txt

# 5. 서버 실행
uvicorn main:app --reload
```

백엔드 서버가 http://localhost:8000 에서 실행됩니다.

### 3. 프론트엔드 실행

새 터미널을 열고:

```bash
# 1. 프론트엔드 디렉토리로 이동
cd frontend

# 2. 패키지 설치
npm install

# 3. 개발 서버 실행
npm run dev
```

프론트엔드가 http://localhost:3000 에서 실행됩니다.

## 🎯 테스트 방법

### 1. 웹 브라우저 테스트
1. http://localhost:3000 접속
2. 채팅창에 메시지 입력 ("식사 관련 추천해줘")
3. AI 응답 확인
4. 상품 카드 표시 확인

### 2. API 테스트
```bash
# FastAPI 문서 확인
curl http://localhost:8000/docs

# 채팅 API 테스트
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "식사 관련 추천해줘", "user_id": "demo-user"}'
```

### 3. Playwright UI 테스트
```bash
# 프론트엔드 디렉토리에서
npm run test
```

## 🔧 현재 구현된 기능

### ✅ 완료된 기능
- **기본 프로젝트 구조**: 폴더와 파일 모두 생성
- **FastAPI 백엔드**: 기본 서버 및 API 엔드포인트
- **Next.js 프론트엔드**: 채팅 인터페이스 및 상품 카드
- **LangChain 에이전트**: AI 도구 3개 구현
- **러버블 CSS**: 아름다운 UI 스타일링
- **Playwright 테스트**: 기본 UI 테스트 작성

### 🔄 현재 동작 방식
1. 사용자가 채팅창에 메시지 입력
2. 프론트엔드가 백엔드 API 호출
3. 백엔드에서 샘플 데이터로 응답 (현재는 실제 AI 연결 안됨)
4. 상품 카드로 결과 표시

## 🚨 주의사항

### 현재 제한사항
- **AI 에이전트**: OpenAI API 키 없이는 샘플 응답만 반환
- **데이터베이스**: Supabase 설정 없이는 하드코딩된 샘플 데이터 사용
- **실제 추천**: 현재는 더미 데이터로 동작

### 완전한 기능을 위해 필요한 것
1. **OpenAI API 키** 설정
2. **Supabase 데이터베이스** 설정 및 테이블 생성
3. **환경변수** 모두 올바르게 설정

## 🎨 UI 미리보기

### 채팅 인터페이스
- 실시간 대화형 UI
- 타이핑 인디케이터
- 퀵 버튼 (식사, 건강, 생활, 저렴한)

### 상품 카드
- 카테고리별 색상 구분
- 별점 표시
- 가격 포맷팅
- 액션 버튼 (상세보기, 찜하기)

### 반응형 디자인
- 데스크톱: 2열 레이아웃 (채팅 + 상품목록)
- 모바일: 1열 레이아웃 (세로 배치)

## 🐛 문제 해결

### 백엔드 실행 오류
```bash
# 포트 충돌시
uvicorn main:app --reload --port 8001

# Python 패키지 오류시
pip install --upgrade pip
pip install -r ../requirements.txt --force-reinstall
```

### 프론트엔드 실행 오류
```bash
# 패키지 설치 오류시
rm -rf node_modules package-lock.json
npm install

# 포트 충돌시
npm run dev -- -p 3001
```

### API 연결 오류
- 백엔드 서버가 실행 중인지 확인
- CORS 설정 확인
- 환경변수 설정 확인

## 🎉 다음 단계

프로토타입이 완성되었습니다! 이제 다음과 같이 진행할 수 있습니다:

1. **환경변수 설정** → 실제 AI 기능 활성화
2. **Supabase 데이터베이스** → 실제 상품 데이터 연결
3. **기능 확장** → 사용자 인증, 상세 기능 추가
4. **배포** → Vercel 등을 통한 실제 서비스 배포

---

**🎊 축하합니다! Benefit Station AI 프로토타입이 완성되었습니다!** 