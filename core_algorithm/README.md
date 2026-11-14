# VoiceCare 核心算法

孟浩 - 特征提取与模型开发

## 目录结构

```
core_algorithm/
├── feature_extractor/   # 特征提取模块
├── models/              # 分类模型
├── training/            # 训练脚本
└── evaluation/          # 评估脚本
```

## 开发进度

- ADReSS 数据集基线：🔄 待开始
- 特征提取模块：⏳ 待开发
- 分类模型与 SHAP：⏳ 待开发
- 基线偏离判定：⏳ 待开发

## 算法接口契约

```python
def analyze_features(text: str, timestamps: list) -> dict:
    """
    输入：规整后的文本与时间戳
    输出：指标、SHAP、基线偏离与风险分层
    
    timestamps 格式：
    [{"word": "厨房", "start_ms": 120, "end_ms": 480}]
    """
```

---

开发者：孟浩