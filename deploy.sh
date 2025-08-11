#!/bin/bash

# AI Digital Workforce Deployment Script
# This script helps deploy the application using Docker Compose

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_status "Docker is installed ✓"
}

# Check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    print_status "Docker Compose is installed ✓"
}

# Check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from .env.example..."
        cp .env.example .env
        print_error "Please edit .env file and add your API keys before continuing."
        echo "Required keys:"
        echo "  - OPENAI_API_KEY"
        echo "  - TAVILY_API_KEY"
        exit 1
    fi
    
    # Check if API keys are set
    if grep -q "your_openai_api_key_here" .env; then
        print_error "Please set your OPENAI_API_KEY in the .env file"
        exit 1
    fi
    
    if grep -q "your_tavily_api_key_here" .env; then
        print_error "Please set your TAVILY_API_KEY in the .env file"
        exit 1
    fi
    
    print_status "Environment configuration found ✓"
}

# Stop and remove existing containers
cleanup() {
    print_status "Cleaning up existing containers..."
    docker-compose down -v 2>/dev/null || true
}

# Build Docker images
build_images() {
    print_status "Building Docker images..."
    docker-compose build --no-cache
}

# Start services
start_services() {
    print_status "Starting services..."
    docker-compose up -d
    
    # Wait for services to be healthy
    print_status "Waiting for services to be healthy..."
    sleep 10
    
    # Check service health
    if docker-compose ps | grep -q "unhealthy\|Exit"; then
        print_error "Some services failed to start properly"
        docker-compose logs
        exit 1
    fi
}

# Display service URLs
display_info() {
    echo ""
    print_status "🎉 Deployment successful! Services are running at:"
    echo ""
    echo "  📱 Frontend:  http://localhost"
    echo "  🔧 Backend:   http://localhost:8000"
    echo "  🗄️  Adminer:   http://localhost:8080"
    echo ""
    echo "  MySQL Credentials:"
    echo "    Server:   mysql"
    echo "    Database: ai_workforce"
    echo "    Username: ai_user"
    echo "    Password: (check your .env file)"
    echo ""
    print_status "To view logs: docker-compose logs -f"
    print_status "To stop services: docker-compose down"
}

# Main execution
main() {
    echo "======================================"
    echo "AI Digital Workforce Deployment"
    echo "======================================"
    echo ""
    
    # Run checks
    check_docker
    check_docker_compose
    check_env_file
    
    # Ask for confirmation
    echo ""
    read -p "Do you want to proceed with deployment? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Deployment cancelled"
        exit 0
    fi
    
    # Deploy
    cleanup
    build_images
    start_services
    display_info
}

# Run main function
main "$@"