# flaskr

### Requirements
```bash
createdb bookshelf

pip3 install Flask-SQLAlchemy==2.4.4
pip3 install Flask-Cors==3.0.9
```
### Endpoints 
  * curl http://localhost:5000/books ```Retrieve all books```
  * curl http://localhost:5000/books/book_id ```get a specific book```
  * curl http://localhost:5000/books/search?q=search_term ```Search for a book```
  * curl http://localhost:5000/books/create ```Create a new book```
  * curl http://localhost:5000/books/book_id/edit ```Edit a book```
  * curl http://localhost:5000/books/book_id/delete ```Delete a book```
  
<hr>

### Run tests
```bash
createdb bookshelf_test
python3 test_flaskr.py
```