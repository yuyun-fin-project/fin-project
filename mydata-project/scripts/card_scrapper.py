from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import json


# 크롬 헤드리스 옵션
options = Options()
# options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# 드라이버 경로 설정
driver = webdriver.Chrome(options=options)

# 크롤링 대상 num 값 범위
nums = list(range(1,11))
nums.append(32)
card_company_list = {}

for num in nums:
    url = f"https://www.card-gorilla.com/team/detail/{num}"
    driver.get(url)

    # 렌더링 대기
    time.sleep(2)
    selector = f"#q-app > section > div.team_detail.team_{num} > div > div.top_bar > div > b"
    card_company = driver.find_element(By.CSS_SELECTOR, selector).text
    print(card_company)
    card_company_list[card_company] = []
    for i in range(1, 11):  # 1~10번째 카드
        try:
            if num == 32:
                selector = f"#q-app > section > div.team_detail.team_32 > section > div.inner > article.con_area > div > div > ul > li:nth-child({i})) > div > div.card_data > div.name > p > span.card_name"
            else:
                selector = f"#q-app > section > div.team_detail.team_{num} > section > div:nth-child(3) > article.con_area > div > div > ul > li:nth-child({i}) > div > div.card_data > div.name > p > span.card_name"
            card_name = driver.find_element(By.CSS_SELECTOR, selector).text
            card_company_list[card_company].append(card_name)
            print(f"{i}: {card_name}")
        except Exception as e:
            print(f"{i}: [카드 없음 또는 구조 다름]")


with open("card_company_list.json", "w", encoding="utf-8") as f:
    json.dump(card_company_list, f, ensure_ascii=False, indent=2)

driver.quit()