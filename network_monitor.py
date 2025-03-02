import json
import os


def parse_traffic(traffic_file, hashmap):

    with open(traffic_file) as file:
        for line in file:
            if 'eth' in line:
                total_k_bytes = round(float(line.strip().split('bytes:')[-1]) / 1024, 2)
                if hashmap.get("total_k_bytes"):
                    hashmap["total_k_bytes"] += total_k_bytes
                    hashmap["total_k_bytes"] = round(hashmap["total_k_bytes"], 2)
                else:
                    hashmap["total_k_bytes"] = total_k_bytes

            if '<->' in line:
                parts = line.split()
                
                source_ip = parts[0].split(':')[0]
                source_port = parts[0].split(':')[1]

                destination_ip = parts[2].split(':')[0]
                destination_port = parts[2].split(':')[1]
                
                total_k_bytes_for_ip = float(parts[10].replace(',', ''))
                if parts[11] == 'bytes':
                    total_k_bytes_for_ip = total_k_bytes_for_ip / 1024


                hashmap_key = tuple(sorted((source_ip, destination_ip)))
                if hashmap.get(hashmap_key) is None:
                    hashmap[hashmap_key] = total_k_bytes_for_ip
                    hashmap[hashmap_key] = round(hashmap[hashmap_key], 2)
                else:
                    hashmap[hashmap_key] += total_k_bytes_for_ip
                    hashmap[hashmap_key] = round(hashmap[hashmap_key], 2)

    return hashmap



def load_traffic_json(filename="network_log.json"):
    if not os.path.exists(filename) or os.stat(filename).st_size == 0:
        return {}

    with open(filename, "r") as f:
        json_data = json.load(f)

    total_k_bytes = json_data.pop("total_k_bytes", 0)

    hashmap = {tuple(eval(k)): v for k, v in json_data.items()}


    hashmap["total_k_bytes"] = total_k_bytes  
    return hashmap



def log_traffic_json(hashmap, filename="network_log.json"):
    json_data = {str(k): v for k, v in hashmap.items()}
    
    with open(filename, "w") as f:
        json.dump(json_data, f, indent=2)



if __name__ == "__main__":

    hashmap = load_traffic_json()
    hashmap = parse_traffic('traffic.log', hashmap)
    log_traffic_json(hashmap)