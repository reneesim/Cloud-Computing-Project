#!/bin/bash

docker build -f Dockerfile.api_gateway -t project-api-gateway .
docker build -f Dockerfile.order_worker -t project-order-worker .
docker build -f Dockerfile.workload_service -t project-workload-service .
