'''
#################################################
@product: Guide Product Analysis
@filename: ReviewScraping File (Scraps the reviews from given URL)

@author: Raj Patel
@date: August 5, 2020
##################################################
'''

import AmazonConfig as config
import SetupDriver as setup
import time
import datetime
import random
import pandas as pd

# define dictionary to store data
amazon_reviews = {
    'verified_purchase' : [],
    'review_title' : [],
    'review_text' : [],
    'date' : [],
    'author' : [],
    'ratings' : [],
    'people_find_helpful' : [],
    'author_profile':[],
    'start_time':[],
    'end_time':[]
}

configuration = None # AmazonConfig file instance
total_review = "" # total Canadian reviews

# check if all reviews are not loaded, them load them first
def checkMoreReviews(driver):

    """
    This function checks if main page contains more reviews to load before scraping

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium

    Returns
    -------
    bool
        True if contains more reviews else False
    """
    
    try:
        isMoreReviews = driver.find_element_by_partial_link_text('See all reviews')
        if isMoreReviews:
            isMoreReviews.click()
            time.sleep(5)
            return True
    except:
        print('no link to see more reviews')
        return False
    
# fetch reviews and store in a dictionary
def getReviews(driver):

    """
    This function collects all reviews and stores in dictionary

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium
    
    """
    
    all_reviews = configuration.getPageContent(driver)
    for rev in all_reviews:
    #     print(rev.text)
        id = rev.find_elements_by_xpath('//div[@data-hook="review"]')
        for i in id:
            unique_id = i.get_attribute('id')
            start = datetime.datetime.now()
            reviewer = configuration.getReviewer(i,unique_id)
            if reviewer:
                
                date = configuration.getDate(i,unique_id)
                ratings = configuration.getRatings(i,unique_id)
                review = configuration.getReview(i,unique_id)
                number = configuration.peopleFindHelpful(i,unique_id)
                verified_purchase = configuration.isVerifiedPurchase(i,unique_id)
                review_title = configuration.getReviewTitle(i, unique_id)
                author_profile = configuration.getAuthorProfile(i,unique_id)
                
                amazon_reviews['author_profile'].append(author_profile)                
                amazon_reviews['author'].append(reviewer)
                amazon_reviews['date'].append(date)
                amazon_reviews['ratings'].append(ratings)
                amazon_reviews['review_text'].append(review)
                amazon_reviews['people_find_helpful'].append(number)
                amazon_reviews['review_title'].append(review_title)
                amazon_reviews['verified_purchase'].append(verified_purchase)
            end = datetime.datetime.now()
            amazon_reviews['start_time'].append(start)
            amazon_reviews['end_time'].append(end)

def totalReviews(driver):
    """
    Get total reviews in Canada

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium

    Returns
    -------
    reviews : string
        Total reviews in Canada if reviews are found or False   
    """
    path = '#filter-info-section > span';
    try:
        reviews = driver.find_element_by_css_selector(path).text
        print(reviews)
        reviews = reviews.split()[-2]
        reviews = reviews.replace(',','')
        print(reviews)
        return reviews
    except:
        return False
                    
# reinitiate driver if all reviews are not fetched and an error occurs
def reinitiate(driver,url):
    
    """
    This function reinitiates web driver object if some error occurs while
    scraping reviews

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium
    url : string
        url of the page from where to begin with

    Returns
    -------
    driver : selenium webdriver object
        web driver of selenium    
    """
    
    driver.quit()
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt);
    driver.get(url)
    return driver

# refresh when an error occurs and all reviews are not extracted
def extractReviews(driver):

    """
    This function made necessary calls to collect all the reviews

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium
    
    """
    
    global count
    global total_review
    if len(amazon_reviews['author']) == 0:
##        total_review = ""
        count = 0
        checkMoreReviews(driver)
        getReviews(driver)
        if (len(amazon_reviews['author']) == 0):
            return

    else:
        try:
            print("--------refreshing page to load ---------------------")
            driver.refresh()
            time.sleep(random.randint(2,6))
            getReviews(driver)
        except:
            driver.refresh()
            time.sleep(random.randint(2,6))
            getReviews(driver)
    
    while True:
        try:
            if str(len(amazon_reviews['author'])) == total_review:
                return
            if(total_review == ""):
                total_review = totalReviews(driver)
            next_button =  driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')
            next_button.click()
            time.sleep(random.randint(2,6))
            getReviews(driver)
        except:
            if total_review != "" and len(amazon_reviews['author']) != int(total_review):
                print("Unable to load reviews...")
                count = count+1
                if count > 5:
                    url = str(driver.current_url)
                    print(url)
                    driver = reinitiate(driver,url)
                if count > 9: # break and exit if no reviews found after nine continuous attempts
                    count = 0
                    return
                break
    extractReviews(driver)


# main function
def main():
    """
    Main function
    """
    global configuration # AmazonConfig file obj
    
    print("Enter the url to scrap data from: ")
    url = input()

    #set up driver
    driver = setup.SetupDriver().driver
    driver.get(url)

    # setup all configurations defined in Amazonconfig file
    configuration = config.AmazonConfig()

    try:
        avg_rating = configuration.getAvgRating(driver) #avg rating of product
    except:
        avg_rating = ""
    try:
        total_reviews = configuration.getReviewCount(driver) #toal reviews of product(contains international reviews as well)
    except:
        total_reviews = ""
    try:
        prod_name = configuration.getProductName(driver)
    except:
        prod_name = ""

    extractReviews(driver)
    print('all reviews are collected')

    # close and destroy the web instance
    driver.quit()

    if (len(amazon_reviews['author']) > 0):
        # create data frame
        df = pd.DataFrame.from_dict(amazon_reviews)

        # create extra columns for product name, avg rating and total reviews
        df['product_name'] = prod_name # product name
        df['average_rating'] = avg_rating # overall average rating
        df['total_reviews'] = total_review # reviews in Canada.

        # save to csv
        df.to_csv(f'{prod_name}_amazon_review.csv')


if __name__ == '__main__':
    main()
