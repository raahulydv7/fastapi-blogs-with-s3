# Blog API Platform
A high-performance RESTful API for blog management with image upload capabilities, built with FastAPI, SQLAlchemy, and AWS S3 integration.

## Features
### Authentication
- JWT-based authentication system
- Secure password hashing with bcrypt
- Protected routes with token validation
- User registration and login functionality

### Blog Management
- Create, read, update, and delete blog posts
- Image uploads with AWS S3 integration
- User-specific blog listing
- Owner-only blog modifications

### Technical Implementation
- High-performance API with FastAPI
- ORM using SQLAlchemy
- PostgreSQL database
- Secure image storage in AWS S3
- Clean architecture with separation of concerns

## Project Structure
```
├── config.py          # Environment variables and configuration settings
├── database.py        # Database connection and session management
├── models.py          # SQLAlchemy ORM models
├── schemas.py         # Pydantic validation schemas
├── crud.py            # Database operations
├── s3_service.py      # S3 image upload and deletion management
└── main.py            # FastAPI application and route definitions
```

## Setup
### Prerequisites
- Python 3.8 or higher
- PostgreSQL
- AWS account with S3 bucket

### Environment Variables
Create a `.env` file with the following variables:
```
# Database
DATABASE_URL=postgresql://user:password@localhost/db_name

# JWT
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AWS S3
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=your_bucket_name
S3_REGION=your_region
```

### Installation
#### Clone the repository
```bash
git clone https://github.com/username/blog-api.git
cd blog-api
```

#### Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
```

#### Create the database
```bash
python -m scripts.create_db
```

#### Run the application
```bash
uvicorn main:app --reload
```

## API Endpoints
### Authentication
- `POST /users/register` - Register a new user
- `POST /users/login` - Login and get access token

### Blog Management
- `POST /blogs/` - Create a new blog post with image
- `GET /blogs/` - Get all blogs for the authenticated user
- `GET /blogs/{blog_id}` - Get a specific blog
- `PUT /blogs/{blog_id}` - Update a blog post
- `DELETE /blogs/{blog_id}` - Delete a blog post

## Development
### Dependencies
Main dependencies:
- FastAPI
- SQLAlchemy
- Pydantic
- Python-jose (JWT)
- Passlib
- Boto3 (AWS S3)
- Python-multipart (for file uploads)

#### Install development dependencies:
```bash
pip install -r requirements-dev.txt
```
