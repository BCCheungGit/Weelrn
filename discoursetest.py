from fluent_discourse import Discourse
from dotenv import load_dotenv
import os
from classes import DiscourseClient
from classes import GoogleSheetsClient
import time
  

def learning_cycle(category_name, topic_name, sheet_id, sheet_index, params):
    load_dotenv()
    baseurl = os.getenv("DISCOURSE_PROD_URL")
    username = os.getenv("DISCOURSE_USERNAME")
    apikey = os.getenv("DISCOURSE_PROD_KEY")
    newclient = DiscourseClient(baseurl, username, apikey)
    sheetclient = GoogleSheetsClient()
    
    questions = sheetclient.get_questions(sheet_id, sheet_index)
    
    newclient.create_category(category_name, "FF0000", "FFFFFF")
    category_id = newclient.list_categories()[category_name]
    print(category_id)
    print(questions[0])
    

    newclient.create_topic(topic_name, topic_name, category_id)
    topic_id = newclient.get_topics()[topic_name]
    time.sleep(10)
    
    if params == "time":
        for question in questions:
            newclient.create_post(topic_id, question)
            time.sleep(5)

    elif params == "replies":
        for question in questions:
            post_id = newclient.create_post(topic_id, question)
            while True:
                replies = newclient.get_replies(post_id)
                if len(replies) == 2:
                    break
                time.sleep(5)
                   
    print("Learning cycle complete")

def collect_replies(category_name, topic_name):
    load_dotenv()
    baseurl = os.getenv("DISCOURSE_PROD_URL") 
    username = os.getenv("DISCOURSE_USERNAME")
    apikey = os.getenv("DISCOURSE_PROD_KEY")
    newclient = DiscourseClient(baseurl, username, apikey)
    category_id = newclient.list_categories()[category_name]
    topic_id = newclient.get_topics()[topic_name]
    posts = newclient.get_posts(topic_id)
    replies = []
    for post in posts:
        if post['reply_count'] > 0:

            replies.append(post['raw'])
            replies.append(newclient.get_replies(post['id']))
            
    print(replies)
    return replies
    
    
        
def main():
    # learning_cycle(
    #     "Learning Cycle 1", 
    #     "All About Atoms", 
    #     "1Iy6LzGU1yQ_I4u9o0ueEC3ZrzypOk-d_Jlxq2cLkKsE", 
    #     0, 
    #     "replies"
    # )
    # learning_cycle(
    #     "Learning Cycle 2",
    #     "All About Chemistry",
    #     "1Iy6LzGU1yQ_I4u9o0ueEC3ZrzypOk-d_Jlxq2cLkKsE",
    #     1,
    #     "time"
    # ) 
    collect_replies("Learning Cycle 2", "All About Chemistry")
    
    
    
if __name__ == "__main__":
    main()