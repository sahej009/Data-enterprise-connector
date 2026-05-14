# 1. Use the official lightweight Python image
FROM python:3.11-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first (this makes future builds faster)
COPY requirements.txt .

# 4. Install the enterprise dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code
COPY . .

# 6. Expose the port FastAPI will use
EXPOSE 8000

# 7. Start the Uvicorn server (bound to 0.0.0.0 so the cloud can access it)
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]