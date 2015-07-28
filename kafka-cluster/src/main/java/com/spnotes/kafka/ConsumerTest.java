package com.spnotes.kafka;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import kafka.consumer.ConsumerIterator;
import kafka.consumer.KafkaStream;

public class ConsumerTest implements Runnable {
	private KafkaStream m_stream;
	private int m_threadNumber;
	private String group;
	private String topic;
	private String outputfile;
	private ArrayList<String> messages = new ArrayList<String>();
	private String consumerId;
	private ArrayList<ConsumerTestListener> eventListeners = new ArrayList<ConsumerTestListener>();

	public ConsumerTest(KafkaStream a_stream, int a_threadNumber, String gID, String tp, String output,
			String consumerId) {
		m_threadNumber = a_threadNumber;
		m_stream = a_stream;
		group = gID;
		topic = tp;
		outputfile = output;
		this.consumerId = consumerId;
		//System.out.println("Writing to: " + outputfile);
	}

	public void run() {
		ConsumerIterator<byte[], byte[]> it = m_stream.iterator();
		boolean firstRun = true;

		int i=0;
		while (it.hasNext()) {
			if( i > 5 ){
				finishedRunning();
			}
			i++;
			String message = new String(it.next().message());
			//Tell all the listeners that a new message has been received
			sendMessage(message);
			
			try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(outputfile, true)))) {
				if (firstRun) {
					out.println("<<<" + consumerId + ">>>");
					firstRun = false;
				}
				System.out.println(consumerId + " receiving: " + message);
				out.println(message);
			} catch (IOException e) {
				System.out.println("oups, error in Consumer test PrintWriter: " + e);
				System.out.println("Failed to read: " + outputfile);
			}
		}
		System.out.println("Shutting down Thread: " + m_threadNumber);
	}

	/*
	 * Method adds listeners
	 */
	public void addListeners(ConsumerGroupExample consumer) {
		eventListeners.add(consumer);
	}

	/*
	 * Method called when an event is heard
	 */
	public void sendMessage(String s) {
		for( ConsumerTestListener list:eventListeners){
			list.newMessage(s);
		}
	}
	
	
	/*
	 * Method called when all messages have been received
	 */
	public void finishedRunning(){
		for( ConsumerTestListener list:eventListeners){
			list.finishedRunning();
		}
	}
}