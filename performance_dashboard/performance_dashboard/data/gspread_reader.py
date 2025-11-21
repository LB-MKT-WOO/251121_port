"""Google Sheets reader module."""

import gspread
import gspread_dataframe as gd
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
import logging
import os

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_google_sheet_to_df(sheet_url, sheet_name, credentials_file):
    """
    Google Sheets에서 데이터를 읽어 pandas DataFrame으로 변환
    
    Args:
        sheet_url (str): Google Sheets URL
        sheet_name (str): 시트 이름
        credentials_file (str): Google Service Account 인증 파일 경로
    
    Returns:
        pd.DataFrame: 시트 데이터를 담은 DataFrame, 실패시 None
    """
    try:
        # 인증 파일 존재 확인
        creds_path = Path(credentials_file)
        if not creds_path.exists():
            logger.error(f"❌ 인증 파일을 찾을 수 없습니다: {credentials_file}")
            return None
        
        # Google Sheets API 스코프 설정
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        logger.info("🔐 Google Sheets 인증 중...")
        # 인증 및 클라이언트 생성
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            str(creds_path), scope
        )
        client = gspread.authorize(credentials)
        
        logger.info("📊 스프레드시트 열기 중...")
        # 스프레드시트 열기
        doc = client.open_by_url(sheet_url)
        
        logger.info(f"📋 시트 '{sheet_name}' 찾는 중...")
        # 시트 찾기
        sheet = None
        for worksheet in doc.worksheets():
            if worksheet.title == sheet_name:
                sheet = worksheet
                break
        
        if sheet is None:
            available_sheets = [ws.title for ws in doc.worksheets()]
            logger.error(f"❌ 시트 '{sheet_name}'을 찾을 수 없습니다.")
            logger.error(f"사용 가능한 시트: {available_sheets}")
            return None
        
        logger.info("📖 데이터 읽기 중...")
        # 모든 데이터 읽기
        data = sheet.get_all_records()
        
        if not data:
            logger.warning("⚠️ 시트에 데이터가 없습니다.")
            return pd.DataFrame()
        
        # DataFrame으로 변환
        df = pd.DataFrame(data)
        
        logger.info(f"✅ 데이터 읽기 완료: {len(df)} 행, {len(df.columns)} 열")
        logger.info(f"📊 컬럼: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Google Sheets 읽기 실패: {e}")
        import traceback
        traceback.print_exc()
        return None

