# Kronos BTC Prediction Dashboard

基于 [Kronos](https://github.com/shiyu-coder/Kronos) 金融 K 线预测模型的比特币价格预测工作台。

纯 NumPy 推理，无需 PyTorch/GPU，CPU 即可运行。

## 功能

- **Streamlit 可视化工作台** — 上传 K 线数据，一键预测，交互式 K 线图展示
- **自动获取 BTC 数据** — 从 Binance 公开 API 拉取真实 BTC/USDT 日 K 数据（无需 API Key）
- **预测评估** — 对比预测结果与实际价格，计算 MAE/RMSE/MAPE/方向准确率
- **批量预测** — 多组参数对比测试
- **模型优化计划** — 基于实测结果的 6 大优化方案（Word 文档输出）

## 项目结构

```
kronos-btc-prediction/
├── kronos_dashboard.py       # Streamlit 主界面
├── kronos_numpy/             # 纯 NumPy 推理引擎
│   ├── __init__.py           # KronosEngine 封装
│   ├── model.py              # 模型定义（Transformer + BSQ Tokenizer）
│   ├── inference.py          # 自回归推理
│   └── utils.py              # safetensors 读取工具
├── fetch_btc_data.py         # 从 Binance 获取 BTC 日 K 数据
├── eval_btc_prediction.py    # 预测 vs 实际价格评估
├── download_models.py        # 从 HuggingFace 下载模型权重
├── gen_word_plan.py          # 生成模型优化计划 Word 文档
├── requirements.txt
└── README.md
```

## 快速开始

### 1. 环境要求

- Python 3.10+
- 网络连接（首次需下载模型权重）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 下载模型权重

```bash
python download_models.py
```

模型文件会保存到 `model_cache/` 目录（约 50MB）。

模型来源：
- [NeoQuasar/Kronos-mini](https://huggingface.co/NeoQuasar/Kronos-mini) — 4.1M 参数预测模型
- [NeoQuasar/Kronos-Tokenizer-2k](https://huggingface.co/NeoQuasar/Kronos-Tokenizer-2k) — BSQ 分词器

### 4a. 启动工作台（GUI 模式）

```bash
streamlit run kronos_dashboard.py
```

浏览器自动打开 `http://localhost:8501`，支持以下操作：

- 上传 CSV 数据或生成合成数据（演示用）
- 调节 lookback/预测长度/Temperature 等参数
- 一键运行预测，查看 K 线对比图
- 批量预测对比不同参数组合
- 下载预测结果 CSV

### 4b. 命令行模式（获取数据 + 评估）

```bash
# 获取最近 500 天 BTC 日 K 数据
python fetch_btc_data.py
# 输出: btc_history_500days.csv

# 在工作台生成预测后，用评估脚本对比
python eval_btc_prediction.py
```

## CSV 数据格式

上传的 CSV 文件需包含以下列（列名不区分大小写）：

| 列名 | 必需 | 说明 |
|------|------|------|
| timestamp / date | 推荐 | 日期时间 |
| open | 是 | 开盘价 |
| high | 是 | 最高价 |
| low | 是 | 最低价 |
| close | 是 | 收盘价 |
| volume | 否 | 成交量 |
| amount | 否 | 成交额 |

**最少数据量**：lookback + pred_len 行（默认 200 + 30 = 230 行）。

## 预测参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| lookback | 200 | 使用多少个历史数据点 |
| pred_len | 30 | 预测未来多少步 |
| Temperature | 1.0 | 采样温度，越低越保守 |
| top_p | 0.9 | 核采样概率 |
| greedy | false | 贪心解码（无随机性） |

## 实测评估结果

使用 Kronos-mini 对 BTC/USDT 30 天预测的评估指标：

| 指标 | 值 |
|------|------|
| MAE | $21,104 |
| RMSE | $24,425 |
| MAPE | 30.17% |
| 方向准确率 | 69% |

详见 `kronos_optimization_plan.md` 中的 6 大优化方案。

## 技术栈

- **推理引擎**：纯 NumPy（无 PyTorch 依赖）
- **模型**：Kronos-mini (4.1M params, Decoder-only Transformer)
- **分词器**：BSQ (Binary Spherical Quantization)
- **前端**：Streamlit + Plotly
- **数据源**：Binance 公开 API

## 致谢

- [Kronos](https://github.com/shiyu-coder/Kronos) — 金融 K 线基础模型
- [Binance API](https://api.binance.com/) — 加密货币市场数据
