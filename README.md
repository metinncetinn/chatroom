
# Chatroom

This project is a chatroom application developed in Python, utilizing TCP and UDP protocols for client-server communication. The chatroom allows multiple clients to connect and exchange messages in real-time.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Requirements](#requirements)
- [Contribution](#contribution)
- [License](#license)

## Features

- **Multi-client Support**: Multiple clients can connect and chat simultaneously.
- **TCP and UDP Support**: Enables messaging using both TCP and UDP protocols.
- **Broadcast Messaging**: The server broadcasts received messages to all connected clients.
- **Simple Usage**: User-friendly command-line interface.

## Installation

To run this project on your local machine, follow these steps:

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/chatroom.git
    cd chatroom
    ```

2. Install Python and necessary packages (default Python setup is sufficient).

## Usage

1. **Start the Server**:
    ```bash
    python Server.py
    ```
    This command starts the server and waits for client connections.

2. **Start a TCP Client**:
    ```bash
    python ClientTCP.py
    ```
    This command starts a TCP client and connects to the server.

3. **Start a UDP Client**:
    ```bash
    python ClientUDP.py
    ```
    This command starts a UDP client and connects to the server.

4. On the client side, type your message in the command line and press Enter to send.

## Requirements

- Python 3.x
- Internet connection or local network

## Contribution

1. Fork this project.
2. Create a new branch: `git checkout -b new-feature`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to your branch: `git push origin new-feature`
5. Create a pull request.
