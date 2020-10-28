'''
#################################################
@product: Guide Product Analysis
@filename: SetupDriver File (setup the driver object of selenium for chrome browser)

@author: Raj Patel
@date: August 5, 2020
##################################################
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class SetupDriver:
    """
    Selenium web driver setup

    ...

    Attributes
    ----------
    driver : selenium web driver object
        object of webdriver.

    """
    driver = None
    
    def __init__(self):
        opt = Options()
##        opt.headless = True # set headless mode to True
        opt.add_argument('--incognito')
        opt.add_argument('--no-sandbox') try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = opt)
        except ValueError:
            print("Could not get version for Chrome from this webdriver installation. Please install Chrome browser")
            exit(-1)
