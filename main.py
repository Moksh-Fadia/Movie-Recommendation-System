# Loads/creates Flask app when this file is ran and connects/registers the /recommend route. It starts the server

from flask import Flask
from app.routes import bp   # bp is the Blueprint (folder of routes grouped together) object which contains/stores the routes; basically a clean way to organize routes in a file, eg: @bp.route()


# Without Blueprint:
# main.py
#  ├─ route1
#  ├─ route2
#  ├─ route3
#  ├─ route4
#  ├─ route5
# Everything dumped into one room/all inside one file

# With Blueprint:
# main.py
# routes.py
#  ├─ route1
#  ├─ route2
#  ├─ route3
# Cleaner and organized


def create_app():    # Factory function to create/build and return the Flask app
    app = Flask(     # creates the Flask app object
    __name__,       # tells Flask where to look for resources (like templates and static files); __name__ is a special variable in Python that holds the name of the current module/file
    template_folder="app/templates",     # tells Flask where to look for HTML templates (the folder where our HTML files are stored)
    static_folder="app/static"      # tells Flask where to look for static files (like CSS, JS, images)
)       
# this creates the Flask app instance

    app.register_blueprint(bp)      # registers/imports all API routes
    return app      # returns the app instance

if __name__ == "__main__":      # ensures this block runs only when the script is executed directly
    app = create_app()      
    app.run(debug=True)  # starts the Flask development server (ie. runs the backend for testing)




