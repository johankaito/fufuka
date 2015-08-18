package com.spnotes.kafka;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Properties;

import org.I0Itec.zkclient.ZkClient;

import com.spnotes.kafka.output.ZooProducerObj;

import kafka.javaapi.producer.Producer;
import kafka.producer.KeyedMessage;
import kafka.producer.ProducerConfig;
import kafka.utils.ZKStringSerializer$;

/**
 * Created by user on 8/4/14.
 */
public class ProducerTest extends Thread {
	public String TOPIC;
	public ArrayList<String> MESSAGES;
	public String SERVERURL;
	public int PORT;
	public String OUTPUTFILE;
	public ArrayList<String> INPUTFILE;
	public SimpleDateFormat sdf = new SimpleDateFormat();
	public String ProducerId;
	public int sessionTimeoutMs = 10000;
	public int connectionTimeoutMs = 10000;
	ZkClient zkClient;

	public static void main(String[] args) {
		// ProducerTest p1 = new ProducerTest("t1", "p1");
		// p1.start();
	}

	/*
	 * Constructor for null producer
	 */
	public ProducerTest() {
		MESSAGES = new ArrayList<String>();
		SERVERURL = "";
		PORT = 0;
		TOPIC = "";
		OUTPUTFILE = "";
	}

	/*
	 * Constructor for CONSECUTIVE producers
	 */
	public ProducerTest(String serverUrl, int portNumber, String topic, String prod, String output) {

		SERVERURL = serverUrl;
		PORT = portNumber;
		TOPIC = topic;
		OUTPUTFILE = output;
		ProducerId = prod;

		zkClient = new ZkClient("localhost:2181", sessionTimeoutMs, connectionTimeoutMs, ZKStringSerializer$.MODULE$);

		// MESSAGES is set during run-time as the producer receives from other
		// nodes

		// System.out.println("Producer is: " + Prod + " posting on: " + TOPIC +
		// " and writing to: " + OUTPUTFILE);

		// Read all the emssages
		// System.out.println("About to read " + MESSAGES.size() + " messages
		// for: " + Prod);

		// System.out.println("Messages:");
		// for (String s : MESSAGES) {
		// System.out.println(s);
		// }
	}

	/*
	 * Constructor for the very first producers
	 */
	public ProducerTest(String serverUrl, int portNumber, String topic, String prod, String output,
			ArrayList<String> inputfiles) {
		// MESSAGES =
		// readFile("/Users/JKeto/Documents/Development/HelloKafka-master/src/main/java/com/spnotes/kafka/hamlet.txt",0);
		ProducerId = prod;
		SERVERURL = serverUrl;
		PORT = portNumber;
		TOPIC = topic;
		OUTPUTFILE = output;
		INPUTFILE = inputfiles;
		// System.out.println("Producer is: " + Prod + " posting on: " + TOPIC +
		// " and writing to: " + OUTPUTFILE);

		// Read all the emssages
		// System.out.println("About to read " + inputfiles.size() + " files
		// for: " + Prod);
		MESSAGES = new ArrayList<String>();
		for (String file : inputfiles) {
			// System.out.println("Reading: " + file);
			MESSAGES.addAll(readFile(file, 0));
		}

		zkClient = new ZkClient("localhost:2181", sessionTimeoutMs, connectionTimeoutMs, ZKStringSerializer$.MODULE$);
		// System.out.println("Messages:");
		// for (String s : MESSAGES) {
		// System.out.println(s);
		// }
	}

	@Override
	public void run() {
		// Keep reading the input file one second at a time
		String dest = SERVERURL + ":" + PORT;
		Properties properties = new Properties();
		properties.put("metadata.broker.list", dest);// ,"localhost:9093");
		properties.put("serializer.class", "kafka.serializer.StringEncoder");
		ProducerConfig producerConfig = new ProducerConfig(properties);
		Producer<String, String> producer = new Producer<String, String>(producerConfig);

		KeyedMessage<String, String> message;

		try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(OUTPUTFILE, true)))) {
			out.println(">>>" + ProducerId + ">>>OUTPUT");
		} catch (IOException e) {
			// exception handling left as an exercise for the reader
			System.out.println("oups, error: " + e);
			System.out.println("Failed to write to: " + OUTPUTFILE);
		}
		// System.out.println(Prod + " before the msg for loop");

		for (String s : MESSAGES) {
			// try {
			// Thread.sleep(1000);
			// String s = MESSAGES.get(s);
			message = new KeyedMessage<String, String>(TOPIC, "Prod: " + ProducerId + " MSG: " + s);
			// System.out.println("About to send");
			try {
				producer.send(message);
				// Register producer on to zookeeper
				//System.out.println("Registering producer in kafka :" + ProducerId);
				//createZKNode();

			} catch (Exception e) {
				System.err.println(ProducerId + " failed to send message because " + e);
			}

			System.out.println(ProducerId + " sending: " + s);
			try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(OUTPUTFILE, true)))) {
				out.println(s);
			} catch (IOException e) {
				// exception handling left as an exercise for the reader
				System.out.println("oups, error");
			}
			// } catch (InterruptedException ie) {
			// // Handle exception
			// System.err.println("sleeping was interrupted");
			// }
		}

		producer.close();
	}

	private void createZKNode() {
		ZooProducerObj zB = new ZooProducerObj();
		zB.setServer(SERVERURL + ":" + PORT);
		zB.addTopic(TOPIC);
		// System.out.println("JSON is: " + zB.prod);
		try {
			if (!zkClient.exists("/producers")) {
				// Create the root producer node
				zkClient.createPersistent("/producers");
			}
			
			// Create the node for this producer and corresponding server
			// and topics
			zkClient.createPersistent("/producers/" + ProducerId, zB.toString());
			zkClient.createPersistent("/producers/" + ProducerId + "/topics");
			zkClient.createPersistent("/producers/" + ProducerId + "/server");
			zkClient.createPersistent("/producers/" + ProducerId + "/server/" + SERVERURL + ":" + PORT);
			zkClient.createPersistent("/producers/" + ProducerId + "/topics/" + TOPIC);
		} catch (Exception e) {
			System.out.println("Not created. Exception " + e);
		}

	}

	public static ArrayList<String> readFile(String file, int lines) {

		// System.out.println("Reading: " + file);
		// The name of the file to open.
		String fileName = file;
		ArrayList<String> output = new ArrayList<String>();

		// This will reference one line at a time
		String line = null;

		// Counter for lines
		int counter = 0;

		try {
			// FileReader reads text files in the default encoding.
			FileReader fileReader = new FileReader(fileName);

			// Always wrap FileReader in BufferedReader.
			BufferedReader bufferedReader = new BufferedReader(fileReader);

			while ((line = bufferedReader.readLine()) != null) {
				counter++;
				output.add(line);
				// System.out.println(line);

				if (lines != 0) {
					if (counter == lines) {
						// Always close files.
						bufferedReader.close();
						return output;
					}
				}
			}

			// Always close files.
			bufferedReader.close();

		} catch (FileNotFoundException ex) {
			System.out.println("Unable to open file '" + fileName + "'");
		} catch (IOException ex) {
			System.out.println("Error reading file '" + fileName + "'");
			// Or we could just do this:
			// ex.printStackTrace();
		}
		return output;
	}

}
