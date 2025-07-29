import { useState } from 'react'
import ChatInterface from '../components/ChatInterface'
import RecommendationList from '../components/RecommendationList'

export default function Home() {
  const [products, setProducts] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleProductsUpdate = (newProducts) => {
    setProducts(newProducts)
  }

  const handleLoadingChange = (loading) => {
    setIsLoading(loading)
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 Benefit Station AI</h1>
        <p>AI와 대화하며 맞춤 복리후생 상품을 찾아보세요!</p>
      </header>

      <main className="main-content">
        <div className="chat-section">
          <ChatInterface 
            onProductsUpdate={handleProductsUpdate}
            onLoadingChange={handleLoadingChange}
          />
        </div>
        
        <div className="recommendations-section">
          <RecommendationList 
            products={products} 
            isLoading={isLoading}
          />
        </div>
      </main>

      <footer className="app-footer">
        <p>Made with ❤️ for Benefit Station users</p>
      </footer>
    </div>
  )
} 