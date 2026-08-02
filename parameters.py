
#알파 성능 기준 (이 기준을 통과해야 제출됨)
SIMULATION_CRITERIA = {
    'SHARPE_THRESHOLD': 1.25,    # Delay 1 Alpha 기준 (Sharpe > 1.25)
    'TURNOVER_MIN': 1.0,         # 최소 회전율 1%
    'TURNOVER_MAX': 70.0,        # 최대 회전율 70%
    'FITNESS_THRESHOLD': 0.9,    # 최소 Fitness 0.9 (가능성 있는 알파)
    'MAX_WEIGHT': 0.1,           # 최대 가중치 10%
    'SUBUNIVERSE_SHARPE_RATIO': 0.75,  # Sub-universe Sharpe 비율
    'MIN_INSTRUMENTS': 100       # 최소 주식 수
}

DEFAULT_SETTINGS = {
    'region': 'USA',             # 지역: USA, CHN, EUR 등
    'universe': 'TOP3000',       # 유니버스: TOP3000, TOP1000 등
    'delay': 1,                  # 지연: 1일 (실제 거래 지연)
    'instrumentType': 'EQUITY',
    'decay': 6,                  # 감쇠: 6일 (포지션 유지 기간)
    'truncation': 0.1,           # 절단: 10% (극값 제거)
    'neutralization': 'SUBINDUSTRY',  # 중립화: SUBINDUSTRY, SECTOR 등
    'pasteurization': 'ON',      # 살균: ON (데이터 정제)
    'nanHandling': 'OFF',        # NaN 처리: OFF
    'unitHandling': 'VERIFY',    # 단위 검증: VERIFY
    'maxTrade': 'OFF'            # 최대 거래량 제한: OFF
}
