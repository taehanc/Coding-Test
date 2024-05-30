import requests
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import matplotlib.font_manager as fm
import os

API_KEY = 'FzDJqyRO2T4ATFl7hpHPb6E7smYSnOHW'
BASE_URL = 'https://api.neople.co.kr/df'

# 나눔고딕 폰트 설정 함수
def set_korean_font():
    font_path = os.path.join(os.getcwd(), 'NanumGothic.ttf')
    fm.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'NanumGothic'
    plt.rcParams['axes.unicode_minus'] = False

def get_character_info(server_id, character_name):
    url = f"{BASE_URL}/servers/{server_id}/characters"
    params = {
        'characterName': character_name,
        'apikey': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        character_data = response.json()
        if character_data['rows']:
            return character_data['rows'][0]
        else:
            print(f"캐릭터 {character_name}을(를) 찾을 수 없습니다.")
            return None
    else:
        print(f"오류: {response.status_code}")
        return None

def get_character_items(server_id, character_id):
    url = f"{BASE_URL}/servers/{server_id}/characters/{character_id}/equip/equipment?apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('equipment', [])
    else:
        print(f"오류: {response.status_code}")
        return None

def get_all_characters_items(servers, characters):
    all_items = []
    for server, character in zip(servers, characters):
        char_info = get_character_info(server, character)
        if char_info:
            items = get_character_items(server, char_info['characterId'])
            for item in items:
                all_items.append([
                    server,
                    character,
                    item['itemId'],
                    item['itemName']
                ])
    return all_items

def check_duplicate_items(items):
    item_names = [item[3] for item in items]
    item_counts = Counter(item_names)
    duplicates = {item: count for item, count in item_counts.items() if count > 1}
    return duplicates

def plot_duplicates(duplicates):
    if duplicates:
        items = list(duplicates.keys())
        counts = list(duplicates.values())
        
        # 한글 폰트 설정
        set_korean_font()
        
        plt.figure(figsize=(10, 6))
        plt.barh(items, counts, color='skyblue')
        plt.xlabel('수량')
        plt.ylabel('아이템 이름')
        plt.title('중복된 아이템 이름 및 수량')
        plt.show()
    else:
        print("중복된 아이템이 없습니다.")

def get_item_prices(item_name):
    url = f"{BASE_URL}/auction-sold"
    params = {
        'itemName': item_name,
        'wordType': 'full',
        'wordShort': 'false',
        'limit': 1,
        'apikey': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        auction_data = response.json()
        if auction_data['rows']:
            return auction_data['rows'][0]['unitPrice']
        else:
            return None
    else:
        return None

def get_all_items_prices(items):
    items_with_prices = []
    for item in items:
        price = get_item_prices(item[3])
        items_with_prices.append(item + [price])
    return items_with_prices

def calculate_average_prices(items_with_prices):
    price_dict = {}
    for item in items_with_prices:
        if item[3] not in price_dict:
            price_dict[item[3]] = []
        if item[4] is not None:
            price_dict[item[3]].append(item[4])
    
    average_prices = {item: sum(prices)/len(prices) for item, prices in price_dict.items() if prices}
    return average_prices

def plot_average_prices(average_prices_by_class):
    classes = list(average_prices_by_class.keys())
    avg_prices = [average_prices_by_class[cls] for cls in classes]
    
    # 한글 폰트 설정
    set_korean_font()
    
    plt.figure(figsize=(10, 6))
    plt.bar(classes, avg_prices, color='lightgreen')
    plt.xlabel('직업')
    plt.ylabel('평균 가격')
    plt.title('모든 캐릭터의 아이템 평균 가격')
    plt.show()

# 서버 및 캐릭터 리스트
characters_by_class = {
    "귀검사": {
        "servers": ["cain", "cain", "cain", "casillas", "bakal", "siroco", "prey", "diregie"],
        "characters": ["빨래줄", "백나람", "루승룡", "무기마이스터", "-요재-", "마우스", "원이검", "검슨"]
    },
    "격투가(남)": {
        "servers": ["cain", "hilder", "cain", "cain", "diregie", "prey", "cain", "anton"],
        "characters": ["나막신", "스카사의레어", "샌막", "Cb_NM", "랑셀N", "십사기캐001", "백만볼트두식", "팡능이"]
    },
    "거너(남)": {
        "servers": ["cain", "cain", "cain", "cain", "cain", "casillas", "siroco", "prey"],
        "characters": ["총", "포르세티", "칸리볼트", "asd84136", "문하생", "레잉븐", "chzk곽두식TV", "출혈문의"]
    },
    "마법사(남)": {
        "servers": ["hilder", "prey", "hilder", "siroco", "cain", "cain", "cain", "cain"],
        "characters": ["구양", "시샘달하루", "짬뽕", "아기남님11", "정신분석교수", "불멍", "응잉모기", "배기바기부기"]
    },
    "프리스트(남)": {
        "servers": ["cain", "cain", "diregie", "hilder", "prey", "cain", "siroco", "bakal"],
        "characters": ["슨림이", "™토르", "확이적해버려", "DaeMa", "배크주의", "천망치", "라인하르트†", "떨어진대통령"]
    }
}

if __name__ == "__main__":
    # 한글 폰트 설정
    set_korean_font()

    average_prices_by_class = {}

    for character_class, data in characters_by_class.items():
        servers = data["servers"]
        characters = data["characters"]

        # 모든 캐릭터의 아이템 정보를 가져오기
        all_character_items = get_all_characters_items(servers, characters)

        # 각 아이템의 시세를 가져오기
        all_character_items_with_prices = get_all_items_prices(all_character_items)

        # 테이블 형식으로 출력
        headers = ["Server", "Character", "Item ID", "Item Name", "Price"]
        print(f"\n{character_class} 아이템 목록:")
        print(tabulate(all_character_items_with_prices, headers, tablefmt="grid"))

        # 중복 아이템 확인 및 출력
        duplicates = check_duplicate_items(all_character_items)
        if duplicates:
            print("\nDuplicate Items:")
            for item, count in duplicates.items():
                print(f"{item}: {count} times")
        
        # 중복 아이템 그래프로 출력
        plot_duplicates(duplicates)

        # 평균 가격 계산 및 출력
        average_prices = calculate_average_prices(all_character_items_with_prices)
        print(f"\n{character_class} 아이템 평균 가격:")
        for item, avg_price in average_prices.items():
            print(f"{item}: {avg_price:.2f}")

        # 클래스별 평균 가격 저장
        total_avg_price = sum(average_prices.values()) / len(average_prices) if average_prices else 0
        average_prices_by_class[character_class] = total_avg_price

    # 전체 평균 가격 그래프 출력
    plot_average_prices(average_prices_by_class)
