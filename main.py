# Loads Flask server when this file is ran and registers /recommend route

from flask import Flask
from app.routes import bp   # bp is the Blueprint (folder of routes grouped together) object which contains the routes; basically a clean way to organize routes in another file

def create_app():    # Factory function to create/build and return the Flask app
    app = Flask(__name__, template_folder="app/templates", static_folder="app/static")       # creates the Flask app instance
    app.register_blueprint(bp)  # registers your API routes
    return app      # returns the app instance

if __name__ == "__main__":      # ensures this block runs only when the script is executed directly
    app = create_app()      
    app.run(debug=True)  # starts the Flask development server (ie. runs the backend for testing)




