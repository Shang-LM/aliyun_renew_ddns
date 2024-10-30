import requests

def get_public_ip():
    try:
        # 使用公共API获取公网IP
        response = requests.get("https://openapi.lddgo.net/base/gtool/api/v1/GetIp")
        response.raise_for_status()  # 检查请求是否成功
        ip_data = response.json().get("data")
        return ip_data.get("ip")
    except requests.RequestException as e:
        print("无法获取公网 IP:", e)
        return None

if __name__ == "__main__":
    public_ip = get_public_ip()
    if public_ip:
        print("当前公网 IP:", public_ip)
    else:
        print("获取公网 IP 失败")
