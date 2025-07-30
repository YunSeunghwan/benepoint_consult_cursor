"""
로그 조회 및 분석 도구
웹에서 로그를 확인할 수 있는 API들
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

LOG_DIR = "logs"

def get_log_files() -> List[str]:
    """사용 가능한 로그 파일 목록 반환"""
    log_path = Path(LOG_DIR)
    if not log_path.exists():
        return []
    
    return [f.name for f in log_path.glob("*.log")]

def read_log_file(filename: str, lines: int = 100) -> List[str]:
    """로그 파일의 마지막 N줄 읽기"""
    log_file = os.path.join(LOG_DIR, filename)
    
    if not os.path.exists(log_file):
        return []
    
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            return all_lines[-lines:] if lines > 0 else all_lines
    except Exception as e:
        return [f"로그 파일 읽기 오류: {str(e)}"]

def search_logs(filename: str, keyword: str, lines: int = 50) -> List[str]:
    """로그에서 키워드 검색"""
    log_file = os.path.join(LOG_DIR, filename)
    
    if not os.path.exists(log_file):
        return []
    
    try:
        results = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                if keyword.lower() in line.lower():
                    results.append(f"[Line {line_num}] {line.strip()}")
                    if len(results) >= lines:
                        break
        return results
    except Exception as e:
        return [f"로그 검색 오류: {str(e)}"]

def get_log_stats(filename: str) -> Dict:
    """로그 파일 통계 정보"""
    log_file = os.path.join(LOG_DIR, filename)
    
    if not os.path.exists(log_file):
        return {"error": "파일이 존재하지 않습니다"}
    
    try:
        stats = {
            "total_lines": 0,
            "file_size": 0,
            "last_modified": None,
            "error_count": 0,
            "info_count": 0
        }
        
        file_stat = os.stat(log_file)
        stats["file_size"] = file_stat.st_size
        stats["last_modified"] = datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                stats["total_lines"] += 1
                if "ERROR" in line:
                    stats["error_count"] += 1
                elif "INFO" in line:
                    stats["info_count"] += 1
        
        return stats
    except Exception as e:
        return {"error": f"통계 생성 오류: {str(e)}"}

def parse_chat_logs() -> List[Dict]:
    """채팅 로그를 파싱해서 구조화된 데이터로 반환"""
    chat_log_file = os.path.join(LOG_DIR, "chat_interactions.log")
    
    if not os.path.exists(chat_log_file):
        return []
    
    interactions = []
    try:
        with open(chat_log_file, 'r', encoding='utf-8') as f:
            for line in f:
                if "CHAT - INFO" in line:
                    # 로그 파싱
                    parts = line.split(" | ")
                    if len(parts) >= 4:
                        timestamp = line.split(" - ")[0]
                        user_part = next((p for p in parts if p.startswith("User:")), "")
                        message_part = next((p for p in parts if p.startswith("Message:")), "")
                        products_part = next((p for p in parts if p.startswith("Products:")), "")
                        
                        interactions.append({
                            "timestamp": timestamp,
                            "user_id": user_part.replace("User: ", "").strip(),
                            "message": message_part.replace("Message: ", "").strip(),
                            "products_count": products_part.replace("Products: ", "").strip()
                        })
    except Exception as e:
        return [{"error": f"채팅 로그 파싱 오류: {str(e)}"}]
    
    return interactions[-50:]  # 최근 50개만 반환