FROM python:3.11-slim

# Install system dependencies (sqlite3)
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all source code
COPY . .



# Install Python dependencies
RUN pip install -r requirements.txt

# Optional: initialize the database during build
RUN useradd -m flaskuser

# Secure sensitive files
RUN chmod 700 /app

# Change ownership to the non-root user
RUN chown -R flaskuser:flaskuser /app



# Switch to the non-root user
USER flaskuser
EXPOSE 5000
# Command to run your app
CMD ["python", "app.py"]
