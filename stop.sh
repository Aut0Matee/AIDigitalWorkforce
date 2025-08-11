#!/bin/bash

# Stop script for AI Digital Workforce

echo "Stopping AI Digital Workforce..."

# Stop services
docker-compose down

echo "✅ Services stopped successfully!"