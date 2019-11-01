from application import create_app

## Starting point for hosting using WSGI.
## Set up application
app = create_app()

## Run application
if __name__ == "__main__":
    app.run()
