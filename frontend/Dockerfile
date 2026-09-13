# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the frontend files (app.py, requirements.txt) into the image
COPY . .

# Install the light dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Streamlit app on port 8501, reachable from outside the container.
# XSRF protection is disabled so the CSV upload (batch) POST works through the forwarded port.
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
