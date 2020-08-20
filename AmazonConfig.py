'''
#################################################
@product: Guide Product Analysis
@filename: Amazon Config File (Web elements path(CSS / XPath))

@author: Raj Patel
@date: August 5, 2020
##################################################
'''

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
    
    def getReviewer(self, driver, id):
        """
        This function returns name of a reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review
        
        Returns
        -------
        string
            name of reviewer
        """
        path = '#customer_review-'+id+' div.a-profile-content > span'
        try:
            reviewer = driver.find_element_by_css_selector(path).get_attribute('textContent').split('\n')
            return reviewer[0]
        except:
            return False

    def getRatings(self, driver, id):
        """
        This function returns ratings given by a reviewer.

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review
        
        Returns
        -------
        float(or empty if not found)
            ratings given by reviewer
        """
        path = '//*[@id="customer_review-'+id+'"]/div[2]/a[1]'
        try:
            ratings = driver.find_element_by_xpath(path).get_attribute('title')
            ratings = float(ratings[0])
        except:
            return ""
        return ratings

    def getDate(self, driver, id):
        
        """
        This function returns date at which a review was posted by a reviewer

        Parameters
        ----------
        driver : selenium webdriver object
            web driver of selenium
        id : int
            unique id that corresponds to each unique review
        
        Returns
        -------
        string
            date a review was posted
        """
        
        path = '//*[@id="customer_review-'+id+'"]//span[@data-hook="review-date"]'
        message = driver.find_element_by_xpath(path).get_attribute('textContent').split()[-3:]
        date = ' '.join(map(str,message))
        return date

    def isVerifiedPurchase(self, driver, id):
        
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
        
        path = '//*[@id="customer_review-'+id+'"]/div[3]/span/a/span'
        try:
            isverified = driver.find_element_by_xpath(path).text
            return True
        except:
            return False


    def getReview(self, driver, id):

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
        
        path = '//*[@id="customer_review-'+id+'"]/div[4]/span'
        return driver.find_element_by_xpath(path).text

    def peopleFindHelpful(self, driver, id):

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
        
        path = '#customer_review-'+id+' span.cr-vote > div.a-row.a-spacing-small > span'
        
        try:
            text = driver.find_element_by_css_selector(path).get_attribute('textContent')
            number = text.split()[0]
            return number
        except:
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

    def getReviewTitle(self, driver, id):

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
        
        path = '//*[@id="customer_review-'+id+'"]/div[2]/a[2]/span'
        try:
            review = driver.find_element_by_xpath(path).text
            return review
        except:
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
        except:
            return ""

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
        except:
            return ""
