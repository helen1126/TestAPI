import requests
import json
import logging

# 配置日志记录
logging.basicConfig(
    filename="test_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# 接口的 URL
url = "http://127.0.0.1:5000/api/v5/weight/calculate"

# 请求头，包含 Content-Type 和 X-Api-Key
headers = {"Content-Type": "application/json", "X-Api-Key": "your_api_key_here"}

wrong_headers_1 = {"Content-Type": "application/json"}

wrong_headers_2 = {"X-Api-Key": "your_api_key_here"}

standard_input = {
    "info": "1.normal scenarios",
    "input_data": {
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
                    "conflict_terms": ["蒸汽朋克", "极简主义"],
                },
            },
            {
                "name": "光照",
                "type": "text",
                "value": "霓虹灯光",
                "initial_weight": 0.5,
                "constraints": {"min_weight": 0.2, "max_weight": 0.8},
            },
        ],
        "temperature": 1.8,
        "fallback_strategy": "creative",
        "debug_mode": True,
    },
}




def run_tests():
    try:
        # 从 examples.json 文件中读取测试用例
        with open("examples.json", "r", encoding="utf-8") as f:
            test_data = json.load(f)

        for example in test_data["examples"]:
            info = example["info"]
            input_data = example["input_data"]

            try:
                # 发送 POST 请求
                response = requests.post(url, headers=headers, json=input_data)
                response.raise_for_status()
                result = response.json()
                logging.info(f"测试用例 {info} 的响应结果: {response.text}")
            except requests.RequestException as e:
                logging.error(
                    f"测试用例 {info} 发送请求时出错: {e} Output: {response.text}"
                )
            except json.JSONDecodeError as e:
                logging.error(
                    f"测试用例 {info} 解析响应 JSON 时出错: {e} Output: {response.text}"
                )
    except FileNotFoundError:
        logging.error("未找到 examples.json 文件，请确保文件存在。")
        print("未找到 examples.json 文件，请确保文件存在。")
    except KeyError:
        logging.error("examples.json 文件格式有误，请检查是否包含 'examples' 字段。")
        print("examples.json 文件格式有误，请检查是否包含 'examples' 字段。")
def other_examples():
    # 测试无请求头

    info = "lack content-type"
    try:
        # 发送 POST 请求
        response = requests.post(url, json=standard_input)
        response.raise_for_status()
        result = response.json()
        logging.info(f"测试用例 {info} 的响应结果: {response.text}")
    except requests.RequestException as e:
        logging.error(f"测试用例 {info} 发送请求时出错: {e} Output: {response.text}")
    except json.JSONDecodeError as e:
        logging.error(
            f"测试用例 {info} 解析响应 JSON 时出错: {e} Output: {response.text}"
        )

    # 测试缺失content-type的请求头

    info = "lack content-type"
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=wrong_headers_1, json=standard_input)
        response.raise_for_status()
        result = response.json()
        logging.info(f"测试用例 {info} 的响应结果: {response.text}")
    except requests.RequestException as e:
        logging.error(f"测试用例 {info} 发送请求时出错: {e} Output: {response.text}")
    except json.JSONDecodeError as e:
        logging.error(
            f"测试用例 {info} 解析响应 JSON 时出错: {e} Output: {response.text}"
        )

    # 测试缺少x-api-key的请求头

    info = "lack x-api-key"
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=wrong_headers_2, json=standard_input)
        response.raise_for_status()
        result = response.json()
        logging.info(f"测试用例 {info} 的响应结果: {response.text}")
    except requests.RequestException as e:
        logging.error(f"测试用例 {info} 发送请求时出错: {e} Output: {response.text}")
    except json.JSONDecodeError as e:
        logging.error(
            f"测试用例 {info} 解析响应 JSON 时出错: {e} Output: {response.text}"
        )


if __name__ == "__main__":
    run_tests()
    other_examples()
