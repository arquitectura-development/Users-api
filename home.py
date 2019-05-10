from flask import Flask, jsonify
def search(user):
    admins =0
    found = 0

    file_users = open("users.txt", "r")
    file_admins =open("admins.txt", "r")

    for line in file_admins:
        line = line[:len(line)-1]
        if user in line and len(user) == len(line):
                admins=1
                found =1
                break

    if admins == 0:
        for line in file_users:
            line = line[:len(line)-1]
            if user in line and len(user) == len(line):
                found = 1
                break
    return admins, found

app = Flask(__name__)


@app.route('/create/<user>')
def create(user):
    admins, found = search(user)
    if found==1 and admins==0:
        return jsonify({"response": "User "+user+" ya existe"})
    else:
        filetocreate=open("users.txt", "a+")
        filetocreate.write(user+"\n")
        return jsonify({"response": "Se ha creado el user "+user})

@app.route('/login/<user>')
def login(user):
    admins, found = search(user)
    if found ==0:
        #print("El usuario no existe")
        return jsonify({"response": "User "+user+" no existe"})
    elif found ==1 and admins==1:
        #print("Bienvenido administrador")
        return jsonify({"response": "Bienvenido administrador "+user})
    else:
        #print("Bienvenido")
        return jsonify({"response": "Bienvenido "+user})

if __name__ == '__main__':
    app.run(debug=True)
