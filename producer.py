from kafka.admin import KafkaAdminClient, NewTopic
from kafka import KafkaProducer
import random
import json
import time
#from PollResponseAPI import PollResponseAPI 

class PollResponseAPI:
    survey_questions = [
        {
            'Q': 'How was the Conference overall? (Rate between 1 - 5)',
            'A': ['1', '2', '3', '4', '5']
        },
        {
            'Q': 'How would you rate the keynote speaker? (Rate between Very Bad - Very Good)',
            'A': ['V. Bad', 'Bad', 'Moderate', 'Good', 'V. Good']
        },
        {
            'Q': 'Did you find the breakout sessions informative?',
            'A': ['Yes', 'No']
        }
    ]

    def poll_response_api(self):
        response = {}
        sample_response = []
        answer_id = random.randint(1000, 2000)
        response['answer_id'] = answer_id

        for question in self.survey_questions:
            answer_pair = {question['Q']: question['A'][random.randint(0, len(question['A']) - 1)]}
            sample_response.append(answer_pair)

        response['answer_array'] = sample_response

        return json.dumps(response, indent=4)

def create_kafka_topic(bootstrap_servers, topic_name, partitions=1, replication_factor=1):
    '''This Function will create TOPIC in the kafka Server, if not present'''
    admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers,client_id = "01")

    # Create a NewTopic instance with the topic name, number of partitions, and replication factor
    new_topic = NewTopic(name=topic_name, num_partitions=partitions, replication_factor=replication_factor)

    # Create the topic
    admin_client.create_topics(new_topics=[new_topic], validate_only=False)

    print(f"Topic '{topic_name}' created successfully.")

# Kafka configurations
bootstrap_servers = 'localhost:9092'
topic_name = 'poll_responses_1'
partitions = 3
replication_factor = 1
# Function calling to Create Kafka topic
create_kafka_topic(bootstrap_servers, topic_name, partitions, replication_factor)

def data_send_to_kafka(producer, kafka_topic):
    '''This Function will send data to Kafka Server'''
    i=1     #set i value accourding to number of times you want to send data
    while i<16:
    #while True: # to send data continuously
        #print(json.dumps(PollResponseAPI().survey_questions,indent=4))
        sample_response = PollResponseAPI().poll_response_api() 
        type(sample_response)       
        producer.send(kafka_topic, sample_response.encode('utf-8'))
        #print("Sent data to kafka server: ", sample_response)
        i+=1            
        time.sleep(5) #to send data every 5 seconds

def main():
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    topic_name = 'poll_responses_1'
    data_send_to_kafka(producer, topic_name)

if __name__ == "__main__": # Call the main function to transmit data to Kafka.
    main() 
#------------------------------------------------End of Code------------------------------------------------#
