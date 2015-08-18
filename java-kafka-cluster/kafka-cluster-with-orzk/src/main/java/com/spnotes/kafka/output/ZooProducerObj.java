package com.spnotes.kafka.output;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

public class ZooProducerObj {

	public JSONArray topics;
	public String server;
	public JSONObject prod;

	public ZooProducerObj(){
		topics = new JSONArray();
		prod = new JSONObject();
		
	}
	
	public void addTopic(String topic){
		topics.add(topic);
		setJSON();
	}
	
	public void setServer(String inServer){
		server = inServer;
		setJSON();
	}
	
	public JSONObject getJSON(ZooProducerObj z){
		return z.prod;
	}
	
	private void setJSON(){
		prod.put("topics", topics);
		prod.put("server", server);
	}

	public static void main(String[] args) {

		ArrayList<String> topics1 = new ArrayList<String>();
		topics1.add("t1");
		topics1.add("t2");
		topics1.add("t3");
		//
		String server1 = "localhost:9092";
		// JSONObject p1 = new JSONObject();
		// p1.put("topics", topics1);
		// p1.put("server1", "localhost:9092");
		//
		// JSONArray topics2 = new JSONArray();
		// topics2.add("t4");
		// topics2.add("t5");
		// topics2.add("t6");
		//
		// JSONObject p2 = new JSONObject();
		// p2.put("topics", topics2);
		// p2.put("server2", "localhost:9092");
		//
		// JSONObject producers = new JSONObject();
		// producers.put("p1", p1);
		// producers.put("p2", p2);

//		 try {
//		 FileWriter file = new FileWriter("/Users/JKeto/Desktop/test.json");
//		 file.write(producers.toJSONString());
//		 file.flush();
//		 file.close();
//		
//		 } catch (IOException e) {
//		 e.printStackTrace();
//		 }

		ZooProducerObj zB = new ZooProducerObj();
		zB.addTopic("t1");
		zB.addTopic("t2");
		zB.setServer("localhost:9092");
		
//		JSONObject jO = getJSON(zB);
//		System.out.print(prod);
		
//		 try {
//		 FileWriter file = new FileWriter("/Users/JKeto/Desktop/test.json");
//		 file.write(prod.toJSONString());
//		 file.flush();
//		 file.close();
//		
//		 } catch (IOException e) {
//		 e.printStackTrace();
//		 }

	}

}

// JSONObject obj = new JSONObject();
// obj.put("name", "mkyong.com");
// obj.put("age", new Integer(100));
//
// JSONArray list = new JSONArray();
// list.add("msg 1");
// list.add("msg 2");
// list.add("msg 3");
//
// obj.put("messages", list);
//
// try {
// FileWriter file = new FileWriter("/Users/JKeto/Desktop/test.json");
// file.write(obj.toJSONString());
// file.flush();
// file.close();
//
// } catch (IOException e) {
// e.printStackTrace();
// }
//
// System.out.print(obj);
//
// }
