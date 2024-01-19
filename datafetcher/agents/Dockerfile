# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y gnupg
COPY ./generate-key.sh /app/generate-key.sh
RUN chmod +x /app/generate-key.sh
RUN /app/generate-key.sh

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run your script when the container launches
CMD ["python", "send_public_key.py"]
