import requests
import json

resp = requests.Session()
payload = {
    ------WebKitFormBoundarylPNRhtnHXCTBliTp
    Content - Disposition: form - data;
    name = "file";
    filename = ""
    Content - Type: application / octet - stream

    ------WebKitFormBoundarylPNRhtnHXCTBliTp
    Content - Disposition: form - data;
    name = "keyword"

    你是个傻逼吗
    ------WebKitFormBoundarylPNRhtnHXCTBliTp - -
}
resp = resp.post(url='http://www.picdata.cn/index.php', post=payload)
