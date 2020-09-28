import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy #, or_
from flask_cors import CORS

from .models import setup_db, Book

#
BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
	page = request.args.get('page', 1, type=int)
	start =  (page - 1) * BOOKS_PER_SHELF
	end = start + BOOKS_PER_SHELF

	books = [book.format() for book in selection]
	current_books = books[start:end]
#

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__)
	setup_db(app)
	CORS(app)

	# CORS Headers 
	@app.after_request
	def after_request(response):
		response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
		response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
		return response

	# Functions

	@app.route("/books")	
	def get_books():

		selection = Book.query.order_by(Book.id).all()
		current_books = paginate_books(request, selection)

		if len(current_books) == 0:
			return jsonify({
					"message": "Nothing to show!"
				})

		return jsonify({
				"success":True,
				"books":formatted_books,
				"total_books":len(books)
			})

	@app.route("/books/<int:book_id>")
	def get_book(book_id):
		book = Book.query.get_or_404(book_id)

		return jsonify({
				"book": book.format()
			})


	@app.route("/books/<int:book_id>/edit", methods=['PATCH'])
	def update_book(book_id):

		book = Book.query.get_or_404(book_id)
		rating = request.get_json()['rating']
		book.rating = rating
		book.update()

		return jsonify({
				'success':True
			})

	@app.route("/books/<int:book_id>/delete", methods=['DELETE'])
	def delete_book(book_id):

		book = Book.query.get_or_404(book_id)
		book.delete()

		return jsonify({
				'success':True,
				'deleted':book.id,
			})

	@app.route("/books/create", methods=["POST"])
	def create_book():
		title = request.get_json()['title']
		author = request.get_json()['author']
		rating = request.get_json()['rating']

		book = Book(title=title, author=author, rating=rating)
		book.insert()

		return jsonify({
				"success": True,
				"created": book.id
			})
	#

	# Error handling

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
				"success": False,
				"error": 404,
				"message": "not found"
			}), 404

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({
				"success": False,
				"error": 422,
				"message": "unprocessable"
			}), 422

	@app.errorhandler(405)
	def not_allowed(error):
		return jsonify({
				"success": False,
				"error": 405,
				"message": "not allowed"
			}), 405
	#

	return app