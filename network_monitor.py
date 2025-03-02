import json
import os


total_k_bytes = 0
checked_ids_map = {}

def parse_traffic(traffic_file, hashmap):
    with open(traffic_file) as file:
        for line in file:
            if 'eth' in line:
                total_k_bytes = round(float(line.strip().split('bytes:')[-1]) / 1024, 2)

            if '<->' in line:
                parts = line.split()
                
                source_ip = parts[0].split(':')[0]
                source_port = parts[0].split(':')[1]

                destination_ip = parts[2].split(':')[0]
                destination_port = parts[2].split(':')[1]
                
                total_k_bytes_for_ip = float(parts[10].replace(',', ''))
                if parts[11] == 'bytes':
                    total_k_bytes_for_ip = total_k_bytes_for_ip / 1024

                if hashmap.get((source_ip,destination_ip)) is None:
                    hashmap[(source_ip,destination_ip)] = [total_k_bytes_for_ip, total_k_bytes]
                    hashmap[(source_ip,destination_ip)][0] = round(hashmap[(source_ip,destination_ip)][0], 2)
                    checked_ids_map[(source_ip,destination_ip)] = 1
                else:
                    if checked_ids_map.get((source_ip,destination_ip)) is None:
                        hashmap[(source_ip,destination_ip)][1] += total_k_bytes
                        hashmap[(source_ip,destination_ip)][1] = round(hashmap[(source_ip,destination_ip)][1], 2)
                        checked_ids_map[(source_ip,destination_ip)] = 1

                    hashmap[(source_ip,destination_ip)][0] += total_k_bytes_for_ip
                    hashmap[(source_ip,destination_ip)][0] = round(hashmap[(source_ip,destination_ip)][0], 2)

    return hashmap



def load_traffic_json(filename="network_log.json"):
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        return {}  
    
    with open(filename, "r") as f:
        json_data = json.load(f)

    # Convert string keys back to tuples
    hashmap = {eval(k): v for k, v in json_data.items()}
    return hashmap



def log_traffic_json(hashmap, filename="network_log.json"):
    json_data = {str(k): v for k, v in hashmap.items()}
    
    with open(filename, "w") as f:
        json.dump(json_data, f, indent=2)



if __name__ == "__main__":

    hashmap = load_traffic_json()
    hashmap = parse_traffic('traffic.log', hashmap)
    log_traffic_json(hashmap)