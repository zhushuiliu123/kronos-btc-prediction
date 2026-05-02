"""
国际化模块 - 支持中文 / English / 한국어
在 dashboard 侧边栏选择语言后，所有 UI 文本自动切换。
"""

LANGUAGES = {
    "中文": "zh",
    "English": "en",
    "한국어": "ko",
}

# 语言名称（用于语言选择器本身的显示）
LANG_NAMES = {
    "zh": "中文",
    "en": "English",
    "ko": "한국어",
}

STRINGS = {
    # ====== 通用 ======
    "app_title": {
        "zh": "Kronos 金融预测工作台",
        "en": "Kronos Financial Prediction Workspace",
        "ko": "Kronos 금융 예측 워크스페이스",
    },
    "version": {
        "zh": "Kronos 金融 K 线预测工作台 v1.0",
        "en": "Kronos Financial K-Line Prediction Workspace v1.0",
        "ko": "Kronos 금융 K라인 예측 워크스페이스 v1.0",
    },
    "backend_info": {
        "zh": "纯 NumPy 推理 | 无需 PyTorch | CPU",
        "en": "Pure NumPy Inference | No PyTorch | CPU",
        "ko": "순수 NumPy 추론 | PyTorch 불필요 | CPU",
    },

    # ====== 侧边栏 ======
    "sidebar_title": {
        "zh": "控制面板",
        "en": "Control Panel",
        "ko": "제어판",
    },
    "model_status": {
        "zh": "模型状态",
        "en": "Model Status",
        "ko": "모델 상태",
    },
    "model_loaded": {
        "zh": "{} 已加载",
        "en": "{} Loaded",
        "ko": "{} 로드됨",
    },
    "model_not_loaded": {
        "zh": "模型未加载",
        "en": "Model not loaded",
        "ko": "모델 미로드",
    },
    "param_count": {
        "zh": "参数量",
        "en": "Parameters",
        "ko": "파라미터 수",
    },
    "context_length": {
        "zh": "上下文",
        "en": "Context",
        "ko": "컨텍스트",
    },
    "backend": {
        "zh": "后端",
        "en": "Backend",
        "ko": "백엔드",
    },
    "load_model_btn": {
        "zh": "加载模型",
        "en": "Load Model",
        "ko": "모델 로드",
    },
    "loading_model": {
        "zh": "正在加载模型权重...",
        "en": "Loading model weights...",
        "ko": "모델 가중치 로딩 중...",
    },
    "model_load_success": {
        "zh": "模型加载成功！",
        "en": "Model loaded successfully!",
        "ko": "모델 로드 성공!",
    },
    "model_load_fail": {
        "zh": "模型加载失败: {}",
        "en": "Model load failed: {}",
        "ko": "모델 로드 실패: {}",
    },
    "data_upload": {
        "zh": "数据上传",
        "en": "Data Upload",
        "ko": "데이터 업로드",
    },
    "upload_csv": {
        "zh": "上传 CSV 文件（OHLCV 格式）",
        "en": "Upload CSV file (OHLCV format)",
        "ko": "CSV 파일 업로드 (OHLCV 형식)",
    },
    "upload_csv_help": {
        "zh": "CSV 文件需包含 open, high, low, close 列，volume 和 amount 可选",
        "en": "CSV must contain open, high, low, close columns; volume and amount are optional",
        "ko": "CSV에 open, high, low, close 열이 포함되어야 하며, volume과 amount는 선택사항",
    },
    "gen_synthetic_btn": {
        "zh": "生成合成数据（演示）",
        "en": "Generate Synthetic Data (Demo)",
        "ko": "합성 데이터 생성 (데모)",
    },
    "generating": {
        "zh": "生成中...",
        "en": "Generating...",
        "ko": "생성 중...",
    },
    "synthetic_done": {
        "zh": "已生成 {} 天合成 K 线数据",
        "en": "Generated {} days of synthetic K-line data",
        "ko": "{}일치 합성 K라인 데이터 생성됨",
    },
    "pred_params": {
        "zh": "预测参数",
        "en": "Prediction Parameters",
        "ko": "예측 파라미터",
    },
    "lookback_window": {
        "zh": "回看窗口",
        "en": "Lookback Window",
        "ko": "룩백 윈도우",
    },
    "lookback_help": {
        "zh": "使用多少个历史数据点进行预测",
        "en": "Number of historical data points for prediction",
        "ko": "예측에 사용할 과거 데이터 포인트 수",
    },
    "pred_length": {
        "zh": "预测长度",
        "en": "Prediction Length",
        "ko": "예측 길이",
    },
    "pred_length_help": {
        "zh": "预测未来多少个时间步",
        "en": "How many future time steps to predict",
        "ko": "예측할 미래 타임스텝 수",
    },
    "temperature_help": {
        "zh": "控制预测随机性，越低越保守",
        "en": "Controls randomness; lower = more conservative",
        "ko": "예측의 무작위성 제어; 낮을수록 보수적",
    },
    "top_p_help": {
        "zh": "核采样概率",
        "en": "Nucleus sampling probability",
        "ko": "핵 샘플링 확률",
    },
    "greedy_decode": {
        "zh": "贪心解码",
        "en": "Greedy Decoding",
        "ko": "탐욕 디코딩",
    },
    "greedy_help": {
        "zh": "使用贪心策略而非采样",
        "en": "Use greedy strategy instead of sampling",
        "ko": "샘플링 대신 탐욕 전략 사용",
    },
    "run_pred_btn": {
        "zh": "运行预测",
        "en": "Run Prediction",
        "ko": "예측 실행",
    },
    "language_label": {
        "zh": "语言 / Language",
        "en": "Language / 语言",
        "ko": "언어 / Language",
    },

    # ====== Tab 标签 ======
    "tab_prediction": {
        "zh": "预测",
        "en": "Prediction",
        "ko": "예측",
    },
    "tab_data_mgmt": {
        "zh": "数据管理",
        "en": "Data Management",
        "ko": "데이터 관리",
    },
    "tab_model_info": {
        "zh": "模型信息",
        "en": "Model Info",
        "ko": "모델 정보",
    },
    "tab_batch": {
        "zh": "批量预测",
        "en": "Batch Prediction",
        "ko": "배치 예측",
    },
    "tab_history": {
        "zh": "历史",
        "en": "History",
        "ko": "기록",
    },

    # ====== Tab 1: 预测 ======
    "kline_prediction": {
        "zh": "K 线预测",
        "en": "K-Line Prediction",
        "ko": "K라인 예측",
    },
    "data_loaded": {
        "zh": "已加载数据: {} 行",
        "en": "Data loaded: {} rows",
        "ko": "데이터 로드됨: {} 행",
    },
    "data_load_fail": {
        "zh": "数据加载失败: {}",
        "en": "Data load failed: {}",
        "ko": "데이터 로드 실패: {}",
    },
    "input_preview": {
        "zh": "输入数据预览",
        "en": "Input Data Preview",
        "ko": "입력 데이터 미리보기",
    },
    "data_rows": {
        "zh": "数据行数",
        "en": "Data Rows",
        "ko": "데이터 행 수",
    },
    "time_range": {
        "zh": "时间范围",
        "en": "Time Range",
        "ko": "시간 범위",
    },
    "close_volatility": {
        "zh": "Close 波动幅度",
        "en": "Close Volatility",
        "ko": "Close 변동폭",
    },
    "history_kline": {
        "zh": "历史 K 线",
        "en": "Historical K-Line",
        "ko": "과거 K라인",
    },
    "history_kline_title": {
        "zh": "历史数据 K 线图",
        "en": "Historical Data K-Line Chart",
        "ko": "과거 데이터 K라인 차트",
    },

    # ====== 预测结果 ======
    "pred_result": {
        "zh": "预测结果",
        "en": "Prediction Results",
        "ko": "예측 결과",
    },
    "pred_steps": {
        "zh": "预测步数",
        "en": "Prediction Steps",
        "ko": "예측 스텝 수",
    },
    "pred_steps_unit": {
        "zh": "{} 步",
        "en": "{} steps",
        "ko": "{} 스텝",
    },
    "pred_data": {
        "zh": "预测数据",
        "en": "Prediction Data",
        "ko": "예측 데이터",
    },
    "download_pred": {
        "zh": "下载预测结果 (CSV)",
        "en": "Download Prediction (CSV)",
        "ko": "예측 결과 다운로드 (CSV)",
    },
    "pred_complete": {
        "zh": "预测完成！MAE (Close): {:.4f}",
        "en": "Prediction complete! MAE (Close): {:.4f}",
        "ko": "예측 완료! MAE (Close): {:.4f}",
    },
    "data_insufficient": {
        "zh": "数据不足：需要 {} 行，当前仅有 {} 行",
        "en": "Insufficient data: need {} rows, only {} available",
        "ko": "데이터 부족: {}행 필요, 현재 {}행만 사용 가능",
    },
    "predicting": {
        "zh": "正在预测未来 {} 步...",
        "en": "Predicting next {} steps...",
        "ko": "향후 {} 스텝 예측 중...",
    },
    "preparing": {
        "zh": "准备数据...",
        "en": "Preparing data...",
        "ko": "데이터 준비 중...",
    },
    "start_inference": {
        "zh": "开始推理...",
        "en": "Starting inference...",
        "ko": "추론 시작 중...",
    },
    "inference_progress": {
        "zh": "推理中: {}/{}",
        "en": "Inference: {}/{}",
        "ko": "추론 중: {}/{}",
    },
    "generating_result": {
        "zh": "生成结果...",
        "en": "Generating results...",
        "ko": "결과 생성 중...",
    },
    "done": {
        "zh": "完成！",
        "en": "Done!",
        "ko": "완료!",
    },
    "pred_failed": {
        "zh": "预测失败: {}",
        "en": "Prediction failed: {}",
        "ko": "예측 실패: {}",
    },

    # ====== 图表 ======
    "kline_chart": {
        "zh": "K 线图",
        "en": "K-Line Chart",
        "ko": "K라인 차트",
    },
    "price": {
        "zh": "价格",
        "en": "Price",
        "ko": "가격",
    },
    "volume": {
        "zh": "成交量",
        "en": "Volume",
        "ko": "거래량",
    },
    "kline_result_title": {
        "zh": "K 线预测结果（{} 历史数据 + {} 预测数据）",
        "en": "K-Line Prediction Results ({} Historical + {} Predicted)",
        "ko": "K라인 예측 결과 ({} 과거 + {} 예측)",
    },
    "close_compare_title": {
        "zh": "Close 价格对比（实际 vs 预测）",
        "en": "Close Price Comparison (Actual vs Predicted)",
        "ko": "Close 가격 비교 (실제 vs 예측)",
    },
    "time": {
        "zh": "时间",
        "en": "Time",
        "ko": "시간",
    },
    "legend_historical": {
        "zh": "历史数据",
        "en": "Historical Data",
        "ko": "과거 데이터",
    },
    "legend_predicted": {
        "zh": "预测数据",
        "en": "Predicted Data",
        "ko": "예측 데이터",
    },
    "legend_actual": {
        "zh": "实际数据",
        "en": "Actual Data",
        "ko": "실제 데이터",
    },
    "legend_kline": {
        "zh": "K 线",
        "en": "K-Line",
        "ko": "K라인",
    },
    "legend_actual_close": {
        "zh": "实际 Close",
        "en": "Actual Close",
        "ko": "실제 Close",
    },
    "legend_pred_close": {
        "zh": "预测 Close",
        "en": "Predicted Close",
        "ko": "예측 Close",
    },

    # ====== Tab 2: 数据管理 ======
    "data_mgmt_title": {
        "zh": "数据管理",
        "en": "Data Management",
        "ko": "데이터 관리",
    },
    "data_stats": {
        "zh": "数据统计",
        "en": "Data Statistics",
        "ko": "데이터 통계",
    },
    "basic_stats": {
        "zh": "基本统计",
        "en": "Basic Statistics",
        "ko": "기본 통계",
    },
    "missing_check": {
        "zh": "缺失值检查",
        "en": "Missing Values",
        "ko": "결측값 확인",
    },
    "missing_count": {
        "zh": "缺失数",
        "en": "Missing",
        "ko": "결측 수",
    },
    "no_missing": {
        "zh": "无缺失",
        "en": "None",
        "ko": "없음",
    },
    "data_quality": {
        "zh": "数据质量",
        "en": "Data Quality",
        "ko": "데이터 품질",
    },
    "data_quality_good": {
        "zh": "数据质量良好",
        "en": "Data quality is good",
        "ko": "데이터 품질 양호",
    },
    "full_data": {
        "zh": "完整数据",
        "en": "Full Data",
        "ko": "전체 데이터",
    },
    "download_data": {
        "zh": "下载数据 (CSV)",
        "en": "Download Data (CSV)",
        "ko": "데이터 다운로드 (CSV)",
    },
    "upload_or_gen": {
        "zh": "请先上传数据文件或生成合成数据",
        "en": "Please upload a data file or generate synthetic data first",
        "ko": "데이터 파일을 업로드하거나 합성 데이터를 생성해 주세요",
    },
    "high_lt_low": {
        "zh": "High < Low: {} 行",
        "en": "High < Low: {} rows",
        "ko": "High < Low: {} 행",
    },
    "negative_vals": {
        "zh": "负值: {} 个",
        "en": "Negative values: {}",
        "ko": "음수 값: {}개",
    },

    # ====== Tab 3: 模型信息 ======
    "model_info_title": {
        "zh": "模型信息",
        "en": "Model Information",
        "ko": "모델 정보",
    },
    "model_params": {
        "zh": "模型参数",
        "en": "Model Parameters",
        "ko": "모델 파라미터",
    },
    "model_name": {
        "zh": "模型名称",
        "en": "Model Name",
        "ko": "모델 이름",
    },
    "param_count_label": {
        "zh": "参数量",
        "en": "Parameters",
        "ko": "파라미터 수",
    },
    "context_len_label": {
        "zh": "上下文长度",
        "en": "Context Length",
        "ko": "컨텍스트 길이",
    },
    "tokenizer_label": {
        "zh": "Tokenizer",
        "en": "Tokenizer",
        "ko": "토크나이저",
    },
    "inference_backend": {
        "zh": "推理后端",
        "en": "Inference Backend",
        "ko": "추론 백엔드",
    },
    "model_arch": {
        "zh": "模型架构",
        "en": "Model Architecture",
        "ko": "모델 아키텍처",
    },
    "bsq_tokenizer": {
        "zh": "BSQ 分词器",
        "en": "BSQ Tokenizer",
        "ko": "BSQ 토크나이저",
    },
    "bsq_desc_type": {
        "zh": "类型: Binary Spherical Quantization (BSQ)",
        "en": "Type: Binary Spherical Quantization (BSQ)",
        "ko": "유형: Binary Spherical Quantization (BSQ)",
    },
    "bsq_desc_quant": {
        "zh": "量化: 归一化 -> 二值化 -> 缩放",
        "en": "Quantization: Normalize -> Binarize -> Scale",
        "ko": "양자화: 정규화 -> 이진화 -> 스케일링",
    },
    "bsq_desc_encode": {
        "zh": "编码: OHLCV (6维) -> 层次化 token (s1, s2)",
        "en": "Encoding: OHLCV (6-dim) -> Hierarchical token (s1, s2)",
        "ko": "인코딩: OHLCV (6차원) -> 계층적 토큰 (s1, s2)",
    },
    "inference_flow": {
        "zh": "推理流程",
        "en": "Inference Pipeline",
        "ko": "추론 파이프라인",
    },
    "flow_step1": {
        "zh": "编码: OHLCV -> BSQ 量化 -> s1/s2 token",
        "en": "Encode: OHLCV -> BSQ Quantization -> s1/s2 token",
        "ko": "인코드: OHLCV -> BSQ 양자화 -> s1/s2 토큰",
    },
    "flow_step2": {
        "zh": "自回归生成: 逐步预测 s1 token (主解码器)",
        "en": "Autoregressive: Step-by-step s1 token prediction (main decoder)",
        "ko": "자기회귀: 단계별 s1 토큰 예측 (메인 디코더)",
    },
    "flow_step3": {
        "zh": "交叉注意力: 用 s1 token 引导 s2 解码 (依赖感知层)",
        "en": "Cross-Attention: s1 tokens guide s2 decoding (dependency-aware layer)",
        "ko": "크로스 어텐션: s1 토큰이 s2 디코딩 가이드 (의존 인식 레이어)",
    },
    "flow_step4": {
        "zh": "解码: token -> OHLCV 输出",
        "en": "Decode: token -> OHLCV output",
        "ko": "디코드: 토큰 -> OHLCV 출력",
    },

    # ====== Tab 4: 批量预测 ======
    "batch_title": {
        "zh": "批量预测",
        "en": "Batch Prediction",
        "ko": "배치 예측",
    },
    "batch_info": {
        "zh": "可上传多个参数组合进行对比预测",
        "en": "Run multiple parameter combinations for comparison",
        "ko": "여러 파라미터 조합으로 비교 예측을 실행합니다",
    },
    "batch_runs": {
        "zh": "预测轮次",
        "en": "Prediction Rounds",
        "ko": "예측 라운드",
    },
    "batch_run_btn": {
        "zh": "批量运行",
        "en": "Batch Run",
        "ko": "배치 실행",
    },
    "batch_progress": {
        "zh": "批量预测中...",
        "en": "Batch prediction in progress...",
        "ko": "배치 예측 진행 중...",
    },
    "batch_round_done": {
        "zh": "轮次 {}/{} 完成",
        "en": "Round {}/{} complete",
        "ko": "라운드 {}/{} 완료",
    },
    "batch_result_title": {
        "zh": "批量结果对比",
        "en": "Batch Results Comparison",
        "ko": "배치 결과 비교",
    },
    "batch_col_round": {
        "zh": "轮次",
        "en": "Round",
        "ko": "라운드",
    },

    # ====== Tab 5: 历史 ======
    "history_title": {
        "zh": "预测历史",
        "en": "Prediction History",
        "ko": "예측 기록",
    },
    "no_history": {
        "zh": "暂无预测历史记录",
        "en": "No prediction history yet",
        "ko": "예측 기록이 없습니다",
    },
}


def t(key, lang="zh", **kwargs):
    """翻译函数: t("app_title", lang) -> 对应语言的文本

    Args:
        key: STRINGS 中的键
        lang: 语言代码 "zh" / "en" / "ko"
        **kwargs: format 参数，如 t("data_loaded", lang, count=100) -> "已加载数据: 100 行"
    """
    entry = STRINGS.get(key, {})
    text = entry.get(lang, entry.get("zh", key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except (KeyError, IndexError):
            pass
    return text
