from selenium import webdriver
import yaml


class ArgSet():
    ## 프로그램 상수
    CHROME_DRVIER_PATH = r"C:\Users\EZFARM\PycharmProjects\Saramin\chrome_driver\chromedriver.exe"
    CONFIG_PATH = r"C:\Users\EZFARM\PycharmProjects\Saramin\config\information.yml"
    ## ------------------------------------------------------------------------------------------

    def __init__(self):
        self.chromeObj = ArgSet.getSelenium()
        self.confg = ArgSet.getUrlInformation()

    @classmethod
    def getUrlInformation(cls):
        try:
            f=open(ArgSet.CONFIG_PATH, "r", encoding="utf-8")
        except FileNotFoundError as e:
            print(e)
            return
        else:
            confg = yaml.safe_load(f)
            f.close()
            return confg["url"]

    @classmethod
    def getSelenium(cls):
        chrome_option = webdriver.ChromeOptions()
        # ====================================================
        chrome_option.add_argument("headless")
        chrome_option.add_argument("window-size=1920x1080")
        chrome_option.add_argument("disable-gpu")
        # ====================================================

        #chrome_driver = webdriver.Chrome(executable_path= ArgSet.CHROME_DRVIER_PATH, chrome_options =chrome_option)
        chrome_driver = webdriver.Chrome(executable_path=ArgSet.CHROME_DRVIER_PATH)
        return chrome_driver