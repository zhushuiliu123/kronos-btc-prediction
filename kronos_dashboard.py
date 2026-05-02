"""
Kronos 金融 K 线预测工作台
纯 NumPy 推理 + Streamlit 可视化界面
支持中文 / English / 한국어 三语切换
"""

import os
import sys
import io
import time
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# 将当前目录加入 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kronos_numpy import KronosEngine
from i18n import t, LANGUAGES, LANG_NAMES

# ============ 页面配置 ============
st.set_page_config(
    page_title="Kronos Financial Prediction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ 语言初始化 ============
if 'lang' not in st.session_state:
    st.session_state.lang = 'zh'

# ============ 自定义样式 ============
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-card .value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-card .label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-ready { background: #c6f6d5; color: #22543d; }
    .status-loading { background: #fefcbf; color: #744210; }
    .status-error { background: #fed7d7; color: #742a2a; }
</style>
""", unsafe_allow_html=True)

# ============ 辅助函数（必须在调用前定义） ============

def generate_synthetic_data(num_days=600):
    """生成合成 K 线数据"""
    np.random.seed(42)
    price = 100.0
    data = []
    dates = []
    current_date = np.datetime64('2023-01-02')

    for _ in range(num_days):
        while current_date.astype('datetime64[D]').astype(int) % 7 >= 5:
            current_date += np.timedelta64(1, 'D')
        dates.append(current_date)

        daily_return = np.random.normal(0.0003, 0.02)
        price = price * (1 + daily_return)
        open_p = price * (1 + np.random.normal(0, 0.005))
        high_p = max(open_p, price) * (1 + abs(np.random.normal(0, 0.01)))
        low_p = min(open_p, price) * (1 - abs(np.random.normal(0, 0.01)))
        close_p = price
        high_p = max(open_p, close_p, low_p, high_p)
        low_p = min(open_p, close_p, high_p, low_p)
        volume = int(abs(np.random.normal(1000000, 300000)))
        amount = volume * close_p
        data.append([open_p, high_p, low_p, close_p, volume, amount])
        current_date += np.timedelta64(1, 'D')

    df = pd.DataFrame(data, columns=['open', 'high', 'low', 'close', 'volume', 'amount'])
    df['timestamps'] = dates
    return df


def process_dataframe(df):
    """处理上传的 DataFrame"""
    col_map = {}
    for col in df.columns:
        lower = col.lower().strip()
        if lower in ('open', 'high', 'low', 'close', 'volume', 'amount'):
            col_map[col] = lower
        elif lower == 'timestamp' or lower == 'date' or lower == 'datetime' or lower == 'time':
            col_map[col] = 'timestamps'
    df = df.rename(columns=col_map)

    if 'timestamps' in df.columns:
        df['timestamps'] = pd.to_datetime(df['timestamps'], errors='coerce')
    else:
        df['timestamps'] = pd.date_range('2024-01-01', periods=len(df), freq='D')

    for col in ['open', 'high', 'low', 'close', 'volume', 'amount']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    for col in ['volume', 'amount']:
        if col not in df.columns:
            df[col] = 0

    df = df.dropna(subset=['open', 'high', 'low', 'close']).reset_index(drop=True)
    return df


def prepare_input(df, lookback, pred_len):
    """准备模型输入"""
    lb = min(lookback, len(df) - pred_len)
    x_data = df[['open', 'high', 'low', 'close', 'volume', 'amount']].values[:lb]

    x_mean = np.mean(x_data, axis=0)
    x_std = np.std(x_data, axis=0) + 1e-5
    x_norm = (x_data - x_mean) / x_std
    x_norm = np.clip(x_norm, -5, 5)
    x_input = x_norm.reshape(1, lb, 6).astype(np.float32)

    dates_x = df['timestamps'].values[:lb]
    dates_y = df['timestamps'].values[lb:lb + pred_len]

    x_stamps = np.zeros((1, lb, 5), dtype=np.float32)
    for i, dt in enumerate(dates_x):
        dt_obj = pd.Timestamp(dt)
        x_stamps[0, i] = [dt_obj.minute, dt_obj.hour, dt_obj.weekday(), dt_obj.day, dt_obj.month]

    y_stamps = np.zeros((1, pred_len, 5), dtype=np.float32)
    for i in range(pred_len):
        dt_obj = pd.Timestamp(dates_y[i])
        y_stamps[0, i] = [dt_obj.minute, dt_obj.hour, dt_obj.weekday(), dt_obj.day, dt_obj.month]

    return x_input, x_stamps, y_stamps, x_mean, x_std, dates_x, dates_y


def run_prediction(lookback, pred_len, temperature, top_p, greedy):
    """执行预测并显示结果"""
    L = st.session_state.lang
    df = st.session_state.input_data
    engine = st.session_state.engine

    if len(df) < lookback + pred_len:
        st.error(t("data_insufficient", L, need=lookback + pred_len, have=len(df)))
        return

    with st.spinner(t("predicting", L, n=pred_len)):
        progress = st.progress(0, text=t("preparing", L))
        time.sleep(0.3)

        try:
            x_input, x_stamps, y_stamps, x_mean, x_std, dates_x, dates_y = \
                prepare_input(df, lookback, pred_len)

            progress.progress(0.1, text=t("start_inference", L))

            def callback(step, total):
                pct = 0.1 + 0.85 * (step / total)
                progress.progress(pct, text=t("inference_progress", L, step=step, total=total))

            preds = engine.predict(
                x_input, x_stamps, y_stamps,
                pred_len=pred_len,
                max_context=2048,
                clip=5,
                T=0.0 if greedy else temperature,
                top_p=top_p,
                callback=callback
            )

            preds_denorm = preds * x_std + x_mean
            preds_only = preds_denorm[-pred_len:]

            progress.progress(1.0, text=t("generating_result", L))

            pred_df = pd.DataFrame(preds_only, columns=['open', 'high', 'low', 'close', 'volume', 'amount'])
            pred_df['timestamps'] = dates_y[:pred_len]

            actual = df[['open', 'high', 'low', 'close']].values[lookback:lookback + pred_len]
            pred_ohlc = preds_only[:, :4]
            mae = np.mean(np.abs(actual - pred_ohlc))
            rmse = np.sqrt(np.mean((actual - pred_ohlc) ** 2))
            close_mae = np.mean(np.abs(actual[:, 3] - pred_ohlc[:, 3]))

            st.session_state.prediction_result = {
                'pred_df': pred_df,
                'lookback': lookback,
                'pred_len': pred_len,
                'mae': mae,
                'rmse': rmse,
                'close_mae': close_mae,
                'actual_close': actual[:, 3],
                'pred_close': pred_ohlc[:, 3],
            }

            st.session_state.history.append({
                'time': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'params': {'lookback': lookback, 'pred_len': pred_len, 'T': temperature, 'top_p': top_p},
                'metrics': {
                    'mae': float(close_mae),
                    'rmse': float(rmse),
                    'pred_close_mean': float(pred_ohlc[:, 3].mean()),
                    'pred_close_std': float(pred_ohlc[:, 3].std()),
                },
                'pred_df': pred_df.copy(),
            })

            progress.progress(1.0, text=t("done", L))
            time.sleep(0.5)
            progress.empty()

            st.success(t("pred_complete", L, v=close_mae))
            st.rerun()

        except Exception as e:
            st.error(t("pred_failed", L, msg=e))
            raise


def run_prediction_silent(lookback, pred_len, temperature, top_p, greedy):
    """静默预测（批量模式用）"""
    df = st.session_state.input_data
    engine = st.session_state.engine
    lb = min(lookback, len(df) - pred_len)

    x_input, x_stamps, y_stamps, x_mean, x_std, dates_x, dates_y = \
        prepare_input(df, lookback, pred_len)

    preds = engine.predict(
        x_input, x_stamps, y_stamps,
        pred_len=pred_len, max_context=2048, clip=5,
        T=0.0 if greedy else temperature, top_p=top_p
    )

    preds_denorm = preds * x_std + x_mean
    preds_only = preds_denorm[-pred_len:]
    pred_df = pd.DataFrame(preds_only, columns=['open', 'high', 'low', 'close', 'volume', 'amount'])
    pred_df['timestamps'] = dates_y[:pred_len]
    return pred_df


def show_kline(df, title=None, show_volume=True):
    """显示 K 线图"""
    L = st.session_state.lang
    if title is None:
        title = t("kline_chart", L)

    fig = go.Figure(data=[go.Candlestick(
        x=df['timestamps'],
        open=df['open'], high=df['high'],
        low=df['low'], close=df['close'],
        increasing_line_color='#ef5350',
        decreasing_line_color='#26a69a',
        name=t("legend_kline", L)
    )])

    if show_volume and 'volume' in df.columns:
        colors = ['#ef5350' if c >= o else '#26a69a'
                 for c, o in zip(df['close'], df['open'])]
        fig.add_trace(go.Bar(
            x=df['timestamps'], y=df['volume'],
            marker_color=colors, opacity=0.3,
            yaxis='y2', name=t("volume", L)
        ))

    fig.update_layout(
        title=title,
        template='plotly_white',
        height=500,
        xaxis_rangeslider_visible=False,
        yaxis=dict(title=t("price", L)),
        yaxis2=dict(overlaying='y', side='right', title=t("volume", L), showgrid=False),
    )
    st.plotly_chart(fig, use_container_width=True)


def show_prediction_results():
    """展示预测结果"""
    L = st.session_state.lang
    result = st.session_state.prediction_result
    pred_df = result['pred_df']
    lookback = result['lookback']
    pred_len = result['pred_len']

    st.divider()
    st.subheader(f"🎯 {t('pred_result', L)}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("MAE (Close)", f"{result['close_mae']:.4f}")
    with col2:
        st.metric("MAE (All OHLC)", f"{result['mae']:.4f}")
    with col3:
        st.metric("RMSE", f"{result['rmse']:.4f}")
    with col4:
        st.metric(t("pred_steps", L), t("pred_steps_unit", L, n=pred_len))

    df = st.session_state.input_data
    hist_df = df[['timestamps', 'open', 'high', 'low', 'close']].iloc[:lookback].copy()

    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=hist_df['timestamps'],
        open=hist_df['open'], high=hist_df['high'],
        low=hist_df['low'], close=hist_df['close'],
        increasing_line_color='#ef5350',
        decreasing_line_color='#26a69a',
        name=t("legend_historical", L)
    ))

    fig.add_trace(go.Candlestick(
        x=pred_df['timestamps'],
        open=pred_df['open'], high=pred_df['high'],
        low=pred_df['low'], close=pred_df['close'],
        increasing_line_color='#42a5f5',
        decreasing_line_color='#1e88e5',
        name=t("legend_predicted", L)
    ))

    if lookback + pred_len <= len(df):
        actual_df = df[['timestamps', 'open', 'high', 'low', 'close']].iloc[lookback:lookback+pred_len]
        fig.add_trace(go.Candlestick(
            x=actual_df['timestamps'],
            open=actual_df['open'], high=actual_df['high'],
            low=actual_df['low'], close=actual_df['close'],
            increasing_line_color='#ffa726',
            decreasing_line_color='#ff7043',
            name=t("legend_actual", L),
            opacity=0.5
        ))

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=actual_df['timestamps'], y=actual_df['close'],
            mode='lines+markers', name=t("legend_actual_close", L),
            line=dict(color='#ff7043', width=2)
        ))
        fig2.add_trace(go.Scatter(
            x=pred_df['timestamps'], y=pred_df['close'],
            mode='lines+markers', name=t("legend_pred_close", L),
            line=dict(color='#1e88e5', width=2, dash='dash')
        ))
        fig2.update_layout(
            title=t("close_compare_title", L),
            template='plotly_white',
            height=400,
            xaxis_title=t("time", L),
            yaxis_title=t("price", L)
        )
        st.plotly_chart(fig2, use_container_width=True)

    fig.update_layout(
        title=t("kline_result_title", L, h=lookback, p=pred_len),
        template='plotly_white',
        height=600,
        xaxis_rangeslider_visible=True,
        xaxis_title=t("time", L),
        yaxis_title=t("price", L)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"📋 {t('pred_data', L)}")
    st.dataframe(pred_df, use_container_width=True, height=300)

    col1, col2 = st.columns(2)
    with col1:
        csv_buf = io.StringIO()
        pred_df.to_csv(csv_buf, index=False)
        st.download_button(
            f"📥 {t('download_pred', L)}",
            csv_buf.getvalue(),
            f"kronos_prediction_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "text/csv"
        )


# ============ 初始化 session state ============
if 'engine' not in st.session_state:
    st.session_state.engine = KronosEngine()
    st.session_state.engine_loaded = False
    st.session_state.prediction_result = None
    st.session_state.input_data = None
    st.session_state.pred_df = None
    st.session_state.history = []

# ============ 侧边栏 ============
L = st.session_state.lang

with st.sidebar:
    # ---- 语言选择 ----
    lang_options = list(LANGUAGES.keys())
    selected_label = st.radio(
        "🌐 " + t("language_label", L),
        lang_options,
        index=lang_options.index("中文") if L == "zh" else (lang_options.index("English") if L == "en" else lang_options.index("한국어")),
        horizontal=True,
    )
    st.session_state.lang = LANGUAGES[selected_label]
    L = st.session_state.lang

    st.title(f"⚙️ {t('sidebar_title', L)}")
    st.divider()

    # ---- 模型状态 ----
    st.subheader(f"🤖 {t('model_status', L)}")
    if st.session_state.engine_loaded:
        info = st.session_state.engine.info
        st.success(f"✅ {t('model_loaded', L, name=info['model'])}")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(t("param_count", L), info['params'])
        with col2:
            st.metric(t("context_length", L), f"{info['context_length']}")
        st.caption(f"{t('backend', L)}: {info['backend']}")
    else:
        st.warning(f"⏳ {t('model_not_loaded', L)}")

    if st.button(f"🔄 {t('load_model_btn', L)}", type="primary", use_container_width=True):
        with st.spinner(t("loading_model", L)):
            try:
                st.session_state.engine.load()
                st.session_state.engine_loaded = True
                st.success(t("model_load_success", L))
                st.rerun()
            except Exception as e:
                st.error(t("model_load_fail", L, msg=e))

    st.divider()

    # ---- 数据上传 ----
    st.subheader(f"📁 {t('data_upload', L)}")
    uploaded_file = st.file_uploader(
        t("upload_csv", L),
        type=['csv'],
        help=t("upload_csv_help", L)
    )

    # 合成数据按钮
    if st.button(f"🎲 {t('gen_synthetic_btn', L)}", use_container_width=True):
        with st.spinner(t("generating", L)):
            st.session_state.input_data = generate_synthetic_data()
            st.success(t("synthetic_done", L, n=len(st.session_state.input_data)))

    st.divider()

    # ---- 预测参数 ----
    st.subheader(f"🎛️ {t('pred_params', L)}")
    lookback = st.slider(t("lookback_window", L), 50, 1000, 200, 10,
                         help=t("lookback_help", L))
    pred_len = st.number_input(t("pred_length", L), 1, 120, 30,
                               help=t("pred_length_help", L))
    temperature = st.slider("Temperature", 0.1, 2.0, 1.0, 0.1,
                            help=t("temperature_help", L))
    top_p = st.slider("Top-p", 0.1, 1.0, 0.9, 0.05,
                      help=t("top_p_help", L))
    greedy = st.checkbox(t("greedy_decode", L), value=False,
                         help=t("greedy_help", L))

    st.divider()

    # ---- 运行预测 ----
    run_btn = st.button(f"🔮 {t('run_pred_btn', L)}", type="primary",
                        use_container_width=True,
                        disabled=not st.session_state.engine_loaded)

    st.divider()
    st.caption(t("version", L))
    st.caption(t("backend_info", L))


# ============ 主界面 ============
L = st.session_state.lang
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"📈 {t('tab_prediction', L)}",
    f"📁 {t('tab_data_mgmt', L)}",
    f"🤖 {t('tab_model_info', L)}",
    f"📊 {t('tab_batch', L)}",
    f"📜 {t('tab_history', L)}",
])


# ============ Tab 1: 预测 ============
with tab1:
    st.header(f"📈 {t('kline_prediction', L)}")

    # 处理文件上传
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            df = process_dataframe(df)
            st.session_state.input_data = df
            st.success(t("data_loaded", L, n=len(df)))
        except Exception as e:
            st.error(t("data_load_fail", L, msg=e))

    # 显示输入数据
    if st.session_state.input_data is not None:
        df = st.session_state.input_data
        st.subheader(f"📊 {t('input_preview', L)}")

        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric(t("data_rows", L), len(df))
        with col_info2:
            if 'timestamps' in df.columns:
                st.metric(t("time_range", L),
                         f"{df['timestamps'].min().strftime('%Y-%m-%d')} ~ {df['timestamps'].max().strftime('%Y-%m-%d')}")
            else:
                st.metric(t("time_range", L), "N/A")
        with col_info3:
            close_range = df['close'].max() - df['close'].min()
            st.metric(t("close_volatility", L), f"{close_range:.2f}")

        st.dataframe(df.head(50), use_container_width=True, height=300)

        # 历史数据 K 线图
        st.subheader(f"🕯️ {t('history_kline', L)}")
        show_kline(df, title=t("history_kline_title", L))

    # 运行预测
    if run_btn and st.session_state.input_data is not None:
        run_prediction(lookback, pred_len, temperature, top_p, greedy)

    # 显示预测结果
    if st.session_state.prediction_result is not None:
        show_prediction_results()


# ============ Tab 2: 数据管理 ============
with tab2:
    st.header(f"📁 {t('data_mgmt_title', L)}")
    if st.session_state.input_data is not None:
        df = st.session_state.input_data
        st.subheader(t("data_stats", L))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**{t('basic_stats', L)}**")
            st.dataframe(df[['open', 'high', 'low', 'close', 'volume']].describe())

        with col2:
            st.write(f"**{t('missing_check', L)}**")
            missing = df.isnull().sum()
            st.dataframe(missing[missing > 0].to_frame(t('missing_count', L)) if missing.sum() > 0
                        else pd.DataFrame({t('missing_count', L): [t('no_missing', L)]}))

        with col3:
            st.write(f"**{t('data_quality', L)}**")
            ohlc = df[['open', 'high', 'low', 'close']]
            issues = []
            bad_hl = (df['high'] < df['low']).sum()
            if bad_hl > 0:
                issues.append(t("high_lt_low", L, n=bad_hl))
            neg_vals = (ohlc < 0).sum().sum()
            if neg_vals > 0:
                issues.append(t("negative_vals", L, n=neg_vals))
            if issues:
                for issue in issues:
                    st.warning(issue)
            else:
                st.success(t("data_quality_good", L))

        st.subheader(t("full_data", L))
        st.dataframe(df, use_container_width=True)

        # 下载按钮
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            f"📥 {t('download_data', L)}",
            csv_buffer.getvalue(),
            "kronos_data.csv",
            "text/csv"
        )
    else:
        st.info(t("upload_or_gen", L))


# ============ Tab 3: 模型信息 ============
with tab3:
    st.header(f"🤖 {t('model_info_title', L)}")

    info = st.session_state.engine.info

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t("model_params", L))
        model_info_data = {
            t("model_name", L): info['model'],
            t("param_count_label", L): info['params'],
            t("context_len_label", L): str(info['context_length']),
            t("tokenizer_label", L): info['tokenizer'],
            t("inference_backend", L): info['backend'],
        }
        for k, v in model_info_data.items():
            st.write(f"**{k}**: {v}")

    with col2:
        st.subheader(t("model_arch", L))
        st.markdown("""
        ```
        Kronos-mini (Decoder-only Transformer)
        ├── HierarchicalEmbedding
        │   ├── emb_s1 (1024 vocab, 256 dim)
        │   ├── emb_s2 (1024 vocab, 256 dim)
        │   └── fusion_proj (512 -> 256)
        ├── TemporalEmbedding
        │   └── minute/hour/weekday/day/month
        ├── 4x TransformerBlock
        │   ├── RMSNorm + Self-Attention (4 heads, 64 dim)
        │   └── RMSNorm + SwiGLU FFN
        ├── DependencyAwareLayer (Cross-Attention)
        ├── RMSNorm
        └── DualHead
            ├── proj_s1 (256 -> 1024)
            └── proj_s2 (256 -> 1024)
        ```
        """)

    st.subheader(t("bsq_tokenizer", L))
    st.markdown(f"""
    - **{t('bsq_desc_type', L)}**
    - **codebook_dim**: 20 (s1_bits=10, s2_bits=10)
    - **词汇量**: s1=1024 (2^10), s2=1024 (2^10)
    - **{t('bsq_desc_quant', L)}**
    - **{t('bsq_desc_encode', L)}**
    """)

    st.subheader(t("inference_flow", L))
    st.markdown(f"""
    1. **{t('flow_step1', L)}**
    2. **{t('flow_step2', L)}**
    3. **{t('flow_step3', L)}**
    4. **{t('flow_step4', L)}**
    """)


# ============ Tab 4: 批量预测 ============
with tab4:
    st.header(f"📊 {t('batch_title', L)}")
    st.info(t("batch_info", L))

    n_runs = st.number_input(t("batch_runs", L), 1, 10, 3)

    if st.button(f"🚀 {t('batch_run_btn', L)}", type="primary"):
        if st.session_state.input_data is None or not st.session_state.engine_loaded:
            st.error(t("upload_or_gen", L))
        else:
            results = []
            progress = st.progress(0, text=t("batch_progress", L))
            for r in range(n_runs):
                T = np.random.uniform(0.5, 1.5)
                result = run_prediction_silent(lookback, pred_len, T, 0.9, greedy)
                results.append({
                    t("batch_col_round", L): r + 1,
                    "Temperature": round(T, 2),
                    "Pred_Close": round(result['close'].mean(), 2),
                    "Pred_High": round(result['high'].max(), 2),
                    "Pred_Low": round(result['low'].min(), 2),
                })
                progress.progress((r + 1) / n_runs, text=t("batch_round_done", L, cur=r+1, total=n_runs))

            progress.empty()
            st.subheader(t("batch_result_title", L))
            st.dataframe(pd.DataFrame(results), use_container_width=True)


# ============ Tab 5: 历史 ============
with tab5:
    st.header(f"📜 {t('history_title', L)}")

    if st.session_state.history:
        for i, record in enumerate(reversed(st.session_state.history)):
            with st.expander(f"#{len(st.session_state.history) - i} | {record['time']} | "
                           f"lookback={record['params']['lookback']} | "
                           f"pred_len={record['params']['pred_len']}"):
                cols = st.columns(4)
                with cols[0]:
                    st.metric("MAE (Close)", f"{record['metrics']['mae']:.4f}")
                with cols[1]:
                    st.metric("RMSE", f"{record['metrics']['rmse']:.4f}")
                with cols[2]:
                    st.metric("Pred Close Mean", f"{record['metrics']['pred_close_mean']:.2f}")
                with cols[3]:
                    st.metric("Pred Close Std", f"{record['metrics']['pred_close_std']:.2f}")

                if 'pred_df' in record:
                    st.dataframe(record['pred_df'], use_container_width=True)
    else:
        st.info(t("no_history", L))
