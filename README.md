# Reunion Media API

The Social Media API is a web service built using Django, a Python web framework. It provides various endpoints to interact with the social media platform, including user authentication, user profiles, post management, liking posts, commenting on posts, and more.

## API Endpoints

- POST /api/authenticate
  - Description: Perform user authentication and return a JWT token.
  - Input: Email, Password
  - Return: JWT token

- POST /api/follow/{id}
  - Description: Follow a user with {id}.
  - Authentication required.

- POST /api/unfollow/{id}
  - Description: Unfollow a user with {id}.
  - Authentication required.

- GET /api/user
  - Description: Get the user profile of the authenticated user.
  - Return: User Name, number of followers, number of followings.
  - Authentication required.

- POST /api/posts/
  - Description: Create a new post.
  - Input: Title, Description
  - Return: Post-ID, Title, Description, Created Time(UTC).
  - Authentication required.

- DELETE /api/posts/{id}
  - Description: Delete a post with {id} created by the authenticated user.
  - Authentication required.

- POST /api/like/{id}
  - Description: Like a post with {id}.
  - Authentication required.

- POST /api/unlike/{id}
  - Description: Unlike a post with {id}.
  - Authentication required.

- POST /api/comment/{id}
  - Description: Add a comment for a post with {id}.
  - Input: Comment
  - Return: Comment-ID
  - Authentication required.

- GET /api/posts/{id}
  - Description: Get a single post with {id} populated with its number of likes and comments.

- GET /api/all_posts
  - Description: Get all posts created by the authenticated user sorted by post time.
  - Return: List of posts with their details.
  - Authentication required.

## Setup and Installation

Follow these steps to set up the project:

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/social-media-api.git

2. `python3 -m venv env`
`.\Scripts\activate`

3. `pip install -r requirements.txt`

4. `python manage.py migrate`

5. `python manage.py runserver`

6. Access the site locally:

Open a web browser and visit http://localhost:8000.

## Docker
A Dockerfile is provided with the project to run the full web app in a single Docker image. To build and run the Docker container, follow these steps:

1. Build the Docker image:
`docker build -t social-media-api .`

2. Run the docker container:
`docker run -p 8000:8000 social-media-api` 



## Testing
To run the test cases, use the following command:
   `python manage.py test`



## License
This project is licensed under the MIT License.

## Acknowledgements

- Thanks to the Django community for providing an excellent framework for web development.
- Special thanks to any additional resources, libraries, or tutorials that helped in the development of this project.

