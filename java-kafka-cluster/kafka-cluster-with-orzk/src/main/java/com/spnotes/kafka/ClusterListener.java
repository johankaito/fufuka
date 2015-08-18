package com.spnotes.kafka;

public interface ClusterListener {
	void continueCluster(boolean b);
	void stopCluster(boolean b);

}
