import os
from selenium.webdriver import Chrome, ChromeOptions
import time
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import csv
import numpy as np

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword = input('Enter search keyword: ')
    
    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()


    ##########スクレイピング処理##########
    # dataframe空箱作成
    df = pd.DataFrame(index=[], columns=['企業名', '初任給'])
    # 企業名を格納
    company_list = []
    # 検索結果の企業の初任給を取得
    starting_salary_list = []
    #　スクレイピング開始を表示
    text = "scraping now"
    while True:# ページ終了まで繰り返し
        if len(driver.find_elements_by_link_text("次へ")) > 0:
            # そのページの企業数を格納する
            page_count = []
            #　クラス名から企業名を取得
            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

            # 1ページ分繰り返し会社名を取得し、企業数を把握する
            for name in name_list:
                company_list.append(name.text)
                page_count.append(name.text)

            l = (len(page_count))
            print(l)
            print(text)
            print(company_list)

            for i in range(1, l, 1):

                target1 = "/html/body[@class='js__modal']/div[@class='wrapper']/div[@class='container'][1]/form/div[@class='container__inner']/div[@class='cassetteRecruit']["+str(i)+"]/div[@class='cassetteRecruit__content']/div[@class='cassetteRecruit__detail']/div[@class='cassetteRecruit__main']/table[@class='tableCondition']/tbody/tr[5]/td[@class='tableCondition__body']"
                salary = driver.find_elements_by_xpath(target1)
                for sa in salary:
                    starting_salary_list.append(sa.text) 

        
            driver.find_element_by_link_text("次へ").click()
            time.sleep(5)

        else:
            CompanySeries = pd.Series(company_list)
            SalarySeries = pd.Series(starting_salary_list)
            df = pd.concat([df, CompanySeries, SalarySeries], axis=1)
            df.to_csv('mynavi03.csv', encoding='utf-8')
            text = "finish"
            print(text)
            driver.quit()


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
