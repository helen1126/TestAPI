# TestAPI ��Ŀ�ĵ�

## ��Ŀ����
TestAPI ��һ�����ڴ�������Ȩ�ؼ���ͳ�ͻ���� API ���񡣸÷�����հ���������Ϣ�� JSON ���󣬸���Ԥ��ĳ�ͻ������������ƶȵ�������Ȩ�أ����������յ�Ȩ�ؽ���ͳ�ͻ���档

## ��������
- **���Գ�ͻ���**��֧����ʽ��ͻ����ʽ�����ͻ��⡣
- **Ȩ�ص���**����������÷ֺ��¶Ȳ�����������Ȩ�ء�
- **���˲���**���ṩ `strict`��`balanced` �� `creative` ���ֻ��˲��Դ����ͻ��
- **������**��������ͷ���������ʽ���¶Ȳ�����Χ�Ƚ�����֤����������ϸ�Ĵ�����Ϣ�ͽ��������

## ��Ŀ�ṹ
```
TestAPI/
������ api.py              # API ������
������ test_api.py         # ���Խű�
������ conflicts.json      # ��ͻ���������ļ�
������ examples.json       # ���������ļ�
������ environment.yml     # ���������ļ�
������ .github/
��   ������ workflows/
��       ������ python-package-conda.yml  # GitHub Actions �����ļ�
������ README.md           # ��Ŀ�ĵ�
```

## ��װ������

### ����׼��
ȷ�����Ѿ���װ�� Miniconda �� Anaconda��Ȼ�󴴽����������⻷����
```bash
conda env update --file environment.yml --name test_api
conda activate test_api
```

### ģ�ͼ���
��Ŀʹ�� CLIP ģ�ͽ����������ƶȼ��㣬���� `api.py` ʱ���Զ�����ģ�ͣ�
```bash
python api.py
```

## API �ӿ�

### �ӿڵ�ַ
`POST http://127.0.0.1:5000/api/v5/weight/calculate`

### ����ͷ
- `Content-Type: application/json`
- `X-Api-Key: your_api_key_here`

### ������
������Ϊ JSON ��ʽ��ʾ�����£�
```json
{
    "base_prompt": "δ��������о���",
    "attributes": [
        {
            "name": "���",
            "type": "text",
            "value": "�������",
            "initial_weight": 0.7,
            "constraints": {
                "min_weight": 0.4,
                "max_weight": 0.9,
                "conflict_terms": [
                    "�������",
                    "��������"
                ]
            }
        },
        {
            "name": "����",
            "type": "text",
            "value": "�޺�ƹ�",
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

### ��Ӧ��
��Ӧ��Ϊ JSON ��ʽ��ʾ�����£�
```json
{
    "code": 200,
    "data": {
        "final_weights": {
            "�������": 0.75,
            "�޺�ƹ�": 0.55
        },
        "conflict_report": {
            "detected": false,
            "potential_conflicts": []
        },
        "adjustment_log": [
            "��ʼȨ��: �������(0.7)���޺�ƹ�(0.5)",
            "����ǿ��: �������+0.05��CLIP���ƶ�0.80��",
            "����ǿ��: �޺�ƹ�+0.05��CLIP���ƶ�0.80��"
        ]
    },
    "debug_info": {
        "processing_time_ms": 100,
        "model_version": "v2.1",
        "gpu_utilization": 20
    }
}
```

## ��������
��Ŀ�ṩ�˶�������������洢�� `examples.json` �ļ��С��������� `test_api.py` �ű���ִ����Щ����������
```bash
python test_api.py
```

## ��������
��Ŀʹ�� GitHub Actions ���г������ɣ������ļ�Ϊ `.github/workflows/python-package-conda.yml`��ÿ�δ�������ʱ�����Զ�ִ�����²�����
1. ��װ����
2. �����飨ʹ�� flake8��
3. ���� API �������в��Խű�
