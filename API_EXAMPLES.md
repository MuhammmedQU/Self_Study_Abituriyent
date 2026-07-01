# LMS API Usage Examples

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication Endpoints

### Register User
```bash
POST /auth/register
Content-Type: application/json

{
  "full_name": "John Doe",
  "email": "john@example.com",
  "password": "Password123"
}

Response:
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "email": "john@example.com",
    "full_name": "John Doe"
  }
}
```

### Login
```bash
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "Password123"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_id": 1,
    "email": "john@example.com"
  }
}
```

### Refresh Token
```bash
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

Response:
{
  "success": true,
  "data": {
    "access_token": "new-token...",
    "refresh_token": "new-refresh-token..."
  }
}
```

### Logout
```bash
POST /auth/logout
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "message": "Logged out successfully"
}
```

## Admin Endpoints

### Create Course
```bash
POST /admin/courses
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Python Basics",
  "description": "Learn Python from scratch",
  "thumbnail_path": "courses/python.png"
}

Response:
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Python Basics"
  }
}
```

### Get All Courses
```bash
GET /admin/courses?skip=0&limit=100
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Python Basics"
    }
  ]
}
```

### Create Module
```bash
POST /admin/modules
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "course_id": 1,
  "title": "Module 1: Basics",
  "description": "Introduction to Python",
  "order": 0
}

Response:
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Module 1: Basics"
  }
}
```

### Create Lesson
```bash
POST /admin/lessons
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "module_id": 1,
  "title": "Lesson 1: Variables",
  "description": "Understanding variables",
  "order": 0
}

Response:
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Lesson 1: Variables"
  }
}
```

### Delete Course
```bash
DELETE /admin/courses/1
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "message": "Course deleted"
}
```

## Student Endpoints

### Get All Courses
```bash
GET /student/courses?skip=0&limit=100
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Python Basics",
      "description": "Learn Python from scratch"
    }
  ]
}
```

### Get Course Modules
```bash
GET /student/courses/1/modules?skip=0&limit=100
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Module 1: Basics"
    }
  ]
}
```

### Get Module Lessons
```bash
GET /student/modules/1/lessons?skip=0&limit=100
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Lesson 1: Variables"
    }
  ]
}
```

### Get Lesson Resources
```bash
GET /student/lessons/1/resources
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Python Intro Video",
      "type": "youtube_video",
      "url": "https://youtube.com/watch?v=..."
    }
  ]
}
```

### Get Quiz Questions
```bash
GET /student/quiz/1/questions
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "data": [
    {
      "id": 1,
      "text": "What is a variable?",
      "options": [
        {
          "id": 1,
          "text": "A named storage for data"
        },
        {
          "id": 2,
          "text": "A type of loop"
        }
      ]
    }
  ]
}
```

### Submit Quiz
```bash
POST /student/quiz/submit
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "quiz_id": 1,
  "score": 85,
  "duration": 600,
  "module_id": 1
}

Response:
{
  "success": true,
  "data": {
    "attempt_id": 1,
    "score": 85,
    "passed": true,
    "passing_score": 70
  }
}
```

### Get Progress
```bash
GET /student/progress/1
Authorization: Bearer <access_token>

Response:
{
  "success": true,
  "data": [
    {
      "module_id": 1,
      "completed": 3
    }
  ]
}
```

## Using with cURL

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Password123"}'

# Get courses (replace with actual token)
curl -X GET http://localhost:8000/api/v1/student/courses \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Using with Python

```python
import requests

API_URL = "http://localhost:8000/api/v1"

# Login
response = requests.post(f"{API_URL}/auth/login", json={
    "email": "user@example.com",
    "password": "Password123"
})

data = response.json()
token = data["data"]["access_token"]

# Get courses
headers = {"Authorization": f"Bearer {token}"}
courses = requests.get(f"{API_URL}/student/courses", headers=headers)
print(courses.json())
```

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "message": "Error description",
  "errors": []
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad request (validation error)
- `401`: Unauthorized (invalid token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not found
- `500`: Server error
