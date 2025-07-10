# 🖼️ Art Gallery API

## Overview
The Art Gallery API powers a platform where artists can showcase their artworks and users can interact with them through upvotes and comments—similar to Product Hunt. It supports user authentication, artist dashboards, an admin panel, Stripe integration, and a public storefront.

---

## Table of Contents
- [Features](#features)
- [User Roles](#user-roles)
- [Setup & Installation](#setup--installation)
- [Environment Variables](#environment-variables)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [Auth](#auth)
  - [Store](#store)
  - [Artist](#artist)
- [Data Models & Schemas](#data-models--schemas)
- [Error Handling](#error-handling)
- [Email & Password Reset](#email--password-reset)
- [Stripe Integration](#stripe-integration)
- [Extra Features](#extra-features)

---

## Features
- User registration, login, JWT-based authentication
- Artists can CRUD their own artworks
- Public artwork browsing, upvoting, and commenting
- Nested comments (replies)
- Role-based access (User, Artist, Admin)
- Password reset via email (SendGrid)
- CORS support for frontend integration
- Admin and artist dashboards (API endpoints)
- Stripe integration for orders (planned)

---

## User Roles
- **General User**: Register, login, view/upvote/comment on artworks, manage profile, place orders, track order status
- **Artist**: All user features + manage own artworks, view dashboard, manage orders, update order statuses
- **Admin**: Full control over users, artworks, orders, and platform stats

---

## Setup & Installation

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set environment variables** (see below)
4. **Run the application**:
   ```bash
   export FLASK_APP=src/app
   flask run
   ```

---

## Environment Variables
- `SECRET_KEY`: Secret for Flask sessions and JWT
- `JWT_SECRET_KEY`: Secret for JWT tokens
- `DATABASE_URL`: SQLAlchemy DB URI (default: SQLite `app.db`)
- `SENDGRID_API_KEY`: For sending emails
- `SENDGRID_FROM_EMAIL`: Sender email address
- `FRONTEND_URL`: Used in password reset emails

---

## Authentication
- Uses JWT (JSON Web Tokens) for stateless authentication
- Access tokens are required for protected endpoints (send as `Authorization: Bearer <token>` header)
- Logout is handled by blacklisting tokens

---

## API Endpoints

### Auth
| Method | Endpoint                | Description                  | Auth Required |
|--------|-------------------------|------------------------------|---------------|
| POST   | `/auth/register`        | Register a new user          | No            |
| POST   | `/auth/login`           | Login and get JWT token      | No            |
| GET    | `/auth/profile`         | Get current user profile     | Yes           |
| POST   | `/auth/logout`          | Logout (blacklist token)     | Yes           |
| POST   | `/auth/forgot-password` | Request password reset email | No            |
| PUT    | `/auth/reset-password`  | Reset password with token    | No            |

#### Example: Register
```json
POST /auth/register
{
  "name": "Alice",
  "email": "alice@example.com",
  "password": "password123",
  "confirm_password": "password123"
}
```

#### Example: Login
```json
POST /auth/login
{
  "email": "alice@example.com",
  "password": "password123"
}
Response: { "access_token": "..." }
```

---

### Store
| Method | Endpoint                                 | Description                        | Auth Required |
|--------|------------------------------------------|------------------------------------|---------------|
| GET    | `/store/artworks`                        | List all artworks                  | No            |
| GET    | `/store/artworks/<artwork_id>`           | Get artwork details                | No            |
| GET    | `/store/upvote/<type>/<id>`              | Get upvotes for artwork/comment    | No            |
| POST   | `/store/upvote/<type>/<id>`              | Upvote artwork/comment             | Yes           |
| DELETE | `/store/upvote/<type>/<id>`              | Remove upvote                      | Yes           |
| POST   | `/store/artworks/<artwork_id>/comments`  | Add comment to artwork             | Yes           |
| GET    | `/store/artworks/<artwork_id>/comments`  | List comments for artwork          | No            |
| POST   | `/store/comments/<comment_id>`           | Reply to a comment                 | Yes           |
| DELETE | `/store/comments/<comment_id>`           | Delete a comment                   | Yes (owner)   |
| GET    | `/store/comments/<comment_id>`           | List replies for a comment         | No            |

#### Example: Get All Artworks
```json
GET /store/artworks
Response: {
  "status": "success",
  "data": [ { ...artwork fields... } ]
}
```

#### Example: Add Comment
```json
POST /store/artworks/1/comments
Authorization: Bearer <token>
{
  "content": "Amazing artwork!"
}
```

---

### Artist
All endpoints require authentication and artist role.

| Method | Endpoint                        | Description                |
|--------|---------------------------------|----------------------------|
| GET    | `/artist/dashboard`             | List own artworks          |
| POST   | `/artist/artwork`               | Create new artwork         |
| GET    | `/artist/artwork/<id>`          | Get own artwork details    |
| PUT    | `/artist/artwork/<id>`          | Update own artwork         |
| DELETE | `/artist/artwork/<id>`          | Delete own artwork         |
| GET    | `/artist/tags`                  | List all tags              |
| GET    | `/artist/categories`            | List all categories        |
| GET    | `/artist/currencies`            | List all currencies        |

#### Example: Create Artwork
```json
POST /artist/artwork
Authorization: Bearer <token>
{
  "title": "Sunset",
  "price": 100.0,
  "currency_id": 1,
  "stock": 5,
  "description": "A beautiful sunset.",
  "category_name": "Nature",
  "tag_names": ["sunset", "nature"]
}
```

---

## Data Models & Schemas

### User
```json
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com",
  "role_id": 2
}
```

### Artwork (Output)
```json
{
  "id": 1,
  "title": "Sunset",
  "price": 100.0,
  "stock": 5,
  "description": "A beautiful sunset.",
  "image_path": "/uploads/sunset.jpg",
  "category": { "id": 1, "title": "Nature" },
  "tags": [ { "id": 1, "title": "sunset" } ],
  "currency": { "id": 1, "title": "USD", "code": "USD", "symbol": "$" },
  "artist": { "id": 2, "name": "Bob" }
}
```

### Artwork (Input)
```json
{
  "title": "Sunset",
  "price": 100.0,
  "currency_id": 1,
  "stock": 5,
  "description": "A beautiful sunset.",
  "category_name": "Nature",
  "tag_names": ["sunset", "nature"],
  "image_path": "/uploads/sunset.jpg"
}
```

### Comment
```json
{
  "id": 1,
  "content": "Amazing!",
  "created_at": "2024-07-01T12:00:00Z",
  "user_id": 1,
  "upvotes": 3,
  "replies": [ ... ]
}
```

---

## Error Handling
- Errors are returned as JSON with `status` and `message` fields
- Example:
```json
{
  "status": "error",
  "message": "No artworks found"
}
```

---

## Email & Password Reset
- Password reset requests send an email with a reset link (using SendGrid)
- The frontend should provide a `/reset-password?token=...` page to handle the reset
- Example reset email content:
  - Subject: "Password Reset Request"
  - Body: Link to `${FRONTEND_URL}/reset-password?token=...`

---

## Stripe Integration
- Stripe integration is planned for order and checkout endpoints
- Endpoints will include creating checkout sessions, handling webhooks, and saving order data

---

## Extra Features
- Upvote and comment system for artworks
- Public artist pages
- Dashboards for artists and admins
- Notification system for orders and interactions
- Order status tracking
- Manual delivery handled by artist

---

## Dependencies
See `requirements.txt` for all dependencies. Major ones include:
- Flask, Flask-RESTx, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Migrate
- Marshmallow (schemas)
- SendGrid (email)
- bcrypt (password hashing)

---

## Contact & Contribution
For questions or contributions, please open an issue or pull request.
