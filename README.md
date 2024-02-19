# Microservices E-commerce Application

This project is a microservices-based e-commerce application built with Python. It consists of four main services:

- User Service: Handles user registration, authentication, and user profile management.
- Product Service: Manages product creation, updates, retrieval, and deletion.
- Cart Service: Allows users to add products to their cart, update cart items, and checkout.
- Order Service: Handles order creation and updates, and communicates with the User and Product services.

Each service is a separate application, running in its own Docker container. They communicate with each other using HTTP and RPC calls.

The project also includes a comprehensive suite of unit tests for each service, ensuring the reliability and stability of the application.

The application is designed to be scalable and resilient, making it suitable for deployment in a cloud environment.

## Technologies Used

- Python
- FastAPI
- Docker
- Docker Compose
- MongoDB
- RabbitMQ

## Getting Started

To run the application, it requires Docker and Docker Compose installed. Start the application by running `docker-compose up --build` in the /src directory of the project.
