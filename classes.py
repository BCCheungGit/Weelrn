from fluent_discourse import Discourse
from dotenv import load_dotenv
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import gspread
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer



class DiscourseClient:
    def __init__(self, base_url, username, api_key):
        self.client = Discourse(base_url=base_url, username=username, api_key=api_key)
    
    def list_categories(self):
        categories_dict = {}
        try:
            categories = self.client.categories.json.get()
            categories_list = categories['category_list']['categories']
            for category in categories_list:
                # print(f"Category: {category['name']}, ID: {category['id']}")
                categories_dict[category['name']] = category['id']
            return categories_dict
        except Exception as e:
            print(e)
    
    def create_topic(self, title, raw, category):
        try:
            topic = self.client.posts.json.post({
                "title": title,
                "raw": raw,
                "category": category,
                "archetype": "topic",
            })
            print("Successfully added topic")
        except Exception as e:
            print(e)
    
    def get_topics(self):
        topics_dict = {}
        try:
            topics = self.client.latest.json.get()
            topics_list = topics['topic_list']['topics']
            for topic in topics_list:
                # print(f"Topic: {topic['title']}, ID: {topic['id']}")
                topics_dict[topic['title']] = topic['id']
            return topics_dict
        except Exception as e:
            print(e)
    
    def create_post(self, topic_id, raw, reply_to_post_number=None):
        try:
            post = self.client.posts.json.post({
                "topic_id": topic_id,
                "raw": raw,
                "reply_to_post_number": reply_to_post_number,
            })
            # print(f"Successfully created a new post with id: {post['id']}")
            return post['id']
        except Exception as e:
            print(e)
    
    def get_posts(self, topic_id):
        try:
            posts = self.client.posts.json.get()
            posts_list = posts['latest_posts']
            # for post in posts_list:
            #     if post['topic_id'] == topic_id:
                    # print(f"Post by: {post['username']}, ID: {post['id']}, Content: {post['raw']}, Created At: {post['created_at']}, Reply to: {post['reply_to_post_number']}")
            return posts_list
        except Exception as e:
            print(e)
    
    def get_replies(self, post_id):
        try:
            replies = self.client.posts[post_id].replies.json.get()
            replies_list = []
            for reply in replies:
                replies_list.append([reply['username'], reply['created_at'], reply['cooked'].split('<p>')[1].split('</p>')[0]])
            # print(replies_list)
            return replies_list
        except Exception as e:
            print(e)

    def create_category(self, name, color, text_color, parent_category_id=None):
        try:
            category = self.client.categories.json.post({
                "name": name,
                "color": color,
                "text_color": text_color,
                "parent_category_id": parent_category_id
            })
            response = category.json()
            #print(response)
            #print('successfully created a new category')
        except Exception as e:
            print(e)
    
    def get_users(self):
        try:
            usernames = []
            users = self.client.admin.users.list['active'].json.get()
            for user in users:
                usernames.append(user['username'])
            #print(usernames)
            return usernames
        except Exception as e:
            print(e)
    


class GoogleSheetsClient():
    def __init__(self, token_file="token.json", credentials_file="credentials.json"):
        self.token_file = token_file
        self.credentials_file = credentials_file
        self.SCOPES = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
    
    def get_params(self, sheet_id, worksheet_number):
        creds = self.authenticate()
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(sheet_id).get_worksheet(worksheet_number)
        sheet_title = sheet.title
        print(sheet_title)
        return sheet_title
        
        
    def authenticate(self):
        creds = None
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, "w") as token:
                token.write(creds.to_json())
        return creds
    
    def get_worksheets(self, sheet_id):
        creds = self.authenticate()
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(sheet_id)
        print(sheet.worksheets())
    
    def read_data(self, sheet_id, worksheet_number):
        creds = self.authenticate()
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(sheet_id).get_worksheet(worksheet_number)
        unfiltered_values = sheet.get_all_values()
        values = []
        for row in unfiltered_values:
            values.append(row[1:])
        df = pd.DataFrame(values, columns=["Question", "Edit", "Approved", "Category"])
        print(df)
        return df
    
    def get_questions(self, sheet_id, worksheet_number):
        data = self.read_data(sheet_id, worksheet_number)
        questions = data["Question"].tolist()
        return questions
    
    def post_data(self, sheet_id, sheet_name, data: pd.DataFrame):
        creds = self.authenticate()
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(sheet_id)
        try:
            new_worksheet = sheet.worksheet(sheet_name)
        except:
            new_worksheet = sheet.add_worksheet(title=sheet_name, rows=100, cols=100)
        
        new_worksheet.clear()
        new_worksheet.update([data.columns.values.tolist()] + data.values.tolist())

        print("Data posted successfully")
    
    def add_sent_analysis(self, sheet_id, sheet_name, data: pd.DataFrame):
        sia = SentimentIntensityAnalyzer()
        data["Sentiment"] = data["Answer"].apply(lambda x: str(sia.polarity_scores(x)))
        print(data)
        self.post_data(sheet_id, sheet_name, data)
        print("Sentiment analysis added successfully")


