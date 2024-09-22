from flask import Flask, jsonify, request, render_template
import requests
import logging

app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Open Library API URL
OPEN_LIBRARY_API_URL = "https://openlibrary.org/search.json"


# Fetch books based on search criteria
def fetch_books(query_params):
    try:
        response = requests.get(OPEN_LIBRARY_API_URL, params=query_params)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
        return {"error": f"HTTP Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Connection Error: {errc}")
        return {"error": f"Connection Error: {errc}"}
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
        return {"error": f"Timeout Error: {errt}"}
    except requests.exceptions.RequestException as err:
        logging.error(f"Request Exception: {err}")
        return {"error": f"Request Exception: {err}"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/books")
def get_books():
    query = request.args.get("query")
    author = request.args.get("author")
    isbn = request.args.get("isbn")
    publish_year = request.args.get("publish_year")

    if not query and not author and not isbn and not publish_year:
        return jsonify({"error": "Missing query parameters"}), 422

    # Define the search parameters for the API
    query_params = {}
    if query:
        query_params["title"] = query
    if author:
        query_params["author"] = author
    if isbn:
        query_params["isbn"] = isbn
    if publish_year:
        query_params["publish_year"] = publish_year

    data = fetch_books(query_params)

    if "error" in data:
        return jsonify(data), 500

    # Filter the results based on the publish_year parameter if provided
    filtered_books = data["docs"]
    if publish_year:
        try:
            publish_year = int(publish_year)  # Ensure it's an integer
            # Filter books to include only those with the specified publish year in their list
            filtered_books = [
                book
                for book in data["docs"]
                if "publish_year" in book and publish_year in book["publish_year"]
            ]
        except ValueError:
            return jsonify({"error": "Invalid publish year format"}), 422

    # Return the filtered or original data to the client
    return jsonify(filtered_books)


@app.route("/book/<isbn>")
def get_book_by_isbn(isbn):
    if not isbn:
        return jsonify({"error": "ISBN parameter is missing"}), 422

    query_params = {"isbn": isbn}
    data = fetch_books(query_params)

    if "error" in data:
        return jsonify(data), 500

    # Assuming that the first result is the best match
    if data["docs"]:
        return jsonify(data["docs"][0])
    else:
        return jsonify({"error": "Book not found"}), 404


# Error Handler for 404 Not Found
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Resource not found"}), 404


# Error Handler for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)
