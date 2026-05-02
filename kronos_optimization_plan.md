# Kronos 模型优化计划

## 问题诊断（基于实测结果）

| 问题 | 数据 |
|------|------|
| 系统性偏高预测 | 29/30 天预测值 > 实际值 |
| MAE | $21,104 |
| MAPE | 30.17% |
| 方向准确率 | 69%（尚可） |
| 根本问题 | 模型输出分布偏移（bias toward higher values） |

---

## 优化方案（按优先级排序）

### 方案一：推理参数调优【最优先，立即可做】

**问题**：Temperature=1.0 导致预测发散，采样偏向高值区间

**行动计划**：
1. 在工作台测试不同 Temperature 参数组合（批量预测功能）
   - T=0.3 / T=0.5 / T=0.7 各跑 5 次，取平均
   - 固定 top_p=0.9，greedy=false
2. 加入**后校准（Post-hoc Calibration）**
   - 用最近 30 天实际数据计算预测偏差系数
   - `calibrated_pred = raw_pred × calibration_factor`
   - calibration_factor = actual_mean / pred_mean

**预期效果**：MAPE 从 30% → 15~20%

---

### 方案二：换更大模型【推荐，效果最明显】

**问题**：mini 版（70M 参数）容量太小，拟合能力不足

**可用模型**（Kronos 系列）：
| 模型 | 参数量 | 上下文 | 预计效果 |
|------|--------|--------|----------|
| Kronos-mini（当前）| ~70M | 1024 | 基线 |
| Kronos-small | ~180M | 2048 | MAPE 降至 15~20% |
| Kronos-base | ~400M | 2048 | MAPE 降至 10~15% |
| Kronos-large | ~1B | 4096 | 最佳效果 |

**行动计划**：
1. 下载 Kronos-small 权重（HuggingFace: NeoQuasar/Kronos-small）
2. 修改 `kronos_numpy/` 支持加载不同尺寸模型
3. 用相同数据对比 mini vs small vs base 的 MAPE

**成本**：下载 ~2GB（small）到 ~8GB（base）

---

### 方案三：滑动窗口回溯测试（Walk-Forward Validation）

**问题**：当前只测了 30 天，样本太少，结论不可靠

**行动计划**：
1. 用 500 天数据做滚动预测测试
   - 窗口 1：用第 1~200 天预测第 201~230 天
   - 窗口 2：用第 1~201 天预测第 202~231 天
   - ... 滚动 200 个窗口
2. 输出综合指标：整体 MAE / MAPE / 方向准确率
3. 分析模型在不同市场状态下的表现（牛市 vs 熊市 vs 震荡）

**输出**：一份完整的回测报告（CSV + 图表）

---

### 方案四：特征工程优化

**问题**：当前只用 OHLCV 5 个特征，信息量不足

**可加入的特征**：
| 特征 | 计算方式 | 作用 |
|------|----------|------|
| RSI(14) | 相对强弱指标 | 捕捉超买超卖 |
| SMA(20) | 20日均线 | 趋势方向 |
| ATR(14) | 真实波幅 | 波动率 |
| 成交量 MA(20) | 成交量均线 | 确认趋势 |
| 收盘价 vs 24h 前 | 短期收益率 | 动量 |

**行动计划**：
1. 修改 `process_dataframe()` 支持额外特征列
2. 修改 `kronos_numpy` 的输入维度（从 6 → 11）
3. 注意：需要重新理解模型是否支持额外特征（可能需要微调）

**风险**：Kronos 预训练只接受 OHLCV，额外特征需要微调或换用其他模型

---

### 方案五：集成预测（Ensemble）

**问题**：单模型预测方差大

**行动计划**：
1. 用不同 random seed 跑多次预测（Temperature sampling）
2. 对预测结果取 median（比 mean 更抗异常值）
3. 或者：mini + small + base 三个模型预测取加权平均

**预期效果**：方向准确率从 69% → 75~80%

---

### 方案六：换用专业金融时序模型（根本解决方案）

**问题**：Kronos 是通用时间序模型，不是专为金融预测设计的

**可考虑的替代方案**：
| 模型 | 类型 | 优点 | 缺点 |
|------|------|------|------|
| **TFT**（Temporal Fusion Transformer）| 专用金融模型 | 内置特征重要性、可解释性好 | 需要训练 |
| **N-BEATS** | 时序专用 | 在 M4 竞赛表现优异 | 需要训练 |
| **PatchTST** | Transformer 时序 | 最新 SOTA | 需要训练 |
| **直接使用 Kronos + 线性回归校准** | 混合方案 | 快速部署 | 效果有限 |

**行动计划（推荐混合方案）**：
1. 保留 Kronos 作为"特征提取器"
2. 用 Kronos 的输出 + 技术指标 作为特征
3. 上层加一个轻量线性回归 / XGBoost 做最终预测
4. 这样不需要重新训练 Kronos，只需要训练上层模型（< 1000 样本即可）

---

## 推荐执行顺序

```
第 1 步（今天）：方案一 → 调 Temperature + 后校准
第 2 步（本周）：方案二 → 下载 small/base 模型对比
第 3 步（本周）：方案三 → 完整回测，确认模型真实能力
第 4 步（下周）：方案六 → 混合模型，上线更可靠的预测
```

---

## 快速见效：后校准实现（方案一详细）

在 `kronos_dashboard.py` 中加入校准功能：

```python
def calibrate_predictions(pred_df, actual_df, method="scalar"):
    """
    用历史实际数据校准预测结果
    method: "scalar" 标量缩放, "quantile" 分位数映射
    """
    if method == "scalar":
        # 简单缩放：pred_calibrated = pred * (actual_mean / pred_mean)
        pred_mean = pred_df['close'].mean()
        actual_mean = actual_df['close'].mean()
        factor = actual_mean / pred_mean
        for col in ['open', 'high', 'low', 'close']:
            pred_df[col] = pred_df[col] * factor
        return pred_df, factor
```

加入后，在预测完成后自动显示"校准后 MAPE"，预计从 30% 降至 15% 左右。

---

## 成功指标（优化目标）

| 指标 | 当前值 | 目标值 |
|------|--------|--------|
| MAPE | 30.17% | < 15% |
| 方向准确率 | 69% | > 75% |
| 系统性偏差 | +$21K（偏高）| < ±$5K |
| 预测区间覆盖率 | 未知 | 80~90%（预测区间） |
