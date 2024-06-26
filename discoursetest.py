from fluent_discourse import Discourse
from dotenv import load_dotenv
import os
from classes import DiscourseClient
from classes import GoogleSheetsClient
import time
from datetime import datetime
import pandas as pd
import datetime




#! get_params(): returns the worksheet title of a given sheet id.
def get_params(sheet_id, sheet_index):
    sheetclient = GoogleSheetsClient()
    sheet_params = sheetclient.get_params(sheet_id, sheet_index)
    return sheet_params

#! count_mentions(): This function will count the number of mentions of another student.
def count_mentions(text):
    count = 0
    for word in text.split(" "):
        if 'class="mention"' in word:
            count += 1
    return count

#! count_words(): This function will count the number of words in a given text.
def count_words(text):
    if "<img src=" in text:
        return 0
    return len(text.split(" "))
    


#! collect_replies(): This function will collect the replies to the questions posted in the Discourse forum.  
def collect_replies(category_name, topic_name, start_time, post_sheet_id):
    load_dotenv()
    baseurl = os.getenv("DISCOURSE_HOST") 
    username = os.getenv("DISCOURSE_USERNAME")
    apikey = os.getenv("DISCOURSE_KEY")
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
    print(replies)
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
    sheetsclient.post_data(post_sheet_id, topic_name, df)
    newclient.get_users()
    #! adds sentiment analysis column
    sheetsclient.add_sent_analysis(post_sheet_id, topic_name, df)
    return df



#! learning_cycle(): This function is the main function that will be called to run the learning cycle. 
#! It will take in the category name, topic name, sheet id, and sheet index as parameters.
def learning_cycle(category_name, topic_name, sheet_id, sheet_index, api_url, api_key, username, post_sheet_id):
    # load_dotenv()
    # baseurl = os.getenv("DISCOURSE_HOST")
    # username = os.getenv("DISCOURSE_USERNAME")
    # apikey = os.getenv("DISCOURSE_KEY")
    newclient = DiscourseClient(api_url, username, api_key)
    sheetclient = GoogleSheetsClient()
    
    questions = sheetclient.get_questions(sheet_id, sheet_index)
    sheet_data = sheetclient.read_data(sheet_id, sheet_index)
    
    try:
        newclient.list_categories()[category_name]
    except KeyError:
        newclient.create_category(category_name, "FF0000", "FFFFFF")
        
    category_id = newclient.list_categories()[category_name]

    try:
        newclient.get_topics()[topic_name]

    except KeyError:
        newclient.create_topic(topic_name, topic_name, category_id)
    
    topic_id = newclient.get_topics()[topic_name]            
    
    start_time = str(datetime.datetime.now(datetime.timezone.utc))
    
    
    
    #! IMPORTANT: POSTS QUESTIONS AND CHALLENGES TO DISCOURSE FORUM, CHANGE PARAMETERS IF NEEDED!!
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
    replies = collect_replies(category_name, topic_name, start_time, post_sheet_id)
    
        
def main():
    pass
    ## Testing purposes
    
    # # sheet_index = 0
    # # title = get_params("1Iy6LzGU1yQ_I4u9o0ueEC3ZrzypOk-d_Jlxq2cLkKsE", sheet_index)
    # # learning_cycle(
    # #     "Weelrn", 
    # #     title, 
    # #     "1Iy6LzGU1yQ_I4u9o0ueEC3ZrzypOk-d_Jlxq2cLkKsE", 
    # #     sheet_index,
    # # )
    # load_dotenv()
    # baseurl = os.getenv("DISCOURSE_HOST")
    # username = os.getenv("DISCOURSE_USERNAME")
    # apikey = os.getenv("DISCOURSE_KEY")
    # # print(baseurl, username, apikey)
    # # newclient = DiscourseClient(baseurl, username, apikey)
    # # newclient.list_categories()
    # start_time = str(datetime.datetime.now(datetime.timezone.utc))
    # collect_replies("Weelrn", "All About Atoms", start_time)
    
    
if __name__ == "__main__":
    main()