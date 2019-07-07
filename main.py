import requests
import json

# "cortarNo" : "4117310300" (지역 id)
# "hscpNo" : "26428" (건물 id)
# "hscpNm" : "경남" (건물 브랜드)
# "hscpTypeNm" : "아파트" (건물 타입)
# "dealCnt" : '매매' 건 수
# "leaseCnt" : '전세' 건 수
# "rentCnt" : '월세' 건 수
# "lat" : "37.389553" (경도)
# "lng" : "126.974261" (위도)

base_url = 'https://m.land.naver.com/complex/ajax/complexListByCortarNo?cortarNo='

# 평촌동
code_area = '4117310300'

list_area_apt = base_url + code_area


send_request = requests.get(list_area_apt)
json_response = send_request.json()['result']

list_code_apt = []
list_apt_details = []

i = 0
for each_apt in json_response:
    code_apt = json_response[i]['hscpNo']
    if json_response[i]['cortarNo'] == code_area:
        list_code_apt.append(code_apt)
    i += 1


def get_apt_details(each_code, page):
    global apt_details
    url = 'https://m.land.naver.com/complex/getComplexArticleList?hscpNo=' + \
        each_code + '&tradTpCd=B1&order=point_&showR0=N&page=' + str(page)
    apt_details = requests.get(url).json()


for each_code in list_code_apt:
    page = 1
    get_apt_details(each_code, page)

    while apt_details['result']['totAtclCnt'] != 0:

        result_list = apt_details['result']['list']
        i = 0
        for result in result_list:
            list_apt_details.append({
                "apt_id": result_list[i]['atclNo'],
                "apt_name": result_list[i]['atclNm'],
                "apt_number": result_list[i]['bildNm'],
                "apt_price": result_list[i]['prcInfo'].replace(',', ''),
                "apt_space": result_list[i]['spc2'],
            })
            i += 1

        if apt_details['result']['moreDataYn'] == 'Y':
            page += 1
            get_apt_details(each_code, page)
        elif apt_details['result']['moreDataYn'] == 'N':
            break


f = open('/Users/manofpeace/Desktop/result.csv', 'x')

f.write(
    'apt_id,' +
    'apt_name,' +
    'apt_number,' +
    'apt_price,' +
    'apt_space' +
    '\n'
)

i = 0
for item in list_apt_details:
    f.write(
        f'{list_apt_details[i]["apt_id"]},' +
        f'{list_apt_details[i]["apt_name"]},' +
        f'{list_apt_details[i]["apt_number"]},' +
        f'{list_apt_details[i]["apt_price"]},' +
        f'{list_apt_details[i]["apt_space"]}' +
        '\n'
    )
    i += 1

f.close()
