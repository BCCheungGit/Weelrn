from fluent_discourse import Discourse
from dotenv import load_dotenv
import os


class DiscourseClient:
    def __init__(self, base_url, username, api_key):
        self.client = Discourse(base_url=base_url, username=username, api_key=api_key)
    
    def list_categories(self):
        try:
            categories = self.client.categories.json.get()
            categories_list = categories['category_list']['categories']
            for category in categories_list:
                print(f"Category: {category['name']}, ID: {category['id']}")
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
            print("Successfully added topic with ID: ", topic['id'])
        except Exception as e:
            print(e)
    
    def get_topics(self):
        try:
            topics = self.client.latest.json.get()
            topics_list = topics['topic_list']['topics']
            for topic in topics_list:
                print(f"Topic: {topic['title']}, ID: {topic['id']}")
        except Exception as e:
            print(e)
    
    def create_post(self, topic_id, raw):
        try:
            post = self.client.posts.json.post({
                "topic_id": topic_id,
                "raw": raw,
            })
            print(f"Successfully created a new post with id: {post['id']}")
        except Exception as e:
            print(e)
    
    def get_posts(self, topic_id):
        try:
            posts = self.client.posts.json.get()
            posts_list = posts['latest_posts']
            for post in posts_list:
                if post['topic_id'] == topic_id:
                    print(f"Post by: {post['username']}, ID: {post['id']}, Content: {post['raw']}, Created At: {post['created_at']}")
        except Exception as e:
            print(e)
            
        
def main():
    load_dotenv()
    baseurl = os.getenv("DISCOURSE_URL")
    username = os.getenv("DISCOURSE_USERNAME")
    apikey = os.getenv("DISCOURSE_API_KEY")
    newclient = DiscourseClient(base_url=baseurl, username = username, api_key=apikey)
    newclient.list_categories()
    newclient.get_posts(13)
    #list_categories()
    #create_topic()
    # create_post()
    # get_topics()
    # get_posts()
    
if __name__ == "__main__":
    main()