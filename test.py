import requests
import json
import config

area_code = '4113511000'
area_url = 'https://m.land.naver.com/complex/ajax/complexListByCortarNo?cortarNo=' + area_code


complex_code = '106922'
complex_url = 'https://m.land.naver.com/complex/getComplexArticleList?hscpNo=' + \
    complex_code + '&tradTpCd=A1&order=point_&showR0=N&page=1'

print(area_url)
print(complex_url)
