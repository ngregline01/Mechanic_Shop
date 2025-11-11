# 🏗️ Mechanic Shop Database API

A **RESTful API** for a mechanic shop that manages records related to **customers**, **mechanics**, and **service tickets**.
This project demonstrates a modular Flask architecture using **Blueprints**, **SQLAlchemy models**, and **Marshmallow** for serialization and validation.

---

## 🔹 Project Overview

- **General `__init__.py`**

  - Contains the `create_app()` function to initialize and run the Flask application.
  - Registers all **Blueprints** with their corresponding URL prefixes.
- **`models.py`**

  - Defines all **database models/classes** used in the API, including `Customer`, `Mechanic`, and `ServiceTicket`.
- **`extensions/`**

  - Initializes **Marshmallow** and other Flask extensions.
  - Handles **serialization** and **deserialization** for models.
- **Blueprint Folders**The application is modularized into three main blueprint folders:

  1. **Customers**
  2. **Mechanics**
  3. **Service Tickets**

  Each folder contains:

  - `__init__.py` → Initializes the blueprint.
  - `schema.py` → Defines **Marshmallow schemas** for request validation and response formatting.
  - `routes.py` → Implements all **CRUD operations** for the resource.

---

## ⚙️ Features

- Create, read, update, and delete **customers**.
- Create, read, update, and delete **mechanics**.
- Create and read **service tickets**.
- Assign and remove mechanics from service tickets.
- Validated API input and structured JSON output using **Marshmallow schemas**.

---

## 💻 Technologies Used

- **Python 3.11+**
- **Flask** – Web framework for building REST APIs
- **Flask-SQLAlchemy** – ORM for database modeling
- **Flask-Marshmallow** – Serialization, deserialization, and validation
- **MySQL** (via `mysqlconnector`) – Database backend

---
