from flask import Flask, jsonify
from flask import request

def search(user):
    line_counter = -1
    file_users = open("users.txt", "r")
    for line in file_users:
        line_counter = line_counter+1
        word = line.split('%')
        word[2]= word[2][:len(word[2])-1]
        if user in word[1] and len(word[1]) == len(user):
            return word, line_counter
    return list(), line_counter

def searchId(user):
    file_users = open("users.txt", "r")
    for line in file_users:
    #    print(line)
        word = line.split('%')
        word[2]= word[2][:len(word[2])-1]
        if user == word[0]:
            return word
    return list()

application = Flask(__name__)
#print(__name__)

@application.route('/', methods = ['GET'])
def isAlive():
    return jsonify(success=True), 200

@application.route('/users/signup', methods = ['POST'])
def create():
    content = request.get_json()
    if not 'name' in content or not 'email' in content:
        return jsonify(success=False), 400

    word, line_counter=search(content['email'])
    line_counter = line_counter+1

    if not word:
        filetocreate=open("users.txt", "a+")
        filetocreate.write(str(line_counter)+"%"+content['email']+"%"+content['name']+"\n")
        return jsonify(success=True, email=content['email'], id=line_counter, name=content['name']), 201

    else:
        return jsonify(success=False), 409



@application.route('/users/login', methods =['POST'])
def login():
    content = request.get_json()
    #print(content)
    if not 'email' in content:
        return jsonify(success=False), 400

    word,_= search(content['email'])
    #print(word)
    if word:
        return jsonify(success=True, email=word[1], id=word[0], name=word[2]), 200
    else:
        return jsonify(success=False), 404


@application.route('/users/name')
def name():
    userid = request.args.get('userId')
#    print(userid)
    word= searchId(userid)
    if word:
        return jsonify(success=True, email=word[1], name=word[2]), 200
    else:
        return jsonify(success=False), 404


@application.route('/users/auth')
def auth():
    userid = request.args.get('userId')
    #print(userid)
    word= searchId(userid)
    if word:
        return jsonify(success=True), 200
    else:
        return jsonify(success=False), 404


if __name__ == '__main__':
    application.run()
