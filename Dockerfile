# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Set environment variable to avoid buffering Python output
ENV PYTHONUNBUFFERED=1

# Set up the command to run the script (replace main.py with delete_events.py if needed)
CMD ["python", "main.py"]
