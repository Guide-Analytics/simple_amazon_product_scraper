# data_scraper_v2

Install the following packages:<br>

-selenium: To automate scraping. You can download using pip through command line as:<br>
<pre><em> pip install selenium</em></pre><br>

-webdriver-manager: Install the chrome driver inplace so no need to download explicitly. 
You can download it through command line as:
<pre><em> pip install webdriver_manager</em></pre><br>

-word to number conversion:
<pre><em> pip install word2number</em></pre><br>

Currently this script works on chrome browser. <br>

File structure:
--AmazonConfig.py: Contains user-defined functions to retrieve data.<br>
--SetupDriver.py: Defines and initiate webdriver object of selenium.<br>
--ReviewScraping.py: Run this file to start scraping by entering the url of the page.<br>
