# Budget Manager

<a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-gray?color=0B1121&logo=python" /></a>
<a href="https://python-poetry.org/"><img src="https://img.shields.io/badge/Poetry-gray?color=0B1121&logo=poetry" /></a>
<a href="https://docs.djangoproject.com/en/5.1/"><img src="https://img.shields.io/badge/Django-gray?color=0B1121&logo=django" /></a>
<a href="https://django-ninja.dev/"><img src="https://img.shields.io/badge/DjangoNinja-gray?color=0B1121&logo=django" /></a>
<a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/PostgreSQL-gray?color=0B1121&logo=postgresql" /></a>
<a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-gray?color=0B1121&logo=docker" /></a>

This app solves the problem of budget management. It allows users to keep track of their expenses and income, as well as track their spending activity.

**FrontEnd** can be found [here](https://github.com/MrQuackDuck/BudgetManagerClient.git).

---

## Features

- **User Authentication**: Secure user registration and login with token-based authentication.
- **Budget Management**: CRUD budgets with different currencies.
- **Expense Tracking**: CRUD expenses with different categories.
- **Reporting**: Generate summaries and insights on budget with expenses(budget operations).
- **Scalable Architecture**: Designed to support future integrations and scaling. Designed with layer segregation with DDD-ish (Onion) architecture

---

## Tech Stack

- **Programming Language**: Python
- **Framework**: Django Ninja
- **Database**: PostgreSQL
- **Authentication**: UUID tokens
- **Documentation**: Swagger (OpenAPI)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/defuzia/BudgetManagement-backend.git
   ```
2. Navigate to the project directory:
   ```bash
   cd BudgetManager/
   ```
3. Create a `.env` file in the root directory and configure using `.env.example`.

4. Create a `local.py` settings in BudgetManager/core/project/settings and configure using `local_example.py`.

5. Use `Makefile` commands for further development.

6. (optional but explicit) Run `Makefile`: `make app` command to up infrastructure then run `Makefile`: `make migrate` to populate DB with tables.

---

## Implemented `Makefile` commands

### General commands:

* `make app` - up application(Dockerfile) and storages(DB) infrastructure

* `make app-logs` - follow the logs in app container

* `make app-down` - down application(Dockerfile) and storages(DB) infrastructure

* `make storages` - up only storages(DB)

* `make storages-logs` - follow the logs in storages container

* `make storages-down` - down only storages(DB)


### Django specific commands:
* `make makemigrations` - generate migration to models based on changes

* `make migrate` - apply all made migrations to DB

* `make createsuperuser` - create admin user

* `make collectstatic` - collect static

* `make run-tests` - run tests

---

## General URLS
- `/admin`: Go to admin panel. (before that, create admin user using `Makefile` Django specific commands)

## API Endpoints

### General
- `GET /api/ping`: Ping a server.
- `GET /api/docs`: Go to OpenAPI generated documentation.

### Authentication
- `POST /api/v1/customers/auth`: Start authentication process: get/crate customer and send code to a phone number.
- `POST /api/v1/customers/confirm`: Complete authentication process and receive a UUID token.

### Customer related
- `GET /api/v1/customers/profile`: Fetch customer info.
- `PUT /api/v1/customers/profile`: Update customer info.

### Budgets
- `GET /api/v1/currencies`: Fetch all available currencies.
- `GET /api/v1/currencies/{short_name}`: Fetch specific currency by its short_name.
- `POST /api/v1/budgets`: Create a new budget.
- `GET /api/v1/budgets`: Fetch all budgets.
- `GET /api/v1/budgets/{budget_id}`: Fetch specific budget by its id.
- `GET /api/v1/budgets/{budget_id}/operations`: Fetch specific budget operations by its id.
- `PUT /api/v1/budgets/{budget_id}`: Update specific budget by its id.
- `DELETE /api/v1/budgets/{budget_id}`: Delete specific budget by its id.

### Budget operations
- `POST /api/v1/categories`: Create a new category.
- `GET /api/v1/categories`: Fetch all available categories.
- `GET /api/v1/categories/{category_id}`: Fetch category by its id.
- `PUT /api/v1/categories/{category_id}`: Update specific budget by its id.
- `DELETE /api/v1/categories/{category_id}`: Delete specific budget by its id.
- `POST /api/v1/operations`: Create a new budget operation.
- `GET /api/v1/operations`: Fetch all available operations.
- `GET /api/v1/operations/{operation_id}`: Fetch specific operation by its id.
- `PUT /api/v1/operations/{operation_id}`: Update specific operation by its id.
- `DELETE /api/v1/operations/{operation_id}`: Delete specific operation by its id.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.

2. Aware and use conventional commits: https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13

3. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
4. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
5. Push to your branch:
   ```bash
   git push origin feature-name
   ```
6. Submit a pull request.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For any questions or feedback, please reach out to `roman.zhyvchyn.kn.2022@lpnu.ua`.

