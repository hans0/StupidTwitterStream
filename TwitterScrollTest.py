"""
the one that works
"""



import json
import random
import requests
import tweepy
import tkinter as tk

import unicodedata

'''
Load developer keys
'''
f = open('keys', 'r')
tw_api_key = ''
tw_api_secret = ''
tw_access_token = ''
tw_access_token_secret = ''

for line in f:
    if line == 'Twitter API Key\n':
        tw_api_key = f.readline()
    if line == 'Twitter API Secret\n':
        tw_api_secret = f.readline()
    if line == 'Twitter Access Token\n':
        tw_access_token = f.readline()
    if line == 'Twitter Access Token Secret\n':
        tw_access_token_secret = f.readline()
        # print(line)

tw_api_key = tw_api_key.strip('\n')
tw_api_secret = tw_api_secret.strip('\n')
tw_access_token = tw_access_token.strip('\n')
tw_access_token_secret = tw_access_token_secret.strip('\n')

f.close()

'''
Load Twitter users to sample tweets from
'''
f = open("users", "r")
user_list = []
for line in f:
    user_list.append(str(line).strip("\n"))

f.close()
print(user_list)


def random_user():
    return user_list[random.randint(0, len(user_list)-1)]

'''
Authentication
'''
auth = tweepy.OAuthHandler(tw_api_key, tw_api_secret)

auth.set_access_token(tw_access_token, tw_access_token_secret)

api = tweepy.API(auth)


class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(self, height=60, width=150)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        status_list = api.user_timeline(random_user(), count=20)
        status = status_list[random.randint(0, len(status_list)-1)]
        json_str = json.dumps(status._json)
        #print(str(json_str.index("text")) + " " + str(json_str.index(",")))
        self.get_text_from_tweet(json_str)
        self.latest_tweet = self.get_text_from_tweet(json_str).replace(u"\u2019", "'").replace("\\n", "\n").replace("u\u201c", "\"")
        self.text.insert("end", str(self.latest_tweet) + "\n")
        self.add_timestamp()

    def add_timestamp(self):
        temp_tweet = api.user_timeline(random_user(), count=20)
        # temp_tweet = api.user_timeline("InternetHippo", count=10)
        status = temp_tweet[random.randint(0, len(temp_tweet)-1)]
        json_str = json.dumps(status._json)
        #print(self.latest_tweet)

        self.latest_tweet = self.get_text_from_tweet(json_str).replace(u"\u2019", "'").replace("\\n", "\n").replace("u\u201c", "\"")
        print(self.latest_tweet)

        self.text.insert(1.0, self.latest_tweet + "\n")
        self.text.see(1.0)
        # self.text.insert("end", self.latest_tweet + "\n")
        # self.text.see("end")
        '''
        if temp_tweet != self.latest_tweet:
            self.latest_tweet = temp_tweet
            self.text.insert("end", self.get_text_from_tweet(temp_tweet) + "\n")
            self.text.see("end")
        '''
        self.after(1000, self.add_timestamp)

    def get_text_from_tweet(self, txt):
        try:
            text_maybe_index = txt.index("text\":")
        except:
            text_maybe_index = 0
        substring_from_text_tag = txt[text_maybe_index:]
        #print(substring_from_text_tag)
        try:
            index_of_comma = substring_from_text_tag.index("\", \"")
            # index_of_comma = substring_from_text_tag.index(",")
            result = substring_from_text_tag[8:index_of_comma]
        except:
            result = substring_from_text_tag
        result = result.replace("\\u2019", "\'")
        return result


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Stupid little Twitter stream")
    frame = Example(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()