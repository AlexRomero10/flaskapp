from flask import Flask
import os
import os.path as path
app = Flask(__name__)	


@app.route('/',methods=["GET"])
def inicio():
    file="contador.txt"
    if path.exists(file):
        with open(file,"r") as fichero:

            contador=int(fichero.read())
            contador=contador+1
    else:
        contador=1
    with open(file,"w") as fichero:
        fichero.write(str(contador))
    try:
        nombre=os.environ["NOMBRE"]
    except:
        nombre="xxx"
    return "<h1>App de: "+nombre+"</h1><br/><h2>"+str(contador)+" visitas.</h2>"

if __name__ == '__main__':
    app.run('0.0.0.0',5002,debug=True)
