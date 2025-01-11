# client-server-networking
# RSA, Diffie-Hellman, and AES Encryption 

This project demonstrates a secure communication between a client and server using RSA, Diffie-Hellman key exchange, and AES encryption. The client encrypts a file using AES and sends it to the server, which then decrypts it.

## Project Structure

- `client.py`: The client script that generates RSA keys, performs Diffie-Hellman key exchange, and encrypts a file using AES.
- `server.py`: The server script that accepts a connection from the client, performs Diffie-Hellman key exchange, and decrypts the received file using AES.
- `docker-compose.yml`: A Docker Compose configuration file to run both the client and server in Docker containers.
- `Dockerfile`: Dockerfiles for both the client and server to build their respective images.
- `file.txt`: A sample file that the client will encrypt and send to the server (you can modify this file for testing).

## Requirements

- Docker
- Docker Compose

## How to Run the Project

### Steps: Clone the Repository

Clone this repository to your local machine:


git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name

Use Docker Compose to build and run the containers:

docker-compose up --build
This command will:
