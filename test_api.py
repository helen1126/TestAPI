import requests
import json
import time
import logging

# 配置日志
logging.basicConfig(
    filename="test_api.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# API地址
API_URL = "http://127.0.0.1:5000/process"


def test_api():
    '''
        测试接口
    '''
    # 读取测试数据
    with open("examples.json", "r", encoding="gbk") as f:
        example_data = json.load(f)

    for example in example_data['examples']:
        # 获取测试信息
        info = example['info']
        data = example['input_data']
        start_time = time.time()
        response = requests.post(API_URL, json=data)
        end_time = time.time()
        letancy = (end_time - start_time) * 1000

        try:
            assert response.status_code == 200
            assert len(response.json().get("data", {}).get("final_weights", [])) == 2
            result = "Pass"
        except AssertionError:
            result = "Fail"

        logging.info(
            f"Test: {info}, Result: {result}, Letancy: {letancy}ms, Output: {response.text}"
        )

def test_wrong_json():
    '''
        测试错误的json
    '''
    example = ('{"model_version": "v2.1", "prompt": "赛博朋克+夜景", "temperature": 0.7,}')
    info = "11.worng json"
    start_time = time.time()
    response = requests.post(API_URL, json=example)
    end_time = time.time()
    letancy = (end_time - start_time) * 1000
    
    try:
        assert response.status_code == 200
        assert len(response.json().get("data", {}).get("final_weights", [])) == 2
        result = "Pass"
    except AssertionError:
        result = "Fail"
    logging.info(
        f"Test: {info}, Result: {result}, Letancy: {letancy}ms, Output: {response.text}"
    )

if __name__ == "__main__":
    print("Test start")
    logging.info("Test start")

    test_api()
    test_wrong_json()

    print("Test finished")
    logging.info("Test finished")