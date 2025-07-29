import ProductCard from './ProductCard'

export default function RecommendationList({ products, isLoading }) {
  if (isLoading) {
    return (
      <div className="recommendations-container">
        <div className="recommendations-header">
          <h3>🔍 추천 상품</h3>
        </div>
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>AI가 최적의 상품을 찾고 있어요...</p>
        </div>
      </div>
    )
  }

  if (!products || products.length === 0) {
    return (
      <div className="recommendations-container">
        <div className="recommendations-header">
          <h3>🔍 추천 상품</h3>
        </div>
        <div className="empty-state">
          <div className="empty-icon">🤖</div>
          <h4>아직 추천 상품이 없어요</h4>
          <p>AI에게 원하는 상품을 말해보세요!<br/>
             "식사 관련 추천해줘" 또는 "3만원 이하 상품 보여줘" 같이요.</p>
          <div className="suggestion-examples">
            <div className="example-tag">💡 예시</div>
            <ul>
              <li>"커피 쿠폰 있어?"</li>
              <li>"건강 관련 상품 추천해줘"</li>
              <li>"생활용품 할인 상품은?"</li>
              <li>"2만원 이하로 추천해줘"</li>
            </ul>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <h3>🔍 추천 상품</h3>
        <div className="results-count">
          총 {products.length}개의 상품을 찾았어요
        </div>
      </div>

      <div className="products-grid">
        {products.map((product, index) => (
          <ProductCard 
            key={product.id || index} 
            product={product} 
          />
        ))}
      </div>

      <div className="recommendations-footer">
        <p className="footer-text">
          더 정확한 추천을 위해 구체적으로 말씀해주세요! 
          예: "스타벅스 말고 다른 커피는?", "1만원대 건강 상품은?"
        </p>
      </div>
    </div>
  )
} 