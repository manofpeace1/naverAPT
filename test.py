import requests
import json

complex_code = '108126'

complex_url = 'https://m.land.naver.com/complex/getComplexArticleList?hscpNo=' + \
    complex_code + '&tradTpCd=A1&order=point_&showR0=N&page=1'

area_code = '4117310300'
area_url = 'https://m.land.naver.com/complex/ajax/complexListByCortarNo?cortarNo=' + area_code


send_request = requests.get(area_url)

json_response = json.dumps(send_request.json(), ensure_ascii=False, indent=4)


print(json_response)
