# data_scraper_v2

Install the following packages:

selenium: To automate scraping. You can download using pip through command line as:
	pip install selenium 

webdriver-manager: Install the chrome driver inplcae so no need to download explicitly. 
You can download it through command line as:
	pip install webdriver_manager

Currently this script works on chrome browser.

File structure:
--AmazonConfig.py: Contains user-defined fuctions to retrive data.
--SetupDriver.py: Defines and initiate webdriver object of selenium
--ReviewScraping.py: Run this file to start scraping
