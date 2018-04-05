import re
import json
import sys

def append_json0(log_text0, log_json_obj):

    if re.match(r"# Time", log_text0):
        time_split = re.split(r":", log_text0, maxsplit=1)
        log_json_obj[time_split[0]] = str(time_split[1]).strip()
	
    #User@Host
    elif re.match(r"# User@Host", log_text0):
        user_host_other = re.split(r":",log_text0)
        idKey = re.split(r"Id", str(user_host_other[1]))
        log_json_obj[user_host_other[0]] = idKey[0]
        log_json_obj["Id"] = user_host_other[-1]
        
    #Query_time
    elif re.match(r"# Query_time", log_text0):
        query_time_words = str(log_text0).split()
        log_json_obj["# "+ query_time_words[1]] = query_time_words[2]
        log_json_obj[query_time_words[3]] = query_time_words[4]
        log_json_obj[query_time_words[5]] = query_time_words[6]
        log_json_obj[query_time_words[7]] = query_time_words[8]
        
    #Database
    elif re.match(r"use", log_text0):
        use_db_name = log_text0.split()
        log_json_obj["db"] = use_db_name[1]
        
    #Timestamp
    elif re.match(r"SET timestamp", log_text0):
        timestamp = str(log_text0).split(r"=")
        log_json_obj["timestamp"] = timestamp[1]
        
    #SQL
    elif re.match(r"select", log_text0) or re.match(r"delete", log_text0) or re.match(r"update", log_text0):
        log_json_obj["sql"] = log_text0
    
def append_json(log_text, rows):
    line_item = {}
    items = re.split("\n", log_text)
    #print(items)
    for item in items:
        append_json0(item, line_item)
    rows.append(line_item)

def main():
    if len(sys.argv) < 3:
        print("Usage: python <log2json.py> <mysql-slow-query-log-file-path> <output-json-file-path>")
        sys.exit(2)

    with open(str(sys.argv[1]), 'r') as content_file:
        content = content_file.read()
    rows = []
    st_idx = -1
    ed_idx = -1
    while(ed_idx < len(content)):
        log_text = ""
        st_idx = content.find("# Time", st_idx + 1)
        ed_idx = content.find("# Time", st_idx + 6)
        if (ed_idx == -1):
            log_text = content[st_idx:-1]
            append_json(log_text, rows)
            break
        log_text = content[st_idx:ed_idx]
        append_json(log_text, rows)
        
    with open(str(sys.argv[2]), 'w') as outfile:
        json.dump(rows, outfile)
    print("Data Written to "+ str(sys.argv[2]))

if __name__== "__main__":
  main()