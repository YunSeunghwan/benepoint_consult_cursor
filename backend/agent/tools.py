from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
import sys
import os

# 백엔드 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_products, search_products, get_user_preferences

# 도구 입력 스키마 정의
class SearchProductsInput(BaseModel):
    query: str = Field(description="검색할 상품 키워드")

class FilterByCategoryInput(BaseModel):
    category: str = Field(description="상품 카테고리 (food, health, shopping, life, education)")
    max_price: int = Field(default=None, description="최대 가격 (선택사항)")

class GetRecommendationsInput(BaseModel):
    user_id: str = Field(description="사용자 ID")
    limit: int = Field(default=5, description="추천할 상품 개수")

# LangChain 도구 구현
class SearchProductsTool(BaseTool):
    name = "search_products"
    description = "키워드를 사용하여 상품을 검색합니다. 사용자가 특정 상품이나 키워드를 언급할 때 사용하세요."
    args_schema: Type[BaseModel] = SearchProductsInput

    async def _arun(self, query: str) -> str:
        """비동기 실행"""
        return await self._run(query)
    
    def _run(self, query: str) -> str:
        """키워드로 상품 검색"""
        try:
            # 실제 구현에서는 비동기 함수를 동기적으로 호출
            # 임시로 샘플 데이터 반환
            sample_results = [
                {"name": "스타벅스 아메리카노", "price": 4500, "rating": 4.8, "category": "food"},
                {"name": "배달의민족 2만원권", "price": 20000, "rating": 4.6, "category": "food"}
            ]
            
            result = f"'{query}' 검색 결과:\n"
            for product in sample_results:
                result += f"- {product['name']} ({product['price']}원, 평점: {product['rating']}, 카테고리: {product['category']})\n"
                
            return result
        except Exception as e:
            return f"상품 검색 중 오류가 발생했습니다: {str(e)}"

class FilterByCategoryTool(BaseTool):
    name = "filter_by_category"  
    description = "특정 카테고리의 상품을 필터링합니다. 카테고리: food(식음료), health(건강), shopping(쇼핑), life(생활), education(교육)"
    args_schema: Type[BaseModel] = FilterByCategoryInput

    async def _arun(self, category: str, max_price: int = None) -> str:
        """비동기 실행"""
        return await self._run(category, max_price)
    
    def _run(self, category: str, max_price: int = None) -> str:
        """카테고리별 상품 필터링"""
        try:
            # 임시 샘플 데이터
            category_products = {
                "food": [
                    {"name": "스타벅스 아메리카노", "price": 4500, "rating": 4.8},
                    {"name": "배달의민족 2만원권", "price": 20000, "rating": 4.6},
                    {"name": "점심식사 지원권", "price": 10000, "rating": 4.5}
                ],
                "health": [
                    {"name": "헬스장 1개월 이용권", "price": 50000, "rating": 4.5},
                    {"name": "홈트레이닝 세트", "price": 35000, "rating": 4.2},
                    {"name": "건강검진 패키지", "price": 120000, "rating": 4.7}
                ],
                "life": [
                    {"name": "넷플릭스 1개월 구독권", "price": 17000, "rating": 4.7},
                    {"name": "생활용품 할인권", "price": 15000, "rating": 4.1}
                ]
            }
            
            products = category_products.get(category, [])
            
            # 가격 필터링
            if max_price:
                products = [p for p in products if p["price"] <= max_price]
            
            if not products:
                return f"'{category}' 카테고리에서 조건에 맞는 상품을 찾을 수 없습니다."
            
            result = f"{category} 카테고리 상품"
            if max_price:
                result += f" ({max_price}원 이하)"
            result += ":\n"
            
            for product in products:
                result += f"- {product['name']} ({product['price']}원, 평점: {product['rating']})\n"
                
            return result
        except Exception as e:
            return f"카테고리 필터링 중 오류가 발생했습니다: {str(e)}"

class GetRecommendationsTool(BaseTool):
    name = "get_recommendations"
    description = "사용자의 선호도를 기반으로 개인 맞춤 상품을 추천합니다."
    args_schema: Type[BaseModel] = GetRecommendationsInput

    async def _arun(self, user_id: str, limit: int = 5) -> str:
        """비동기 실행"""
        return await self._run(user_id, limit)
    
    def _run(self, user_id: str, limit: int = 5) -> str:
        """사용자 기반 개인 맞춤 추천"""
        try:
            # 임시 추천 로직 - 실제로는 사용자 선호도와 상품 데이터를 기반으로 추천
            recommended_products = [
                {"name": "스타벅스 아메리카노", "price": 4500, "rating": 4.8, "reason": "식음료 선호도 기반"},
                {"name": "넷플릭스 1개월 구독권", "price": 17000, "rating": 4.7, "reason": "생활 편의 선호도 기반"},
                {"name": "온라인 강의 수강권", "price": 25000, "rating": 4.3, "reason": "자기계발 관심 기반"},
                {"name": "헬스장 1개월 이용권", "price": 50000, "rating": 4.5, "reason": "건강 관심 기반"},
                {"name": "점심식사 지원권", "price": 10000, "rating": 4.5, "reason": "실용성 기반"}
            ]
            
            # 제한된 개수만큼 반환
            limited_products = recommended_products[:limit]
            
            result = f"{user_id}님을 위한 개인 맞춤 추천:\n"
            for i, product in enumerate(limited_products, 1):
                result += f"{i}. {product['name']} ({product['price']}원, 평점: {product['rating']}) - {product['reason']}\n"
                
            return result
        except Exception as e:
            return f"상품 추천 중 오류가 발생했습니다: {str(e)}"

# 도구 목록
def get_tools():
    """사용 가능한 모든 도구 반환"""
    return [
        SearchProductsTool(),
        FilterByCategoryTool(), 
        GetRecommendationsTool()
    ] 