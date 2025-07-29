"""
추천 시스템 구현
사용자 선호도와 상품 데이터를 기반으로 개인 맞춤 추천을 제공
"""

import random
from typing import List, Dict, Optional
from db import get_products, get_user_preferences

class RecommendationEngine:
    def __init__(self):
        self.category_weights = {
            'food': 1.2,
            'health': 1.1,
            'life': 1.0,
            'shopping': 0.9,
            'education': 0.8
        }
    
    async def get_personalized_recommendations(
        self, 
        user_id: str, 
        limit: int = 5,
        category: Optional[str] = None,
        max_price: Optional[int] = None
    ) -> List[Dict]:
        """
        개인 맞춤 상품 추천
        """
        try:
            # 사용자 선호도 조회
            user_prefs = await get_user_preferences(user_id)
            preferred_categories = []
            
            if user_prefs and user_prefs.get('preferences'):
                preferred_categories = user_prefs['preferences'].get('categories', [])
            
            # 상품 목록 조회
            products = await get_products(category=category, max_price=max_price)
            
            # 추천 점수 계산
            scored_products = []
            for product in products:
                score = self._calculate_recommendation_score(
                    product, 
                    preferred_categories
                )
                scored_products.append({
                    **product,
                    'recommendation_score': score
                })
            
            # 점수 순으로 정렬
            scored_products.sort(key=lambda x: x['recommendation_score'], reverse=True)
            
            # 상위 N개 반환
            return scored_products[:limit]
            
        except Exception as e:
            print(f"추천 생성 오류: {e}")
            return []
    
    def _calculate_recommendation_score(
        self, 
        product: Dict, 
        preferred_categories: List[str]
    ) -> float:
        """
        상품의 추천 점수 계산
        """
        base_score = product.get('rating', 0) * 20  # 평점 기반 점수 (최대 100점)
        
        # 카테고리 선호도 보너스
        category_bonus = 0
        if product.get('category') in preferred_categories:
            category_bonus = 30
        
        # 카테고리별 가중치 적용
        category_weight = self.category_weights.get(product.get('category', ''), 1.0)
        weight_bonus = (category_weight - 1.0) * 20
        
        # 가격 점수 (저렴할수록 높은 점수)
        price = product.get('price', 0)
        if price > 0:
            price_score = max(0, 50 - (price / 1000))  # 가격이 낮을수록 높은 점수
        else:
            price_score = 0
        
        # 랜덤 요소 추가 (다양성을 위해)
        random_bonus = random.uniform(-5, 5)
        
        total_score = base_score + category_bonus + weight_bonus + price_score + random_bonus
        
        return round(total_score, 2)
    
    async def get_similar_products(self, product_id: str, limit: int = 3) -> List[Dict]:
        """
        유사 상품 추천
        """
        try:
            # 임시 구현 - 실제로는 더 정교한 유사도 계산 필요
            products = await get_products()
            
            # 현재 상품 제외하고 랜덤하게 선택
            similar_products = [p for p in products if p.get('id') != product_id]
            random.shuffle(similar_products)
            
            return similar_products[:limit]
            
        except Exception as e:
            print(f"유사 상품 추천 오류: {e}")
            return []
    
    async def get_trending_products(self, limit: int = 5) -> List[Dict]:
        """
        인기 상품 추천 (평점 및 가격 기준)
        """
        try:
            products = await get_products()
            
            # 평점과 가격을 고려한 인기도 점수 계산
            for product in products:
                rating = product.get('rating', 0)
                price = product.get('price', 0)
                
                # 인기도 점수 = 평점 * 가중치 - 가격 페널티
                popularity_score = rating * 20 - (price / 10000)
                product['popularity_score'] = popularity_score
            
            # 인기도 순으로 정렬
            products.sort(key=lambda x: x.get('popularity_score', 0), reverse=True)
            
            return products[:limit]
            
        except Exception as e:
            print(f"인기 상품 조회 오류: {e}")
            return []

# 전역 추천 엔진 인스턴스
recommendation_engine = RecommendationEngine()

def get_recommendation_engine():
    """추천 엔진 인스턴스 반환"""
    return recommendation_engine 