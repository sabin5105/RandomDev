#!/usr/bin/env python
"""
기상청 API 데이터 가져오기 (종관기상관측)
개요 :
종관기상관측이란 정해진 시각의 대기 상태를 파악하기 위해 모든 관측소에서 같은 시각에 실시하는 지상관측을 말합니다. 시정, 구름, 증발량, 일기현상 등 일부 목측 요소를 제외하고 종관기상관측장비(ASOS, Automated Synoptic Observing System)를 이용해 자동으로 관측합니다.

요소:
기온, 강수, 기압, 습도, 풍향, 풍속, 일사, 일조, 적설, 구름, 시정, 지면 · 초상온도 등

상세 기능 기상청 API 문서 참고
https://apihub.kma.go.kr/

Usage: fetch.py -tm -stn -help
"""
import os
import json
import requests
import argparse
import time

# API KEY
BASEDIR = os.path.abspath(os.path.dirname(__file__))
SECRETFILE = os.path.join(BASEDIR, 'secrets.json')
with open(SECRETFILE) as f:
    secrets = json.loads(f.read())
APIKEY = secrets['KMA_APIKEY']

# argparse
parser = argparse.ArgumentParser()
#202308250700
parser.add_argument('-tm', help='시간 / time / 없으면 현재시간', type=str, default='')
parser.add_argument('-stn', help='지점 / station / 0일 때 전체', type=str, default='0')
parser.add_argument('-help', help='도움말 / verbose', type=str, default='0')
args = parser.parse_args()

def main():
    tm = args.tm
    stn = args.stn
    help = args.help
    # 시간별 자료(기간X)
    url = f"https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm={tm}&stn={stn}&help={help}&authKey={APIKEY}"
    # 일 자료
    # url = f"https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd.php?tm={tm}&stn={stn}&help={help}&authKey={APIKEY}"
    response = requests.get(url)
    
    # troubleshooting - response type
    try:
        json_response = response.json()
    except:
        json_response = response.text
    print(json_response)
    
    # save to json file
    
    with open(f'./output/{tm}_{stn}_{help}.json', 'w') as f:
        json.dump(json_response, f, indent=4)
    
if __name__ == '__main__':
    main()
