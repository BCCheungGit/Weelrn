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
    
    def create_post(self, topic_id, raw, reply_to_post_number=None):
        try:
            post = self.client.posts.json.post({
                "topic_id": topic_id,
                "raw": raw,
                "reply_to_post_number": reply_to_post_number,
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
                    print(f"Post by: {post['username']}, ID: {post['id']}, Content: {post['raw']}, Created At: {post['created_at']}, Reply to: {post['reply_to_post_number']}")
        except Exception as e:
            print(e)
    
    def get_replies(self, post_id):
        try:
            replies = self.client.posts[post_id].json.get()
            print(replies)
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
            print(response)
        except Exception as e:
            print(e)
    
     
        
def main():
    load_dotenv()
    baseurl = os.getenv("DISCOURSE_PROD_URL")
    username = os.getenv("DISCOURSE_USERNAME")
    apikey = os.getenv("DISCOURSE_PROD_KEY")
    newclient = DiscourseClient(base_url=baseurl, username = username, api_key=apikey)
    # newclient.create_category("Weelrn", "FF0000", "FFFFFF")  ID: 5
    newclient.list_categories()
    
    
if __name__ == "__main__":
    main()