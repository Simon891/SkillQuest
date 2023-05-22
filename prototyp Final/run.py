import os
from flask import Flask, render_template, request, Markup, jsonify, flash, redirect, url_for
import topicS
import title_finder

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Replace with your desired secret key

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_input', methods=['POST'])
def process_input():
    input_value = request.form.get('input_value')
    modified_value = title_finder.match_job_ads(input_value)
    flash('yay')
    return render_template('index.html', input_value=input_value, modified_value=Markup(modified_value))

@app.route('/send_selected', methods=['POST'])
def send_selected():
    selected_html = request.json['selected_html']
    retur_html, antal = topicS.main(selected_html)
    flash('Selected HTML received successfully.')
    return jsonify({
        'retur': retur_html,
        'antal': antal
                    })

if __name__ == '__main__':
    app.run(debug=True)
