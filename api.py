from flask import Flask, request, jsonify
import clip
import torch
from torch import nn
import json
from typing import List, Dict, Union

app = Flask(__name__)

# 加载CLIP模型
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model = clip.load('ViT-B/32', device=device)[0]


def calculate_semantic_score(value1: str, value2: str) -> float:
    """
    计算两个文本的语义对齐得分
    :param value1: 文本1
    :param value2: 文本2
    :return: 语义对齐得分
    """
    text1 = clip.tokenize(value1).to(device)
    text2 = clip.tokenize(value2).to(device)
    with torch.no_grad():
        text1_features = clip_model.encode_text(text1)
        text2_features = clip_model.encode_text(text2)
        similarity = nn.functional.cosine_similarity(text1_features, text2_features).item()
    return similarity


def adjust_weights(attributes: List[Dict], temperature: float = 1.2) -> Dict[str, float]:
    """
    根据语义得分和温度参数调整权重
    :param attributes: 属性列表
    :param temperature: 温度参数
    :return: 调整后的权重字典
    """
    alpha = 2.0
    final_weights = {}
    for attr in attributes:
        base_weight = attr['initial_weight']
        # 这里假设用第一个属性的value作为基准计算语义得分，实际应用中可能更复杂
        semantic_score = calculate_semantic_score(attr['value'], attributes[0]['value'])
        # 将计算结果转换为Tensor类型
        exponent = torch.tensor(alpha * (semantic_score - temperature), device=device)
        adjusted_weight = base_weight * torch.exp(exponent)
        final_weights[attr['value']] = adjusted_weight.item()
    return final_weights


def load_conflicts() -> Dict:
    """
    从conflicts.json文件加载显式冲突数据
    :return: 冲突数据字典
    """
    try:
        with open('conflicts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"conflict_cases": []}


def detect_conflict(attr1: Dict, attr2: Dict, conflicts: Dict) -> bool:
    """
    检测两个属性是否冲突
    :param attr1: 属性1
    :param attr2: 属性2
    :param conflicts: 从conflicts.json加载的冲突数据
    :return: 是否冲突
    """
    # 检查自定义的显式冲突
    combined_name = f"{attr1['value']}+{attr2['value']}"
    for case in conflicts['conflict_cases']:
        if combined_name in case['name']:
            return True

    # 隐式语义冲突（基于CLIP）
    similarity = calculate_semantic_score(attr1['value'], attr2['value'])
    return similarity < 0.3


def validate_request(data):
    """
    验证请求数据的有效性
    :param data: 请求数据
    :return: 验证结果和错误信息
    """
    if 'base_prompt' not in data or 'attributes' not in data:
        return False, {"code": 400, "message": "base_prompt和attributes是必填参数"}
    if not isinstance(data['attributes'], list) or len(data['attributes']) < 2:
        return False, {"code": 400, "message": "attributes必须是至少包含2个属性对象的数组"}
    return True, None


def handle_conflicts(data, conflicts, fallback_strategy, temperature):
    """
    处理属性冲突
    :param data: 请求数据
    :param conflicts: 冲突数据
    :param fallback_strategy: 回退策略
    :param temperature: 温度参数
    :return: 最终权重和冲突报告
    """
    conflict_detected = False
    potential_conflicts = []
    for i in range(len(data['attributes'])):
        for j in range(i + 1, len(data['attributes'])):
            if detect_conflict(data['attributes'][i], data['attributes'][j], conflicts):
                conflict_detected = True
                potential_conflicts.append([data['attributes'][i]['value'], data['attributes'][j]['value']])

    if conflict_detected:
        if fallback_strategy == 'strict':
            return None, {"code": 42201, "message": "显式冲突检测", "solution": ["移除冲突属性"]}
        # 这里简单实现balanced策略，重置为平均权重
        elif fallback_strategy == 'balanced':
            num_attrs = len(data['attributes'])
            avg_weight = 1.0 / num_attrs
            final_weights = {attr['value']: avg_weight for attr in data['attributes']}
        else:
            # creative策略可根据具体需求实现，这里暂不详细处理
            final_weights = adjust_weights(data['attributes'], temperature)
    else:
        final_weights = adjust_weights(data['attributes'], temperature)

    conflict_report = {
        "detected": conflict_detected,
        "potential_conflicts": potential_conflicts
    }
    return final_weights, conflict_report


@app.route('/api/v5/weight/calculate', methods=['POST'])
def calculate_weights():
    try:
        # 检查请求头
        if 'Content-Type' not in request.headers or request.headers['Content-Type'] != 'application/json':
            return jsonify({"code": 400, "message": "Content-Type必须为application/json"}), 400
        if 'X-Api-Key' not in request.headers:
            return jsonify({"code": 400, "message": "缺少X-Api-Key"}), 400

        data = request.get_json()

        # 验证请求数据
        valid, error = validate_request(data)
        if not valid:
            return jsonify(error), 400

        temperature = data.get('temperature', 1.2)
        if temperature < 0.1 or temperature > 5.0:
            temperature = 1.2

        fallback_strategy = data.get('fallback_strategy', 'balanced')
        if fallback_strategy not in ['strict', 'balanced', 'creative']:
            fallback_strategy = 'balanced'

        debug_mode = data.get('debug_mode', False)

        # 加载冲突数据
        conflicts = load_conflicts()

        # 处理冲突
        final_weights, conflict_report = handle_conflicts(data, conflicts, fallback_strategy, temperature)
        if final_weights is None:
            return jsonify(conflict_report), 422

        adjustment_log = []
        # 这里简单记录初始权重，实际应更详细记录调整过程
        initial_weights = {attr['value']: attr['initial_weight'] for attr in data['attributes']}
        adjustment_log.append(f"初始权重: {initial_weights}")

        response = {
            "code": 200,
            "data": {
                "final_weights": final_weights,
                "conflict_report": conflict_report,
                "adjustment_log": adjustment_log
            }
        }
        if debug_mode:
            response["debug_info"] = {
                "processing_time_ms": 0,  # 这里未实际计算时间，需后续补充
                "model_version": "v2.1",
                "gpu_utilization": 0  # 这里未实际获取GPU利用率，需后续补充
            }
        return jsonify(response), 200
    except json.JSONDecodeError:
        return jsonify({"code": 40001, "message": "JSON格式错误", "solution": ["检查括号闭合或逗号分隔"]}), 400


if __name__ == '__main__':
    app.run(debug=True)
    