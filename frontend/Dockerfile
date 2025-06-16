FROM node:18-alpine AS build

# Version information
ARG VERSION=0.0.1
ARG REACT_APP_API_URL=http://localhost:8888/api/v1
ARG REACT_APP_APP_NAME="Data Contracts Studio"
ARG REACT_APP_VERSION=0.0.1

LABEL version=${VERSION}
LABEL description="Data Contracts Studio Frontend"
LABEL maintainer="Data Contracts Studio Team"

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy source code
COPY . .

# Set build-time environment variables
ENV REACT_APP_API_URL=${REACT_APP_API_URL}
ENV REACT_APP_APP_NAME=${REACT_APP_APP_NAME}
ENV REACT_APP_VERSION=${REACT_APP_VERSION}

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
