from flask import Flask, render_template, request
from discoursetest import learning_cycle
app = Flask(__name__)



@app.route('/')
def main_application():
    return render_template('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        topic_name = request.form.get('topic_name')
        sheet_id = request.form.get('sheet_id')
        sheet_index = int(request.form.get('sheet_index'))
        api_url = request.form.get('api_url')
        api_key = request.form.get('api_key')
        username = request.form.get('username')
        learning_cycle(category_name, topic_name, sheet_id, sheet_index, api_url, api_key, username)
        return render_template('index.html')
    else:
        return "Error: Invalid request method"
