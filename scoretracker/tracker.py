import connexion
import requests

app = connexion.FlaskApp(__name__, specification_dir='.')
app.add_api('swagger.yaml')
app.run(port=80)

def recv_msg():
    return connexion.jsonify(connexion.request.json), 501
