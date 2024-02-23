#!/bin/bash

# kubectl apply -f ingress.yaml
kubectl apply -f rabbit.yaml
kubectl apply -f mongo-config.yaml
kubectl apply -f mongo-secret.yaml
kubectl apply -f postgres-config.yaml
kubectl apply -f postgres-secret.yaml
kubectl apply -f databases.yaml
kubectl apply -f microservices.yaml