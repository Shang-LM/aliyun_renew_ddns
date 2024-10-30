# from aliyunsdkcore.client import AcsClient
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest, DescribeDomainsRequest, DescribeDomainRecordsRequest
import json
import requests
import time
import config

# 初始化客户端

ID = config.ID
Secret = config.Secret
RegionId = "cn-hangzhou"  # 根据实际区域替换
DomainNameList =config.DomainNameList
HostNameList = config.HostNameList
Types = "A"

clt = client.AcsClient(ID, Secret, RegionId)

# 获取当前公网IP
def GetLocalIP():
    # 这里可以根据实际情况调用第三方服务获取公网IP，例如使用requests库访问ipify等服务
    try:
        # 使用公共API获取公网IP
        response = requests.get("https://openapi.lddgo.net/base/gtool/api/v1/GetIp")
        response.raise_for_status()  # 检查请求是否成功
        ip_data = response.json().get("data")
        return ip_data.get("ip")
    except requests.RequestException as e:
        print("无法获取公网 IP:", e)
        return None
    
def EditDomainRecord(HostName, RecordId, Types, IP):
    UpdateDomainRecord = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    UpdateDomainRecord.set_accept_format('json')
    UpdateDomainRecord.set_RecordId(RecordId)
    UpdateDomainRecord.set_RR(HostName)
    UpdateDomainRecord.set_Type(Types)
    UpdateDomainRecord.set_TTL('600')
    UpdateDomainRecord.set_Value(IP)
    UpdateDomainRecordJson = json.loads(clt.do_action_with_exception(UpdateDomainRecord))
    print(UpdateDomainRecordJson)

# 记录IP到文件
def RecordIPToFile(IP):
    with open('old_ip.txt', 'a') as file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        file.write(f"{timestamp}: {IP}\n")

# 获取域名信息
def GetAllDomainRecords(DomainNameList, Types, IP):
    for DomainName in DomainNameList:
        DomainRecords = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
        DomainRecords.set_accept_format('json')
        DomainRecords.set_DomainName(DomainName)
        DomainRecords.set_Type(Types)

        DomainRecordsResponse = json.loads(clt.do_action_with_exception(DomainRecords))
        for record in DomainRecordsResponse['DomainRecords']['Record']:
            HostName = record['RR']
            RecordId = record['RecordId']
            RecordIP = record['Value']
            if HostName in HostNameList:
                if RecordIP != IP:
                    EditDomainRecord(HostName, RecordId, Types, IP)
                    RecordIPToFile(RecordIP)  # 记录旧 IP
            else:
                continue



IP = GetLocalIP()

# GetAllDomainRecords(DomainNameList, Types, IP)
print(IP)