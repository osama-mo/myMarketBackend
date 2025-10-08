# MyMarket Backend

A Flask-based REST API for an e-commerce marketplace. Built this to learn backend development and modern architecture patterns.

## What This Does

Simple online marketplace backend with user auth, products, and shopping cart. Users can browse products, add them to cart, and checkout. Admins can manage the product catalog.

## Tech Stack

- **Flask** - Web framework
- **SQLAlchemy** - Database ORM
- **JWT** - Authentication tokens
- **SQLite** - Database (for now)
- **Bcrypt** - Password hashing

## Project Structure

```
src/
├── models/          # Database models
├── repositories/    # Database queries
├── services/        # Business logic
├── routes/          # API endpoints
├── middleware/      # Auth middleware
└── utils/           # Helper functions
```

Using layered architecture - keeps everything organized and makes testing easier.

## Setup

1. Clone and create virtual environment:
```bash
git clone https://github.com/osama-mo/myMarketBackend.git
cd myMarketBackend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
DATABASE_URL=sqlite:///market.db
FLASK_ENV=development
```

4. Create admin user:
```bash
python create_admin.py
```

5. Run the server:
```bash
python run.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info (requires auth)

### Products
- `GET /products` - List all products (supports pagination, filtering, search)
- `GET /products/:id` - Get single product
- `POST /products` - Create product (admin only)
- `PUT /products/:id` - Update product (admin only)
- `DELETE /products/:id` - Delete product (admin only)
- `GET /products/categories` - Get all categories

### Shopping Cart
- `GET /basket` - Get current cart
- `POST /basket/add` - Add item to cart
- `PUT /basket/update` - Update item quantity
- `DELETE /basket/remove/:id` - Remove item
- `DELETE /basket/clear` - Clear cart
- `POST /basket/checkout` - Complete order
- `GET /basket/orders` - Order history


## Features

- JWT authentication
- Role-based access (admin/user)
- Product management with stock tracking
- Shopping cart with quantity management
- Order history
- Input validation
- Stock availability checks
- Pagination and filtering

## Database Schema

**Users**
- id, username, email, password_hash, role, created_at

**Products**
- id, name, description, price, stock, category, image_url, created_by, created_at, updated_at

**Baskets**
- id, user_id, status, created_at, updated_at

**BasketItems**
- id, basket_id, product_id, quantity, added_at

## What I Learned

- Clean architecture and separation of concerns
- JWT token authentication
- Password hashing and security basics
- RESTful API design
- Database relationships (one-to-many, many-to-many)
- Input validation and error handling
- Repository pattern for data access
- Service layer for business logic

## Things to Improve

- [ ] Switch to PostgreSQL for production
- [ ] Add database migrations (Alembic)
- [ ] Write unit tests
- [ ] Add rate limiting
- [ ] Better error logging
- [ ] API documentation (Swagger)
- [ ] File upload for product images
- [ ] Email notifications
- [ ] Password reset functionality

## Notes

Built with help from various tutorials and documentation. Still learning!

## License

MIT
