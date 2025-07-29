import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Supabase 설정
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase 클라이언트 초기화
def get_supabase_client() -> Client:
    """Supabase 클라이언트 인스턴스 반환"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL과 SUPABASE_KEY 환경변수가 필요합니다")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# 전역 클라이언트 인스턴스
supabase_client = None

try:
    supabase_client = get_supabase_client()
    print("✅ Supabase 연결 성공")
except Exception as e:
    print(f"❌ Supabase 연결 실패: {e}")

# 데이터베이스 유틸리티 함수들
async def get_products(category: str = None, max_price: int = None):
    """상품 목록 조회"""
    try:
        query = supabase_client.table("products").select("*")
        
        if category:
            query = query.eq("category", category)
        if max_price:
            query = query.lte("price", max_price)
            
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"상품 조회 오류: {e}")
        return []

async def get_user_preferences(user_id: str):
    """사용자 선호도 조회"""
    try:
        response = supabase_client.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"사용자 선호도 조회 오류: {e}")
        return None

async def search_products(query: str):
    """키워드로 상품 검색"""
    try:
        # 상품명에서 키워드 검색
        response = supabase_client.table("products").select("*").ilike("name", f"%{query}%").execute()
        return response.data
    except Exception as e:
        print(f"상품 검색 오류: {e}")
        return [] 