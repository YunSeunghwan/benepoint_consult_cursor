"""
로깅 설정 및 관리
API 요청, 응답, 오류 등을 파일로 저장하여 나중에 분석 가능
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# 로그 디렉토리 생성
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """로거 설정"""
    
    # 파일 핸들러 (5MB마다 롤오버, 최대 5개 파일 보관)
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, log_file),
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5
    )
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    
    # 포맷터 설정
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 로거 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 다양한 용도의 로거들
api_logger = setup_logger('API', 'api_requests.log')
chat_logger = setup_logger('CHAT', 'chat_interactions.log')
error_logger = setup_logger('ERROR', 'errors.log', logging.ERROR)
system_logger = setup_logger('SYSTEM', 'system.log')

def log_api_request(method: str, path: str, user_id: str = None, data: dict = None):
    """API 요청 로깅"""
    api_logger.info(f"{method} {path} | User: {user_id} | Data: {data}")

def log_chat_interaction(user_id: str, message: str, response: str, products_count: int = 0):
    """채팅 상호작용 로깅"""
    chat_logger.info(f"User: {user_id} | Message: '{message}' | Products: {products_count} | Response: '{response[:100]}...'")

def log_error(error_type: str, error_message: str, context: dict = None):
    """오류 로깅"""
    error_logger.error(f"{error_type}: {error_message} | Context: {context}")

def log_system_event(event: str, details: dict = None):
    """시스템 이벤트 로깅"""
    system_logger.info(f"{event} | Details: {details}")