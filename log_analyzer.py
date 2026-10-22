import re
import json

def read_log_file():
    """ reads the log file and gives the output to be manipulated """

    with open("/home/milan/Documents/PythonPJTS/log_file_analyzer/logfile.log",'r') as file:
        content=file.read()
    return content

def generate_log_data(log_content):
    """ analzyes the lof content and returns the ouput to stored """

    activity_counter={}
    activity_data={}
    common_activiys=["ERROR","INFO","WARNING"]

    for activity in common_activiys:

        pattern=rf"\b{re.escape(activity)}\b"
        matchs=re.findall(pattern,log_content)

        activity_counter[activity]=len(matchs)

    for key,value in activity_counter.items():
        pattern=rf"\b{key}\b\s*(.*)"
        matchs=re.findall(pattern,log_content,flags=re.IGNORECASE)
        activity_data[key]=matchs

    found_ids=[]
    found_names=[]
    5
    for level,entries in activity_data.items():
        for entry in entries:
            login_ids=re.findall(r"\blogin\b.*?\buser[_-]id\s*[:=](\d+)\b",entry,flags=re.IGNORECASE)
            useranames=re.findall(r"\busername\s*[:=]\s*([^\s,;]+)",entry,flags=re.IGNORECASE)
            found_ids.extend(login_ids)
            found_names.extend(useranames)

    activity_data['login_ids']=found_ids
    activity_data['usernames']=found_names

    return[activity_counter,activity_data]

def save_log_result(data):
    """ saves the log-analyzation result to a cvs file"""

    with open("/home/milan/Documents/PythonPJTS/log_file_analyzer/log_analyzed_result.json",'w') as file:
        json.dump(data,file,indent=4)

    with open("/home/milan/Documents/PythonPJTS/log_file_analyzer/log_analyzed_result.json",'r') as file:
        saved=json.load(file)
    print(saved)

def main():

    raw_log=read_log_file()
    analyzation_result=generate_log_data(raw_log)
    save_log_result(analyzation_result)

if __name__=="__main__":
    main()

