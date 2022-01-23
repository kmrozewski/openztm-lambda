#!/bin/bash
set -e

while getopts ":n:f:h" o; do
    case "${o}" in
    	h)
        echo "Build docker image with lambda function:"
        echo "-n required, lambda function name (e.g. my-lambda)"
        echo "-f required, lambda file (e.g. app.py) in the functions directory"
        exit 1
        ;;
        n)
            lambda_name=${OPTARG}
            ;;
        f)
            file_name=${OPTARG}
            ;;
        *)
            echo "Invalid parameter ${OPTARG}, use -h for help"
            exit 1
            ;;
    esac
done

if [ -n "$lambda_name" ] && [ -n "$file_name" ]; then
	echo "Building docker image with tag $lambda_name:latest. Using $file_name as lambda function"
	docker build -t "$lambda_name" --build-arg LAMBDA_FUNCTION="$file_name" .
else
	echo "Please fill in required arguments, use -h for help"
	exit 1
fi
