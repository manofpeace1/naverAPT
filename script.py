import requests
import config


def select_area_code():
    global area_name, area_code
    code_of_areas = {
        "1": ['안양-평촌동', '4117310300'],
        "2": ['관악-봉천동', '1162010100'],
        "3": ['분당-백현동', '4113511000'],
        "4": ['분당-수내동', '4113510200'],
        "5": ['분당-야탑동', '4113510700'],
        "6": ['분당-서현동', '4113510500'],
        "7": ['수지-상현동', '4146510700'],
        "8": ['수지-동천동', '4146510300'],
        "9": ['수지-죽전동', '4146510200'],
    }

    print('\n' + '===== 네이버 부동산 데이터 긁어오기 =====')
    print('\n' + '지역을 선택하세요' + '\n')
    for item in code_of_areas:
        print(f'[{item}] {code_of_areas[item][0]} {code_of_areas[item][1]}')

    user_input = input(f'\n>>> ')
    area_name = code_of_areas[user_input][0]
    area_code = code_of_areas[user_input][1]


def select_sale_type():
    global user_sale_name, user_sale_code, user_sale_type
    sale_types = {
        "1": ['전세', 'B1', 'leaseCnt'],
        "2": ['월세', 'B2', 'rentCnt'],
        "3": ['매매', 'A1', 'dealCnt'],
    }
    print('\n' + '매물 종류를 선택하세요' + '\n')
    for item in sale_types:
        print(f'[{item}] {sale_types[item][0]} {sale_types[item][1]}')
    user_input = input(f'\n>>> ')
    user_sale_name = sale_types[user_input][0]
    user_sale_code = sale_types[user_input][1]
    user_sale_type = sale_types[user_input][2]


def collect_apt_code():
    global list_apt_code
    get_list_area_apt = 'https://m.land.naver.com/complex/ajax/complexListByCortarNo?cortarNo=' + area_code
    send_request = requests.get(get_list_area_apt)
    json_response = send_request.json()['result']
    list_apt_code = []

    i = 0
    for item in json_response:
        apt_code = json_response[i]['hscpNo']
        if (json_response[i]['cortarNo'] == area_code) and (json_response[i][user_sale_type] > 0):
            list_apt_code.append(apt_code)
        i += 1


def collect_apt_details():

    def get_apt_details(apt_code, page):
        global apt_details
        get_list_apt_details = 'https://m.land.naver.com/complex/getComplexArticleList?hscpNo=' + \
            apt_code + f'&tradTpCd={user_sale_code}' + \
            '&order=point_&showR0=N&page=' + str(page)
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
                apt_number = result_list[i]['bildNm'] if 'bildNm' in result_list[i] else ''
                apt_description = result_list[i]['atclFetrDesc'] if 'atclFetrDesc' in result_list[i] else ''
                apt_confirm_date = result_list[i]['cfmYmd'] if 'cfmYmd' in result_list[i] else ''

                list_apt_details.append({
                    "apt_sale_type": result_list[i]['tradTpNm'],
                    "apt_id": result_list[i]['atclNo'],
                    "apt_name": result_list[i]['atclNm'].replace(',', ''),
                    "apt_number": apt_number.replace(',', ''),
                    "apt_direction": result_list[i]['direction'],
                    "apt_price": result_list[i]['prcInfo'].replace(',', ''),
                    "apt_space1_sq": result_list[i]['spc1'],
                    "apt_space2_sq": result_list[i]['spc2'],
                    "apt_space1_py": "%.2f" % (float(result_list[i]['spc1']) / 3.3),
                    "apt_space2_py": "%.2f" % (float(result_list[i]['spc2']) / 3.3),
                    "apt_space_percent": "%.2f" % ((float(result_list[i]['spc2']) / float(result_list[i]['spc1'])) * 100),
                    "apt_floor": result_list[i]['flrInfo'],
                    "apt_confirm_date": apt_confirm_date.replace(',', ''),
                    "apt_description": apt_description.strip().replace(',', ''),
                })
                i += 1

            if apt_details['result']['moreDataYn'] == 'Y':
                page += 1
                get_apt_details(apt_code, page)
            elif apt_details['result']['moreDataYn'] == 'N':
                break


def export_to_file():
    global export_file_name
    export_file_name = user_sale_name + '_' + area_name + config.file_type
    f = open(config.folder_path + export_file_name, 'x')

    f.write(
        '지역명'
        + ',' + '거래방식'
        + ',' + '매물id'
        + ',' + '아파트명'
        + ',' + '아파트동'
        + ',' + '방향'
        + ',' + '거래가'
        + ',' + 'm^2 (분양/전용)'
        + ',' + '평 (분양/전용)'
        + ',' + '전용면적률'
        + ',' + '층(현재/최고)'
        + ',' + '확인날짜'
        + ',' + '설명'
        + ',' + 'URL'
        + '\n'
    )

    i = 0
    for item in list_apt_details:
        f.write(
            f'{area_name}'
            + ',' + f'{list_apt_details[i]["apt_sale_type"]}'
            + ',' + f'{list_apt_details[i]["apt_id"]}'
            + ',' + f'{list_apt_details[i]["apt_name"]}'
            + ',' + f'{list_apt_details[i]["apt_number"]}'
            + ',' + f'{list_apt_details[i]["apt_direction"]}'
            + ',' + f'{list_apt_details[i]["apt_price"]}'
            + ',' +
            f'{list_apt_details[i]["apt_space1_sq"]} / {list_apt_details[i]["apt_space2_sq"]}'
            + ',' +
            f'{list_apt_details[i]["apt_space1_py"]} / {list_apt_details[i]["apt_space2_py"]}'
            + ',' + f'{list_apt_details[i]["apt_space_percent"]} %'
            + ',' + f'{list_apt_details[i]["apt_floor"]}'
            + ',' + f'{list_apt_details[i]["apt_confirm_date"]}'
            + ',' + f'{list_apt_details[i]["apt_description"]}'
            + ',' +
            f'https://land.naver.com/article/articleDetailInfo.nhn?atclNo={list_apt_details[i]["apt_id"]}'
            + '\n'
        )
        i += 1

    f.close()
