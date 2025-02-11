# Use the official Python image as the base image
FROM python:3.10

# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1

# Ensures that the output from Python is sent straight to the terminal without being buffered
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /code/

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . /code/

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
