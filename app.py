"""
copy of main project to try pagination ((success))
to try search categorization ((succes)) but not working properly with pagination
"""
from Urology_app import create_app
## to show you all the available endpoints and their corresponding rules
# with Urology_app.test_request_context():
#     print(Urology_app.url_map)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)