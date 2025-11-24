# Use Ubuntu Jammy as the base image
FROM ubuntu:jammy

# Update the package list and install necessary packages
RUN apt update && apt install -y python3-venv python3-pip

# Create a Python virtual environment, activate it, and install
# dependencies
RUN python3 -m venv .venv && .venv/bin/pip install flask python-openstackclient

# Copy the application source code into the container.
# The COPY has the following form COPY [OPTIONS] <src> ... <dest>
COPY ./app/main.py ./app/main.py

# Describe which ports your application is listening on.
EXPOSE 5000

# Define the command to run the application
CMD [".venv/bin/python", "./app/main.py"]