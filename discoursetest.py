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
            
            
            

    
    
        
def main():
    learning_cycle(
        "Learning Cycle 1", 
        "The First Learning Cycle Test", 
        "1Iy6LzGU1yQ_I4u9o0ueEC3ZrzypOk-d_Jlxq2cLkKsE", 
        0, 
        "replies"
    )
    # load_dotenv()
    # baseurl = os.getenv("DISCOURSE_PROD_URL")
    # username = os.getenv("DISCOURSE_USERNAME")
    # apikey = os.getenv("DISCOURSE_PROD_KEY")
    # newclient = DiscourseClient(baseurl, username, apikey)
    # newclient.create_category("Learning Cycle 1", "FF0000", "FFFFFF")
    # category_id = newclient.list_categories()["Learning Cycle 1"]
    # newclient.create_topic("Atoms", "Atoms", category_id)
    # topic_id = newclient.get_topics()["Atoms"]
    # post_id = newclient.create_post(topic_id, "What is an atom?")
    # newclient.get_replies(64)

    
    
    
if __name__ == "__main__":
    main()