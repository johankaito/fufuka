package com.spnotes.kafka;

import java.util.ArrayList;

/*
 * This is a Node representing a computer in any kafka network
 * 
 * It can have either a consumer, a producer, or both
 */
public class KafkaNode implements ConsumerGroupListener{
	
	ProducerTest producer;
	ConsumerGroupExample consumerGroup;
	String serverUrl = "localhost";
	public ArrayList<String> MESSAGES = new ArrayList<String>();
	public ArrayList<ClusterListener> clusterListeners = new ArrayList<ClusterListener>();
	private boolean lastLayerSink;
	
	public KafkaNode(boolean isProducer, boolean isConsumer, boolean lls){
		if(isProducer){
			producer = new ProducerTest();
		}
				
		if(isConsumer){
			consumerGroup = new ConsumerGroupExample();
		}

		lastLayerSink = lls;
	}
	
	public void newMessage(String message){
		//System.out.println( consumerGroup.consumerId + ": New message: " + message);
		MESSAGES.add(message);
	}
	
	public void sendMessages(){
		
	}
	

	/*
	 * Method called when all messages have been sent(non-Javadoc)
	 * @see com.spnotes.kafka.ConsumerGroupListener#finishedRunning()
	 */
	public void finishedRunning(){
		//consumerGroup.shutdown();
	}
	
}
