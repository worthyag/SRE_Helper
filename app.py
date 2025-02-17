from flask import *

import os
from google import genai
from google.genai import types

import pymysql
import traceback
import pymysql.cursors

# genai.configure(api_key=os.environ["GEMINI_API_KEY"])

prompts = [
    "As a Site Reliability Engineer, how do you diagnose and handle high CPU load on production systems? Provide best practices for monitoring, alerting, and remediation.",
    "As a Site Reliability Engineer, how do you troubleshoot disk space issues? Provide steps for diagnosing, monitoring, and preventing disk exhaustion.",
    "What are the best practices for handling high network load as a Site Reliability Engineer? Include guidance on identifying bottlenecks, monitoring traffic, and optimising performance.",
    "As a Site Reliability Engineer, how do you address memory-related performance issues? Provide advice on monitoring, diagnosing memory leaks, and optimising usage."
]

app = Flask("SRE Helper")

# app.config["MYSQL_HOST"] = "192.168.2.136"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "sreUser"
app.config["MYSQL_PASSWORD"] = "password12-"
app.config["MYSQL_DB"] = "sreHelper"
app.config["MYSQL_PORT"] = 3306

# Database Configuration
db_config = {
    "host": app.config["MYSQL_HOST"],
    "user": app.config["MYSQL_USER"],
    "password": app.config["MYSQL_PASSWORD"],
    "database": app.config["MYSQL_DB"],
    "port": app.config["MYSQL_PORT"]
}


def get_db_connection():
    # Returning the rows as dictionaries to make them easier to work with.
    return pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)


def create_table(cursor):
    # Selecting the database.
    cursor.execute("USE sreHelper")

    # Creating the table.
    cursor.execute("""CREATE TABLE IF NOT EXISTS library (
                    book_id INT AUTO_INCREMENT PRIMARY KEY,
                    book_name VARCHAR(500) NOT NULL,
                    book_author VARCHAR(500) NOT NULL,
                    book_desc VARCHAR(2000)
                   )""")
    return cursor


def start_db_connection():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            create_table(cursor)
            # Making sure that the changes persist.
            connection.commit()
    # Returning a new connection for further use.
    return get_db_connection()


def get_error(e, msg=None):
    error_message = str(e)
    error_trace = traceback.format_exc()

    msg = "Error occurred." if msg is None else msg
    return jsonify({"error": f"{msg}\nError msg: {error_message}\nError trace: {error_trace}"}), 500


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/advice", methods=['POST'])
def advice():
    prompt_selection = request.form.get("prompt-selection")

    prompt_map = {
        "cpu": 0,
        "disk": 1,
        "network": 2,
        "memory": 3
    }

    print(f"prompt_map: {prompt_map[prompt_selection]}")

    client = genai.Client(api_key=os.environ["SRE_HELPER_GEMINI_API_KEY"])
    prompt = prompts[prompt_map[prompt_selection]]

    print(f"prompt: {prompts[prompt_map[prompt_selection]]}")

    # if prompt is None:
    #     return "Invalid selection", 400

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{prompt}",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a staff senior reliability engineer who is giving advice to your juniors",
                "Format your entire response using valid HTML, including headers, paragraphs, and lists.",
                "Ensure the content is user-friendly and professional. Add colours and modern UI styling to make the content captivating."
            ),
            response_mime_type="text/plain"
        )
    )
    # Strip leading/trailing code block markers if present
    cleaned_response = (response.text.lstrip("```html")).rstrip("```")
    return render_template("advice.html", res=cleaned_response)


@app.route("/library", methods=['GET'])
def viewLibrary():
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Selecting all the books.
                cursor.execute("SELECT * FROM library")

                # Fetching all the results.
                all_books = cursor.fetchall()

                if all_books:
                    return render_template("library.html", books=all_books)
                return render_template("emptyLibrary.html")

    except Exception as e:
        return get_error(e)
    return render_template("library.html")


@app.route("/library/add/")
def addBook():
    return render_template("addBook.html")


@app.route("/library/view/", methods=['POST'])
def viewBook():
    book_id = request.form.get("book-id")

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Selecting a specific book.
                sql = "SELECT * FROM library WHERE book_id = %s"
                cursor.execute(sql, (book_id,))
                selected_book = cursor.fetchone()

                if selected_book:
                    return render_template("viewBook.html", book=selected_book)
                else:
                    return jsonify({"message": f"Book not found {book_id}"}), 404
    except Exception as e:
        return get_error(e)


@app.route("/library/search/<id>/", methods=['GET'])
def getBook(id):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM library WHERE book_id = %s"
                cursor.execute(sql, (id,))
                selected_book = cursor.fetchone()

                if selected_book:
                    return render_template("viewBook.html", movie=selected_book)
                else:
                    return jsonify({"message": "Book not found"}), 404
    except Exception as e:
        return get_error(e)


@app.route("/library/save/", methods=["POST"])
def addedBook():
    book_name = request.form.get("book-name")
    book_author = request.form.get("book-author")
    book_desc = request.form.get("book-desc")

    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = "INSERT INTO library (book_name, book_author, book_desc) VALUES (%s, %s, %s)"
                cursor.execute(sql, (book_name, book_author, book_desc))
                # Committing the transaction.
                connection.commit()
                return render_template("saved.html", book_name=book_name, book_author=book_author, book_desc=book_desc)
    except Exception as e:
        return get_error(e, "Error occurred when adding book. Book not added.")


# Creating the table
start_db_connection()
app.run(host="0.0.0.0", port=5002)

# mimetypes are `text/plain`, `application/json` and `text/x.enum
