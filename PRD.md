# 🖼️ Art Gallery API – Product Requirements Document

## 📌 Overview
The Art Gallery API powers a platform where artists can showcase their artworks and users can interact with them through upvotes and comments—similar to **Product Hunt**. It supports user authentication, artist dashboards, an admin panel, Stripe integration, and a public storefront.

---

## 👥 User Roles

### 👤 General User
- Register, login, manage profile  
- View and upvote artworks  
- Comment on artworks  
- View public artist profiles  
- Manage cart and orders  
- Place an order for an artwork  
- Track order status  

### 🎨 Artist
- CRUD on own artworks  
- View sales and stats dashboard  
- Receive notifications  
- Manage orders related to own artworks  
- Update order statuses (e.g., delivered to courier, add tracking URL)  

### 🛠️ Admin
- Manage users, artworks, and orders  
- View overall statistics  
- Promote or demote users to/from artist role  

---

## 🔧 Blueprints / Modules

### 1. `auth` Blueprint
Handles authentication and password management.

#### Endpoints:
- `POST /auth/register`  
- `POST /auth/login`  
- `GET /auth/profile`  
- `PUT /auth/profile`  
- `POST /auth/forgot-password`  
- `POST /auth/reset-password`  

---

### 2. `store` Blueprint
Public browsing, artwork details, voting, and comments.

#### Endpoints:
- `GET /store/artworks`  
- `GET /store/artworks/<id>`  
- `POST /store/artworks/<id>/upvote`  
- `POST /store/artworks/<id>/comment`  
- `GET /store/artworks/<id>/comments`  
- `GET /store/artist/<id>` — Public artist profile  

---

### 3. `artist` Blueprint
Manages an artist’s own content and stats.

#### Endpoints:
- `GET /artist/artworks`  
- `POST /artist/artworks`  
- `PUT /artist/artworks/<id>`  
- `DELETE /artist/artworks/<id>`  
- `GET /artist/dashboard`  
- `GET /artist/orders`  
- `PUT /artist/orders/<id>` — Update order status and tracking URL  
- `GET /artist/notifications`  

---

### 4. `admin` Blueprint
Full control over the platform.

#### Endpoints:
- `GET /admin/users`  
- `PATCH /admin/users/<id>` — Promote/demote artist  
- `DELETE /admin/users/<id>`  
- `GET /admin/artworks`  
- `DELETE /admin/artworks/<id>`  
- `GET /admin/orders`  
- `GET /admin/dashboard`  

---

### 5. `cart` Blueprint
Shopping cart and checkout process.

#### Endpoints:
- `GET /cart`  
- `POST /cart/add/<artwork_id>`  
- `DELETE /cart/remove/<artwork_id>`  
- `POST /cart/checkout`  
- `GET /orders` — User's order history  
- `GET /orders/<id>` — Get order status and tracking details  

---

### 6. `notifications` Blueprint
Alerts and internal messages.

#### Endpoints:
- `GET /notifications`  
- `PUT /notifications/<id>` — Mark as read  
- `POST /notifications` — (Internal use: admin/artist)  

---

## 💳 Stripe Integration
- Create checkout session  
- Handle success/cancel webhooks  
- Save order data and notify users/artists  

---

## ✨ Extra Features

- ✅ **Upvote + Comment system** for artworks (like Product Hunt)  
- ✅ **Public artist pages** with profile and artworks  
- ✅ **Dashboards** for artists and admins  
- ✅ **Notification system** for orders and interactions  
- ✅ **Email sending**, password reset flows  
- ✅ **Order status tracking** by user  
- ✅ **Manual delivery handled by artist** with status updates  

---
