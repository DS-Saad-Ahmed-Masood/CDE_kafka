from kafka import KafkaConsumer
import json

def retrieve_data_from_kafka(topic_name, bootstrap_servers='localhost:9092', group_id=None):
    # Create a Kafka consumer
    consumer = KafkaConsumer(topic_name,
                             group_id=group_id,
                             bootstrap_servers=bootstrap_servers,
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    
    try:
        # Consume messages from the topic
        for message in consumer:
            yield message.value
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Stopping consumer...")
    finally:
        consumer.close()

# Example usage
if __name__ == "__main__":
    topic_name = 'poll_responses_1'
    bootstrap_servers = 'localhost:9092'
    group_id = 'none'  # Optional, set to None if not using consumer groups

    for data in retrieve_data_from_kafka(topic_name, bootstrap_servers, group_id):
        print(f"Received message: {data}")


# Close the consumer when done
#consumer.close()

# def process_poll_responses():

#     # Kafka configurations
#     bootstrap_servers = 'localhost:9092'
#     topic_name = 'poll_responses_1'
#     group_id = 'my_consumer_group'  # Choose a unique group ID for your consumer

#     # Create a Kafka consumer
#     consumer = KafkaConsumer(topic_name,
#                             group_id=group_id,
#                             bootstrap_servers=bootstrap_servers,
#                             auto_offset_reset='earliest',
#                             enable_auto_commit=True,
#                             value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    
#     for message in consumer:
#         print(f"Received message: {message.value}")

#     return consumer

# def consume_poll_responses():
#     consumer = process_poll_responses()
#     poll_data = []
#     for message in consumer:
#         poll_data.append(message.value)
#         #update_poll_data(poll_data)
#         time.sleep(5)  # Adjust the time interval as needed

# consume_poll_responses()
