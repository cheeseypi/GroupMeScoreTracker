import connexion

def recv_msg():
    return connexion.jsonify(connexion.request.json), 501
