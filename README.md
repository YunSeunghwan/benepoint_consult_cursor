# Benefit Station AI 추천 서비스 🤖

Benefit Station 상품을 AI로 추천하는 대화형 복리후생 서비스 MVP입니다. LangChain 기반 AI 에이전트가 사용자와 대화를 통해 상품을 추천합니다.

## 🌟 핵심 기능 (MVP)

### 🤖 AI 대화형 추천
- **자연어 검색**: 간단한 질문으로 상품 찾기
- **개인 맞춤 추천**: 사용자 선호도 기반 상품 제안
- **카테고리 필터링**: 특정 분야 상품만 보기

### 💬 채팅 인터페이스
- **실시간 상호작용**: 대화를 통한 정보 전달
- **시각적 상품 카드**: 추천 결과를 카드형으로 표시
- **간편한 사용성**: 복잡한 검색 없이 질문으로 해결

### 📊 간단한 사용자 관리
- **사용자 선호도**: 기본 카테고리 선호도 저장
- **데모 모드**: 로그인 없이 테스트 가능

## 🏗️ 기술 스택

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Next.js       │    │   FastAPI        │    │   Supabase      │
│   Frontend      │◄──►│   Backend        │◄──►│   PostgreSQL    │
│                 │    │                  │    │                 │
│ • 채팅 인터페이스  │    │ • LangChain 에이전트│    │ • 사용자 테이블   │
│ • 러버블 CSS      │    │ • AI 도구         │    │ • 상품 테이블     │
│ • 상품 카드 컴포넌트│    │ • API 엔드포인트   │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 프론트엔드
- **Next.js**: 서버사이드 렌더링 지원 프레임워크
- **러버블 CSS**: 심플하고 직관적인 스타일링
- **Playwright MCP**: UI 테스트 및 개선

### 백엔드
- **FastAPI**: 고성능 Python API 프레임워크
- **LangChain**: AI 에이전트 및 도구 구현
- **Python 3.11+**: 최신 안정 버전 활용

### AI 컴포넌트
- **OpenAI gpt-4o**: 대화형 AI 모델
- **LangChain 도구**: 상품 검색, 추천, 필터링

### 데이터베이스
- **Supabase**: 서버리스 PostgreSQL
- **2개 테이블**: 사용자, 상품

### 배포
- **Vercel**: 프론트엔드 및 백엔드 배포

## 🚀 시작하기

### 사전 요구사항
- Node.js 18+
- Python 3.11+
- Supabase 계정
- OpenAI API 키

### 설치 및 실행

1. **저장소 클론**
```bash
git clone <repository-url>
cd benefit-station-ai
```

2. **환경 변수 설정**
`.env` 파일 생성:
```
# 프론트엔드
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
BACKEND_URL=http://localhost:8000

# 백엔드
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
OPENAI_API_KEY=your-openai-api-key
```

3. **백엔드 설정**
```bash
# 가상환경 생성
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
uvicorn main:app --reload
```

4. **프론트엔드 설정**
```bash
# 패키지 설치
cd frontend
npm install

# 개발 서버 실행
npm run dev
```

5. **접속**
- 웹 앱: http://localhost:3000
- API 문서: http://localhost:8000/docs

## 📁 프로젝트 구조

```
benefit-station-ai/
├── frontend/                  # Next.js 프로젝트
│   ├── pages/
│   │   ├── _app.js            # 앱 설정
│   │   ├── index.js           # 메인 페이지 (AI 채팅 인터페이스)
│   │   ├── api/
│   │   │   └── chat.js        # AI 에이전트 연결 API
│   ├── components/
│   │   ├── ChatInterface.js   # 채팅 UI 컴포넌트
│   │   ├── ProductCard.js     # 상품 카드 컴포넌트
│   │   └── RecommendationList.js # 추천 목록 컴포넌트
│   ├── styles/
│   │   └── lovelace.css       # 러버블 CSS 스타일
│   ├── tests/
│   │   └── ui.spec.js         # Playwright 테스트
│   └── package.json
├── backend/
│   ├── main.py                # FastAPI 앱
│   ├── agent/
│   │   ├── agent.py           # LangChain 에이전트 설정
│   │   └── tools.py           # 에이전트 도구 구현
│   ├── db.py                  # Supabase 연결
│   └── recommendation.py      # 추천 로직
├── .env                       # 환경변수
├── requirements.txt           # Python 패키지
└── README.md                  # 프로젝트 문서
```

## 💡 기능 사용 예시

### AI 대화 예시

```
사용자: "식사 관련 추천해줘"

AI: "식사 관련 상품을 찾아봤어요:

카테고리 상품:
- 스타벅스 아메리카노 (4500원, 평점: 4.8)
- 배달의민족 2만원권 (20000원, 평점: 4.6)
- 점심식사 지원권 (10000원, 평점: 4.5)

어떤 상품이 마음에 드시나요?"
```

```
사용자: "30000원 이하 상품만 보여줘"

AI: "30,000원 이하 상품들을 찾아봤어요:

추천 상품:
- 스타벅스 아메리카노 (4500원, 평점: 4.8)
- 넷플릭스 1개월 구독권 (17000원, 평점: 4.7)
- 점심식사 지원권 (10000원, 평점: 4.5)
- 생활용품 할인권 (15000원, 평점: 4.1)
- 온라인 강의 할인쿠폰 (25000원, 평점: 4.4)

이 중에 관심 있는 상품이 있으신가요?"
```

## 🗄️ 데이터베이스 설정

Supabase에서 아래 SQL로 테이블을 생성하세요:

```sql
-- 사용자 테이블
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  preferences JSONB DEFAULT '{"categories": []}'::jsonb
);

-- 상품 테이블
CREATE TABLE products (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price INTEGER NOT NULL,
  rating REAL DEFAULT 0
);

-- 샘플 데이터
INSERT INTO users (id, name, preferences) 
VALUES ('demo-user', '테스트 사용자', '{"categories": ["food", "health"]}'::jsonb);

INSERT INTO products (id, name, category, price, rating) VALUES
('p1', '스타벅스 아메리카노', 'food', 4500, 4.8),
('p2', '헬스장 1개월 이용권', 'health', 50000, 4.5),
('p3', '온라인 쇼핑몰 5천원 할인', 'shopping', 5000, 4.2),
('p4', '넷플릭스 1개월 구독권', 'life', 17000, 4.7),
('p5', '온라인 강의 수강권', 'education', 25000, 4.3),
('p6', '생활용품 할인권', 'life', 15000, 4.1),
('p7', '점심식사 지원권', 'food', 10000, 4.5),
('p8', '배달의민족 2만원권', 'food', 20000, 4.6),
('p9', '홈트레이닝 세트', 'health', 35000, 4.2),
('p10', '건강검진 패키지', 'health', 120000, 4.7);
```

## 🧠 AI 에이전트 아키텍처

LangChain 에이전트는 다음 도구들을 사용합니다:

1. **SearchProductsTool**: 키워드로 상품 검색
2. **GetRecommendationsTool**: 사용자 기반 추천 생성
3. **FilterByCategoryTool**: 카테고리별 상품 필터링

```python
# 에이전트 초기화 예시
agent = initialize_agent(
    tools=[SearchProductsTool(), GetRecommendationsTool(), FilterByCategoryTool()],
    llm=ChatOpenAI(model_name="gpt-4o"),
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=ConversationBufferMemory(memory_key="chat_history"),
    verbose=True
)
```

## 🔧 개발자 가이드

### LangChain 도구 추가하기
```python
# 새로운 도구 예시
from langchain.tools import BaseTool
from pydantic import BaseModel, Field

class PriceFilterInput(BaseModel):
    max_price: int = Field(description="최대 가격")

class FilterByPriceTool(BaseTool):
    name = "filter_by_price"
    description = "특정 가격 이하의 상품을 찾습니다"
    args_schema: Type[BaseModel] = PriceFilterInput
    
    def _run(self, max_price: int) -> str:
        # 가격 필터링 로직
        response = supabase_client.table("products").select("*").lte("price", max_price).execute()
        products = response.data
        
        # 결과 반환
        result = f"{max_price}원 이하 상품:\n"
        for product in products:
            result += f"- {product['name']} ({product['price']}원, 평점: {product['rating']})\n"
        
        return result
```

### 새 컴포넌트 추가하기
```jsx
// 예시: 카테고리 선택 컴포넌트
const CategorySelector = ({ onSelect }) => {
  const categories = [
    { id: 'food', name: '맛집 & 레저', color: 'bg-blue-100' },
    { id: 'shopping', name: '쇼핑', color: 'bg-green-100' },
    { id: 'health', name: '건강', color: 'bg-red-100' },
    { id: 'education', name: '교육', color: 'bg-yellow-100' },
    { id: 'life', name: '생활', color: 'bg-purple-100' },
  ];
  
  return (
    <div className="category-selector">
      <h3>카테고리 선택</h3>
      <div className="category-buttons">
        {categories.map(category => (
          <button 
            key={category.id}
            className={`category-button ${category.color}`}
            onClick={() => onSelect(category.id)}
          >
            {category.name}
          </button>
        ))}
      </div>
    </div>
  );
};
```

## 🚀 Playwright MCP를 활용한 UI 개선

Playwright MCP로 다음과 같은 UI 테스트와 개선이 가능합니다:

```javascript
// 반응형 테스트 예시
test('모바일 화면에서 UI 테스트', async ({ page }) => {
  // 모바일 화면 크기로 설정
  await page.setViewportSize({ width: 375, height: 667 });
  
  await page.goto('/');
  
  // 모바일 UI 요소 확인
  await expect(page.locator('.chat-container')).toHaveCSS('flex-direction', 'column');
  
  // 메시지 입력 및 전송
  await page.fill('input[type="text"]', '추천 상품');
  await page.click('button[type="submit"]');
  
  // 응답 확인
  await page.waitForSelector('.product-card');
  
  // 모바일에서 상품 카드가 세로로 정렬되는지 확인
  const firstCardBounds = await page.locator('.product-card').first().boundingBox();
  const secondCardBounds = await page.locator('.product-card').nth(1).boundingBox();
  
  // 세로 배치 확인 (첫 번째 카드 아래에 두 번째 카드가 위치)
  expect(secondCardBounds.y).toBeGreaterThan(firstCardBounds.y + firstCardBounds.height);
});
```

## 🚧 현재 상태

**⚠️ 프로젝트 시작 단계**: 현재 README만 작성된 상태입니다.

## 📈 상세 개발 계획

### 🏗️ Phase 0: 프로젝트 초기 설정 (1주차)

#### 환경 설정 및 기본 구조
- [ ] **프로젝트 폴더 구조 생성**
  - [ ] `frontend/` 디렉토리 생성
  - [ ] `backend/` 디렉토리 생성
  - [ ] 각 폴더별 기본 파일 생성

#### 백엔드 기본 설정
- [ ] **FastAPI 프로젝트 초기화**
  - [ ] `requirements.txt` 작성
  - [ ] `main.py` 기본 구조 생성
  - [ ] 환경변수 설정 (`.env` 파일)
  - [ ] Supabase 연결 테스트

#### 프론트엔드 기본 설정  
- [ ] **Next.js 프로젝트 초기화**
  - [ ] `npm init` 및 필수 패키지 설치
  - [ ] 기본 페이지 구조 생성
  - [ ] 러버블 CSS 기본 스타일 적용

### 🛠️ Phase 1: 핵심 기능 구현 (2-3주차)

#### 데이터베이스 설정
- [ ] **Supabase 테이블 생성**
  - [ ] `users` 테이블 생성 및 스키마 정의
  - [ ] `products` 테이블 생성 및 스키마 정의
  - [ ] 샘플 데이터 입력 (10개 상품)
  - [ ] 데이터베이스 연결 함수 구현

#### AI 에이전트 구현
- [ ] **LangChain 에이전트 설정**
  - [ ] OpenAI API 연결 설정
  - [ ] 기본 LangChain 에이전트 구현
  - [ ] 대화 메모리 설정
  - [ ] 에이전트 테스트 및 디버깅

#### AI 도구 개발
- [ ] **SearchProductsTool 구현**
  - [ ] 키워드 기반 상품 검색 로직
  - [ ] 검색 결과 포맷팅
  - [ ] 오류 처리 및 예외 상황 대응
- [ ] **GetRecommendationsTool 구현**
  - [ ] 사용자 선호도 기반 추천 알고리즘
  - [ ] 평점 및 카테고리 가중치 적용
  - [ ] 추천 결과 순위 정렬
- [ ] **FilterByCategoryTool 구현**
  - [ ] 카테고리별 필터링 로직
  - [ ] 다중 카테고리 지원
  - [ ] 가격 범위 필터링 추가

### 🎨 Phase 2: UI/UX 구현 (4-5주차)

#### 기본 컴포넌트 개발
- [ ] **ChatInterface 컴포넌트**
  - [ ] 메시지 입력/출력 UI
  - [ ] 실시간 채팅 인터페이스
  - [ ] 로딩 상태 표시
  - [ ] 오류 메시지 처리
- [ ] **ProductCard 컴포넌트**
  - [ ] 상품 정보 카드 UI 디자인
  - [ ] 평점 별점 표시
  - [ ] 가격 포맷팅
  - [ ] 카테고리 태그 표시
- [ ] **RecommendationList 컴포넌트**
  - [ ] 추천 상품 목록 레이아웃
  - [ ] 그리드/리스트 뷰 지원
  - [ ] 무한 스크롤 또는 페이지네이션

#### API 연결
- [ ] **프론트엔드-백엔드 API 연결**
  - [ ] `/api/chat` 엔드포인트 구현
  - [ ] WebSocket 또는 SSE를 통한 실시간 통신
  - [ ] API 오류 처리 및 재시도 로직
  - [ ] 로딩 상태 관리

### 🔧 Phase 3: 고급 기능 및 최적화 (6-7주차)

#### 사용자 기능 확장
- [ ] **사용자 선호도 관리**
  - [ ] 선호 카테고리 설정 UI
  - [ ] 사용자 프로필 저장/로드
  - [ ] 선호도 기반 추천 개선
- [ ] **채팅 히스토리**
  - [ ] 대화 내역 저장
  - [ ] 이전 대화 불러오기
  - [ ] 대화 컨텍스트 유지

#### 추천 알고리즘 개선
- [ ] **고급 추천 로직**
  - [ ] 협업 필터링 기본 구현
  - [ ] 상품 유사도 계산
  - [ ] 사용자 행동 패턴 분석
  - [ ] A/B 테스트 준비

### 🧪 Phase 4: 테스트 및 품질 관리 (8주차)

#### 테스트 구현
- [ ] **Playwright 테스트 설정**
  - [ ] 기본 E2E 테스트 작성
  - [ ] 모바일 반응형 테스트
  - [ ] 채팅 플로우 테스트
  - [ ] 추천 기능 테스트
- [ ] **백엔드 유닛 테스트**
  - [ ] AI 도구 테스트
  - [ ] 데이터베이스 연결 테스트
  - [ ] API 엔드포인트 테스트

#### 성능 최적화
- [ ] **프론트엔드 최적화**
  - [ ] 번들 크기 최적화
  - [ ] 이미지 최적화
  - [ ] 코드 스플리팅
- [ ] **백엔드 최적화**
  - [ ] 데이터베이스 쿼리 최적화
  - [ ] 캐싱 구현
  - [ ] API 응답 시간 개선

### 🚀 Phase 5: 배포 및 운영 (9-10주차)

#### 배포 준비
- [ ] **Vercel 배포 설정**
  - [ ] 프론트엔드 배포 설정
  - [ ] 백엔드 서버리스 함수 설정
  - [ ] 환경변수 설정
  - [ ] 도메인 연결
- [ ] **모니터링 설정**
  - [ ] 에러 트래킹 (Sentry 등)
  - [ ] 성능 모니터링
  - [ ] 로그 관리
  - [ ] API 사용량 모니터링

## 📋 현재 개발 상태

- [ ] **기본 설정**: 아직 시작 안됨
- [ ] **백엔드 구현**: 아직 시작 안됨  
- [ ] **프론트엔드 구현**: 아직 시작 안됨
- [ ] **AI 에이전트 연결**: 아직 시작 안됨
- [ ] **데이터베이스 설정**: 아직 시작 안됨
- [ ] **UI/UX 구현**: 아직 시작 안됨
- [ ] **테스트 작성**: 아직 시작 안됨
- [ ] **배포**: 아직 시작 안됨

## ⏰ 예상 일정

- **1주차**: 프로젝트 초기 설정 및 환경 구축
- **2-3주차**: 핵심 백엔드 기능 및 AI 에이전트 구현  
- **4-5주차**: 프론트엔드 UI/UX 구현
- **6-7주차**: 고급 기능 및 사용자 경험 개선
- **8주차**: 테스트 및 품질 보증
- **9-10주차**: 배포 및 운영 준비

## 🎯 주간별 목표

### 1주차 목표
1. 프로젝트 폴더 구조 완성
2. FastAPI 기본 서버 실행
3. Next.js 기본 페이지 표시
4. Supabase 연결 확인

### 2주차 목표  
1. 데이터베이스 테이블 생성 및 샘플 데이터 입력
2. 첫 번째 AI 도구 (SearchProductsTool) 구현
3. 기본 채팅 API 엔드포인트 생성

### 3주차 목표
1. 나머지 AI 도구들 구현 완료
2. LangChain 에이전트 통합 테스트
3. 기본 채팅 인터페이스 구현

## 🤝 기여하기

1. 이 저장소를 포크하세요
2. 기능 브랜치를 만드세요 (`git checkout -b feature/amazing-feature`)
3. 변경 사항을 커밋하세요 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시하세요 (`git push origin feature/amazing-feature`)
5. Pull Request를 열어주세요

## 📝 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

**Made with ❤️ for Benefit Station users**
