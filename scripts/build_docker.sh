#!/bin/bash

print_usage() {
    echo "Usage: $0 [--image_name=service_name] [--host=0.0.0.0] [--port=5000] [--worker=1]"
}

# Read image_name, host, port and worker from terminal
# image_name is required
# host is optional, default 0.0.0.0
# port is optional, default 80
# worker is optional, default 1
# example: ./build_docker.sh --image_name=service_name --host=0.0.0.0 --port=5000 --worker=1

# Run the script with -h or --help to get help# Run the script without arguments to get usage

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
        --host)
            host="$2"
            shift
            shift
            ;;
        --port)
            port="$2"
            shift
            shift
            ;;
        --worker)
            worker="$2"
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

if [ -z "$image_name" ]; then
    echo "--image_name is required"
    exit 1
fi


if [ -z "$host" ]; then
    host="0.0.0.0"
fi


if [ -z "$port" ]; then
    port="80"
fi


if [ -z "$worker" ]; then
    worker="1"
fi


docker build \
    --build-arg host=$host \
    --build-arg port=$port \
    --build-arg worker=$worker \
    -t $image_name .
