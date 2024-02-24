# Microservices E-commerce Application

This is a microservices-based e-commerce application built with Python. The application is composed of four main services:

- [User Service](src/user): Handles user registration, authentication, and user profile management.
- [Product Service](src/product): Manages product creation, updates, retrieval, and deletion.
- [Cart Service](src/cart): Allows users to add products to their cart, update cart items, and checkout.
- [Order Service](src/order): Handles order creation and updates, and communicates with the User and Product services.

Each service is a separate application with its own database, running in its own Docker container. They communicate with each other using HTTP and RPC calls. The project also includes a comprehensive suite of unit tests for each service, ensuring the reliability and stability of the application.

The application is designed to be scalable and resilient, making it suitable for deployment in a cloud environment. It uses Kubernetes for orchestration, as defined in the [k8s](k8s/kubernetes-deploy.sh) directory. The application is also configured for continuous integration and deployment using GitHub Actions, as defined in the [main.yaml](.github/workflows/main.yaml) workflow.

## Technologies Used

- Python
- FastAPI
- Docker
- Docker Compose
- MongoDB
- PostgreSQL
- RabbitMQ
- Kubernetes
- GitHub Actions

## Getting Started

This application can be run using either Docker and Docker Compose or Kubernetes. Make sure you have the necessary tools installed:

- Docker and Docker Compose for the Docker deployment.
- Minikube for the Kubernetes deployment.

Follow these steps to get the application running:

1. **Set up environment variables:** Create a `.env` file in the `src` directory and populate it with the necessary environment variables. Here's an example:

    ```env
    USER_SERVICE_NAME=user_service
    USER_POSTGRES_HOST=user_postgres
    USER_POSTGRES_PORT=5432
    USER_POSTGRES_USER=myuser
    USER_POSTGRES_PASSWORD=mysecretpassword
    USER_POSTGRES_DB=userdb
    PRODUCT_SERVICE_NAME=product_service
    PRODUCT_POSTGRES_HOST=product_postgres
    PRODUCT_POSTGRES_PORT=5432
    PRODUCT_POSTGRES_USER=myuser
    PRODUCT_POSTGRES_PASSWORD=mysecretpassword
    PRODUCT_POSTGRES_DB=productdb
    CART_SERVICE_NAME=cart_service
    CART_MONGODB_HOST=cart_mongodb
    CART_MONGODB_USER=myuser
    CART_MONGODB_PASSWORD=mysecretpassword
    CART_MONGODB_DB=cartdb
    ORDER_SERVICE_NAME=order_service
    ORDER_MONGODB_HOST=order_mongodb
    ORDER_MONGODB_USER=myuser
    ORDER_MONGODB_PASSWORD=mysecretpassword
    ORDER_MONGODB_DB=orderdb
    TESTING=True
    ```

    Replace the placeholders (`myuser`, `mysecretpassword`, etc.) with your actual database credentials and service names.

2. **Run the application:** Depending on your chosen deployment method, do one of the following:

    - For Docker: Navigate to the `src` directory and start the application using Docker Compose:

        ```bash
        docker-compose up --build
        ```

    - For Kubernetes: 
        ```bash
        minikube start
        ```

    Then use the provided Kubernetes scripts in the [k8s](k8s/kubernetes-deploy.sh) directory.

3. **Run unit tests:** To run the unit tests, use the following command:

    ```bash
    docker-compose -f ./src/docker-compose.tests up -d
    ```