import os
import time
import getpass
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import RequestException
from secret import secret_name, secret_pwd


class Instagram():

    # def __init__(self) -> None:
    #     #Initialize a browser instance

    browser = webdriver.Chrome('/Users/femboss/Python/selenium/webdriver/bin/chromedriver')
    #browser = webdriver.Chrome()

    def login(self):
        # Log into the website
        browser = self.browser
        browser.get(f'http://www.instagram.com')

        try:
           #usr = getpass.getpass("Enter Username ")
           #pwd = getpass.getpass("Enter Password ")

            time.sleep(1)

            #Find the username and password elements and enter values
            username = browser.find_element_by_name("username")
            username.send_keys(secret_name)

            password = browser.find_element_by_name("password")
            password.send_keys(secret_pwd)

            submit_btn = browser.find_element_by_css_selector("button[type='submit']")
            submit_btn.click()

            time.sleep(2)


        except Exception as error:
            print('Error:', error)

        # Say Hi to the user
        print(f'Welcome {username}!')

    def click_follow_user(self, user):
        """ Take list of users to follow and follow one by one
            Checking to see if you already follow them or not
            (or blocked)
        """
        try:
            self.browser.get(user)
            time.sleep(3)
            btn_search = "//button[(contains(text(), 'Follow'))]"

            btn_elm = self.browser.find_element_by_xpath(btn_search)

        except NoSuchElementException:
            message = f'Are you following {user[25:].title()} already?'
            print(f'Element not found.\n'+ message)

        else:
            if btn_elm.text == 'Follow':
                btn_elm.click()
                print(f"Just followed {user[25:].title()}!")
                time.sleep(1)

            elif btn_elm.text == 'Message':
                print(f'You are already following {user[25:].title()}!')


    def click_unfollow_user(self, user):
        """ Take list of users to unfollow and unfollow one by one
                    Checking to see if you already unfollow them or not
        """
        # try:

    #     self.browser.get(user)
    #     time.sleep(3)
    #
    #     btn_search = "//button[contains(text(), 'Message')]'"
    #     btn_elm = self.browser.find_element_by_xpath(btn_search)
    #
    #     if btn_elm.text == 'Message':
    #         btn_elm.click()
    #         print(f"Just unfollowed {user[25:].title()}!")
    #         time.sleep(1)
    #
    #     elif btn_elm.text == 'Follow':
    #         print(f'You are not following {user[25:].title()}!')

    def click_like_post(self, users):

        users_posts = []
        self.browser.get(users)
        time.sleep(1)
        post_format = '/p/'
        try:
            links = [post_elm.get_attribute("href") for post_elm in self.browser.find_elements_by_tag_name('a')]
            for link in links:
                if post_format in link:
                    print(link)
                    self.browser.get(link)
                    time.sleep(1)
                    users_posts.append(link)

                    like_elm = self.browser.find_element_by_xpath('//*[contains(@aria-label, "Like")]')
                    like_btn = like_elm.find_element_by_xpath('..')
                    like_btn.click()
                    if len(users_posts) == 1:
                        print(f"Done liking {users[25:]}'s posts!")
                        break


        except Exception as e:
            print(e)

    def get_users_to_like(self):
        """
        Get List of users who we want to like their recent post
        :return:
        """
        user_list = []
        users = input("Who would you like to like? ").split()
        for user in users:
            url = f'http://www.instagram.com/{user}'
            user_list.append(url)
        return user_list

    def get_users_to_follow(self):
        """Search for a user, if not following user, follow user"""
        #try using selenim xpath

        # get list of users to find
        # search each user by url
        user_list = []
        users = input("Who would you like to follow? ").split()
        for user in users:
            url = f'http://www.instagram.com/{user}'
            user_list.append(url)

        return user_list

    def get_users_to_unfollow(self):
        """Search for a user, if not following user, follow user"""
        #try using selenium xpath

        # get list of users to find
        # search each user by url
        user_list = []
        users = input("Who would you like to unfollow? ").split()
        for user in users:
            url = f'http://www.instagram.com/{user}'
            user_list.append(url)

        return user_list

    def get_user_post(self):
        """
        Go to users instagram profile.
        Grab the first item in on their page [video]
        store that in a list
        :return: List of
        """
        user_list = []
        users = input("Who's page would you like to go to? ").split()
        for user in users:
            url = f'http://www.instagram.com/{user}'
            user_list.append(url)

        post_format = f'/p/'

        for url in user_list:
            user_post_dict = {}
            user_final_links = []
            self.browser.get(url)
            time.sleep(3)
            try:
                links = [post_elm.get_attribute("href") for post_elm in self.browser.find_elements_by_tag_name('a')]
                for link in links:
                    if post_format in link and link not in user_post_dict:
                        print(link)
                        user_final_links.append(link)
                    if len(user_final_links) == 1:
                        break

                user_post_dict[url]=user_final_links
                print(f'First post: {user_post_dict}')
                time.sleep(3)
                return user_post_dict
            except Exception as e:
                print(e)

    def dowload_user_data(self):
        """
        Attempts to get the content at `url` by making an HTTP GET request.
        If the content-type of response is some kind of HTML/XML, return the
        text content, otherwise return None.

        Create directory to put downloaded data in, if data is from a new user, create a new subdirectory
        """
        user_post_dict = self.get_user_post()

        # Check if directory exist
        # If not create it
        # If so, use it
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'IG Data')
        os.makedirs(data_dir,  exist_ok = True)

        post_elements =[]

        for user_posts in user_post_dict.values():
            for url in user_posts:
                try:
                    self.browser.get(url)
                    video_elm = self.browser.find_element_by_xpath("//video")
                    post_elements.append(video_elm.get_attribute('src'))
                except NoSuchElementException:
                    image_elm = self.browser.find_element_by_xpath("//img")
                    post_elements.append(image_elm.get_attribute('src'))
                    pass
                time.sleep(2)
        #print(post_elements)

        try:
            #closing.()
            for url in post_elements:
                print(url)
                base_url = urlparse(url).path
                filename = os.path.basename(base_url)
                filepath = os.path.join(data_dir, filename)
                print(filepath)
                with requests.get(url) as r:
                    response = self.is_good_response(r)
                    if response:
                        print(response)
                        with open(filepath, "wb") as f:
                                f.write(r.content)

        except RequestException as e:
            self.log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None

    def is_good_response(self, resp):
        """
        Returns True if the response seems to be HTML, False otherwise.
        """
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None)
                #and content_type.find('html') > -1)

    def log_error(e):
        """
        It is always a good idea to log errors.
        This function just prints them, but you can
        make it do anything.
        """
        print(e)



##################################################################################################
# RUN MAIN CODE

def run():
    #Get Instagram webdriver instance
    ig = Instagram()

    # Open browser and Login to app
    ig.login()

    #Ask user if you want to do [Follow/Unfollow, Like/ Web-Scrape]
    options = ['Follow', 'Unfollow', 'Like', 'Scrape']
    choice = (input(f'Hi, {secret_name} --What would you like to do on instagram today? \n'
                     f'Choose an option 1-4:\n' +
                     str(options) + " "))

    # Follow Users
    if choice == '1':

        # Get list if users that you want to follow and follow them
        users_to_follow = ig.get_users_to_follow()

        for user in users_to_follow:
            try:
                ig.click_follow_user(user)
            except:
                pass
        print('Done following selected users!')

    # Unfollow users

    elif choice == '2':

        # Get list if users that you want to ufollow and follow them
        users_to_unfollow = ig.get_users_to_unfollow()

        for user in users_to_unfollow:
            try:
                ig.click_unfollow_user(user)
            except:
                pass
        print('Done unfollowing selected users!')

    # Like users photos
    elif choice == '3':
        # Get list if users that you want to unfollow and follow them
        users_to_like = ig.get_users_to_like()

        for user in users_to_like:
            try:
                ig.click_like_post(user)
            except:
                pass

    # Scrape information
    # Collect a list of users to scrape from - get a list off all post link (first 3)
    # Pass list to requests - which will download the data and place it in a folder
    elif choice == '4':
        try:
            ig.dowload_user_data()
        except Exception as e:
            print(e)
        else:
            print('Done scraping users posts!')

run()

