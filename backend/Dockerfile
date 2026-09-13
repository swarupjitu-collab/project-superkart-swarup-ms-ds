# Python 3.11 base — matches Colab's runtime and supports the scikit-learn version
# recorded in requirements.txt (recent scikit-learn requires Python >= 3.10).
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files (app.py, requirements.txt, superkart_model.joblib) into the image
COPY . .

# Install the pinned dependencies without caching to keep the image small
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Serve the Flask app with gunicorn: 4 workers, bound to port 7860 on all interfaces
# app:superkart_api -> module 'app' (app.py), Flask instance 'superkart_api'
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
