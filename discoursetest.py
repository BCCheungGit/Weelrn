from fluent_discourse import Discourse
from dotenv import load_dotenv
import os
from classes import DiscourseClient
from classes import GoogleSheetsClient
import time
from datetime import datetime
import pandas as pd
import datetime





#TODO: Implement get_params
def get_params(sheet_id, sheet_index):
    sheetclient = GoogleSheetsClient()
    sheet_params = sheetclient.get_params(sheet_id, sheet_index)
    return sheet_params

def count_mentions(text):
    count = 0
    for word in text.split(" "):
        if 'class="mention"' in word:
            count += 1
    return count

def count_words(text):
    if "<img src=" in text:
        return 0
    return len(text.split(" "))
    
    
def collect_replies(category_name, topic_name, start_time):
    load_dotenv()
    baseurl = os.getenv("DISCOURSE_PROD_URL") 
    username = os.getenv("DISCOURSE_USERNAME")
    apikey = os.getenv("DISCOURSE_PROD_KEY")
    newclient = DiscourseClient(baseurl, username, apikey)
    df = pd.DataFrame(columns=["Start Time", "Time Since Start", "Question", "User", "Timestamp", "Answer", "Word Count", "Mentions"])
    
    category_id = newclient.list_categories()[category_name]
    topic_id = newclient.get_topics()[topic_name]
    posts = newclient.get_posts(topic_id)
    replies = []
    
    for post in posts:
        if post['reply_count'] > 0:
            replies.append(post['raw'])
            replies.append(newclient.get_replies(post['id']))
    rows = []
    for i in range(0, len(replies), 2):
        question = replies[i]
        answers = replies[i + 1]
        for user, timestamp, response in answers:
            # Parsing and formatting timestamps
            start_timestamp = datetime.datetime.fromisoformat(start_time.replace("+00:00", ""))
            answer_timestamp = datetime.datetime.fromisoformat(timestamp.replace("Z", ""))

            start_time_string = start_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            answer_time_string = answer_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            time_since_start = (answer_timestamp - start_timestamp).total_seconds()
            
            mentions = count_mentions(response)
            
            #Constructing row dictionary
            row = {
                "Start Time": start_time_string,
                "Time Since Start": time_since_start,
                "Question": question,
                "User": user,
                "Timestamp": answer_time_string, 
                "Answer": response,
                "Word Count": count_words(response), 
                "Mentions": mentions,
            }
            rows.append(row)
    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
    
    sheetsclient = GoogleSheetsClient()
    sheetsclient.post_data("18o8TFdohAnvxUbD6pMB4USQdpUeLoKpyNnf5iAsKxlU", topic_name, df)
    newclient.get_users()
    return df


def learning_cycle(category_name, topic_name, sheet_id, sheet_index):
    load_dotenv()
    baseurl = os.getenv("DISCOURSE_PROD_URL")
    username = os.getenv("DISCOURSE_USERNAME")
    apikey = os.getenv("DISCOURSE_PROD_KEY")
    newclient = DiscourseClient(baseurl, username, apikey)
    sheetclient = GoogleSheetsClient()
    
    questions = sheetclient.get_questions(sheet_id, sheet_index)
    sheet_data = sheetclient.read_data(sheet_id, sheet_index)
    
    try:
        newclient.list_categories()[category_name]
    except KeyError:
        newclient.create_category(category_name, "FF0000", "FFFFFF")
        
    category_id = newclient.list_categories()[category_name]
    print("Category id: ", category_id)

    try:
        newclient.get_topics()[topic_name]
        topic_id = newclient.get_topics()[topic_name]
    except KeyError:
        newclient.create_topic(topic_name, topic_name, category_id)
        topic_id = newclient.get_topics()[topic_name]
    
    start_time = str(datetime.datetime.now(datetime.timezone.utc))
    
    if not sheet_data.empty:
        for i in range(len(sheet_data)):
            if sheet_data.loc[i, "Category"] == "Discussion Question" and sheet_data.loc[i, "Approved"] != "FALSE":
                newclient.create_post(topic_id, sheet_data.loc[i, "Question"])
                time.sleep(5)
            elif sheet_data.loc[i, "Category"] == "Challenge" and sheet_data.loc[i, "Approved"] != "FALSE":
                post_id = newclient.create_post(topic_id, sheet_data.loc[i, "Question"])
                while True:
                    replies = newclient.get_replies(post_id)
                    if len(replies) == 2:
                        break
                    time.sleep(5)
    
    print("Learning cycle complete")
    replies = collect_replies(category_name, topic_name, start_time)
    
    
    



    
    
        
def main():
    sheet_index = 0
    title = get_params("1Iy6LzGU1yQ_I4u9o0ueEC3ZrzypOk-d_Jlxq2cLkKsE", sheet_index)
    learning_cycle(
        "Weelrn", 
        title, 
        "1Iy6LzGU1yQ_I4u9o0ueEC3ZrzypOk-d_Jlxq2cLkKsE", 
        sheet_index,
    )
    # replies = collect_replies("Weelrn", title)
    # print(replies)
    
    
    
    
    
if __name__ == "__main__":
    main()