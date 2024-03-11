# Set base image (host OS) to Python 3.10 to match your local Python version
FROM python:3.10

# By default listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install necessary system packages for building your dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libblas-dev \
    liblapack-dev \
    gfortran \
    libfreetype6-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Set environment variables
#ENV FLASK_APP=main.py
#ENV FLASK_ENV=development

# Run the application
#CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]



