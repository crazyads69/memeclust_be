#!/bin/bash


print_usage() {
    echo "Usage: ./start_docker.sh --image_name=service_name --container_name=0.0.0.0 [--port=8080] [--mode DEVELOPMENT]"
}


image_name="khiemledev/fastapi_template"
container_name="fastapi_template"
port=8080
mode="PRODUCTION"


# Read image_name, container_name, port and mode from terminal
# image_name is required
# container_name is required
# port is optional, default 8080
# mode is optional, choices: DEVELOPMENT or PRODUCTION, default PRODUCTION
# example: ./start_docker.sh --image_name=service_name --container_name=0.0.0.0 --port=8080 --mode DEVELOPMENT

# Run the script with -h or --help to get help
# Run the script without arguments to get usage

if [ $# -eq 0 ]; then
    print_usage
    exit 0
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        --image_name)
            image_name="$2"
            shift
            shift
            ;;
        --container_name)
            container_name="$2"
            shift
            shift
            ;;
        --port)
            port="$2"
            shift
            shift
            ;;
        --mode)
            mode="$2"
            shift
            shift
            ;;
        -h | --help)
            print_usage
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

# Check if image_name is empty
if [ -z "$image_name" ]; then
    echo "image_name is required"
    exit 1
fi

# Check if container_name is empty
if [ -z "$container_name" ]; then
    echo "container_name is required"
    exit 1
fi

# Check if port is empty
if [ -z "$port" ]; then
    port="8080"
fi

# Check if mode is empty
if [ -z "$mode" ]; then
    mode="PRODUCTION"
fi

# Check if mode is valid
if [ "$mode" != "DEVELOPMENT" ] && [ "$mode" != "PRODUCTION" ]; then
    echo "mode must be DEVELOPMENT or PRODUCTION"
    exit 1
fi

# Example of run docker container
docker run -d \
    -p $port:8080 \
    -e mode=$mode \
    --name $container_name \
    $image_name
