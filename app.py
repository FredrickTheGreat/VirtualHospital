from db_init import app
from route import init_routes
init_routes(app)

app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)