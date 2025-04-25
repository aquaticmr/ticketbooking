# Use an official Python runtime as a parent image, >= 3.10 for Django 5.x
FROM python:3.12-slim

# Install dependencies for mysqlclient (which uses mariadb client libs now) and other build tools
# apt-get update updates the package list
# apt-get install -y installs the packages without asking for confirmation
# --no-install-recommends avoids installing extra suggested packages
# build-essential includes gcc, make, etc. (needed for compiling)
# pkg-config is a build tool required by mysqlclient
# libmariadb-dev-compat and libmariadb-dev provide the necessary libraries/headers
# for mysqlclient build on Debian Bookworm+
# curl is for the healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    curl \
    netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Add the wait-for-it.sh script
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Add the current directory contents into the container at /app
# This copies your requirements.txt, manage.py, settings.py, apps, etc.
ADD . /app

# Install any needed packages specified in requirements.txt
# This step should now find the necessary build tools and libraries and succeed
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the wait script, then migrate, then start the server
# wait-for-it.sh takes host:port as first arg, followed by the command to run
CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh db:3306 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]