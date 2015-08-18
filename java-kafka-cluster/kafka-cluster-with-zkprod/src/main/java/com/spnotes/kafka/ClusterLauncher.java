package com.spnotes.kafka;

import java.util.ArrayList;
import java.util.Random;

/*
 * Class launches two Kafka Clusters managed by one zookeeper: THE ORDER OF THE CALLING DOES MATTER BECAUSE THIS GUARANTEES THAT 
 * ALL THE DATA NEEDED BY A LATER PROCESS IS PRODUCED 
 */
public class ClusterLauncher implements ClusterListener {
	private static long startTime = System.currentTimeMillis();

	static String pre = "/Users/JKeto/Desktop/";
	static String hampre = "/Users/JKeto/Documents/Development/HelloKafka-master/src/main/java/com/spnotes/kafka/";
	static int threads = 1;
	static boolean run = true;
	public int runClusterFor;
	public ArrayList<KafkaNode> consumers = new ArrayList<KafkaNode>();
	public ArrayList<KafkaNode> producers = new ArrayList<KafkaNode>();
	public int sleepTime = 1000; // Sleeping time in milliseconds
	public int sleepThreads = 3;

	public ClusterLauncher(int numRuns) {
		runClusterFor = numRuns;

		int i = 0;
		while (i < runClusterFor) {
			System.out.println("----------------------------------------------");
			System.out.println("----------------------------------------------");
			System.out.println("-------------------Run: " + i + "-------------");
			System.out.println("----------------------------------------------");
			System.out.println("----------------------------------------------");

			try {
				ArrayList<String> node1In = new ArrayList<String>();
				node1In.add(hampre + "hamlet.txt");

				ArrayList<String> node2In = new ArrayList<String>();
				node2In.add(hampre + "hamlet.txt");

				ArrayList<String> node3In = new ArrayList<String>();
				node3In.add(hampre + "hamlet.txt");

				KafkaNode node1 = new KafkaNode(true, false, false); // Only
																		// producer
				node1.producer = new ProducerTest("localhost", 9092, "t1", "node1", pre + "node1p.out", node1In);
				producers.add(node1);
				node1.producer.start();
				node1.producer.join();

				KafkaNode node2 = new KafkaNode(true, false, false); // Only
																		// producer
				node2.producer = new ProducerTest("localhost", 9092, "t2", "node2", pre + "node2p.out", node2In);
				producers.add(node2);
				node2.producer.start();
				node2.producer.join();

				KafkaNode node3 = new KafkaNode(true, false, false); // Only
																		// producer
				node3.producer = new ProducerTest("localhost", 9092, "t3", "node3", pre + "node3p.out", node3In);
				producers.add(node3);
				node3.producer.start();
				node3.producer.join();

				// Consumer and producer
				KafkaNode node4 = new KafkaNode(true, true, false);
				node4.consumerGroup = new ConsumerGroupExample("localhost:2181", "node4", "t1", pre + "node4c.out",
						"node4");
				node4.consumerGroup.addListeners(node4);
				node4.consumerGroup.run(threads);
				// Delay to make sure processing finishes
				Thread.sleep(sleepTime);
				node4.producer = new ProducerTest("localhost", 9093, "t4", "node4", pre + "node4p.out");
				node4.producer.MESSAGES = node4.MESSAGES;
				producers.add(node4);
				consumers.add(node4);
				node4.producer.start();
				node4.producer.join();

				// Consumer
				KafkaNode node5 = new KafkaNode(true , true, false);
				node5.consumerGroup = new ConsumerGroupExample("localhost:2181", "node5", "t1", pre + "node5c.out",
						"node5");
				node5.consumerGroup.addListeners(node5);
				node5.consumerGroup.run(threads);
				consumers.add(node5);
				
				// Consumer and producer
				KafkaNode node6 = new KafkaNode(true, true, false);
				node6.consumerGroup = new ConsumerGroupExample("localhost:2181", "node6", "t3", pre + "node6c.out",
						"node6");
				node6.consumerGroup.addListeners(node6);
				node6.consumerGroup.run(threads);
				// Delay to make sure processing finishes
				Thread.sleep(sleepTime);
				node6.producer = new ProducerTest("localhost", 9093, "t6", "node6", pre + "node6p.out");
				node6.producer.MESSAGES = node6.MESSAGES;
				producers.add(node6);
				consumers.add(node6);
				node6.producer.start();
				node6.producer.join();

				// Consumer and producer
				KafkaNode node7 = new KafkaNode(true, true, false);
				node7.consumerGroup = new ConsumerGroupExample("localhost:2181", "node7", "t2", pre + "node7c.out",
						"node7:" + i);
				consumers.add(node7);
				node7.consumerGroup.addListeners(node7);
				node7.consumerGroup.run(threads);
				Thread.sleep(sleepTime);
				node7.producer = new ProducerTest("localhost", 9093, "t7", "node7", pre + "node7p.out");
				node7.producer.MESSAGES = node7.MESSAGES;
				producers.add(node7);
				consumers.add(node7);
				node7.producer.start();
				node7.producer.join();

				// Consumer
				KafkaNode node9 = new KafkaNode(false, true, true);
				node9.consumerGroup = new ConsumerGroupExample("localhost:2181", "node9", "t4", pre + "node9c.out",
						"node9");
				consumers.add(node9);
				node9.consumerGroup.run(threads);

				// Consumer
				KafkaNode node11 = new KafkaNode(false, true, true);
				node11.consumerGroup = new ConsumerGroupExample("localhost:2181", "node11", "t4", pre + "node11c.out",
						"node11");
				consumers.add(node11);
				node11.consumerGroup.run(threads);

				// Consumer
				KafkaNode node8 = new KafkaNode(false, true, true);
				node8.consumerGroup = new ConsumerGroupExample("localhost:2181", "node8", "t6", pre + "node8c.out",
						"node8");
				consumers.add(node8);
				node8.consumerGroup.run(threads);

				// Consumer
				KafkaNode node10 = new KafkaNode(false, true, true);
				node10.consumerGroup = new ConsumerGroupExample("localhost:2181", "node10", "t6", pre + "node10c.out",
						"node10");
				consumers.add(node10);
				node10.consumerGroup.run(threads);
				
				// Consumer
				KafkaNode node12 = new KafkaNode(false, true, true);
				node12.consumerGroup = new ConsumerGroupExample("localhost:2181", "node12", "t7", pre + "node12c.out",
						"node12");
				consumers.add(node12);
				node12.consumerGroup.run(threads);
				
				Random r = new Random();
				int sleeptime = 5000 + r.nextInt(10000);
				System.out.println("----------------------------------------------");
				System.out.println("----------------------------------------------");
				System.out.println("------Sleeping-for: " + sleeptime + "ms-------");
				System.out.println("----------------------------------------------");
				System.out.println("----------------------------------------------");
				Thread.sleep(sleeptime);
				// Shutdown all the consumer threads
				for (KafkaNode con : consumers) {
					try {
						con.consumerGroup.shutdown();
						System.out.println(con.consumerGroup.consumerId + " is shutdown.");
					} catch (Exception e) {
						System.err.println(e + " when shutting down consumer: " + con.consumerGroup.consumerId);
					}
				}

				// Finished

				// for(KafkaNode pro: producers){
				//
				// }

			} catch (InterruptedException e) {
				System.out.println(e);
			}
			System.out.println("----------------------------------------------");
			System.out.println("----------------------------------------------");
			System.out.println("-------------End-of-Run: " + i + "------------");
			System.out.println("----------------------------------------------");
			System.out.println("----------------------------------------------");
			i++;
		}
		System.out.println("All threads have been shutdown.");
		long endTime = System.currentTimeMillis();
		System.out.println("Program took " + (endTime - startTime) + " milliseconds including "
				+ runClusterFor * sleepThreads * sleepTime + " milliseconds of sleep time");

	}

	public static void main(String[] args) throws InterruptedException {
		ClusterLauncher newL = new ClusterLauncher(30);

		// try {
		// Thread.sleep(40000);
		// } catch (Exception e) {
		// System.err.println("Thread not sleeping");
		// }
		//
		// System.out.println("All consumer threads done!");
		//
		// try {
		// node1.consumerGroup.shutdown();
		// node2.consumerGroup.shutdown();
		// node3.consumerGroup.shutdown();
		// //node4.consumerGroup.shutdown();
		// node5.consumerGroup.shutdown();
		// node6.consumerGroup.shutdown();
		// node7.consumerGroup.shutdown();
		// node8.consumerGroup.shutdown();
		// node9.consumerGroup.shutdown();
		// } catch (Exception e) {
		// System.out.println("All threads shutdown");
		// }
	}

	public void continueCluster(boolean input) {
		run = true;
	}

	public void stopCluster(boolean input) {
		run = false;

	}

	// public static void main(String[] args) throws InterruptedException {
	//
	// ArrayList<String> node1In = new ArrayList<String>();
	// node1In.add(hampre + "hamlet.txt");
	//
	// ArrayList<String> node2In = new ArrayList<String>();
	// node2In.add(hampre + "hamlet.txt");
	//
	// ArrayList<String> node3In = new ArrayList<String>();
	// node3In.add(hampre + "hamlet.txt");
	//
	//
	// KafkaNode node1 = new KafkaNode(true, false); // Only producer
	// node1.producer = new ProducerTest("t1", node1In, "node1", pre +
	// "node1.out");
	// node1.producer.start();
	// node1.producer.join();
	//
	// KafkaNode node4 = new KafkaNode(false, true);// Only consumer
	// node4.consumerGroup = new ConsumerGroupExample("localhost:2181", "g4",
	// "t1", pre + "node4.out", "node4");
	// node4.consumerGroup.run(threads);
	//
	// KafkaNode node5 = new KafkaNode(false, true);// Only consumer
	// node5.consumerGroup = new ConsumerGroupExample("localhost:2181", "g5",
	// "t1", pre + "node5.out", "node5");
	// node5.consumerGroup.run(threads);
	//
	// KafkaNode node6 = new KafkaNode(false, true);// Only consumer
	// node6.consumerGroup = new ConsumerGroupExample("localhost:2181", "g6",
	// "t3", pre + "node6.out", "node6");
	// node6.consumerGroup.run(threads);
	//
	// KafkaNode node7 = new KafkaNode(false, true);// Only consumer
	// node7.consumerGroup = new ConsumerGroupExample("localhost:2181", "g7",
	// "t2", pre + "node7.out", "node7");
	// node7.consumerGroup.run(threads);
	//
	// KafkaNode node2 = new KafkaNode(true, false); // Only producer
	// node2.producer = new ProducerTest("t2", node2In, "node2", pre +
	// "node2.out");
	// node2.producer.start();
	// node2.producer.join();
	//
	// KafkaNode node3 = new KafkaNode(true, false); // Only producer
	// node3.producer = new ProducerTest("t3", node3In, "node3", pre +
	// "node3.out");
	// node3.producer.start();
	// node3.producer.join();
	//
	// node4.consumerGroup.join();
	// node5.consumerGroup.join();
	// node6.consumerGroup.join();
	// node7.consumerGroup.join();
	//
	// System.out.println("All consumer threads done!");
	// node4.consumerGroup.shutdown();
	// node5.consumerGroup.shutdown();
	// node6.consumerGroup.shutdown();
	// node7.consumerGroup.shutdown();
	// }
}