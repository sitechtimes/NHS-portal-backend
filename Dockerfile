# Use a base Python image
FROM python:3.10

# Set working directory
WORKDIR /

# Copy files
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN py manage.py runscript reset_db
# Expose port
EXPOSE 8000

# Run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
