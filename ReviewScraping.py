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

# define dictionary to store data
amazon_reviews = {
    'avg_rating' : None,
    'total_reviews': None,
    'product_name' : '',
    'verified_purchase' : [],
    'review_title' : [],
    'review_text' : [],
    'date' : [],
    'author' : [],
    'ratings' : [],
    'people_find_helpful' : []
}

print("Enter the url to scrap data from: ")
url = input()

#set up driver
driver = setup.SetupDriver().driver
driver.get(url)

# setup all configurations defined in Amazonconfig file
config = config.AmazonConfig()


avg_rating = config.getAvgRating(driver) #avg rating of product
amazon_reviews['avg_rating'] = avg_rating

total_reviews = config.getReviewCount(driver) #toal reviews of product
amazon_reviews['total_reviews'] = total_reviews

def getReviews(driver):

    """
    This function collects all reviews and stores in dictionary

    Parameters
    ----------
    driver : selenium webdriver object
        web driver of selenium
    
    """
    
    all_reviews = config.getPageContent(driver)
    for rev in all_reviews:
    #     print(rev.text)
        id = rev.find_elements_by_xpath('//div[@data-hook="review"]')
        for i in id:
            unique_id = i.get_attribute('id')
            print(unique_id)
            reviewer = config.getReviewer(i,unique_id)
            if reviewer:
                
                date = config.getDate(i,unique_id)
                ratings = config.getRatings(i,unique_id)
                review = config.getReview(i,unique_id)
                number = config.peopleFindHelpful(i,unique_id)
                verified_purchase = config.isVerifiedPurchase(i,unique_id)
                review_title = config.getReviewTitle(i, unique_id)
                
                amazon_reviews['author'].append(reviewer)
                amazon_reviews['date'].append(date)
                amazon_reviews['ratings'].append(ratings)
                amazon_reviews['review_text'].append(review)
                amazon_reviews['people_find_helpful'].append(number)
                amazon_reviews['review_title'].append(review_title)
                
                if verified_purchase:
                    amazon_reviews['verified_purchase'].append(verified_purchase)

# check if all reviews are not loaded, them load them first
try:
    
    
    isMoreReviews = driver.find_element_by_partial_link_text('See all reviews')
    if isMoreReviews:
        isMoreReviews.click()
        time.sleep(5)
except:
    print('no link to see more reviews')

getReviews(driver)
while True:
    try:
        next_button =  driver.find_element_by_xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a')
        next_button.click()
        time.sleep(5)
        getReviews(driver)
    except:
        print('no more reviews to fetch')
        print('exiting...')
        break
print('reviews are collected')
