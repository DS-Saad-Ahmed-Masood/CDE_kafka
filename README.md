# Live Polling System with Kafka

## Overview

The Live Polling System with Kafka is a real-time polling application designed to collect and display audience responses during events or conferences. The system utilizes Apache Kafka as a distributed streaming platform for collecting, processing, and delivering poll data to consumers. It features a modular architecture that allows for scalability and flexibility in handling large volumes of poll responses.

## Features

- **Real-time Data Streaming**: Poll responses are streamed in real-time using Apache Kafka, enabling instant updates to the polling results.
- **Scalability**: The system can handle a large number of concurrent users and scale horizontally to accommodate increasing traffic.
- **Fault Tolerance**: Kafka's distributed architecture ensures fault tolerance and high availability of poll data.
- **Interactive Dashboard**: The web-based dashboard provides an interactive interface for event organizers to view live polling results.
- **Customizable Polls**: Event organizers can create custom polls with dynamic questions and response options.

## Architecture

The architecture of the Live Polling System consists of the following components:

1. **Producer**: Generates poll responses and publishes them to Kafka topics.
2. **Kafka Cluster**: A distributed cluster of Kafka brokers that stores and manages poll data.
3. **Consumer**: Subscribes to Kafka topics, processes poll responses, and updates the dashboard.
4. **Dashboard**: A web-based interface for viewing live polling results, built using Streamlit or similar technologies.

![System Architecture](architecture_diagram.png)

## Installation

### Requirements

- Apache Kafka
- Python 3.x
- Kafka-Python library
- Streamlit (for the dashboard)

### Setup Instructions

1. Install Apache Kafka and Zookeeper on your system.
2. Clone the project repository from GitHub.
3. Install Python dependencies using pip:

   ```bash
   pip install kafka-python streamlit
   ```

4. Start Zookeeper and Kafka servers.
5. Run the producer and consumer scripts to start streaming poll data.
6. Launch the Streamlit dashboard to view live polling results.

## Usage

1. **Producer Script**: Run the producer script to generate poll responses and publish them to Kafka topics. Customize the script to generate specific poll questions and response options.

   ```bash
   python producer.py
   ```

2. **Consumer Script**: Run the consumer script to subscribe to Kafka topics, process poll responses, and update the dashboard with live polling results.

   ```bash
   python consumer.py
   ```

3. **Streamlit Dashboard**: Launch the Streamlit dashboard to view live polling results in real-time.

   ```bash
   streamlit run dashboard.py
   ```

## Configuration

- **Kafka Configuration**: Update the Kafka broker and topic configurations in the producer and consumer scripts as needed.
- **Dashboard Configuration**: Customize the dashboard layout, styling, and functionality according to your requirements.

## Future Enhancements

- Integration with databases for persistent storage of poll data.
- Support for user authentication and authorization in the dashboard.
- Implementation of real-time analytics and visualization features.
- Deployment of the system on cloud platforms for improved scalability and reliability.

## Contributors

- [Your Name or Organization]

## License

This project is licensed under the [MIT License](LICENSE).
