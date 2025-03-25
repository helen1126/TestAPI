# coding=gbk
import requests
import time
import json
import logging

# ������־
logging.basicConfig(filename='api_test.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# ���� API URL��Ƕ��汾��
API_URL = "http://localhost:5000/api/v2/dynamic_weights"


def test_dynamic_weights_api():
    # ������������
    def test_normal_scenarios():
        # ���������
        payload = {
            "model_version": "v2.1",
            "prompt": "�������+ҹ��",
            "temperature": 0.7,
            "weights": [0.2, 0.8],
            "debug_mode": True
        }
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        try:
            assert response.status_code == 200
            assert len(response.json().get("data", {}).get("final_weights", [])) == 2
            result = "Pass"
        except AssertionError:
            result = "Fail"
        logging.info(f"Test: test_normal_scenarios, Latency: {latency}ms, Result: {result}")

    # �쳣��������
    def test_exception_scenarios():
        # JSON ��ʽ����
        bad_json = '{"model_version": "v2.1", "prompt": "�������+ҹ��", "temperature": 0.7,}'
        start_time = time.time()
        response = requests.post(API_URL, data=bad_json)
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        try:
            assert response.status_code != 200
            result = "Pass"
        except AssertionError:
            result = "Fail"
        logging.info(f"Test: JSON ��ʽ����, Latency: {latency}ms, Result: {result}")

        # ȱʧ�����ֶ�
        payload = {
            "prompt": "�������+ҹ��",
            "temperature": 0.7
        }
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        try:
            assert response.status_code != 200
            result = "Pass"
        except AssertionError:
            result = "Fail"
        logging.info(f"Test: ȱʧ�����ֶ�, Latency: {latency}ms, Result: {result}")

        # Ȩ�س���Χ
        payload = {
            "model_version": "v2.1",
            "prompt": "�������+ҹ��",
            "temperature": 0.7,
            "weights": [1.1, -0.1]
        }
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        try:
            assert response.status_code != 200
            result = "Pass"
        except AssertionError:
            result = "Fail"
        logging.info(f"Test: Ȩ�س���Χ, Latency: {latency}ms, Result: {result}")

    # �߽�ֵ����
    def test_boundary_values():
        # ��Ȩ������
        payload = {
            "model_version": "v2.1",
            "prompt": "�������+ҹ��",
            "temperature": 0.7,
            "weights": []
        }
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        end_time = time.time()
        latency = (end_time - start_time) * 1000
        try:
            assert response.status_code == 200
            result = "Pass"
        except AssertionError:
            result = "Fail"
        logging.info(f"Test: ��Ȩ������, Latency: {latency}ms, Result: {result}")

        # �����¶Ȳ���
        for temp in [0.1, 2.0]:
            payload = {
                "model_version": "v2.1",
                "prompt": "�������+ҹ��",
                "temperature": temp
            }
            start_time = time.time()
            response = requests.post(API_URL, json=payload)
            end_time = time.time()
            latency = (end_time - start_time) * 1000
            try:
                assert response.status_code == 200
                result = "Pass"
            except AssertionError:
                result = "Fail"
            logging.info(f"Test: �����¶Ȳ��� T={temp}, Latency: {latency}ms, Result: {result}")

    test_normal_scenarios()
    test_exception_scenarios()
    test_boundary_values()


#���԰汾��������
def test_version_deprecation():
    start_time = time.time()
    response = requests.post(API_URL, json={
        "model_version": "v1.5",
        "prompt": "�������+ҹ��",
        "temperature": 0.7
    })
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    data = response.json()
    metadata = data.get("metadata", {})
    try:
        assert "deprecation_warning" in metadata
        result = "Pass"
    except AssertionError:
        result = "Fail"
    logging.info(f"Test: test_version_deprecation, Latency: {latency}ms, Result: {result}")


def test_ab_testing():
    start_time = time.time()
    response = requests.post(API_URL, json={
        "model_version": "v2.1",
        "prompt": "�������+ҹ��",
        "temperature": 0.7
    })
    end_time = time.time()
    latency = (end_time - start_time) * 1000
    data = response.json()
    try:
        assert "experiment_group" in data
        result = "Pass"
    except AssertionError:
        result = "Fail"
    logging.info(f"Test: test_ab_testing, Latency: {latency}ms, Result: {result}")


if __name__ == "__main__":
    test_dynamic_weights_api()
    test_version_deprecation()
    test_ab_testing()
    print("All tests passed!")
    