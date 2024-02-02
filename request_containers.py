from flask import Flask, jsonify
import docker

app = Flask(__name__)
client = docker.from_env()

# Dictionary to store the count of requests for each container
container_requests_count = {}

# Maximum number of requests before replicating a new container
MAX_REQUESTS = 3

@app.route('/initialize_container', methods=['POST'])
def initialize_container():
    try:
        # Initialize a new Docker container (for demonstration purposes, the container ID is generated)
        container_id = f'container_{len(container_requests_count) + 1}'

        # Reset the request count for the initialized container
        container_requests_count[container_id] = 0

        result = {'message': 'Container initialized', 'container_id': container_id}
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/process_request/<container_id>', methods=['GET'])
def process_request(container_id):
    try:
        # Increment the request count for the specified container
        container_requests_count[container_id] = container_requests_count.get(container_id, 0) + 1

        # Check if the request count exceeds the threshold
        if container_requests_count[container_id] > MAX_REQUESTS:
            # Replicate a new container (for demonstration purposes, the container ID is generated)
            new_container_id = f'new_container_{len(container_requests_count) + 1}'

            # Reset the request count for the replicated container
            container_requests_count[new_container_id] = 1

            # Create a new Docker container based on the specified image
            new_container = client.containers.run("nginx", detach=True, name=new_container_id)

            result = {'message': 'New container replicated', 'new_container_id': new_container_id}
        else:
            result = {'message': 'Request processed by existing container', 'container_id': container_id}

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
