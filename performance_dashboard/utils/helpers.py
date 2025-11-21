"""Utility helper functions."""

import numpy as np
import pandas as pd
from matplotlib.cm import get_cmap
from matplotlib.colors import LinearSegmentedColormap, to_hex


def safe_divide(a, b):
    """0으로 나누기 방지"""
    return np.where(b == 0, np.nan, a / b)


def split_periods(data, days=7):
    """기간을 현재/이전으로 분할"""
    if data["date"].nunique() < days * 2:
        return None, None
    latest = data["date"].max()
    current = data[(data["date"] >= latest - pd.Timedelta(days=days-1)) & (data["date"] <= latest)]
    previous = data[(data["date"] >= latest - pd.Timedelta(days=days*2-1)) & (data["date"] < latest - pd.Timedelta(days=days))]
    return current, previous


def calculate_percentage_delta(current, previous, column):
    """변화율 계산"""
    if current is None or previous is None or current.empty or previous.empty:
        return np.nan
    current_sum = current[column].sum()
    previous_sum = previous[column].sum()
    return np.nan if previous_sum == 0 else (current_sum - previous_sum) / previous_sum


def add_time_bucket(dataframe, granularity, date_col="Date"):
    """시간 버킷 추가"""
    df = dataframe.copy()
    if granularity == "Daily":
        df["bucket"] = pd.to_datetime(df[date_col]).dt.date
    elif granularity == "Weekly":
        df["bucket"] = pd.to_datetime(df[date_col]).dt.to_period("W").apply(lambda r: r.start_time.date())
    else:  # Monthly
        df["bucket"] = pd.to_datetime(df[date_col]).dt.to_period("M").apply(lambda r: r.start_time.date())
    return df


def normalize_date_range(date_range, min_date, max_date):
    """날짜 범위 정규화"""
    try:
        if isinstance(date_range, (list, tuple)):
            if len(date_range) == 2:
                start, end = date_range[0], date_range[1]
            elif len(date_range) == 1:
                start = end = date_range[0]
            else:
                start, end = min_date, max_date
        else:
            start = end = date_range
    except Exception:
        start, end = min_date, max_date
    start = start or min_date
    end = end or max_date
    if start > end:
        start, end = end, start
    
    # 선택된 날짜가 데이터 범위를 벗어나지 않도록 보정
    start = max(start, min_date)
    end = min(end, max_date)
    
    return start, end


def get_color_palette(name="Greens", n=5, reverse=False):
    """색상 팔레트 생성"""
    cmap = get_cmap(name, n)
    vals = [to_hex(cmap(i)) for i in range(cmap.N)]
    return list(reversed(vals)) if reverse else vals


def get_gradient_colors(base="#2E7D32", n=5, to="white"):
    """그라데이션 색상 생성"""
    cmap = LinearSegmentedColormap.from_list("custom", [base, to])
    return [to_hex(cmap(i/(n-1))) for i in range(n)]
