import requests
import json
import config

area_code = '1162010100'
area_url = 'https://m.land.naver.com/complex/ajax/complexListByCortarNo?cortarNo=' + area_code


complex_code = '18550'
complex_url = 'https://m.land.naver.com/complex/getComplexArticleList?hscpNo=' + \
    complex_code + '&tradTpCd=A1&order=point_&showR0=N&page=1'

print(area_url)
print(complex_url)


def collect_apt_code():
    global list_apt_code
    get_list_area_apt = 'https://m.land.naver.com/complex/ajax/complexListByCortarNo?cortarNo=' + area_code
    send_request = requests.get(get_list_area_apt)
    json_response = send_request.json()['result']
    list_apt_code = []

    i = 0
    for item in json_response:
        apt_code = json_response[i]['hscpNo']
        if (json_response[i]['cortarNo'] == area_code) and (json_response[i]['leaseCnt'] > 0):
            list_apt_code.append(apt_code)
        i += 1

    print(list_apt_code)


def collect_apt_details():

    def get_apt_details(apt_code, page):
        global apt_details
        get_list_apt_details = 'https://m.land.naver.com/complex/getComplexArticleList?hscpNo=' + \
            apt_code + '&tradTpCd=B1&order=point_&showR0=N&page=' + str(page)
        apt_details = requests.get(get_list_apt_details).json()

    global list_apt_details
    list_apt_details = []

    for apt_code in list_apt_code:
        page = 1
        get_apt_details(apt_code, page)

        while apt_details['result']['totAtclCnt'] > 0:
            result_list = apt_details['result']['list']
            i = 0
            for item in result_list:
                f = open(config.folder_path + f'test{i}.json', 'x')
                json_pretty = json.dumps(result_list)
                f.write(json_pretty)
                f.close()
                apt_number = result_list[i]['bildNm'] if 'bildNm' in result_list[i] else ''
                list_apt_details.append({
                    # "apt_id": result_list[i]['atclNo'],
                    "apt_name": result_list[i]['atclNm'],
                    "apt_number": apt_number,

                    # "apt_direction": result_list[i]['direction'],
                    # "apt_price": result_list[i]['prcInfo'].replace(',', ''),
                    # "apt_space1_sq": result_list[i]['spc1'],
                    # "apt_space2_sq": result_list[i]['spc2'],
                    # "apt_space1_py": "%.2f" % (float(result_list[i]['spc1']) / 3.3),
                    # "apt_space2_py": "%.2f" % (float(result_list[i]['spc2']) / 3.3),
                    # "apt_space_percent": "%.2f" % ((float(result_list[i]['spc2']) / float(result_list[i]['spc1'])) * 100),
                    # "apt_floor": result_list[i]['flrInfo'],
                })
                i += 1

            if apt_details['result']['moreDataYn'] == 'Y':
                page += 1
                get_apt_details(apt_code, page)
            elif apt_details['result']['moreDataYn'] == 'N':
                break
    print(list_apt_details)


collect_apt_code()
collect_apt_details()
