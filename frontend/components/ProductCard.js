export default function ProductCard({ product }) {
  const getCategoryInfo = (category) => {
    const categoryMap = {
      food: { name: '맛집 & 레저', color: 'blue', emoji: '🍽️' },
      health: { name: '건강', color: 'green', emoji: '💪' },
      shopping: { name: '쇼핑', color: 'purple', emoji: '🛍️' },
      life: { name: '생활', color: 'orange', emoji: '🏠' },
      education: { name: '교육', color: 'red', emoji: '📚' }
    }
    return categoryMap[category] || { name: category, color: 'gray', emoji: '📦' }
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('ko-KR').format(price)
  }

  const renderStars = (rating) => {
    const fullStars = Math.floor(rating)
    const hasHalfStar = rating % 1 !== 0
    const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0)

    return (
      <div className="star-rating">
        {'★'.repeat(fullStars)}
        {hasHalfStar && '☆'}
        {'☆'.repeat(emptyStars)}
        <span className="rating-number">({rating})</span>
      </div>
    )
  }

  const categoryInfo = getCategoryInfo(product.category)

  return (
    <div className="product-card">
      <div className="product-header">
        <div className={`category-tag ${categoryInfo.color}`}>
          <span className="category-emoji">{categoryInfo.emoji}</span>
          <span className="category-name">{categoryInfo.name}</span>
        </div>
        <div className="product-rating">
          {renderStars(product.rating)}
        </div>
      </div>

      <div className="product-body">
        <h4 className="product-name">{product.name}</h4>
        <div className="product-price">
          <span className="price-amount">{formatPrice(product.price)}원</span>
        </div>
      </div>

      <div className="product-actions">
        <button className="action-button primary">
          상세보기
        </button>
        <button className="action-button secondary">
          찜하기 ❤️
        </button>
      </div>

      <div className="product-footer">
        <small className="product-id">상품코드: {product.id}</small>
      </div>
    </div>
  )
} 