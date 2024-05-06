import streamlit as st
#import json
import pandas as pd
from collections import Counter
from PollResponseAPI import PollResponseAPI
import altair as alt
import time
#from kafka import KafkaConsumer

# Set page title and icon
st.set_page_config(
    page_title="Live Poll",
    page_icon="💻",
    layout="wide"
)

with st.container():
    colA,colB= st.columns(spec=[1,0.2], gap="small")

    with colB:
        st.image("https://user-images.githubusercontent.com/37160523/165100232-b1a4dcf0-2f98-4f71-abe7-1fd8f497ed1b.png",
        width=200,) # Manually Adjust the width of the image as per requirement)

    with colA:
        st.title("Live Polling")
        st.subheader("Welcome to the live poll data display app!")
        st.write("This Streamlit app enables real-time polling, offering a dynamic platform for collecting and visualizing live feedback from participants. With interactive bar charts and a tabular view of responses, it provides instant insights into audience opinions and preferences.")

placeholder = st.empty()

# Initialize empty lists to store responses for each question
responses_q1 = []
responses_q2 = []
responses_q3 = []

# Function to update poll data
def update_poll_data(poll_data):
    global responses_q1, responses_q2, responses_q3

    with placeholder.container(border=True):        
        #Count KPI
        st.metric("Total Responses", len(poll_data))
        # Containers
        col1, col2, col3, col4 = st.columns([1, 1, 1, 0.7])

        # Block 2: 
        #with col1:
            #st.metric("Total Responses", len(poll_data))

        # Update responses for each question
        for idx, poll in enumerate(poll_data):
            responses_q1.append(int(poll['answer_array'][0][list(poll['answer_array'][0].keys())[0]]))
            responses_q2.append(poll['answer_array'][1][list(poll['answer_array'][1].keys())[0]])
            responses_q3.append(poll['answer_array'][2][list(poll['answer_array'][2].keys())[0]])

        # Count occurrences of each rating in responses for Question 1
        rating_counts_q1 = Counter(responses_q1)
        # Get all possible ratings (1 to 5) and their counts
        all_ratings_q1 = list(range(1, 6))
        all_ratings_counts_q1 = [rating_counts_q1[rating] for rating in all_ratings_q1]

        # Count occurrences of each answer in responses for Question 2
        answer_counts_q2 = Counter(responses_q2)
        # Get all possible answers and their counts
        all_answers_q2 = ["V. Bad", "Bad", "Moderate", "Good", "V. Good"]
        all_answers_counts_q2 = [answer_counts_q2[answer] for answer in all_answers_q2]

        # Count occurrences of each answer in responses for Question 3
        answer_counts_q3 = Counter(responses_q3)
        # Get all possible answers and their counts
        all_answers_q3 = ["Yes", "No"]
        all_answers_counts_q3 = [answer_counts_q3[answer] for answer in all_answers_q3]

        # Block 3: Bar Chart for Question 1
        with col1:
            st.subheader("Question 1: How was the Conference overall? (Rate between 1 - 5)",divider="gray")
            chart_q1 = create_bar_chart(all_ratings_q1, all_ratings_counts_q1, "Conference Rating",color_palette)
            st.altair_chart(chart_q1, use_container_width=True)

        # Block 4: Bar Chart for Question 2
        with col2:
            st.subheader("Question 2: How would you rate the keynote speaker? (Rate between Very Bad - Very Good)",divider="gray")
            chart_q2 = create_bar_chart(all_answers_q2, all_answers_counts_q2, "keynote speaker Rating",color_palette)
            st.altair_chart(chart_q2, use_container_width=True)

        # Block 5: Bar Chart for Question 3
        with col3:
            st.subheader("Question 3: Did you find the breakout sessions informative?",divider="gray")
            chart_q3 = create_bar_chart(all_answers_q3, all_answers_counts_q3, "Remarks",color_palette)
            st.altair_chart(chart_q3, use_container_width=True)

        # Block 6: Table DataFrame
        with col4:
            poll_df = pd.DataFrame({f"Q{i+1}": [list(poll['answer_array'][i].values())[0] for poll in poll_data] for i in range(len(poll_data[0]['answer_array']))}, index=[poll['answer_id'] for poll in poll_data])
            st.subheader("Poll Data",divider="gray")
            st.write(poll_df) 

def create_bar_chart(x_values, y_values, x_label, color_palette):
    data = pd.DataFrame({'x': x_values, 'y': y_values})
    
    # Find the index of the maximum value
    max_index = y_values.index(max(y_values))
    
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('x:O', axis=alt.Axis(title=x_label, labels=True)),
        y=alt.Y('y:Q', axis=alt.Axis(title='Responses')),
        tooltip=['x', 'y']
    ).properties(
        width=300,
        height=300
    )
    
    # Define the color condition to highlight the highest value
    color_condition = alt.condition(
        alt.datum.y == max(y_values),
        alt.value('seagreen'),  # Change the color you prefer for highlighting
        alt.value(color_palette)
    )
    
    # Apply the color condition to the chart
    chart = chart.encode(color=color_condition)
    
    return chart
color_palette="darkcyan" # Colors for low bars

# Main Streamlit app
def main():
                
    # Simulate live updates from poll responses
    poll_data = []

    # Continuously update data
    while True:
        # Generate a sample poll response
        sample_poll_response = json.loads(PollResponseAPI().poll_response_api()) #(un-comment this line to use PollResponseAPI.py)

        #-------------------------------------------------------------------------------------------------------#
        #Reson to make this below commented out is when i am running this it shows result only one time!

        # # Kafka configurations
        # bootstrap_servers = 'localhost:9092'
        # topic_name = 'poll_responses_1'
        # group_id = 'my_consumer_group1'  # Choose a unique group ID for your consumer

        # # Create a Kafka consumer
        # sample_poll_response = KafkaConsumer(topic_name,
        #                         group_id=group_id,
        #                         bootstrap_servers=bootstrap_servers,
        #                         auto_offset_reset='earliest',
        #                         enable_auto_commit=True,
        #                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))       

        # # Consume messages from the topic
        # for message in sample_poll_response:
        #     print(f"Received message: {message.value}")
        #-------------------------------------------------------------------------------------------------------#
        
        # Append poll response to data
        poll_data.append(sample_poll_response)

        # Update UI
        update_poll_data(poll_data)

        # Wait for a short duration before updating again
        time.sleep(5)  # You can adjust the time interval as needed

    # Block 7: st.Footer("None")
st.success("App created by Mr.Saad Ahmed Masood")

if __name__ == "__main__":
    main()

#For Graph Color Selections
# SchemaValidationError: '{'field': 'x', 'scale': {'range': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']}, 
# 'type': 'nominal'}' is an invalid value for `color`. Valid values are: - One of ['black', 'silver', 'gray', 'white', 
# 'maroon', 'red', 'purple', 'fuchsia', 'green', 'lime', 'olive', 'yellow', 'navy', 'blue', 'teal', 'aqua', 'orange', 
# 'aliceblue', 'antiquewhite', 'aquamarine', 'azure', 'beige', 'bisque', 'blanchedalmond', 'blueviolet', 'brown', 
# 'burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 
# 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen', 'darkgrey', 'darkkhaki', 'darkmagenta', 
# 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 
# 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 
# 'firebrick', 'floralwhite', 'forestgreen', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'greenyellow', 'grey', 
# 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 
# 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgreen', 'lightgrey', 
# 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 
# 'lightyellow', 'limegreen', 'linen', 'magenta', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 
# 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 
# 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'oldlace', 'olivedrab', 'orangered', 'orchid', 'palegoldenrod', 
# 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 
# 'rosybrown', 'royalblue', 'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'skyblue', 
# 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'thistle', 'tomato', 'turquoise', 
# 'violet', 'wheat', 'whitesmoke', 'yellowgreen', 'rebeccapurple'] - Of type 'string' Additional properties are not allowed 
# ('field', 'scale', 'type' were unexpected)'gradient' is a required property 'stops' is a required property 'expr' 
# is a required property

# Example usage:
#x_label = 'Categories'
#color_palette = alt.Color('x:N', scale=alt.Scale(range=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']))  # Example color palette
