# ArtConnect

ArtConnect is a RESTful Flask API for managing an artisan marketplace. It allows artisans to register and manage their products, clients to register and shop, and both to interact through a shopping cart system. The backend uses MongoDB for data storage and supports authentication via JWT.

## Main Features

- **Artisan and Client Registration/Login**
- **Product Management** (CRUD for artisans)
- **Shopping Cart** (clients can add/remove products and checkout)
- **JWT Authentication** for secure access

---

## Available Routes

### Auth (`/auth`)
- `POST /auth/artesaos` — Register a new artisan
- `POST /auth/clientes` — Register a new client
- `POST /auth/login` — Login (artisan or client)

### Artisans (`/artesaos`)
- `POST /artesaos/` — Register a new artisan
- `GET /artesaos/` — List all artisans
- `GET /artesaos/<artesao_id>` — Get artisan by ID

### Products (`/produtos`)
- `POST /produtos/` — Create a new product (artisan only)
- `GET /produtos/` — List all products
- `POST /produtos/remover` — Remove a product by ID (artisan only)
- `POST /produtos/remover_todos` — Remove all products for the authenticated artisan
- `POST /produtos/atualizar_quantidade` — Update product quantity (artisan only)

### Cart (`/carrinho`)
- `GET /carrinho/` — View the current client's cart
- `POST /carrinho/adicionar` — Add products to the cart
- `POST /carrinho/remover` — Remove a product or decrease its quantity in the cart
- `POST /carrinho/limpar` — Clear the cart
- `POST /carrinho/checkout` — Checkout: purchase all products in the cart

---

## Authentication

Most routes require a JWT token in the `Authorization` header:
```
Authorization: Bearer <token>
```

---

## Health Check

- `GET /health` — Check if the API and database are running

---

For more details, see the code and controllers in the `app/`