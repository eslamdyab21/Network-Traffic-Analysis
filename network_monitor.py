

total_bytes = 0
with open('traffic.log') as file:
    for line in file:
        if 'eth' in line:
            total_bytes = int(line.strip().split('bytes:')[-1])
        if '<->' in line:
            parts = line.split()
            print(line.split())
            
            source_ip = parts[0].split(':')[0]
            source_port = parts[0].split(':')[1]

            destination_ip = parts[2].split(':')[0]
            destination_port = parts[2].split(':')[1]
            
            total_data_for_ip = int(parts[10])
            if parts[11] == 'bytes':
                total_data_for_ip = total_data_for_ip / 1024
        
        
            print("Source:", source_ip)
            print("Destination:", destination_ip)
            print("Total Data:", total_data_for_ip, 'KB')
            print()

    print('Total Bytes:', total_bytes/1024, 'KB')