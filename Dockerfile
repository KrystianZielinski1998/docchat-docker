# Using the full Python 3.11 image
FROM python:3.11 

# Setting up the working directory
WORKDIR /app

# Installing C++ compiler to build Python packages with native extensions.
# The cleanup removes package lists downloaded by apt-get update to reduce image size.
# All operations in one RUN command prevents caching of unnecessary data in intermediate layers.
RUN apt-get update && apt-get install -y \
    g++ \
    && rm -rf /var/lib/apt/lists/* 

# Coping requirements 
COPY requirements.txt . 

# Installing all Python dependencies 
RUN pip install --no-cache-dir -r requirements.txt 

# Coping the rest of the application code
COPY . . 

# Exposing Gradio port 
EXPOSE 7860 

# Allowing Gradio to accept connections from any host, not just localhost inside the container
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Starting the application 
CMD ["python", "app.py"]



