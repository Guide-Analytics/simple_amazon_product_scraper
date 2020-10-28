'''
#################################################
@product: Guide Product Analysis
@filename: Amazon Config File (Web elements path(CSS / XPath))

@author: Raj Patel
@date: August 5, 2020
##################################################
'''
from selenium.common.exceptions import NoSuchElementException
from word2number import w2n


class AmazonConfig:
    """
    Specifies web elements path to scrap data from.

    ...

    Methods
    -------
    getPageContent()
        This function finds and return the content of page where all reviews are located.
    getReviewer()
        This function returns name of a reviewer.
    getRatings()
        This function returns ratings given by a reviewer.
    getDate()
        This function returns date at which a review was posted by a reviewer.
    isVerifiedPurchase()
        This function checks whether a product is labeled as Verified Purchase or not.
    getReview()
        This function collects the review posted by a reviewer.
    peopleFindHelpful()    
        This function checks the count for number of people who found the review helpful.
    getAvgRating()
        This function collect the average rating of a product.
    getReviewCount()
        This function collect the total reviews for a product.
    getReviewTitle():
        This function gets the review title given by reviewer.
    getProductName():
        This function gets the name of the product.
    getAuthorProfile():
        This function gets the profile url of the author.
    get_category():
        This function gets the category of the product.
    """

    def getPageContent(self, driver):

        """
        This function finds and return the content of page where all reviews are located.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        
        Returns
        -------
        list
            list of elements attached to the given page
            includes inforation associated with reviews, hyperlinks - See more reviews (from Canada), Next page button
        """
        path = '//div[@id="cm_cr-review_list"]'
        page_content = driver.find_elements_by_xpath(path)
        return page_content

    def getReviewer(self, driver, flag, unique_id):
        """
        This function returns name of a reviewer.

        Parameters
        ----------
        flag
        driver : selenium webdriver object
            web driver of selenium
        unique_id : int
            unique unique_id that corresponds to each unique review

        Returns
        -------
        string
            name of reviewer
        """

        if flag:
            path = '#customer_review-' + unique_id + ' div.a-profile-content > span'
        else:
            path = '#customer_review_foreign-' + unique_id + ' div.a-profile-content > span'
        #        //*[@unique_id="customer_review_foreign-R3MS1MSTBAXCU6"]/div[1]/div/div[2]/span
        try:
            reviewer = driver.find_element_by_css_selector(path).get_attribute('textContent').split('\n')

            return reviewer[0]
        except NoSuchElementException:
            return False

    def getRatings(self, driver, unique_id, is_canada):
        """
        This function returns ratings given by a reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        unique_id : int
            unique unique_id that corresponds to each unique review
        
        Returns
        -------
        float(or empty if not found)
            ratings given by reviewer
        """
        if is_canada:
            path = '//*[@id="customer_review-'+unique_id+'"]/div[2]/a[1]'
            try:
                ratings = driver.find_element_by_xpath(path).get_attribute('title')
                ratings = float(ratings[0])
            except NoSuchElementException:
                return ""
            return ratings
        else:

            path = '//*[@id="customer_review_foreign-'+unique_id+'"]/div[2]/i/span'
            try:
                ratings = driver.find_element_by_xpath(path).get_attribute('textContent')
                # print(ratings)
                ratings = float(ratings[0])
            except NoSuchElementException:
                return ""
            return ratings

    def getDate(self, driver, unique_id):
        
        """
        This function returns date at which a review was posted by a reviewer

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        unique_id : int
            unique unique_id that corresponds to each unique review
        
        Returns
        -------
        string
            date a review was posted
        """
        try:
            path = '//*[@id="customer_review-'+unique_id+'"]//span[@data-hook="review-date"]'

            message = str(driver.find_element_by_xpath(path).get_attribute('textContent'))
            country = message.split()[2].lower()
            if country == 'canada':
                message = message.split()[-3:]
                date = ' '.join(map(str,message))
                return date, country, True
        except NoSuchElementException:
            try:
                path = '//*[@id="customer_review_foreign-'+unique_id+'"]//span[@data-hook="review-date"]'
                message = str(driver.find_element_by_xpath(path).get_attribute('textContent'))
                cnt = message.lower().split()[2:]
                del cnt[-4:]
                country = ' '.join(map(str, cnt))
                message = message.split()[-3:]
                date = ' '.join(map(str,message))
                return date, country, False
            except NoSuchElementException:
                return "","", False

    def isVerifiedPurchase(self, driver, id, is_canada):
        
        """
        This function checks whether a product is labeled as Verified Purchase or not.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review
        
        Returns
        -------
        bool
            True if product is labeled Verified Purchase else False
        """
        if is_canada:
            path = '//*[@id="customer_review-'+id+'"]/div[3]/span/a/span'
        else:
            path = '//*[@id="customer_review_foreign-'+id+'"]/div[3]/span/a/span'
        try:
            isverified = driver.find_element_by_xpath(path).text
            return True
        except NoSuchElementException:
            return False


    def getReview(self, driver, id, is_canada):

        """
        This function collects the review posted by a reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review
        
        Returns
        -------
        string
            review given by a reviewer
        """
        if is_canada:
            path = '//*[@id="customer_review-'+id+'"]/div[4]/span'
        else:
            path = '//*[@id="customer_review_foreign-'+id+'"]/div[4]/span'
        return driver.find_element_by_xpath(path).text

    def peopleFindHelpful(self, driver, id, is_canada):

        """
        This function checks the count for number of people who found the review helpful.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review
        
        Returns
        -------
        string
            number of people found helpful, if none returns empty string
        """
        if is_canada:
            path = '#customer_review-'+id+' span.cr-vote > div.a-row.a-spacing-small > span'
        else:
            path = '//*[@id="customer_review_foreign-'+id+' span.cr-vote > div.a-row.a-spacing-small > span'
        try:
            text = driver.find_element_by_css_selector(path).get_attribute('textContent')
            try:
                number = int(text.split()[0])
                return number
            except ValueError:
                number = w2n.word_to_num(text.split()[0])
                return number
        except NoSuchElementException:
            return 0

    def getAvgRating(self, driver):

        """
        This function collect the average rating of a product.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        
        Returns
        -------
        float
            average rating of a product
        """

        path = '//span[@data-hook="rating-out-of-text"]'
        ratings = driver.find_element_by_xpath(path).text.split()
        rating = float(ratings[0])
        return rating

    def getReviewCount(self, driver):

        """
        This function collect the total reviews for a product.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        
        Returns
        -------
        int
            total reviews of a product
        """

        path = '//div[@data-hook="total-review-count"]/span'
        total_rating = driver.find_element_by_xpath(path).text.split()
        total_count = total_rating[0]
        return total_count

    def getReviewTitle(self, driver, id, is_canada):

        """
        This function gets the review title given by reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review
        
        Returns
        -------
        string
            review title given by reviewer
        """
        if is_canada:
            path = '//*[@id="customer_review-'+id+'"]/div[2]/a[2]/span'
        else:
            path = '//*[@id="customer_review_foreign-'+id+'"]/div[2]/span[2]/span'
        try:
            review = driver.find_element_by_xpath(path).text
            return review
        except NoSuchElementException:
            return ""

    def getProductName(self, driver):

        """
        This function gets the name of the product.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        
        Returns
        -------
        string
            review name of product
        """
        
        path = '//*[@id="productTitle"]'
        try:
            name = driver.find_element_by_xpath(path).text
            return name
        except NoSuchElementException:
            return None

    def getAuthorProfile(self, driver, id):

        """
        This function gets the author url.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review
        
        Returns
        -------
        string
            author profile url
        """
        path = '//*[@id="customer_review-'+id+'"]//div[@data-hook="genome-widget"]/a'
        try:
            profile = driver.find_element_by_xpath(path).get_attribute('href')
            return profile
        except NoSuchElementException:
            return ""

    def get_category(self, driver):

        """
        This function gets the category of the product.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        
        Returns
        -------
        string
            author profile url
        """
        path = '//*[@id="wayfinding-breadcrumbs_feature_div"]/ul'
        try:
            li_list = driver.find_elements_by_xpath(path)
            return li_list
        except NoSuchElementException:
            return ""
    
    def get_summary_table(self, driver):
        """
        This function gets the brand of the product.
        """
        path = '//*[@id="productDetails_techSpec_section_1"]//tbody/tr'
        try:
            table = driver.find_elements_by_xpath(path)
            
            return table
        except NoSuchElementException:
            return None

    def get_brand(self, driver):
        path = '//*[@id="detailBullets_feature_div"]//ul/li'
        try:
            table  = driver.find_elements_by_xpath(path)
            return table
        except NoSuchElementException:
            return None
        
    def get_extra_info(self, driver):
        path = '//*[@id="productDetails_detailBullets_sections1"]//tbody/tr'
        try:
            table = driver.find_elements_by_xpath(path)
            return table
        except NoSuchElementException:
            return None
        
    def get_rank(self, driver):
        path = '//*[@id="SalesRank"]'
        try:
            rank = driver.find_element_by_xpath(path).text
            return rank
        except NoSuchElementException:
            return None
