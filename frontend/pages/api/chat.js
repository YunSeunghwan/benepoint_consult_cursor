// Next.js API route to proxy chat requests to FastAPI backend
import axios from 'axios'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' })
  }

  try {
    const { message, user_id } = req.body

    if (!message) {
      return res.status(400).json({ message: 'Message is required' })
    }

    // Forward request to FastAPI backend
    const response = await axios.post(`${BACKEND_URL}/api/chat`, {
      message,
      user_id: user_id || 'demo-user'
    }, {
      timeout: 30000, // 30 second timeout
      headers: {
        'Content-Type': 'application/json'
      }
    })

    return res.status(200).json(response.data)

  } catch (error) {
    console.error('Chat API error:', error.message)
    
    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({ 
        message: '백엔드 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.',
        error: 'Backend server unavailable'
      })
    }

    if (error.response) {
      return res.status(error.response.status).json({
        message: error.response.data?.detail || '서버 오류가 발생했습니다.',
        error: error.response.data
      })
    }

    return res.status(500).json({ 
      message: '예상치 못한 오류가 발생했습니다.',
      error: error.message 
    })
  }
} 