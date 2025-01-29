FROM nginx:1

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Copy your static files to the NGINX HTML directory
COPY ./static /usr/share/nginx/html

# Expose port 80 for HTTP traffic, not sure if it's necessary
#EXPOSE 80