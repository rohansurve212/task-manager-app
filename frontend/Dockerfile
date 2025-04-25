# Build stage
FROM node:20-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the application code
COPY . .

# Build the React app
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy the build files from the build stage
COPY --from=build /app/build /usr/share/nginx/html

# Remove the default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy our nginx template
COPY nginx.conf /etc/nginx/conf.d/nginx.conf.template

# Create a proper entrypoint script
RUN echo '#!/bin/sh' > /docker-entrypoint.sh && \
    echo 'envsubst "\$PORT \$BACKEND_URL" < /etc/nginx/conf.d/nginx.conf.template > /etc/nginx/conf.d/default.conf' >> /docker-entrypoint.sh && \
    echo 'nginx -g "daemon off;"' >> /docker-entrypoint.sh && \
    chmod +x /docker-entrypoint.sh

# Expose port 8080 (default for Cloud Run)
EXPOSE 8080

# Start nginx with the generated config
CMD ["/docker-entrypoint.sh"]