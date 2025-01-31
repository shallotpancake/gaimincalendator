FROM python:3.11

# Install required system packages
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Clone the GitLab repository
RUN git clone https://github.com/shallotpancake/gaimincalendator.git /app/repo

# Set the working directory to the cloned repo
WORKDIR /app/repo

# Install Python dependencies if there's a requirements.txt
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Set the entrypoint (adjust based on your repo structure)
CMD [ "python3", "main.py" ]
