-- Benefit Station AI 데이터베이스 설정
-- Supabase SQL Editor에서 실행하세요

-- 사용자 테이블
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE,
  preferences JSONB DEFAULT '{"categories": []}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 상품 테이블  
CREATE TABLE products (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price INTEGER NOT NULL,
  rating REAL DEFAULT 0,
  description TEXT,
  image_url TEXT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 사용자 상품 상호작용 테이블 (추천 개선용)
CREATE TABLE user_interactions (
  id SERIAL PRIMARY KEY,
  user_id TEXT REFERENCES users(id),
  product_id TEXT REFERENCES products(id),
  interaction_type TEXT NOT NULL, -- 'view', 'like', 'purchase'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 인덱스 생성 (성능 최적화)
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_rating ON products(rating);
CREATE INDEX idx_user_interactions_user_id ON user_interactions(user_id);

-- 샘플 데이터 삽입
INSERT INTO users (id, name, preferences) VALUES 
('demo-user', '테스트 사용자', '{"categories": ["food", "health"]}'::jsonb),
('user-001', '김철수', '{"categories": ["food", "life"]}'::jsonb),
('user-002', '박영희', '{"categories": ["health", "education"]}'::jsonb);

INSERT INTO products (id, name, category, price, rating, description) VALUES
('p1', '스타벅스 아메리카노', 'food', 4500, 4.8, '신선한 원두로 내린 아메리카노 기프티콘'),
('p2', '헬스장 1개월 이용권', 'health', 50000, 4.5, '전국 체인 헬스장 1개월 자유 이용권'),
('p3', '온라인 쇼핑몰 5천원 할인', 'shopping', 5000, 4.2, '인기 쇼핑몰에서 사용 가능한 할인쿠폰'),
('p4', '넷플릭스 1개월 구독권', 'life', 17000, 4.7, '넷플릭스 프리미엄 플랜 1개월 이용권'),
('p5', '온라인 강의 수강권', 'education', 25000, 4.3, '인기 온라인 강의 플랫폼 수강권'),
('p6', '생활용품 할인권', 'life', 15000, 4.1, '생필품 구매시 사용 가능한 할인권'),
('p7', '점심식사 지원권', 'food', 10000, 4.5, '회사 근처 식당에서 사용 가능한 식사권'),
('p8', '배달의민족 2만원권', 'food', 20000, 4.6, '배달 주문시 사용 가능한 상품권'),
('p9', '홈트레이닝 세트', 'health', 35000, 4.2, '집에서 운동할 수 있는 트레이닝 키트'),
('p10', '건강검진 패키지', 'health', 120000, 4.7, '종합 건강검진 바우처');

-- RLS (Row Level Security) 설정 (선택사항)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_interactions ENABLE ROW LEVEL SECURITY;

-- 기본 정책 (모든 사용자가 읽기 가능)
CREATE POLICY "Enable read access for all users" ON products FOR SELECT USING (is_active = true);
CREATE POLICY "Enable read access for users" ON users FOR SELECT USING (true);