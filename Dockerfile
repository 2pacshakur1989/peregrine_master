FROM python:3.11.3
# Use an official Python runtime as a parent image
#FROM python:3.9-slim-buster

# Set the working directory to /backend
WORKDIR /Perergine

# Copy the current directory contents into the container at /backend
COPY . /Perergine

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
