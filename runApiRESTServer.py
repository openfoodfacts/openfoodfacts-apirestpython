from flask_rest_service import app
import os

port = int(os.environ.get('PORT', 5000))
app.run(debug=True,host= '0.0.0.0',port=port)