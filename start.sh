#!/bin/bash

# Simple startup script for AI Digital Workforce

echo "Starting AI Digital Workforce..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your API keys."
    exit 1
fi

# Start services
docker-compose up -d

# Wait for services
echo "Waiting for services to start..."
sleep 10

# Check status
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Services started successfully!"
    echo ""
    echo "Access the application at:"
    echo "  - Frontend: http://localhost"
    echo "  - Backend API: http://localhost:8000"
    echo "  - Database Admin: http://localhost:8080"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: ./stop.sh"
else
    echo "❌ Failed to start services. Check logs with: docker-compose logs"
    exit 1
fi