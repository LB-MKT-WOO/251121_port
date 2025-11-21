"""Product dates loader."""

import json
import streamlit as st
import os

from performance_dashboard.config import PRODUCT_DATES_FILE


@st.cache_data(show_spinner=False, ttl=3600)
def load_product_dates(file_path: str = None):
    """Product별 날짜 범위 로드"""
    if file_path is None:
        file_path = PRODUCT_DATES_FILE
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('products', [])
    except Exception as e:
        st.error(f"Product 날짜 파일 로드 실패: {e}")
        return []

