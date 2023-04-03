from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import html
import os
from dotenv import load_dotenv


load_dotenv()


application = Flask(__name__)
application.config['DEBUG'] = True


try:
    client = MongoClient(os.environ['MONGO_URI'])
    db = client.mydatabase


except Exception as e:
    print("Error connecting to MongoDB: ", e)
    exit(1)

@application.route('/enviar', methods=['POST'])
def enviar():
    try:
        name = html.escape(request.json['name'])
        email = html.escape(request.json['email'])
        subject = html.escape(request.json['subject'])
        message = html.escape(request.json['message'])

        if not name or not email or not subject or not message:
            return jsonify({'message': 'All fields are required!'}), 400

        db.contacts.insert_one({
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        })
        return jsonify({'message': 'Submitted Form!'})
    except KeyError:
        return jsonify({'message': 'Invalid request body!'}), 400
    except Exception as e:
        return jsonify({'message': 'Error saving data to MongoDB: ' + str(e)}), 500

@application.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    application.run(port=8000)