from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    input_value = request.form.get('input_value')
    modified_value = input_value + "R"
    return render_template('index.html', input_value=input_value, modified_value=modified_value)

if __name__ == '__main__':
    app.run(debug=True)