#!/bin/bash

# Configurable Variables
INTERFACE="wlp8s0"  # Change this to your actual network interface
TIME=10  # Alert threshold in MB
LOG_FILE="network_monitor.log"


# Function to Capture Traffic
capture_traffic() {
    echo "⏳ Capturing traffic for $TIME seconds..."
    tcpdump -i $INTERFACE -w capture.pcap -G "$TIME" -W 1 -v
    echo "✅ Capture complete!"
}


# Function to Analyze Traffic
tshark_analyze_traffic() {
    tshark -r capture.pcap -qz io,phs > traffic.log
}


# Function to Analyze Traffic
python_analyze_traffic_by_ip() {
    tshark -r capture.pcap -q -z conv,udp >> traffic.log

    echo "⏳ Updating josn log..."
    python3 network_monitor.py
    echo "✅ Updating complete!"
}




# Run Monitoring Steps
echo "📡 Starting Packet Core Monitoring..."
capture_traffic
analyze_total_traffic
analyze_traffic_by_ip

echo "✅ Monitoring Complete!"

echo "📡 Starting Packet Core Monitoring..."
while true; do
    capture_traffic
    tshark_analyze_traffic
    python_analyze_traffic_by_ip
done
echo "✅ Monitoring Complete!"