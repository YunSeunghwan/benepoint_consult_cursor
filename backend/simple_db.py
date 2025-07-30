"""
간단한 로컬 데이터베이스 관리 (Supabase 대안)
JSON 파일 기반으로 데이터 저장/조회
"""

import json
import os
from typing import List, Dict, Optional

class SimpleDB:
    def __init__(self, data_file: str = "products_data.json"):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """JSON 파일에서 데이터 로드"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"products": [], "users": []}
    
    def _save_data(self):
        """데이터를 JSON 파일에 저장"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_products(self, category: str = None, max_price: int = None) -> List[Dict]:
        """상품 목록 조회"""
        products = self.data.get("products", [])
        
        # 카테고리 필터링
        if category:
            products = [p for p in products if p.get("category") == category]
        
        # 가격 필터링
        if max_price:
            products = [p for p in products if p.get("price", 0) <= max_price]
        
        return products
    
    def search_products(self, query: str) -> List[Dict]:
        """키워드로 상품 검색"""
        query = query.lower()
        products = self.data.get("products", [])
        
        return [
            p for p in products 
            if query in p.get("name", "").lower() or 
               query in p.get("category", "").lower()
        ]
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """사용자 정보 조회"""
        users = self.data.get("users", [])
        return next((u for u in users if u.get("id") == user_id), None)
    
    def add_product(self, product: Dict):
        """새 상품 추가"""
        self.data.setdefault("products", []).append(product)
        self._save_data()
    
    def update_user_preferences(self, user_id: str, preferences: Dict):
        """사용자 선호도 업데이트"""
        users = self.data.setdefault("users", [])
        user = next((u for u in users if u.get("id") == user_id), None)
        
        if user:
            user["preferences"] = preferences
        else:
            users.append({
                "id": user_id,
                "name": f"사용자_{user_id}",
                "preferences": preferences
            })
        
        self._save_data()

# 전역 인스턴스
simple_db = SimpleDB()