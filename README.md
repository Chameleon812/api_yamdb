# Group project of Yandex.Workshop students on the course "API: program interaction interface"

The YaMDb project collects user feedback on works. Works are not stored in YaMDb, you can not watch a movie or listen to music here.

## Functionality

- JWT tokens are used for authentication.
- Unauthenticated users have read-only access to the API.
- Creation of objects is allowed only for authenticated users.
- Getting a list of all categories and genres, adding and deleting.
- Getting a list of all works, adding them. Obtaining, updating and deleting a specific work.
- Getting a list of all reviews, adding them. Get, update, and delete specific feedback.
- Getting a list of all comments, adding them. Getting, updating and deleting a specific comment.
- Ability to get detailed information about yourself and delete your account.
- Filtering by fields.

### The API documentation is available at [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) after the server has started


### Instructions
 
- Install and activate the virtual environment:
``` python -m venv venv ```
- Install dependencies from requirements.txt file:
``` pip install -r requirements.txt ```
- Apply migrations:
``` python manage.py migrate ```

### Examples of some API requests

User registration:
```
    POST /api/v1/auth/signup/ 
```
Getting your account information:
```
    GET /api/v1/users/me/
```
Adding a new category:
```
    POST /api/v1/categories/
```
Removing a genre:
```
    DELETE /api/v1/genres/{slug}
```
Partial update of information about the work:
```
    PATCH /api/v1/titles/{titles_id}
```
Getting a list of all reviews:
```
    GET /api/v1/titles/{title_id}/reviews/
```
Adding a comment to a review:
```
    POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```    

The full list of API requests are in the documentation
