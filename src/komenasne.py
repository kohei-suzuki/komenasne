# -*- coding: utf-8 -*-
import requests
import json
import datetime
from dateutil.parser import parse
from urllib.parse import quote
from bs4 import BeautifulSoup
import re
import gc
import webbrowser
import subprocess
import configparser
import platform
import os
import sys
import math
from logging import getLogger, StreamHandler, Formatter, FileHandler, INFO

'''
# 必要
pip install requests
pip install beautifulsoup4
iniの設定
'''

jk_chs = {
    'jk1' : (
        1024, 1025, # 関東広域: NHK総合・東京
        10240,   # 北海道(札幌): NHK総合・札幌
        11264,   # 北海道(函館): NHK総合・函館
        12288,   # 北海道(旭川): NHK総合・旭川
        13312,   # 北海道(帯広): NHK総合・帯広
        14336,   # 北海道(釧路): NHK総合・釧路
        15360,   # 北海道(北見): NHK総合・北見
        16384,   # 北海道(室蘭): NHK総合・室蘭
        17408,   # 宮城: NHK総合・仙台
        18432,   # 秋田: NHK総合・秋田
        19456,   # 山形: NHK総合・山形
        20480,   # 岩手: NHK総合・盛岡
        21504,   # 福島: NHK総合・福島
        22528,   # 青森: NHK総合・青森
        25600,   # 群馬: NHK総合・前橋
        26624,   # 茨城: NHK総合・水戸
        28672,   # 栃木: NHK総合・宇都宮
        30720,   # 長野: NHK総合・長野
        31744,   # 新潟: NHK総合・新潟
        32768,   # 山梨: NHK総合・甲府
        33792,   # 愛知: NHK総合・名古屋
        34816,   # 石川: NHK総合・金沢
        35840,   # 静岡: NHK総合・静岡
        36864,   # 福井: NHK総合・福井
        37888,   # 富山: NHK総合・富山
        38912,   # 三重: NHK総合・津
        39936,   # 岐阜: NHK総合・岐阜
        40960,   # 大阪: NHK総合・大阪
        41984,   # 京都: NHK総合・京都
        43008,   # 兵庫: NHK総合・神戸
        44032,   # 和歌山: NHK総合・和歌山
        45056,   # 奈良: NHK総合・奈良
        46080,   # 滋賀: NHK総合・大津
        47104,   # 広島: NHK総合・広島
        48128,   # 岡山: NHK総合・岡山
        49152,   # 島根: NHK総合・松江
        50176,   # 鳥取: NHK総合・鳥取
        51200,   # 山口: NHK総合・山口
        52224,   # 愛媛: NHK総合・松山
        53248,   # 香川: NHK総合・高松
        54272,   # 徳島: NHK総合・徳島
        55296,   # 高知: NHK総合・高知
        56320,   # 福岡: NHK総合・福岡
        56832,   # 福岡: NHK総合・北九州
        57344,   # 熊本: NHK総合・熊本
        58368,   # 長崎: NHK総合・長崎
        59392,   # 鹿児島: NHK総合・鹿児島
        60416,   # 宮崎: NHK総合・宮崎
        61440,   # 大分: NHK総合・大分
        62464,   # 佐賀: NHK総合・佐賀
        63488,   # 沖縄: NHK総合・沖縄
    ),
    'jk2' : (
        1032, 1033, 1034, # 関東広域: NHK-Eテレ
        2056,    # 近畿広域: NHKEテレ大阪
        3080,    # 中京広域: NHKEテレ名古屋
        10248,   # 北海道(札幌): NHKEテレ札幌
        11272,   # 北海道(函館): NHKEテレ函館
        12296,   # 北海道(旭川): NHKEテレ旭川
        13320,   # 北海道(帯広): NHKEテレ帯広
        14344,   # 北海道(釧路): NHKEテレ釧路
        15368,   # 北海道(北見): NHKEテレ北見
        16392,   # 北海道(室蘭): NHKEテレ室蘭
        17416,   # 宮城: NHKEテレ仙台
        18440,   # 秋田: NHKEテレ秋田
        19464,   # 山形: NHKEテレ山形
        20488,   # 岩手: NHKEテレ盛岡
        21512,   # 福島: NHKEテレ福島
        22536,   # 青森: NHKEテレ青森
        30728,   # 長野: NHKEテレ長野
        31752,   # 新潟: NHKEテレ新潟
        32776,   # 山梨: NHKEテレ甲府
        34824,   # 石川: NHKEテレ金沢
        35848,   # 静岡: NHKEテレ静岡
        36872,   # 福井: NHKEテレ福井
        37896,   # 富山: NHKEテレ富山
        47112,   # 広島: NHKEテレ広島
        48136,   # 岡山: NHKEテレ岡山
        49160,   # 島根: NHKEテレ松江
        50184,   # 鳥取: NHKEテレ鳥取
        51208,   # 山口: NHKEテレ山口
        52232,   # 愛媛: NHKEテレ松山
        53256,   # 香川: NHKEテレ高松
        54280,   # 徳島: NHKEテレ徳島
        55304,   # 高知: NHKEテレ高知
        56328,   # 福岡: NHKEテレ福岡
        56840,   # 福岡: NHKEテレ北九州
        57352,   # 熊本: NHKEテレ熊本
        58376,   # 長崎: NHKEテレ長崎
        59400,   # 鹿児島: NHKEテレ鹿児島
        60424,   # 宮崎: NHKEテレ宮崎
        61448,   # 大分: NHKEテレ大分
        62472,   # 佐賀: NHKEテレ佐賀
        63496,   # 沖縄: NHKEテレ沖縄
    ),
    'jk4' : (
        1040, 1041, # 関東広域: 日テレ
        2088,   # 近畿広域: 読売テレビ
        3112,   # 中京広域: 中京テレビ
        4120,   # 北海道域: STV札幌テレビ
        5136,   # 岡山香川: RNC西日本テレビ
        6176,   # 島根鳥取: 日本海テレビ
        10264,  # 北海道(札幌): STV札幌
        11288,  # 北海道(函館): STV函館
        12312,  # 北海道(旭川): STV旭川
        13336,  # 北海道(帯広): STV帯広
        14360,  # 北海道(釧路): STV釧路
        15384,  # 北海道(北見): STV北見
        16408,  # 北海道(室蘭): STV室蘭
        17440,  # 宮城: ミヤギテレビ
        18448,  # 秋田: ABS秋田放送
        19472,  # 山形: YBC山形放送
        20504,  # 岩手: テレビ岩手
        21528,  # 福島: 福島中央テレビ
        22544,  # 青森: RAB青森放送
        30736,  # 長野: テレビ信州
        31776,  # 新潟: TeNYテレビ新潟
        32784,  # 山梨: YBS山梨放送
        34832,  # 石川: テレビ金沢
        35872,  # 静岡: だいいちテレビ
        36880,  # 福井: FBCテレビ
        37904,  # 富山: KNB北日本放送
        47128,  # 広島: 広島テレビ
        51216,  # 山口: KRY山口放送
        52240,  # 愛媛: 南海放送
        54288,  # 徳島: 四国放送
        55312,  # 高知: 高知放送
        56352,  # 福岡: FBS福岡放送
        57376,  # 熊本: KKTくまもと県民
        58408,  # 長崎: NIB長崎国際テレビ
        59432,  # 鹿児島: KYT鹿児島読売TV
        61464,  # 大分: TOSテレビ大分
    ),
    'jk5' : (
        1064, 1065, 1066, # 関東広域: テレビ朝日
        2072,   # 近畿広域: ABCテレビ
        3104,   # 中京広域: メ～テレ
        4128,   # 北海道域: HTB北海道テレビ
        5144,   # 岡山香川: KSB瀬戸内海放送
        10272,  # 北海道(札幌): HTB札幌
        11296,  # 北海道(函館): HTB函館
        12320,  # 北海道(旭川): HTB旭川
        13344,  # 北海道(帯広): HTB帯広
        14368,  # 北海道(釧路): HTB釧路
        15392,  # 北海道(北見): HTB北見
        16416,  # 北海道(室蘭): HTB室蘭
        17448,  # 宮城: KHB東日本放送
        18464,  # 秋田: AAB秋田朝日放送
        19480,  # 山形: YTS山形テレビ
        20520,  # 岩手: 岩手朝日テレビ
        21536,  # 福島: KFB福島放送
        22560,  # 青森: 青森朝日放送
        30744,  # 長野: abn長野朝日放送
        31784,  # 新潟: 新潟テレビ21
        34840,  # 石川: 北陸朝日放送
        35880,  # 静岡: 静岡朝日テレビ
        47136,  # 広島: 広島ホームテレビ
        51232,  # 山口: yab山口朝日
        52248,  # 愛媛: 愛媛朝日
        56336,  # 福岡: KBC九州朝日放送
        57384,  # 熊本: KAB熊本朝日放送
        58400,  # 長崎: NCC長崎文化放送
        59424,  # 鹿児島: KKB鹿児島放送
        61472,  # 大分: OAB大分朝日放送
        63520,  # 沖縄: QAB琉球朝日放送
    ),
    'jk6' : (
        1048, 1049, # 関東広域: TBS
        2064,   # 近畿広域: MBS毎日放送
        3096,   # 中京広域: CBC
        4112,   # 北海道域: HBC北海道放送
        5152,   # 岡山香川: RSKテレビ
        6168,   # 島根鳥取: BSSテレビ
        10256,  # 北海道(札幌): HBC札幌
        11280,  # 北海道(函館): HBC函館
        12304,  # 北海道(旭川): HBC旭川
        13328,  # 北海道(帯広): HBC帯広
        14352,  # 北海道(釧路): HBC釧路
        15376,  # 北海道(北見): HBC北見
        16400,  # 北海道(室蘭): HBC室蘭
        17424,  # 宮城: TBCテレビ
        19488,  # 山形: テレビユー山形
        20496,  # 岩手: IBCテレビ
        21544,  # 福島: テレビユー福島
        22552,  # 青森: ATV青森テレビ
        30752,  # 長野: SBC信越放送
        31760,  # 新潟: BSN
        32792,  # 山梨: UTY
        34848,  # 石川: MRO
        35856,  # 静岡: SBS
        37920,  # 富山: チューリップテレビ
        47120,  # 広島: RCCテレビ
        51224,  # 山口: tysテレビ山口
        52256,  # 愛媛: あいテレビ
        55320,  # 高知: テレビ高知
        56344,  # 福岡: RKB毎日放送
        57360,  # 熊本: RKK熊本放送
        58384,  # 長崎: NBC長崎放送
        59408,  # 鹿児島: MBC南日本放送
        60432,  # 宮崎: MRT宮崎放送
        61456,  # 大分: OBS大分放送
        63504,  # 沖縄: RBCテレビ
    ),
    'jk7' : (
        1072, 1073, 1074, # 関東広域: テレビ東京
        4144,   # 北海道域: TVH
        5160,   # 岡山香川: TSCテレビせとうち
        10288,  # 北海道(札幌): TVH札幌
        11312,  # 北海道(函館): TVH函館
        12336,  # 北海道(旭川): TVH旭川
        13360,  # 北海道(帯広): TVH帯広
        14384,  # 北海道(釧路): TVH釧路
        15408,  # 北海道(北見): TVH北見
        16432,  # 北海道(室蘭): TVH室蘭
        33840,  # 愛知: テレビ愛知
        41008,  # 大阪: テレビ大阪
        56360,  # 福岡: TVQ九州放送
    ),
    'jk8' : (
        1056, 1057, 1058, # 関東広域: フジテレビ
        2080,   # 近畿広域: 関西テレビ
        3088,   # 中京広域: 東海テレビ
        4136,   # 北海道域: UHB
        5168,   # 岡山香川: OHKテレビ
        6160,   # 島根鳥取: 山陰中央テレビ
        10280,  # 北海道(札幌): UHB札幌
        11304,  # 北海道(函館): UHB函館
        12328,  # 北海道(旭川): UHB旭川
        13352,  # 北海道(帯広): UHB帯広
        14376,  # 北海道(釧路): UHB釧路
        15400,  # 北海道(北見): UHB北見
        16424,  # 北海道(室蘭): UHB室蘭
        17432,  # 宮城: 仙台放送
        18456,  # 秋田: AKT秋田テレビ
        19496,  # 山形: さくらんぼテレビ
        20512,  # 岩手: めんこいテレビ
        21520,  # 福島: 福島テレビ
        30760,  # 長野: NBS長野放送
        31768,  # 新潟: NST
        34856,  # 石川: 石川テレビ
        35864,  # 静岡: テレビ静岡
        36888,  # 福井: 福井テレビ
        37912,  # 富山: BBT富山テレビ
        47144,  # 広島: TSS
        52264,  # 愛媛: テレビ愛媛
        55328,  # 高知: さんさんテレビ
        56368,  # 福岡: TNCテレビ西日本
        57368,  # 熊本: TKUテレビ熊本
        58392,  # 長崎: KTNテレビ長崎
        59416,  # 鹿児島: KTS鹿児島テレビ
        60440,  # 宮崎: UMKテレビ宮崎
        62480,  # 佐賀: STSサガテレビ
        63544,  # 沖縄: 沖縄テレビ(OTV)
    ),
    'jk9' : (
        23608,  # 東京: TOKYO MX1
        23609,  # 東京: TOKYO MX2
        23615,  # 東京: TOKYO MX臨時
    ),
    'jk10' : (
        29752, 29753, 29754, # 埼玉: テレ玉
    ),
    'jk11' : (
        24632,  # 神奈川: tvk
    ),
    'jk12' : (
        27704,  # 千葉: チバテレビ
    ),
    'jk101' : (
        101, 102,  # NHK BS1
    ),
    'jk103' : (
        103, 104,  # NHK BSプレミアム
    ),
    'jk141' : (
        141, 142, 143,  # BS日テレ
    ),
    'jk151' : (
        151, 152, 153,  # BS朝日
    ),
    'jk161' : (
        161, 162, 163,  # BS-TBS
    ),
    'jk171' : (
        171, 172, 173,  # BSテレ東
    ),
    'jk181' : (
        181, 182, 183,  # BSフジ
    ),
    'jk191' : (
        191,  # WOWOWプライム
    ),
    'jk211' : (
        211,  # BS11イレブン
    ),
    'jk222' : (
        222,  # BS12トゥエルビ
    ),
    'jk236' : (
        236,  # BSアニマックス
    ),
    'jk333' : (
        333,  # AT-X
    ),
}

jk_names = {
    'jk1' : 'NHK総合',
    'jk2' : 'NHK Eテレ',
    'jk4' : '日本テレビ',
    'jk5' : 'テレビ朝日',
    'jk6' : 'TBSテレビ',
    'jk7' : 'テレビ東京',
    'jk8' : 'フジテレビ',
    'jk9' : 'TOKYO MX',
    'jk101' : 'NHK BS1',
    'jk103' : 'NHK BSプレミアム',
    'jk141' : 'BS日テレ',
    'jk151' : 'BS朝日',
    'jk161' : 'BS-TBS',
    'jk171' : 'BSテレ東',
    'jk181' : 'BSフジ',
    'jk191' : 'WOWOWプライム',
    'jk211' : 'BS11イレブン',
    'jk222' : 'BS12トゥエルビ',
    'jk236' : 'BSアニマックス',
    'jk333' : 'AT-X',
}

def get_logger():
    logger = getLogger(__name__)
    logger.setLevel(INFO)
    sh = StreamHandler()
    sh.setLevel(INFO)
    logger.addHandler(sh)

    fh = FileHandler("komenasne.log")
    fh.setLevel(INFO)
    fh_formatter = Formatter('%(asctime)s - %(message)s')
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    return logger

def get_item(ip_addr, playing_content_id):
    get_title_lists = session.get(f'http://{ip_addr}:64220/recorded/titleListGet?searchCriteria=0&filter=0&startingIndex=0&requestedCount=0&sortCriteria=0&withDescriptionLong=0&withUserData=0')
    title_lists = json.loads(get_title_lists.text)

    for item in title_lists['item']:
        if item['id'] == playing_content_id:
            return item

def get_jkid(service_id):
    for jkch, sevice_ids in jk_chs.items():
        if service_id in sevice_ids:
            return jkch
    return False

def get_datetime(date_time):
    return datetime.datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S+09:00")

# タイムシフトのURL（watch/lv****** ）を取得
def get_tsurl(jkid, date_time):
    # "TBSテレビ【ニコニコ実況】2020年12月26日"等
    ch_name = jk_names[jkid]
    enc_title = ch_name + '【ニコニコ実況】' + date_time.strftime("%Y年%m月%d日")
    logger.info("番組名:" + enc_title)
    load_url = "https://live.nicovideo.jp/search?keyword=" + quote(enc_title) + "&status=onair&sortOrder=recentDesc&providerTypes=channel"
    html = session.get(load_url,headers=headers)
    soup = BeautifulSoup(html.content, "html.parser")
    param = soup.find(class_="searchPage-ProgramList_TitleLink").get('href')
    return 'https://live2.nicovideo.jp/' + param

# ファイル名に使用できない文字を変換
def replace_title(title):
    title = title.replace('\ue180', '[デ]')
    title = title.replace('\ue183', '[多]')
    title = title.replace('\ue184', '[解]') 
    title = title.replace('\ue185', '[SS]') 
    title = title.replace('\ue18c', '[映]')
    title = title.replace('\ue18d', '[無]')
    title = title.replace('\ue190', '[前]') 
    title = title.replace('\ue191', '[後]') 
    title = title.replace('\ue192', '[再]')
    title = title.replace('\ue193', '[新]')
    title = title.replace('\ue195', '[終]')
    title = title.replace('\ue0fe', '[字]')
    title = title.replace('\ue2ca1', 'No1')
    title = title.replace('/', '／')
    title = title.replace('<', '＜')
    title = title.replace('>', '＞')
    title = title.replace(':', '：')
    title = title.replace('?', '？')
    return title

# vposをdateとdate_usecから再計算する（commenomi対策）
def rewrite_vpos(start_date_unixtime, xml_line):
    vpos_start = xml_line.find(' vpos="')
    if vpos_start == -1:
        return xml_line
    # xml内のvposの値を取得
    vpos_pos = vpos_start + 7 # len(' vpos="')
    vpos_str_count = xml_line[vpos_pos:].find('"')
    # xml内dateの値の取得
    date_start = xml_line.find(' date="')
    date_num = xml_line[date_start + 7:date_start + 17]
    # xml内date_usecの値の取得
    date_usec_start = xml_line.find(' date_usec="')
    if date_usec_start == -1:
        date_usec_num = "0"
    else:
        date_usec_str_count = xml_line[date_usec_start + 12:].find('"')
        date_usec_num = xml_line[date_usec_start + 12:date_usec_start + 12 + date_usec_str_count]
    # コメントのunixtimeから動画開始時のunixtime引いた値を新しいvposとする
    comment_unixtime = float(date_num + "." + date_usec_num)
    new_vpos = math.ceil((comment_unixtime - start_date_unixtime) * 100)
    return xml_line[:vpos_pos] + str(new_vpos) + xml_line[vpos_pos + vpos_str_count:]

def get_content_data(playing_info):
    playing_content_id = playing_info['client'][0]['content']['id']
    item = get_item(ip_addr, playing_content_id)
    #print(item)
    #print(item['title'].encode('unicode-escape'))
    title = replace_title(item['title'])
    jkid = get_jkid(item['serviceId'])
    if not jkid:
        logger.info('エラー：「' + item['channelName'] + '」は定義されていないチャンネルのため、連携できません。')
        sys.exit(1)
    start_date_time = get_datetime(item['startDateTime'])
    end_date_time = start_date_time + datetime.timedelta(seconds=item['duration'])
    total_minutes = round(int(item['duration']) / 60)
    logger.info("ファイル名:" + jk_names[jkid] + '_' + start_date_time.strftime("%Y%m%d_%H%M%S") + '_' + str(total_minutes) + '_' + title + '.xml')
    return jkid, start_date_time, end_date_time, total_minutes, title

def open_browser(jkid, start_date_time):
    ts_time = start_date_time - datetime.timedelta(hours=4)
    try:
        url = get_tsurl(jkid, ts_time)
    except:
        logger.info('エラー：タイムシフト番組が見つかりません。')
        sys.exit(1)
    if ts_time.strftime('%Y%m%d') == '20201216':
        # 新ニコニコ実況の初日は11時開始のため7時間減算
        ts_time = ts_time - datetime.timedelta(hours=7)
    shift_time = ts_time.strftime('%H:%M:%S')
    browser_url = url + '#' + shift_time
    print(browser_url)
    webbrowser.open(browser_url)

def open_comment_viewer(jkid, start_date_time, end_date_time, total_minutes, title):
    start_unixtime = start_date_time.timestamp()
    end_unixtime = end_date_time.timestamp()
    kakolog = session.get(f'https://jikkyo.tsukumijima.net/api/kakolog/{jkid}?starttime={start_unixtime}&endtime={end_unixtime}&format=xml',headers=headers)
    logfile = kakolog_dir + jk_names[jkid] + '_' + start_date_time.strftime("%Y%m%d_%H%M%S") + '_' + str(total_minutes) + '_' + title + '.xml'
    logfile_limit = kakolog_dir + jk_names[jkid] + '_' + start_date_time.strftime("%Y%m%d_%H%M%S") + '_' + str(total_minutes)  + '_' + title + '_limit.xml'
    line_count = 0
    with open(logfile, 'w', encoding="utf-8") as saveFile:
        start_date_unixtime = start_date_time.timestamp()
        save_data_lines = []
        for xml_line in kakolog.iter_lines():
            line = rewrite_vpos(start_date_unixtime, xml_line.decode())
            saveFile.write(line + '\n')
            save_data_lines.append(line)
            if '</chat>' in line:
                line_count+=1
            if line == '<title>503 Service Unavailable</title>':
                logger.info('エラー：ニコニコ実況過去ログAPIのサイトから取得できません。')
                sys.exit(1)
        if line_count < 1:
            logger.info('エラー：指定された期間の過去ログは存在しません。')
            sys.exit(1)

    # メモリ解放
    del kakolog
    gc.collect()

    if rate_per_seconde > 0:
        base_date_key = ""
        date_key_count = 0
        aborn_count = 0
        key_pattern = re.compile(r'date=("\d+")') 
        aborn_pattern = re.compile(r'(<chat [^>]+>).+(</chat>)')
        limit_line_data = []
        for line in save_data_lines:
            key = key_pattern.search(line)
            aborn_text = ""
            if key is not None:
                date_key = key.group(1)
                # コメント流量が指定されているときは_limitファイルを作成する
                if base_date_key != date_key:
                    base_date_key = date_key
                    date_key_count = 0
                else:
                    aborn_text = aborn_pattern.sub(r'\1{}\2'.format('\u202A'), line)
                    if len(line) - len(aborn_text) < 6:
                        date_key_count+=.5
                    else:
                        date_key_count+=1
            if date_key_count < rate_per_seconde or aborn_text == "" or '</chat>' not in line or ' shita' in line:
                # 秒間rate値を超えてない、date=が含まれていない、</chat>が含まれていない、"shita"が含まれている場合（歌詞ニキ対応）はそのままファイル出力
                ####saveFileLimit.write(line + '\n')
                limit_line_data.append(line)
            else:
                # comment_aborn_flgがTrueの場合、透明あぼーんで書き込む
                if comment_aborn_flg:
                    limit_line_data.append(aborn_text)
                    #####saveFileLimit.write(aborn_pattern.sub(r'\1{}\2'.format('\u202A'), line) + '\n')
                aborn_count+=1
        if (aborn_count / line_count * 100) <= limit_ratio:
            # 間引きするコメントがlimit_ratioの以下場合（しじみチャンス対策）、limitファイルを作成しない
            logfile_limit = logfile
        else:
            with open(logfile_limit, 'w', encoding="utf-8") as saveFileLimit:
                for line in limit_line_data:
                    saveFileLimit.write(line + '\n')
    total_sec = int(end_unixtime - start_unixtime)
    logger.info("再生時間:{}時{}分{}秒 コメント数:{}".format(total_sec // 3600, (total_sec % 3600) // 60, total_sec % 60, line_count))
    if rate_per_seconde > 0:
        limit_name = {3:'間引き[高]', 4:'間引き[中]', 5:'間引き[低]'}
        logger.info("流量設定:{} 間引きコメント数:{} 間引き率:{}%".format(limit_name[rate_per_seconde], aborn_count, round(aborn_count / line_count * 100, 1)))
        if (aborn_count / line_count * 100) <= limit_ratio:
            logger.info("間引き率が" + str(limit_ratio) + "%以下のため、limitファイルの作成をスキップしました。")
    # mode_silentが0の時はコメントビュアーを起動
    if mode_silent != 1:
        if rate_per_seconde > 0:
            subprocess.Popen([commenomi_path, logfile_limit])
        else:
            subprocess.Popen([commenomi_path, logfile])

# init
logger = get_logger()
logger.info("starting..")
ini = configparser.ConfigParser(interpolation=None)
ini.read('./komenasne.ini', 'UTF-8')
nase_ini = ini['NASNE']['ip']
nasne_ips = [x.strip() for x in nase_ini.split(',')]

session = requests.Session();
headers = {'user-agent':'komenasne'}

is_windows = platform.platform().startswith("Windows")

try:
    commeon_path = ini['PLAYER']['commeon_path']
except KeyError:
    commeon_path = None

try:
    commenomi_path = ini['PLAYER']['commenomi_path']
except KeyError:
    commenomi_path = None

if commeon_path:
    # 以前のiniの互換性維持のためcommeon_pathで上書きする
    commenomi_path = commeon_path

kakolog_dir = None
if commenomi_path and is_windows:
    commenomi_path = commenomi_path.replace(os.sep, os.sep + os.sep)
    kakolog_dir = ini['LOG']['kakolog_dir']
    if '%temp%' in kakolog_dir:
        kakolog_dir = kakolog_dir.replace('%temp%', os.environ['temp'])
    kakolog_dir = kakolog_dir.replace(os.sep, os.sep + os.sep)


args = sys.argv
# ヘルプ表示
if len(args) == 2:
    if '-h' in args[1] or '--help' in args[1]:
        print('直接取得モード: komenasne.exe [channel] [yyyy-mm-dd HH:MM] [total_minutes] option:[title]')
        print('例1: komenasne.exe "jk181" "2021-01-24 26:00" 30')
        print('例2: komenasne.exe "BSフジ" "2021/1/24 26:00" 30 "＜アニメギルド＞ゲキドル　＃３"')
        print('チャンネルリスト: NHK Eテレ 日テレ テレ朝 TBS テレ東 フジ MX BSフジ BS11または以下のjk**を指定')
        for k,v in jk_names.items():
            print(k,v)
        sys.exit(0)

# サイレントモード判断（コメントビュアーは起動せずxmlファイルを作成するだけ）
if "mode_silent" in args:
    mode_silent = 1
else:
    mode_silent = 0

# mode_limitが指定されているときはコメント流量を調整する
try:
    comment_limit = ini['COMMENT']['comment_limit']
except KeyError:
    comment_limit = None

# iniより引数の設定を優先
if "mode_limit_none" in args:
    rate_per_seconde = 0 # 流量調整なし
elif "mode_limit_high" in args:
    rate_per_seconde = 3 # 間引き[高]
elif "mode_limit_middle" in args:
    rate_per_seconde = 4 # 間引き[中]
elif "mode_limit_low" in args:
    rate_per_seconde = 5 # 間引き[低]
elif 'high' == comment_limit:
    rate_per_seconde = 3
elif 'middle' == comment_limit:
    rate_per_seconde = 4
elif 'low' == comment_limit:
    rate_per_seconde = 5
else:
    rate_per_seconde = 0

# mode_limitが指定されているときはコメント流量を制限する
try:
    comment_aborn_or_delete = ini['COMMENT']['aborn_or_delete']
except KeyError:
    comment_aborn_or_delete = None
if 'aborn' == comment_aborn_or_delete:
    comment_aborn_flg = True
else:
    comment_aborn_flg = False

# 間引きしたコメントの割合がこの数値以下だった場合、limitファイルを作成しない(0-99)
try:
    limit_ratio = int(ini['COMMENT']['limit_ratio'])
except KeyError:
    limit_ratio = 0

# 直接取得モード
if len(args) > 3:
    jkid = args[1] # 'jk4' または NHK Eテレ 日テレ テレ朝 TBS テレ東 フジ MX BS11
    # しょぼいカレンダーのチャンネル名も対応
    short_jkids = {"NHK": 1,"NHK総合": 1, "Eテレ": 2, "NHK Eテレ": 2, "日テレ": 4, "日本テレビ": 4,
         "テレ朝": 5, "テレビ朝日": 5,"TBS": 6, "テレ東": 7, "テレ東京": 7, "フジ": 8, "フジテレビ": 8, "MX": 9, "TOKYO MX": 9,
         "BS日テレ": 141, "BS朝日": 151, "BS-TBS": 161, "BSテレ東": 171, "BSフジ": 181, "BS11": 211, "BS11イレブン": 211, "BS12トゥエルビ": 222}
    if jkid in short_jkids:
        # 主要なチャンネルは短縮名でも指定できるように
        jkid = "jk" + str(short_jkids[jkid])
    if jkid not in jk_names:
        logger.info('エラー：「' + args[1] + '」は定義されていないチャンネルのため、連携できません。')
        sys.exit(1)
    start_at = args[2] # "2021-01-27 19:00"
    # しょぼいカレンダーの25:00等表記の対応
    start_date, start_time = start_at.split(" ")
    start_hour, start_min = start_time.split(":")
    if int(start_hour) >= 24:
        start_hour = int(start_hour) - 24
        plus_days = 1
    else:
        plus_days = 0
    start_at = start_date + " " + str(start_hour) + ":" + start_min
    total_minutes = int(args[3]) # 60
    if total_minutes >= 600:
        logger.info('エラー：600分以上は指定できません。')
        sys.exit(1)
    if len(args) > 4:
        title = args[4] # "有吉の壁▼サバゲー場で爆笑ネタ！見取り図＆吉住参戦▼カーベーイーツ！チョコ新技[字]"
    else:
        title = str(total_minutes)
    start_date_time = parse(start_at) - datetime.timedelta(seconds = 15) + datetime.timedelta(days = plus_days)
    end_date_time = start_date_time + datetime.timedelta(minutes = total_minutes) + datetime.timedelta(seconds = 14)
    if not is_windows or kakolog_dir is None:
        # ブラウザ用のコメント再生処理、Windows・Mac兼用
        open_browser(jkid, start_date_time)
    else:
        # commenomi用のコメント再生処理
        open_comment_viewer(jkid, start_date_time, end_date_time, total_minutes, title)
    sys.exit(0)

# main
for ip_addr in nasne_ips:
    try:
        get_playing_info = session.get(f'http://{ip_addr}:64210/status/dtcpipClientListGet')
    except:
        logger.info(f'エラー：{ip_addr} のNASNEが見つかりません。')
        sys.exit(1)
    playing_info = json.loads(get_playing_info.text)
    if 'client' in playing_info:
        # 再生中の番組情報を取得する
        jkid, start_date_time, end_date_time, total_minutes, title = get_content_data(playing_info)
        if not is_windows or kakolog_dir is None:
            # ブラウザ用のコメント再生処理、Windows・Mac兼用
            open_browser(jkid, start_date_time)
        else:
            # commenomi用のコメント再生処理
            open_comment_viewer(jkid, start_date_time, end_date_time, total_minutes, title)
        sys.exit(0)
        break

logger.info('エラー：再生中のnasneの動画が見つからないため、終了します。')
sys.exit(1)


