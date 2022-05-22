from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import csv
import time

class TikTokScraper:

    def __init__(self):
        self.PATH = "chromedriver.exe"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
        self.text = ""
        self.data = {}

    def get_level_1_comments(self, url):
        self.driver.get(url)
        comment_blocks = self.driver.find_elements(By.CLASS_NAME, "tiktok-16r0vzi-DivCommentItemContainer")
        for comment in comment_blocks:
            username = comment.find_element(By.CLASS_NAME, "tiktok-1n2c527-StyledUserLinkName")
            user_comment = comment.find_element(By.TAG_NAME, 'p')
            user_block = username.text + "\n" + user_comment.text + "\n"
            self.text += user_block + "\n"

    def write_to_csv(self, filename, url):
        # opens url
        self.driver.get(url)
        previous_height = 0

        # Gets all comments loaded on page
        new_height = self.driver.find_elements(By.CLASS_NAME, "tiktok-16r0vzi-DivCommentItemContainer")

        # scrolls until no more comments load
        while len(new_height) is not previous_height:
            previous_height = len(new_height)

            # scrolls to bottom of the page
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)

            # gets all comments currently loaded
            new_height = self.driver.find_elements(By.CLASS_NAME, "tiktok-16r0vzi-DivCommentItemContainer")

        with open(filename, 'w', encoding='UTF8', newline='') as f:
            # Header values of csv file
            header_names = ['Username', 'Comment']
            the_writer = csv.DictWriter(f, header_names)
            the_writer.writeheader()

            # grabs all comments loaded
            comment_blocks = self.driver.find_elements(By.CLASS_NAME, "tiktok-16r0vzi-DivCommentItemContainer")
            for comment in comment_blocks:

                # grabs the username of the level 1 comment
                username = comment.find_element(By.CLASS_NAME, "tiktok-1n2c527-StyledUserLinkName")
                username_text = username.text

                # grabs comment text of level 1 comment
                user_comment = comment.find_element(By.TAG_NAME, 'p')
                user_comment_text = user_comment.text

                # creates item to be used for DictWriter
                row = {'Username' : username_text, 'Comment' : user_comment_text}
                the_writer.writerow(row)
            print("done with " + url)

# list of TikTok posts to grab comments from
posts = [""]
TikTokScraper = TikTokScraper()

# location where you want the .csv to be written to
filepath = ''

# iterates through all posts
for post in posts:
    start = post.find('video/')
    stop = post.find('?')

    # grabs post id
    post_id = post[start+6:stop]

    # creates csv filename
    output_file = 'comments_' + post_id + '.csv'
    TikTokScraper.write_to_csv(filepath + output_file, post)