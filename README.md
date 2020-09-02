# Casting Agency Project

As conclusion of the Full Stack ND program, this project was built outlining skills acquired throughout the journey regarding Python, relational databases, RESTful APIs, manage user authentication and access control using Auth0 and deploy database-backed web APIs.

The Casting Agency models a company that is responsible for creating movies, managing and assigning actors to those movies.

## Casting Agency Project is Hosted on Heroku

```bash
https://app-casting-agency.herokuapp.com/
```

you can try the endpoints using Postman or Curl.
Tokens for each role are provided in setup.sh file to let you make an authorized request.

## Authorization
The API uses the Auth0 Role Based Access Control mechanisms for implementing authorization for each endpoint. The following permissions are currently accepted;

 * get:actors
 * get:movies
 * post:actors
 * post:movies
 * patch:actors
 * patch:movies
 * delete:actors
 * delete:movies

### Roles:
 * Casting Assistant
   - Can view actors and movies

 * Casting Director
   - All permissions a Casting Assistant has and…
   - Add or delete an actor from the database
   - Modify actors or movies

 * Executive Producer
   - All permissions a Casting Director has and…
   - Add or delete a movie from the database

## Endpoints:
GET '/actors'
- Fetches actors information from the server
- Request argument: None
- Request body: None
- Response:
```
{
	"actors": [
		{
			"age": "45",
			"gender": "Male",
			"id": 1,
			"name": "Leonardo DiCaprio"
		},
		{
			"age": "56",
			"gender": "Male",
			"id": 2,
			"name": "Brad Pitt"
		},
		{
			"age": "45",
			"gender": "Female",
			"id": 3,
			"name": "Angelina Jolie"
		},
		{
			"age": "44",
			"gender": "Male",
			"id": 8,
			"name": "Ryan Reynlods"
		}
	],
	"success": true
}
```

GET '/movies'
- Fetches movies information from the server
- Request argument: None
- Request body: None
- Response:
```
{
	"movies": [
		{
			"id": 1,
			"release_date": "2000",
			"title": "The mask"
		},
		{
			"id": 2,
			"release_date": "2010",
			"title": "Monster House"
		},
		{
			"id": 3,
			"release_date": "2019",
			"title": "Despicable Me"
		},
		{
			"id": 8,
			"release_date": "1999",
			"title": "Mulan"
		}
	],
	"success": true
}
```

DELETE '/actors/{actor_id}'
- Deletes the actor of the given ID if it exists.
- Request argument: actor_id:int
- Request body: None
- Response:
```
{
	"actor": {
		"age": "44",
		"gender": "Male",
		"id": 8,
		"name": "Ryan Reynlods"
	},
	"success": true
}
```

DELETE '/movies/{movie_id}'
- Deletes the movie of the given ID if it exists.
- Request argument: movie_id:int
- Request body: None
- Response:
```
{
	"movie": {
		"id": 8,
		"release_date": "1998",
		"title": "Mulan"
	},
	"success": true
}
```

POST '/actors'
- Creates a new actor into the server.
- Request argument: None
- Request body: {name:string, age=string , gender:string}
- Response:
```
{
	"actor": {
		"age": "43",
		"gender": "Male",
		"id": 8,
		"name": "Ryan Reynlods"
	},
	"success": true
}
```

POST '/movies'
- Creates a new actor into the server.
- Request argument: None
- Request body: {title:string, release_date:string}
- Response:
```
{
	"movie": {
		"id": 8,
		"release_date": "1999",
		"title": "Mulan"
	},
	"success": true
}
```

PATCH '/actors/{actor_id}'
- Edits the actor of the given ID if it exists.
- Request argument: actor_id:int
- Request body: {name:string, age=string , gender:string}
- Response:
```
{
	"actor": {
		"age": "44",
		"gender": "Male",
		"id": 8,
		"name": "Ryan Reynlods"
	},
	"success": true
}
```

PATCH '/movies/{movie_id}'
- Edits the movie of the given ID if it exists.
- Request argument: movie_id:int
- Request body:{title:string, release_date:string}
- Response:
```
{
	"movie": {
		"id": 8,
		"release_date": "1998",
		"title": "Mulan"
	},
	"success": true
}
```

## Error Handling
* Error example:

```
  {
   "success": False,
   "error": 404,
   "message": "not found"
  }
```

The errors that may occur:

  * 400: Bad Request
  * 400: Permissions were not included in the JWT.
  * 400: Unable to parse authentication token.
  * 400: Unable to parse authentication token.
  * 400: Unable to find the appropriate key.
  * 401: Authorization header is expected.
  * 401: Authorization header must start with "Bearer".
  * 401: Token not found.
  * 401: Authorization header must be bearer token.
  * 401: Authorization malformed.
  * 401: Token expired.
  * 401: Incorrect claims. Please, check the audience and issuer.
  * 403: Permission not found.
  * 405: Method not allowed.
  * 404: Not found.
  * 422: Unprocessable.

## Getting Started Locally

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### setting the user jwts, auth0 credentials

After installing the dependencies, navigate to the project directory and execute the following command to set the user jwts, auth0 credentials:

```bash
source setup.sh
```

## Database Setup

Restore a database using the Casting_Agency.psql file provided. After create a database named casting_agency on Postgres, in terminal run:

```bash
psql casting_agency < Casting_Agency.psql
```

## Running the server

From within the `./app` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Testing

To run the tests, run
```bash
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < Casting_Agency.psql
python test_app.py
```
