import { useState } from 'react'
import axios from 'axios'

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

export default function ChatInterface({ onProductsUpdate, onLoadingChange }) {
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: '안녕하세요! 저는 Benefit Station AI 어시스턴트입니다. 🤖\n어떤 복리후생 상품을 찾고 계신가요?',
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)
    onLoadingChange(true)

    try {
      const response = await axios.post(`${BACKEND_URL}/api/chat`, {
        message: inputMessage,
        user_id: 'demo-user'
      })

      const botMessage = {
        type: 'bot',
        content: response.data.response,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
      
      // 추천 상품이 있으면 부모 컴포넌트에 전달
      if (response.data.products && response.data.products.length > 0) {
        onProductsUpdate(response.data.products)
      }

    } catch (error) {
      console.error('채팅 API 오류:', error)
      const errorMessage = {
        type: 'bot',
        content: '죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      onLoadingChange(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const formatMessage = (content) => {
    return content.split('\n').map((line, index) => (
      <span key={index}>
        {line}
        {index < content.split('\n').length - 1 && <br />}
      </span>
    ))
  }

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>💬 AI 채팅</h3>
      </div>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
          >
            <div className="message-content">
              {formatMessage(message.content)}
            </div>
            <div className="message-time">
              {message.timestamp.toLocaleTimeString()}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message bot-message">
            <div className="message-content loading">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
              AI가 생각하고 있어요...
            </div>
          </div>
        )}
      </div>

      <div className="chat-input">
        <div className="input-group">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="상품을 찾아달라고 말해보세요! (예: 식사 관련 추천해줘)"
            className="message-input"
            rows="2"
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={isLoading || !inputMessage.trim()}
            className="send-button"
          >
            {isLoading ? '전송 중...' : '전송'}
          </button>
        </div>
        
        <div className="quick-buttons">
          <button 
            className="quick-button"
            onClick={() => setInputMessage('식사 관련 추천해줘')}
            disabled={isLoading}
          >
            🍽️ 식사
          </button>
          <button 
            className="quick-button"
            onClick={() => setInputMessage('건강 관련 상품 보여줘')}
            disabled={isLoading}
          >
            💪 건강
          </button>
          <button 
            className="quick-button"
            onClick={() => setInputMessage('생활용품 할인 있어?')}
            disabled={isLoading}
          >
            🏠 생활
          </button>
          <button 
            className="quick-button"
            onClick={() => setInputMessage('3만원 이하로 추천해줘')}
            disabled={isLoading}
          >
            💰 저렴한
          </button>
        </div>
      </div>
    </div>
  )
} 