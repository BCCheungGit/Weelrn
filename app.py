from flask import Flask, render_template, request
from discoursetest import learning_cycle
app = Flask(__name__)



@app.route('/')
def main_application():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    if request.method == 'POST':
        category_name = request.form.get('category_name') # What is the name of the category that you would like to publish the topic under?
        topic_name = request.form.get('topic_name') # What is the name of the topic for the lesson?
        sheet_id = request.form.get('sheet_id') # What is the id of the spreadsheet that you will grab the questions for
        sheet_index = int(request.form.get('sheet_index')) # What is the index of the spreadsheet that you will use?
        api_url = request.form.get('api_url')
        api_key = request.form.get('api_key')
        username = request.form.get('username')
        post_sheet_id = request.form.get('postsheetid')
        learning_cycle(category_name, topic_name, sheet_id, sheet_index, api_url, api_key, username, post_sheet_id)
        return render_template('index.html')
    else:
        return "Error: Invalid request method"
