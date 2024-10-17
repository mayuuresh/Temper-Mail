from datetime import datetime
from flask import Flask, render_template, request
from tempmail import EMail

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_mail', methods=['GET'])
def generate_mail():
    email = EMail()
    generated_email = email.address
    inbox_messages = email.get_inbox()
    return render_template('index.html', email=generated_email, inbox_messages=inbox_messages)

@app.route('/inbox', methods=['GET'])
def inbox():
    sender_name=""
    email_address = request.args.get('email')
    inbox_messages = []
    message_content = None

    if email_address:
        email = EMail(email_address)
        inbox_messages = email.get_inbox()

        if inbox_messages:
            for message in inbox_messages:
                cleaned_message = message.message.body.replace('\n', ' ').strip()
                message.message.body = cleaned_message
                message_content = cleaned_message  
        if inbox_messages:
            sender_name = inbox_messages[0].from_addr        
        
                
    current_time = datetime.now().strftime("%H:%M")
    return render_template('index.html', email=email_address,From=sender_name, inbox_messages=inbox_messages, message_content=message_content, current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True)
