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
    search_keyword = "高収入"
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
    
    #次へを押した回数をcount
    #page = 1 
    text = "scraping now"
    while True:
        if len(driver.find_elements_by_link_text("次へ")) > 0:
            #print("######################page: {} ########################".format(page))
            #1ページ内の企業数をリセットする
            #l = 0
            # ページ終了まで繰り返し取得
            exp_name_list = []
            # 検索結果のページに存在する会社名を取得し、繰り返す回数を決める
            name_list = driver.find_elements_by_class_name("cassetteRecruit__name")

            # 1ページ分繰り返し会社名を取得し、企業数を把握する
            for name in name_list:
                exp_name_list.append(name.text)
            # 繰り返した数を 変数l に格納し、1ページ内の企業数を把握する
            l = (len(exp_name_list))
            print(l)
            print(text)

            # 検索結果の企業の初任給を取得
            starting_salary_list = []
            
            for i in range(1, l, 1):

                target1 = "/html/body[@class='js__modal']/div[@class='wrapper']/div[@class='container'][1]/form/div[@class='container__inner']/div[@class='cassetteRecruit']["+str(i)+"]/div[@class='cassetteRecruit__content']/div[@class='cassetteRecruit__detail']/div[@class='cassetteRecruit__main']/table[@class='tableCondition']/tbody/tr[5]/td[@class='tableCondition__body']"
                salary = driver.find_elements_by_xpath(target1)
                for t in salary:
                    starting_salary_list.append(t.text) 
                    #ssl = starting_salary_list
                    #df.append(ssl)
                    #np.append("mynavi03.csv", ssl)
                    #df.to_csv("mynavi03.csv", encoding="utf-8")

        
            driver.find_element_by_link_text("次へ").click()
            time.sleep(5)

        else:
                np.savetxt("mynavi03.csv", starting_salary_list, delimiter=',', fmt="%s",encoding="utf-8")
                text = "finish"
                print(text)
                driver.quit()


# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
