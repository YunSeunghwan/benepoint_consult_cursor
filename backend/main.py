from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import time
from dotenv import load_dotenv
from simple_db import simple_db
from logger_config import log_api_request, log_chat_interaction, log_error, log_system_event
from log_viewer import get_log_files, read_log_file, search_logs, get_log_stats, parse_chat_logs

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
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://know-antiques-florists-elephant.trycloudflare.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 요청 로깅 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 요청 정보 로깅
    log_api_request(
        method=request.method,
        path=str(request.url.path),
        user_id=None,  # 나중에 사용자 인증 시 추가
        data=None
    )
    
    response = await call_next(request)
    
    # 응답 시간 계산
    process_time = time.time() - start_time
    log_system_event("API_RESPONSE", {
        "path": str(request.url.path),
        "status_code": response.status_code,
        "process_time": f"{process_time:.4f}s"
    })
    
    return response

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



def get_products_by_keyword(keyword: str):
    """키워드로 상품 필터링 - JSON 기반 DB 사용"""
    keyword = keyword.lower()
    results = []
    
    # 카테고리별 키워드 매핑
    category_keywords = {
        'food': ['식사', '먹', '음식', '커피', '스타벅스', '배달'],
        'health': ['건강', '헬스', '운동', '검진', '요가'],
        'life': ['생활', '넷플릭스', '할인', '김치냉장고'],
        'education': ['교육', '강의', '학습'],
        'shopping': ['쇼핑', '구매']
    }
    
    # 키워드에 해당하는 카테고리 찾기
    target_categories = []
    for category, keywords_list in category_keywords.items():
        if any(word in keyword for word in keywords_list):
            target_categories.append(category)
    
    # 카테고리별로 상품 검색
    for category in target_categories:
        category_products = simple_db.get_products(category=category)
        results.extend(category_products)
    
    # 키워드로 직접 검색도 추가
    search_results = simple_db.search_products(keyword)
    results.extend(search_results)
    
    # 가격 필터링
    max_price = None
    if '만원' in keyword or '저렴' in keyword:
        max_price = 30000
    elif '천원' in keyword:
        max_price = 10000
    
    if max_price:
        results = [p for p in results if p.get('price', 0) <= max_price]
    
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
        
        # 요청 로깅
        log_api_request("POST", "/api/chat", request.user_id, {"message": request.message})
        
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
            recommended_products = simple_db.get_products()[:3]  # 기본 추천
        
        # 채팅 상호작용 로깅
        log_chat_interaction(
            user_id=request.user_id,
            message=request.message,
            response=response_text,
            products_count=len(recommended_products)
        )
        
        return ChatResponse(
            response=response_text,
            products=recommended_products
        )
        
    except Exception as e:
        # 오류 로깅
        log_error("CHAT_API_ERROR", str(e), {
            "user_id": request.user_id,
            "message": request.message
        })
        raise HTTPException(status_code=500, detail=f"채팅 처리 중 오류가 발생했습니다: {str(e)}")

# 상품 목록 조회
@app.get("/api/products")
async def get_products():
    """전체 상품 목록 조회"""
    products = simple_db.get_products()
    return {"products": products}

# 새 상품 추가 엔드포인트
@app.post("/api/products")
async def add_product(product: dict):
    """새 상품 추가"""
    try:
        simple_db.add_product(product)
        
        # 상품 추가 로깅
        log_system_event("PRODUCT_ADDED", {
            "product_id": product.get("id"),
            "product_name": product.get("name"),
            "category": product.get("category"),
            "price": product.get("price")
        })
        
        return {"message": "상품이 성공적으로 추가되었습니다", "product": product}
    except Exception as e:
        log_error("PRODUCT_ADD_ERROR", str(e), {"product": product})
        raise HTTPException(status_code=500, detail=f"상품 추가 중 오류: {str(e)}")

# 로그 관리 API들
@app.get("/api/logs")
async def get_logs():
    """사용 가능한 로그 파일 목록"""
    files = get_log_files()
    return {"log_files": files}

@app.get("/api/logs/{filename}")
async def get_log_content(filename: str, lines: int = 100):
    """특정 로그 파일 내용 조회"""
    if not filename.endswith('.log'):
        filename += '.log'
    
    content = read_log_file(filename, lines)
    stats = get_log_stats(filename)
    
    return {
        "filename": filename,
        "lines": content,
        "stats": stats
    }

@app.get("/api/logs/{filename}/search")
async def search_log(filename: str, keyword: str, lines: int = 50):
    """로그에서 키워드 검색"""
    if not filename.endswith('.log'):
        filename += '.log'
    
    results = search_logs(filename, keyword, lines)
    return {
        "filename": filename,
        "keyword": keyword,
        "results": results,
        "count": len(results)
    }

@app.get("/api/logs/chat/interactions")
async def get_chat_interactions():
    """채팅 상호작용 로그 (구조화된 데이터)"""
    interactions = parse_chat_logs()
    return {
        "interactions": interactions,
        "count": len(interactions)
    }

# 서버 시작 시 로깅
log_system_event("SERVER_STARTUP", {
    "app_name": "Benefit Station AI",
    "version": "1.0.0",
    "environment": "development"
})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 