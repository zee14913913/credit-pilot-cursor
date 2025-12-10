# test_api.py
# CreditPilot - API测试脚本

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(method, endpoint, data=None, files=None):
    """测试API端点"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            if files:
                response = requests.post(url, files=files)
            else:
                response = requests.post(url, json=data)
        else:
            print(f"✗ 不支持的HTTP方法: {method}")
            return False
        
        if response.status_code == 200:
            print(f"✓ {method} {endpoint} - {response.status_code} OK")
            if response.headers.get('content-type', '').startswith('application/json'):
                print(f"  响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"✗ {method} {endpoint} - {response.status_code} {response.text}")
            return False
    except Exception as e:
        print(f"✗ {method} {endpoint} - 错误: {e}")
        return False

def main():
    print("=" * 60)
    print("CreditPilot API 测试")
    print("=" * 60)
    print()
    
    # 测试根路径
    test_endpoint("GET", "/")
    print()
    
    # 测试Dashboard
    test_endpoint("GET", "/api/dashboard/stats")
    print()
    test_endpoint("GET", "/api/dashboard/upcoming")
    print()
    
    # 测试账单列表
    test_endpoint("GET", "/api/statements")
    print()
    
    # 测试提醒系统
    test_endpoint("GET", "/api/reminders/test")
    print()
    
    print("=" * 60)
    print("所有测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
