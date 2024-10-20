from flask import Flask, jsonify, request, render_template
import requests
import logging

app = Flask(__name__)

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Google Books API URL
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


# Fetch books based on search criteria
def fetch_books(query_params):
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=query_params)
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

    # Define the search parameters for the Google Books API
    query_params = {}
    search_query = ""
    if query:
        search_query += f"+intitle:{query}"
    if author:
        search_query += f"+inauthor:{author}"
    if isbn:
        search_query += f"+isbn:{isbn}"

    query_params["q"] = search_query.strip("+")  # Prepare the search query

    # Get the data from Google Books API
    data = fetch_books(query_params)

    if "error" in data:
        return jsonify(data), 500

    # Filter the results based on the publish_year parameter if provided
    filtered_books = data.get("items", [])
    if publish_year:
        try:
            publish_year = int(publish_year)  # Ensure it's an integer
            filtered_books = [
                book for book in filtered_books
                if "publishedDate" in book["volumeInfo"] and
                str(publish_year) in book["volumeInfo"]["publishedDate"]
            ]
        except ValueError:
            return jsonify({"error": "Invalid publish year format"}), 422

    # Format the response to include relevant information from Google Books API
    results = [
        {
            "title": book["volumeInfo"].get("title"),
            "authors": book["volumeInfo"].get("authors"),
            "publishedDate": book["volumeInfo"].get("publishedDate"),
            "description": book["volumeInfo"].get("description"),
            "isbn": [identifier["identifier"] for identifier in book["volumeInfo"].get("industryIdentifiers", [])],
            "thumbnail": book["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
        }
        for book in filtered_books
    ]

    return jsonify(results)


@app.route("/book/<isbn>")
def get_book_by_isbn(isbn):
    if not isbn:
        return jsonify({"error": "ISBN parameter is missing"}), 422

    query_params = {"q": f"isbn:{isbn}"}
    data = fetch_books(query_params)

    if "error" in data:
        return jsonify(data), 500

    if data.get("items"):
        book = data["items"][0]
        return jsonify({
            "title": book["volumeInfo"].get("title"),
            "authors": book["volumeInfo"].get("authors"),
            "publishedDate": book["volumeInfo"].get("publishedDate"),
            "description": book["volumeInfo"].get("description"),
            "isbn": [identifier["identifier"] for identifier in book["volumeInfo"].get("industryIdentifiers", [])],
            "thumbnail": book["volumeInfo"].get("imageLinks", {}).get("thumbnail"),
        })
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
