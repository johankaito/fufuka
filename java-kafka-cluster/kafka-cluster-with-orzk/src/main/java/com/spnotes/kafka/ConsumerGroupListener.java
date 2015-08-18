package com.spnotes.kafka;

import java.util.EventListener;

public interface ConsumerGroupListener extends EventListener{
	void newMessage(String message);
	void sendMessages();
	void finishedRunning();

}
