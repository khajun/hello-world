from bs4 import BeautifulSoup
from selenium import webdriver
from IPython.display import Image
from urllib.request import urlopen
import re
import time


# 웹드라이브로 크롬브라우즈 띄운다.
class OpenDriverMovieSite() :
    driver_path = "../driver/chromedriver.exe"
    driver = webdriver.Chrome(executable_path=driver_path)
    url_page = 'https://movie.naver.com/movie/point/af/list.nhn'

    def __init__(self):
        # 클래스를 실행하면 홈페이지로 이동한다.
        self.driver.get(self.url_page)
        time.sleep(1)


    def ReadCSV(self, movie2018):
        movie_name = movie2018['영화명']
        movie_name[1]
        for i in range(1,387):
            try:
                self.BasicOpen()
                self.InputMovieTitle(movie_name[i])
            except:
                print("아마 검색되지 않는 영화명일 것입니다.")

    def BasicOpen(self):
        # 켜진 홈페이지에서 관련영화를 클릭한 후 새로운 창으로 전환하는 것까지
        # 영화명이 지속적으로 바뀔 것이므로 BasicOpen 함수를 활용
        self.driver.find_element_by_xpath('//*[@id="old_content"]/fieldset/form/select').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="old_content"]/fieldset/form/select/option[2]').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="old_content"]/fieldset/form/input[3]').click()
        time.sleep(0.5)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.find_element_by_xpath('//*[@id="page_content"]/div/div/div/div/form/table/tbody/tr/td/input[1]').click()
        time.sleep(0.5)

    def InputMovieTitle(self, movie_title):
        self.driver.find_element_by_css_selector(
            '#page_content > div > div > div > div > form > table > tbody > tr > td > input.input_type_text_1').send_keys(
            movie_title)
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="page_content"]/div/div/div/div/form/table/tbody/tr/td/input[2]').click()
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="page_content"]/div/div/div[2]/table/tbody/tr[2]/td/a/img').click()
        time.sleep(0.5)
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(0.5)
        self.driver.find_element_by_xpath('//*[@id="old_content"]/fieldset/form/input[4]').click()

        html = urlopen(self.driver.current_url)
        soup = BeautifulSoup(html, "lxml")
        # 코드값 찾아주기
        pattern = re.compile("\d{6}")
        result = pattern.findall(self.driver.current_url)
        code = result[0] if len(result) > 0 else ''

        # 리뷰의 총개수
        num = soup.find("strong", "c_88 fs_11").get_text()
        num_total = int(num.replace(',', ''))
        last_page = num_total // 10 + 1

        self.GetReviews(num_total, last_page)

    def GetReviews(self, num_total, last_page):
        print()



if __name__ == "__main__" :
    opendrivermoviesite = OpenDriverMovieSite()
    movie2018 = pd.read_csv('movie2018.csv', sep=',', encoding='euc-kr')
    opendrivermoviesite.ReadCSV(movie2018)