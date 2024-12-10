# Verkefni-5

### VESM Hörður Pálsson
------ 

I prioratized scalabilty and ease of use. I was very cognizant of making sure subscribing to topics and then writing corresponding functions for those topics, would be easy. To do this I added a list that holds all of the topics the user wants to subscribe to, my AsyncMQQTClient classe's function "subscribe_to_topics" then loops through the list and subscribes to each one. Then once your up and running my Mqqt_callback function decodes and reacts to messages sent to the topics, while making sure they're readble through rigourus error handling.
