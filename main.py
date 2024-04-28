from flask import Flask
from website import create_app

# Run website with "flask --app main run"

app = create_app()

if __name__ == '__main__':  # only run this file if running "main" not other files
    app.run(debug=True)  # turn off debug flag when running in prod