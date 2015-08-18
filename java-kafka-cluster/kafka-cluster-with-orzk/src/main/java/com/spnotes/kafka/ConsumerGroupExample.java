package com.spnotes.kafka;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import kafka.consumer.Consumer;
import kafka.consumer.ConsumerConfig;
import kafka.consumer.KafkaStream;
import kafka.javaapi.consumer.ConsumerConnector;

public class ConsumerGroupExample extends Thread implements ConsumerTestListener {
	private final ConsumerConnector consumer;
	private String zooKeeper = "localhost:2181";// args[0];
	private String groupId = "group-test";// args[1];
	private String topic = "group-test-topic";// args[2];
	private int threads = 3;// Integer.parseInt(args[3]);
	private String outputfile;
	public String consumerId;
	private static ArrayList<String> topics = new ArrayList<String>();
	private ArrayList<ConsumerGroupListener> eventListeners = new ArrayList<ConsumerGroupListener>();
	public ConsumerTest cT;

	private ExecutorService executor;

	public ConsumerGroupExample(String a_zookeeper, String a_groupId, String a_topic, String output, String conId) {
		zooKeeper = a_zookeeper;// args[0];
		groupId = a_groupId;// args[1];
		topic = a_topic;// args[2];
		outputfile = output;
		// threads = 3;//Integer.parseInt(args[3]);
		consumerId = conId;
		consumer = kafka.consumer.Consumer.createJavaConsumerConnector(createConsumerConfig(a_zookeeper, a_groupId));
	}

	public ConsumerGroupExample() {
		zooKeeper = null;
		groupId = null;
		topic = null;
		outputfile = null;
		consumerId = null;
		consumer = null; // Consumer.createJavaConsumerConnector(createConsumerConfig(a_zookeeper,
							// a_groupId));
	}

	/*
	 * Method adds listeners
	 */
	public void addListeners(KafkaNode k) {
		eventListeners.add(k);
	}

	@Override
	public void newMessage(String message) {
		// TODO Auto-generated method stub
		// System.out.println("CGE got new message");
		for (ConsumerGroupListener list : eventListeners) {
			list.newMessage(message);
		}

	}

	@Override
	public void sendMessages() {
		// TODO Auto-generated method stub

	}

	@Override
	public void finishedRunning() {
		// TODO Auto-generated method stub
		for (ConsumerGroupListener list : eventListeners) {
			list.finishedRunning();
		}
	}

	public void shutdown() {
		if (consumer != null)
			consumer.shutdown();
		if (executor != null)
			executor.shutdown();
		try {
			if (!executor.awaitTermination(5000, TimeUnit.MILLISECONDS)) {
				System.out.println("Timed out waiting for consumer threads to shut down, exiting uncleanly");
			}
		} catch (InterruptedException e) {
			System.out.println("Interrupted during shutdown, exiting uncleanly");
		}
	}

	public void run(int a_numThreads) {
		// for (String topic : topics) {
		// topic = topics.get(0);
		Map<String, Integer> topicCountMap = new HashMap<String, Integer>();
		topicCountMap.put(topic, new Integer(a_numThreads));
		Map<String, List<KafkaStream<byte[], byte[]>>> consumerMap = consumer.createMessageStreams(topicCountMap);
		List<KafkaStream<byte[], byte[]>> streams = consumerMap.get(topic);

		// now launch all the threads
		//
		executor = Executors.newFixedThreadPool(a_numThreads);

		// now create an object to consume the messages
		//
		int threadNumber = 0;
		for (final KafkaStream stream : streams) {
			// System.out.println("Thread number: " + threadNumber);
			cT = new ConsumerTest(stream, threadNumber, groupId, topic, outputfile, consumerId);
			cT.addListeners(this);
			executor.submit(cT);
			threadNumber++;
		}
		// }
	}

	private static ConsumerConfig createConsumerConfig(String a_zookeeper, String a_groupId) {
		Properties props = new Properties();
		props.put("zookeeper.connect", a_zookeeper);
		props.put("group.id", a_groupId);
		props.put("zookeeper.session.timeout.ms", "400");
		props.put("zookeeper.sync.time.ms", "200");
		props.put("auto.commit.interval.ms", "1000");
		// props.put("auto.offset.reset", "smallest");

		return new ConsumerConfig(props);
	}

	public static void main(String[] args) {
//		zooKeeper = "localhost:2181";// args[0];
//		groupId = "group-test";// args[1];
//		topic = "group-test-topic";// args[2];
//		threads = 3;// Integer.parseInt(args[3]);

//		ConsumerGroupExample example = new ConsumerGroupExample(zooKeeper, groupId, topic, "test", "test");
//		example.run(threads);
//
//		try {
//			Thread.sleep(10000);
//		} catch (InterruptedException ie) {
//
//		}
//		example.shutdown();
	}

}