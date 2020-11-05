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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import glob
import sys

# define dictionary to store data
amazon_reviews = {}
def initialize_dict():
    global amazon_reviews

    amazon_reviews = {
        'author_id': [],
        'verified_purchase' : [],
        'review_title' : [],
        'reviews' : [],
        'country': [],
        'date' : [],
        'reviewer_name' : [],
        'ratings' : [],
        'people_find_helpful' : [],
        # 'reviewer_profile_url':[],
        'start_time': [],
        'end_time': []
    }

configuration = None # AmazonConfig file instance
total_review = "" # total Canadian reviews
flag = True
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
    global flag
    
    all_reviews = configuration.getPageContent(driver)
    for rev in all_reviews:
    #     print(rev.text)
        id = rev.find_elements_by_xpath('//div[@data-hook="review"]')
        for i in id:
            unique_id = i.get_attribute('id')
            start = datetime.datetime.now()
            date, country, flag = configuration.getDate(i,unique_id)

            reviewer = configuration.getReviewer(i,flag,unique_id)
#                if reviewer:
#                    print(reviewer)
#                    # say country respective to the review
#                    date, country, flag = configuration.getDate(i,unique_id)
#                if not flag:
#                    other_countries_id = rev.find_elements_by_xpath('//div[@data-hook="review"]')
#                    for j in other_countries_id:
#                        print("other countries id: ",j.get_attribute('id'))
#                    return

            ratings = configuration.getRatings(i,unique_id,flag)
            review = configuration.getReview(i,unique_id,flag)
            number = configuration.peopleFindHelpful(i,unique_id,flag)
            verified_purchase = configuration.isVerifiedPurchase(i,unique_id,flag)
            review_title = configuration.getReviewTitle(i, unique_id,flag)
            # author_profile = configuration.getAuthorProfile(i,unique_id)
            # id = author_profile.split('/')[-2]
            # id = id.split('.')[-1]
            amazon_reviews['author_id'].append(unique_id)
            amazon_reviews['country'].append(country)
            # amazon_reviews['reviewer_profile_url'].append(author_profile)
            amazon_reviews['reviewer_name'].append(reviewer)
            amazon_reviews['date'].append(date)
            amazon_reviews['ratings'].append(ratings)
            amazon_reviews['reviews'].append(review)
            amazon_reviews['people_find_helpful'].append(number)
            amazon_reviews['review_title'].append(review_title)
            amazon_reviews['verified_purchase'].append(verified_purchase)
            end = datetime.datetime.now()
            amazon_reviews['start_time'].append(start)
            amazon_reviews['end_time'].append(end)
#            else:
#                print('no reviews to collect')
#                flag = False
#                return

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
        reviews = reviews.split()[-2]
        reviews = reviews.replace(',','')
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
    driver = setup.SetupDriver().driver
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
    global flag
    if len(amazon_reviews['reviewer_name']) == 0:

        count = 0
        checkMoreReviews(driver)
        getReviews(driver)
        if (len(amazon_reviews['reviewer_name']) == 0):
            return

    else:
        try:
            print("--------refreshing page to load ---------------------")
            driver.refresh()
            time.sleep(random.randint(4,6))
            getReviews(driver)
        except:
            driver.refresh()
            time.sleep(random.randint(4,6))
            getReviews(driver)
    
    while True:
        try:

            next_button =  driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')
            next_button.click()
            time.sleep(random.randint(2,6))
            getReviews(driver)
        except:
            return

    extractReviews(driver)


# main function
def get_data(urls):
    """
    Main function
    """
    global configuration # AmazonConfig file obj

    for url in urls:
        status = True
        initialize_dict()
        product_id = url.strip().split("dp/")[-1]
        product_id = product_id.split('/')[0].split('?')[0]

        # check whether product is already scraped or not
        files = glob.glob(f'main_product\*.csv')
        if len(files) > 0:
            for file in files:
                if product_id in file:
                    print('file is already present')
                    status = False

        if status:
            print(product_id)
            #set up driver
            driver = setup.SetupDriver().driver
            driver.get(url)
            WebDriverWait(driver, 20).until(ec.number_of_windows_to_be(1))
            # setup all configurations defined in Amazonconfig file
            configuration = config.AmazonConfig()
            
            price = configuration.getPrice(driver)
            prod_name = configuration.getProductName(driver)
            while not prod_name:
                driver.refresh()
                time.sleep(3)
                prod_name = configuration.getProductName(driver)

            # get the brand/manufacturer of the product
            product_info = configuration.get_summary_table(driver)
            # brand = []
            product_metadata = {}
            for i in product_info:
                row = i.find_element_by_xpath('th').text.lower().strip()
                product_metadata[row] = i.find_element_by_xpath('td').text
                # if row == "brand":
                #     brand.append(i.find_element_by_xpath('td').text)
            try:
                product_metadata["brand"]
            except KeyError:

            # if len(brand) == 0:
                rows = configuration.get_brand(driver)
                if rows is not None:
                    for row in rows:
                        bname = row.find_element_by_xpath('span/span[1]').text.lower()
                        if ('manufacturer' in bname) or ('brand' in bname):
                            # print(bname)
                            bname = row.find_element_by_xpath('span/span[2]').text
                            # brand.append(bname)
                            product_metadata[bname] = row.find_element_by_xpath('td').text
                            # print(brand)


            # get the rank of the product

            extra_info = configuration.get_extra_info(driver)
            rank = []
            for i in extra_info:
                row = i.find_element_by_xpath('th').text.lower().strip()
                if "rank" in row:
                    rank.append(i.find_element_by_xpath('td').text)

            if len(rank) == 0:
                row = configuration.get_rank(driver)
                if row is not None:
                    row = row.split('#')[1].split()[0]
                    rank.append(row)
            categories = configuration.get_category(driver)
            category = categories[0].text.split('\n')[0]
            try:
                avg_rating = configuration.getAvgRating(driver) #avg rating of product
            except:
                avg_rating = ""
            try:
                total_reviews = configuration.getReviewCount(driver) #toal reviews of product(contains international reviews as well)
            except:
                total_reviews = ""

            extractReviews(driver)
            print('all reviews are collected')

            # close and destroy the web instance
            driver.quit()

            if (len(amazon_reviews['reviewer_name']) > 0):
                # create data frame
                df = pd.DataFrame.from_dict(amazon_reviews)
        ##        files = glob.glob('main_product\*.csv')
                # create extra columns for product name, avg rating and total reviews
                df['product_name'] = prod_name # product name
                df['average_rating'] = avg_rating # overall average rating
                df['price'] = price
                df['total_reviews'] = total_review # reviews in Canada.
                df['product_category'] = category
                df['product_id'] = product_id
                df['meta_data'] = pd.Series([product_metadata])
                # df['brand_name'] = brand[0] if len(brand) > 0 else ""
                df['rank'] = rank[0] if len(rank) > 0 else ""
                # save to csv

                df.to_csv(f'main_product\{product_id}.csv')
                del df

def main():
   data = pd.read_csv("LED Flashlight Scraping - Sheet1 - Copy.csv")
   urls = data.Link.dropna()
   get_data(urls)
   # for url in urls.unique():

#     print("Enter url to scrape: ")
#     url = input()
#     get_data(url)
    

if __name__ == '__main__':
    main()
