from flask import Flask, make_response,request
data =  [
    {"id": "66c09925-589a-43b6-9a5d-d1601cf53287",
  "first_name": "Westley",
  "last_name": "Birch",
  "email": "wbirch0@networksolutions.com",
  "gender": "Male",
  "ip_address": "75.149.143.252"
}, {
  "id": "66c09925-589a-43b6-9a5d-d1601of53287",
  "first_name": "Olivero",
  "last_name": "Davidovici",
  "email": "odavidovici1@cpanel.net",
  "gender": "Male",
  "ip_address": "92.79.225.111"
}, {
  "id": "66c09925-589a-43b6-9a5d-d1601cuu3287",
  "first_name": "Maurice",
  "last_name": "Pelham",
  "email": "mpelham2@biblegateway.com",
  "gender": "Male",
  "ip_address": "218.100.112.143"
}, {
  "id": "66889925-589a-43b6-9a5d-d1601cf53287",
  "first_name": "Tan",
  "last_name": "Sclater",
  "email": "tsclater3@example.com",
  "gender": "Male",
  "ip_address": "6.159.242.152"
}]

# Create an instance of the Flask class, passing in the name of the current module
app = Flask(__name__)
# Define a route for the root URL ("/")
@app.route("/")
def index():
    # Function that handles requests to the root URL
    # Return a plain text response
    return "hello nothing"

# Define a route for the "/no_content" URL
@app.route("/no_content")
def no_content():

    # Create a dictionary with a message and return it with a 204 No Content status code
    return ({"message": "No content found"}, 204)

# Define a route for the "/exp" URL
@app.route("/exp")
def index_explicit():

    # Create a response object with the message "Hello World"
    resp = make_response({"message": "Hello World"})
    # Set the status code of the response to 200
    resp.status_code = 200
    # Return the response object
    return resp


@app.route("/data")
def get_data():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404


@app.route("/name_search")
def name_search():
    """Find a person in the database based on the provided query parameter.

    Returns:
        json: Person if found, with status of 200
        404: If not found
        422: If the argument 'q' is missing
    """
    # Get the 'q' query parameter from the request URL
    query = request.args.get("q")

    # Check if the query parameter 'q' is missing or empty
    if not query:
        # Return a JSON response with a message indicating invalid input and a 422 Unprocessable Entity status code
        return {"message": "Invalid input parameter"}, 422

    # Iterate through the 'data' list to search for a matching person
    for person in data:
        # Check if the query string is present in the person's first name (case-insensitive)
        if query.lower() in person["first_name"].lower():
            # Return the matching person as a JSON response with a 200 OK status code
            return person

    # If no matching person is found, return a JSON response with a message and a 404 Not Found


@app.route("/count")
def count():
    try:
        # Attempt to return the count of items in 'data' as a JSON response
        return {"data count": len(data)}, 200
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a message and a 500 Internal Server Error status code
        return {"message": "data not defined"}, 500

@app.route("/person/<uuid:id>")
def find_by_uuid(id):
    # Iterate through the 'data' list to search for a person with a matching ID
    for person in data:
        # Check if the 'id' field of the person matches the 'id' parameter
        if person["id"] ==id:
            # Return the matching person as a JSON response with a 200 OK status code
            return person
    # If no matching person is found, return a JSON response with a message and a 404 Not Found status code
    return {"message": "person not found"}, 404

@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    # Iterate through the 'data' list to search for a person with a matching ID
    for person in data:
        # Check if the 'id' field of the person matches the 'id' parameter
        if person["id"] == str(id):
            # Remove the person from the 'data' list
            data.remove(person)
            # Return a JSON response with a message confirming deletion and a 200 OK status code
            return {"message": f"Person with ID {id} deleted"}, 200
    # If no matching person is found, return a JSON response with a message and a 404 Not Found status code
    return {"message": "person not found"}, 404

@app.route("/person", methods=['POST'])
def add_by_uuid():
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    # code to validate new_person ommited
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500

    return {"message": f"{new_person['id']}"}, 200

@app.errorhandler(404)
def api_not_found(error):
    # This function is a custom error handler for 404 Not Found errors
    # It is triggered whenever a 404 error occurs within the Flask application
    return {"message": "API not found"}, 404