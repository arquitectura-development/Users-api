from flask import Flask, jsonify, request

def is_valid(token):
    if not token:
        return False
    elif len(token)==0:
        return False
    else:
        return True



def search(user):
    line_counter = 0
    file_users = open("users.txt", "r")
    for line in file_users:
        word = line.split('%')
        word[2]= word[2][:len(word[2])-1]
        line_counter = int(word[0])
        if user in word[1] and len(word[1]) == len(user):
            file_users.close()
            return word, line_counter
    file_users.close()
    return list(), line_counter

def search_id(user):
    file_users = open("users.txt", "r")
    for line in file_users:
        word = line.split('%')
        word[2]= word[2][:len(word[2])-1]
        if user == word[0]:
            file_users.close()
            return word
    file_users.close()
    return list()


def delete_by_id(user):
    found=0
    buffer = ""
    file_users = open("users.txt", "r")
    for line in file_users:
        word=line.split('%')
        if word[0] != user:
            buffer = buffer + line
        else:
            found=1
    file_users.close()
    file_changer = open("users.txt", "w")
    file_changer.write(buffer)
    file_changer.close()
    return found


application = Flask(__name__)
#print(__name__)

@application.route('/', methods = ['GET'])
def is_alive():
    return jsonify(success=True), 200


@application.route('/users/signup', methods = ['POST'])
def create():
    content = request.get_json()

    if not is_valid(content) or not 'name' in content or not 'email' in content:
        return jsonify(success=False), 400

    elif not is_valid(content['name']) or not is_valid(content['email']):
        return jsonify(success=False), 400

    else:
        word, line_counter=search(content['email'])
        line_counter = line_counter+1

        if not word:
            filetocreate=open("users.txt", "a+")
            filetocreate.write(str(line_counter)+"%"+content['email']+"%"+content['name']+"\n")
            filetocreate.close()
            return jsonify(success=True, email=content['email'], id=line_counter, name=content['name']), 201

        else:
            return jsonify(success=False), 409



@application.route('/users/login', methods =['POST'])
def login():
    content = request.get_json()
    if not 'email' in content:
        return jsonify(success=False), 400
    elif len(content['email'])==0:
        return jsonify(success=False), 400
    else:
        word,_= search(content['email'])
        if word:
            return jsonify(success=True, email=word[1], id=word[0], name=word[2]), 200
        else:
            return jsonify(success=False), 404


@application.route('/admin/users/name', methods =['GET'])
def name():
    user_id = request.args.get('userId')
    searchUserid = request.args.get('searchUserId')
    if userId != '0':
        return jsonify(success=False), 401
    if is_valid(searchUserid):
        word = search_id(searchUserid)
        if word:
            return jsonify(success=True, email=word[1], name=word[2]), 200

    return jsonify(success=False), 404

@application.route('/users/auth', methods =['GET'])
def auth():
    userid = request.args.get('userId')
    if is_valid(userid):
        word= search_id(userid)
        if word:
            return jsonify(success=True), 200

    return jsonify(success=False), 404


@application.route('/users/delete', methods=['DELETE'])
def delete():
    userid=request.args.get('userId')
    if userid==str(0):
        return jsonify(success=False), 403

    if is_valid(userid):
        found = delete_by_id(userid)
        if found == 1:
            return jsonify(success=True), 200

    return jsonify(success=False), 404


if __name__ == '__main__':
    application.run()
