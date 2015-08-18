package com.spnotes.kafka;

public interface ConsumerTestListener {
	void newMessage(String message);
	void sendMessages();
	void finishedRunning();
}
