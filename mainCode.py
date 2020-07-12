import time
from urllib.parse import urlparse, urlencode
import requests
from bs4 import BeautifulSoup
from elasticsearch import helpers

from elaGet import ElaGet
from argSet import ArgSet

class MainCode(ArgSet):

    def __init__(self):

        ArgSet.__init__(self)
        self.searchWord  = "python"
        self.currentTime = time.strftime("%Y", time.localtime())
        self.es = ElaGet.esObj()
        self.totalData = list()

    def urlGet(self):

        self.chromeObj.get(self.confg)
        self.chromeObj.implicitly_wait(3)
        print (self.chromeObj.title)

        # cache 정보에 의해 일전에 검색했던 데이터가 남겨져 있는 경우가 있다.
        self.chromeObj.find_element_by_css_selector("input#ipt_keyword_recruit").clear()
        time.sleep(1)
        self.chromeObj.find_element_by_css_selector("input#ipt_keyword_recruit").send_keys(self.searchWord)
        time.sleep(1)

        # 검색어 닫기 버튼 클릭
        try:
            self.chromeObj.find_element_by_class_name("button.btn_close").click()
        except:
            pass
        else:
            print("검색어 닫기 버튼 클릭 ok")

        self.chromeObj.find_element_by_xpath('//*[@id="btn_search_recruit"]').click()
        time.sleep(1)

        # 채용정보 더 보기 클릭
        try:
            self.chromeObj.find_element_by_xpath('//*[@id="recruit_info_list"]/div[2]/div/a').click()
        except:
            pass
        else:
            print("채용정보 더 보기 클릭 ok")

        #
        current_url = self.chromeObj.current_url
        parse_url = urlparse(url= current_url)
        q = parse_url.query
        self.chromeObj.quit()
        self.detailGet(q=q)

    def detailGet(self, q):

        q = { k[0]: k[1] for k in [j.split("=") for j in [ i for i in q.split('&')]] }
        page = 1
        while True:
            print("work page : {}".format(page))
            q["recruitPage"] = page
            url = "http://www.saramin.co.kr/zf_user/search/recruit?"+urlencode(q)
            sess = requests.Session()

            try:
                html = sess.get(url=url)
            except:
                pass
            else:
                if html.status_code == 200 and html.ok:
                    bsObj = BeautifulSoup(html.text, "html.parser")

                    r = bsObj.select_one("span.foc")

                    if r != None:
                        print(r)
                        break
                    else:
                        page = page + 1

                    recruits = bsObj.select("div.item_recruit")

                    #areaJobs = recruits.select("div.area_job")________________________________________
                    areaJobs = [i.select_one("div.area_job") for i in recruits]
                    corpname = [i.select_one("div.area_corp > strong.corp_name > a") for i in recruits]

                    tmpList = []

                    for a, c in zip(areaJobs, corpname):
                        jobCondition = a.select_one("div.job_condition").select("span")

                        #-----------------------------
                        _date       = None
                        _corp_local = None
                        _sec_1 = None
                        _sec_2 = None
                        _sec_3 = None
                        _sec_4 = None
                        #-----------------------------

                        job_date = str(a.select_one("div.job_date > span.date").string).replace("~ ", "")
                        if job_date != "채용시" or job_date != "상시채용":
                            _date = self.currentTime + job_date.split("(")[0].replace("/", "")
                        else:
                            _date = job_date

                        if len(jobCondition) >= 4:
                            # 회사위치
                            _corp_local = " ".join([i.string for i in jobCondition[0].select("a")])
                            # 경력
                            _sec_1 = jobCondition[1].string
                            # 학력
                            _sec_2 = jobCondition[2].string
                            # 정규직
                            _sec_3 = jobCondition[3].string

                        # 연봉 ------------------------------------------
                        try:
                            _sec_4 = jobCondition[4].string
                        except:
                            pass
                        # ----------------------------------------------

                        self.totalData.append(
                            {
                                "_index": "saramin_" + self.searchWord,
                                "_source": {
                                        "corp_name" : c.attrs["title"],
                                        "crop_href" : "http://www.saramin.co.kr/" + c.attrs["href"],
                                        "corp_local": _corp_local,
                                        "propose"   : a.select_one("h2.job_tit > a").attrs["title"],
                                        "job_date"  : _date,
                                        "sec_1"     : _sec_1,
                                        "sec_2"     : _sec_2,
                                        "sec_3"     : _sec_3,
                                        "sec_4"     : _sec_4
                                }
                            }
                        )

        self.docElaInsert()

    def docElaInsert(self):

        try:

            helpers.bulk(client=self.es, actions=self.totalData)
        except:
            print("indexing fail")
            return
        else:
            print("indexing success!!")

if __name__ == "__main__":
    o = MainCode()
    o.urlGet()