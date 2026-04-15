# uncle-joes-api
FastAPI backend for the Uncle Joe’s Coffee pilot application
#Johnathan Zhu – Database Lead and Tester 
#Dior Charles - Project Lead
#Eric Zhang - Backend Lead
#Rochelle Zhao - Frontend Lead

# Uncle Joe's Coffee API ☕

A FastAPI-based backend service for the Uncle Joe's Coffee Company internal pilot. This API provides programmatic access to coffee shop locations, menu items, and member Coffee Club data stored in Google Cloud BigQuery.

## 🚀 Overview
This service acts as the secure bridge between the BigQuery data warehouse and the Vue.js frontend. It handles database queries, member authentication, and complex business logic like loyalty point calculations.

## 🛠 Tech Stack
- **Framework:** FastAPI
- **Database:** Google Cloud BigQuery
- **Logic:** Python 3.11+
- **Dependency Management:** Poetry
- **Deployment:** Google Cloud Run

## 🔌 API Endpoints (15 Routes)

### 🌍 Public Endpoints
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| GET | `/` | Health Check / Home Page |
| GET | `/menu` | List all menu items |
| GET | `/menu?category={cat}` | Filter menu by category |
| GET | `/menu?name={keyword}` | Search menu items by name |
| GET | `/locations` | List all open store locations |
| GET | `/locations/{id}` | Full details for a specific store |
| GET | `/locations?city={city}` | Filter stores by city or state |

### 🔐 Authentication & Profile
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| POST | `/login` | Member authentication (Bcrypt verification) |
| GET | `/members/{id}` | Retrieve logged-in member's profile |
| GET | `/dashboard` | Summary data for the member dashboard |

### 📋 Orders & Loyalty
| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| GET | `/members/{id}/orders` | Full order history list |
| GET | `/members/{id}/orders?limit=5` | Recent orders widget for dashboard |
| GET | `/orders/{order_id}` | Detailed line items for a specific order |
| GET | `/members/{id}/points` | Compute total Coffee Club loyalty points |
| GET | `/members/{id}/summary` | Total points, total orders, and total spending |

## ⚙️ Development Setup

### Installation & Run
```bash
git clone [https://github.com/rochellezhao/uncle-joes-api.git](https://github.com/rochellezhao/uncle-joes-api.git)
cd uncle-joes-api
poetry install
poetry run uvicorn main:app --reload --port 8080
