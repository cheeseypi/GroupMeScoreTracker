import os

import connexion

PORT=int(os.environ.get('SCORETRACKER_PORT','6660'))

app = connexion.FlaskApp(__name__, specification_dir='.')
app.add_api('swagger.yaml')
app.run(port=PORT)
