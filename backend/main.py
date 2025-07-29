from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI(
    title="Benefit Station AI 추천 서비스",
    description="LangChain 기반 AI 에이전트가 복리후생 상품을 추천하는 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 요청/응답 모델
class ChatRequest(BaseModel):
    message: str
    user_id: str = "demo-user"

class ChatResponse(BaseModel):
    response: str
    products: list = []

# 기본 라우트
@app.get("/")
async def root():
    return {"message": "Benefit Station AI 추천 서비스가 실행 중입니다!"}

# 헬스체크
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "benefit-station-ai"}

# 샘플 상품 데이터
SAMPLE_PRODUCTS = [
    {"id": "p1", "name": "스타벅스 아메리카노", "category": "food", "price": 4500, "rating": 4.8},
    {"id": "p2", "name": "헬스장 1개월 이용권", "category": "health", "price": 50000, "rating": 4.5},
    {"id": "p3", "name": "온라인 쇼핑몰 5천원 할인", "category": "shopping", "price": 5000, "rating": 4.2},
    {"id": "p4", "name": "넷플릭스 1개월 구독권", "category": "life", "price": 17000, "rating": 4.7},
    {"id": "p5", "name": "온라인 강의 수강권", "category": "education", "price": 25000, "rating": 4.3},
    {"id": "p6", "name": "생활용품 할인권", "category": "life", "price": 15000, "rating": 4.1},
    {"id": "p7", "name": "점심식사 지원권", "category": "food", "price": 10000, "rating": 4.5},
    {"id": "p8", "name": "배달의민족 2만원권", "category": "food", "price": 20000, "rating": 4.6},
]

def get_products_by_keyword(keyword: str):
    """키워드로 상품 필터링"""
    keyword = keyword.lower()
    results = []
    
    if any(word in keyword for word in ['식사', '먹', '음식', '커피', '스타벅스', '배달']):
        results.extend([p for p in SAMPLE_PRODUCTS if p['category'] == 'food'])
    
    if any(word in keyword for word in ['건강', '헬스', '운동', '검진']):
        results.extend([p for p in SAMPLE_PRODUCTS if p['category'] == 'health'])
    
    if any(word in keyword for word in ['생활', '넷플릭스', '할인']):
        results.extend([p for p in SAMPLE_PRODUCTS if p['category'] == 'life'])
    
    if any(word in keyword for word in ['교육', '강의', '학습']):
        results.extend([p for p in SAMPLE_PRODUCTS if p['category'] == 'education'])
    
    if any(word in keyword for word in ['쇼핑', '구매']):
        results.extend([p for p in SAMPLE_PRODUCTS if p['category'] == 'shopping'])
    
    # 가격 필터링
    if '만원' in keyword or '저렴' in keyword:
        results = [p for p in results if p['price'] <= 30000]
    
    # 중복 제거
    seen = set()
    unique_results = []
    for product in results:
        if product['id'] not in seen:
            seen.add(product['id'])
            unique_results.append(product)
    
    return unique_results[:5]  # 최대 5개만 반환

# 채팅 엔드포인트
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    AI 에이전트와의 채팅 인터페이스
    현재는 키워드 기반 간단한 추천 시스템으로 구현
    """
    try:
        message = request.message.lower()
        
        # 키워드 기반 상품 추천
        recommended_products = get_products_by_keyword(message)
        
        if recommended_products:
            categories = list(set(p['category'] for p in recommended_products))
            category_names = {
                'food': '식음료',
                'health': '건강',
                'life': '생활',
                'education': '교육',
                'shopping': '쇼핑'
            }
            
            response_text = f"'{request.message}'에 대한 추천 상품을 찾았어요! 🎉\n\n"
            response_text += f"총 {len(recommended_products)}개의 상품을 추천드립니다:\n"
            
            for i, product in enumerate(recommended_products, 1):
                category_kr = category_names.get(product['category'], product['category'])
                response_text += f"{i}. {product['name']} ({category_kr}) - {product['price']:,}원 (평점: ⭐{product['rating']})\n"
            
            response_text += "\n더 구체적인 조건이 있으시면 말씀해주세요!"
        else:
            response_text = f"'{request.message}'에 대한 상품을 찾지 못했어요. 😅\n\n"
            response_text += "다음과 같은 키워드로 다시 시도해보세요:\n"
            response_text += "• 식사, 커피, 음식 관련\n• 건강, 운동, 헬스 관련\n• 생활, 넷플릭스, 할인 관련\n• 교육, 강의 관련"
            recommended_products = SAMPLE_PRODUCTS[:3]  # 기본 추천
        
        return ChatResponse(
            response=response_text,
            products=recommended_products
        )
        
    except Exception as e:
        print(f"채팅 처리 중 오류: {e}")
        raise HTTPException(status_code=500, detail=f"채팅 처리 중 오류가 발생했습니다: {str(e)}")

# 상품 목록 조회
@app.get("/api/products")
async def get_products():
    """전체 상품 목록 조회"""
    return {"products": SAMPLE_PRODUCTS}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 