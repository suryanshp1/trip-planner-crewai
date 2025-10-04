#!/bin/bash

# Trip Planner Docker Management Script

case "$1" in
    "build")
        echo "Building Trip Planner Docker image..."
        docker-compose build
        ;;
    "up")
        echo "Starting Trip Planner application..."
        docker-compose up -d
        ;;
    "down")
        echo "Stopping Trip Planner application..."
        docker-compose down
        ;;
    "logs")
        echo "Showing Trip Planner logs..."
        docker-compose logs -f
        ;;
    "restart")
        echo "Restarting Trip Planner application..."
        docker-compose restart
        ;;
    "status")
        echo "Checking Trip Planner status..."
        docker-compose ps
        ;;
    "clean")
        echo "Cleaning up Docker resources..."
        docker-compose down
        docker system prune -f
        ;;
    "rebuild")
        echo "Rebuilding and starting Trip Planner..."
        docker-compose down
        docker-compose up --build -d
        ;;
    *)
        echo "Usage: $0 {build|up|down|logs|restart|status|clean|rebuild}"
        echo ""
        echo "Commands:"
        echo "  build    - Build the Docker image"
        echo "  up       - Start the application"
        echo "  down     - Stop the application"
        echo "  logs     - Show application logs"
        echo "  restart  - Restart the application"
        echo "  status   - Check application status"
        echo "  clean    - Clean up Docker resources"
        echo "  rebuild  - Rebuild and start the application"
        exit 1
        ;;
esac
