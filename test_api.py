import requests
import json
import logging

# 配置日志记录
logging.basicConfig(filename='test_api.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 接口的 URL
url = 'http://127.0.0.1:5000/api/v5/weight/calculate'
# 请求头，包含 Content-Type 和 X-Api-Key
headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': 'your_api_key_here'
}


def run_tests():
    try:
        # 从 examples.json 文件中读取测试用例
        with open('examples.json', 'r', encoding='utf-8') as f:
            test_data = json.load(f)

        for example in test_data['examples']:
            info = example['info']
            input_data = example['input_data']
            print(f"开始执行测试用例: {info}")

            try:
                # 发送 POST 请求
                response = requests.post(url, headers=headers, json=input_data)
                response.raise_for_status()
                result = response.json()
                logging.info(f"测试用例 {info} 的响应结果: {response.text}")
                print(f"测试用例 {info} 的响应结果:")
                print(json.dumps(result, indent=2))
            except requests.RequestException as e:
                logging.error(f"测试用例 {info} 发送请求时出错: {e} Output: {response.text}")
                print(f"测试用例 {info} 发送请求时出错: {e}")
            except json.JSONDecodeError as e:
                logging.error(f"测试用例 {info} 解析响应 JSON 时出错: {e} Output: {response.text}")
                print(f"测试用例 {info} 解析响应 JSON 时出错: {e}")
    except FileNotFoundError:
        logging.error("未找到 examples.json 文件，请确保文件存在。")
        print("未找到 examples.json 文件，请确保文件存在。")
    except KeyError:
        logging.error("examples.json 文件格式有误，请检查是否包含 'examples' 字段。")
        print("examples.json 文件格式有误，请检查是否包含 'examples' 字段。")


if __name__ == "__main__":
    run_tests()
    