# TestAPI 项目文档

## 项目概述
TestAPI 是一个用于处理属性权重计算和冲突检测的 API 服务。该服务接收包含属性信息的 JSON 请求，根据预设的冲突规则和语义相似度调整属性权重，并返回最终的权重结果和冲突报告。

## 功能特性
- **属性冲突检测**：支持显式冲突和隐式语义冲突检测。
- **权重调整**：根据语义得分和温度参数调整属性权重。
- **回退策略**：提供 `strict`、`balanced` 和 `creative` 三种回退策略处理冲突。
- **错误处理**：对请求头、请求体格式、温度参数范围等进行验证，并返回详细的错误信息和解决方案。

## 项目结构
```
TestAPI/
├── api.py              # API 主程序
├── test_api.py         # 测试脚本
├── conflicts.json      # 冲突规则配置文件
├── examples.json       # 测试用例文件
├── environment.yml     # 环境依赖文件
├── .github/
│   └── workflows/
│       └── python-package-conda.yml  # GitHub Actions 配置文件
└── README.md           # 项目文档
```

## 安装与配置

### 环境准备
确保你已经安装了 Miniconda 或 Anaconda，然后创建并激活虚拟环境：
```bash
conda env update --file environment.yml --name test_api
conda activate test_api
```

### 模型加载
项目使用 CLIP 模型进行语义相似度计算，运行 `api.py` 时会自动加载模型：
```bash
python api.py
```

## API 接口

### 接口地址
`POST http://127.0.0.1:5000/api/v5/weight/calculate`

### 请求头
- `Content-Type: application/json`
- `X-Api-Key: your_api_key_here`

### 请求体
请求体为 JSON 格式，示例如下：
```json
{
    "base_prompt": "未来主义城市景观",
    "attributes": [
        {
            "name": "风格",
            "type": "text",
            "value": "赛博朋克",
            "initial_weight": 0.7,
            "constraints": {
                "min_weight": 0.4,
                "max_weight": 0.9,
                "conflict_terms": [
                    "蒸汽朋克",
                    "极简主义"
                ]
            }
        },
        {
            "name": "光照",
            "type": "text",
            "value": "霓虹灯光",
            "initial_weight": 0.5,
            "constraints": {
                "min_weight": 0.2,
                "max_weight": 0.8
            }
        }
    ],
    "temperature": 1.8,
    "fallback_strategy": "creative",
    "debug_mode": true
}
```

### 响应体
响应体为 JSON 格式，示例如下：
```json
{
    "code": 200,
    "data": {
        "final_weights": {
            "赛博朋克": 0.75,
            "霓虹灯光": 0.55
        },
        "conflict_report": {
            "detected": false,
            "potential_conflicts": []
        },
        "adjustment_log": [
            "初始权重: 赛博朋克(0.7)→霓虹灯光(0.5)",
            "语义强化: 赛博朋克+0.05（CLIP相似度0.80）",
            "语义强化: 霓虹灯光+0.05（CLIP相似度0.80）"
        ]
    },
    "debug_info": {
        "processing_time_ms": 100,
        "model_version": "v2.1",
        "gpu_utilization": 20
    }
}
```

## 测试用例
项目提供了多个测试用例，存储在 `examples.json` 文件中。可以运行 `test_api.py` 脚本来执行这些测试用例：
```bash
python test_api.py
```

## 持续集成
项目使用 GitHub Actions 进行持续集成，配置文件为 `.github/workflows/python-package-conda.yml`。每次代码推送时，会自动执行以下操作：
1. 安装依赖
2. 代码检查（使用 flake8）
3. 启动 API 服务并运行测试脚本
