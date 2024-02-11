from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup
import re
from time import sleep
from datetime import datetime


driver = webdriver.Firefox()
driver.maximize_window() # For maximizing window
driver.implicitly_wait(20) # gives an implicit wait for 20 seconds

# Navigate to the YouTube search results page
url = "https://www.youtube.com/results?search_query=global+breaking+news"
driver.get(url)
sleep(5)
html = driver.page_source
# with open("html", "w") as f:
#     f.write(html)

soup = BeautifulSoup(html)

titles = []
views = []
time_posted = []
channel_names = []
captions = []

tag_list = []
for tag in soup.find_all('ytd-video-renderer'):
    target_block = tag.text
    tag_list.append(target_block)
    split_lines = target_block.strip().split("\n")
    if split_lines[-1] == "LIVE":
        continue

    titles.append(split_lines[0])
    captions.append(split_lines[-8])
    channel_names.append(split_lines[10])
    for line in split_lines:
        if ' views' in line:
            views.append(line)
        if ' ago' in line:
            time_posted.append(line)


    print('=' * 50)

print(len(titles), len(views), len(time_posted), len(channel_names), len(captions))

# Create the dataframe
df = pd.DataFrame({
    'Title': titles,
    'Views': views,
    'Time Posted': time_posted,
    'Channel Name': channel_names,
    'Caption': captions
})
#
# Save the dataframe to a CSV file (new file will be created every day unless you write new file on the same day)
csv_file = 'youtube_video_' + str(datetime.now().strftime('%Y_%m_%d')) + '.csv'
df.to_csv(csv_file, index=False, mode='w')
#
# Display the dataframe
print(df)

with open("tag_list.txt", "w") as f:
     f.writelines(tag_list)

driver. quit()
