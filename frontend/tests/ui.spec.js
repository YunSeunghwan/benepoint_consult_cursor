// Playwright UI tests for Benefit Station AI
const { test, expect } = require('@playwright/test')

test.describe('Benefit Station AI', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000')
  })

  test('홈페이지 로드 및 기본 요소 확인', async ({ page }) => {
    // 페이지 제목 확인
    await expect(page).toHaveTitle(/Benefit Station/)
    
    // 헤더 확인
    await expect(page.locator('h1')).toContainText('Benefit Station AI')
    
    // 채팅 인터페이스 확인
    await expect(page.locator('.chat-interface')).toBeVisible()
    await expect(page.locator('.chat-header h3')).toContainText('AI 채팅')
    
    // 추천 목록 섹션 확인
    await expect(page.locator('.recommendations-container')).toBeVisible()
    await expect(page.locator('.recommendations-header h3')).toContainText('추천 상품')
  })

  test('채팅 인터페이스 기본 동작', async ({ page }) => {
    // 초기 봇 메시지 확인
    await expect(page.locator('.bot-message').first()).toContainText('안녕하세요! 저는 Benefit Station AI')
    
    // 메시지 입력 필드 확인
    const messageInput = page.locator('.message-input')
    await expect(messageInput).toBeVisible()
    await expect(messageInput).toHaveAttribute('placeholder', /상품을 찾아달라고 말해보세요/)
    
    // 전송 버튼 확인
    const sendButton = page.locator('.send-button')
    await expect(sendButton).toBeVisible()
    await expect(sendButton).toContainText('전송')
  })

  test('퀵 버튼 기능 확인', async ({ page }) => {
    // 퀵 버튼들이 존재하는지 확인
    await expect(page.locator('.quick-button')).toHaveCount(4)
    
    // 각 퀵 버튼 텍스트 확인
    await expect(page.locator('.quick-button').nth(0)).toContainText('식사')
    await expect(page.locator('.quick-button').nth(1)).toContainText('건강')
    await expect(page.locator('.quick-button').nth(2)).toContainText('생활')
    await expect(page.locator('.quick-button').nth(3)).toContainText('저렴한')
    
    // 퀵 버튼 클릭시 메시지 입력 필드에 텍스트 입력되는지 확인
    await page.locator('.quick-button').nth(0).click()
    await expect(page.locator('.message-input')).toHaveValue('식사 관련 추천해줘')
  })

  test('빈 상태 UI 확인', async ({ page }) => {
    // 초기 상태에서는 추천 상품이 없으므로 빈 상태 메시지 확인
    await expect(page.locator('.empty-state')).toBeVisible()
    await expect(page.locator('.empty-state h4')).toContainText('아직 추천 상품이 없어요')
    
    // 제안 예시가 표시되는지 확인
    await expect(page.locator('.suggestion-examples')).toBeVisible()
    await expect(page.locator('.example-tag')).toContainText('예시')
  })

  test('반응형 디자인 확인 - 모바일', async ({ page }) => {
    // 모바일 화면 크기로 설정
    await page.setViewportSize({ width: 375, height: 667 })
    
    // 메인 컨텐츠가 세로로 배치되는지 확인
    const mainContent = page.locator('.main-content')
    await expect(mainContent).toHaveCSS('grid-template-columns', '1fr')
    
    // 채팅 인터페이스와 추천 목록이 모두 보이는지 확인
    await expect(page.locator('.chat-interface')).toBeVisible()
    await expect(page.locator('.recommendations-container')).toBeVisible()
  })

  test('키보드 인터랙션 확인', async ({ page }) => {
    const messageInput = page.locator('.message-input')
    
    // 메시지 입력
    await messageInput.fill('테스트 메시지')
    
    // Enter 키로 메시지 전송 (실제 API 호출은 하지 않음)
    await messageInput.press('Enter')
    
    // 입력 필드가 비워지는지 확인 (API 실패시에도 일시적으로 비워짐)
    await expect(messageInput).toHaveValue('')
  })

  test('로딩 상태 확인', async ({ page }) => {
    // 메시지 입력
    const messageInput = page.locator('.message-input')
    await messageInput.fill('테스트 메시지')
    
    // 전송 버튼 클릭
    const sendButton = page.locator('.send-button')
    await sendButton.click()
    
    // 로딩 상태 확인 (짧은 시간이므로 빠르게 확인)
    // 실제 API 연결이 안되어 있으면 빠르게 에러 메시지가 나타남
    await page.waitForTimeout(100)
    
    // 사용자 메시지가 추가되었는지 확인
    await expect(page.locator('.user-message').last()).toContainText('테스트 메시지')
  })

  test('접근성 확인', async ({ page }) => {
    // 주요 요소들이 적절한 ARIA 라벨을 가지고 있는지 확인하거나
    // 키보드 네비게이션이 가능한지 확인
    
    // 메시지 입력 필드로 탭 이동
    await page.keyboard.press('Tab')
    await expect(page.locator('.message-input')).toBeFocused()
    
    // 전송 버튼으로 탭 이동
    await page.keyboard.press('Tab')
    await expect(page.locator('.send-button')).toBeFocused()
  })
}) 