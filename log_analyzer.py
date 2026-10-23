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
    common_activiys=["ERROR","INFO","WARN"]

    for activity in common_activiys:

        pattern=r"\bWARN(:?ING)?\b" if activity=="WARN" else rf"\b{activity}\b"
        match=re.findall(pattern,log_content,re.IGNORECASE)

        activity_counter[activity]=len(match)
        activity_data[activity]=match

    user_ids = re.findall(r"\buser_id[:=]([^\s]+)", log_content)
    usernames = re.findall(r"\busername[:=]([^\s]+)", log_content)
    request_ids = re.findall(r"\brequest_id[:=]([^\s]+)", log_content)

    activity_data["user-ids"]=list(set(user_ids))
    activity_data["useranames"]=list(set(usernames))
    activity_data["request-ids"]=list(set(request_ids))

    return {
    "activity_counter": activity_counter,
    "activity_data": activity_data
    }


def health_overview(logfile,data):
    """makes a report of the entire health of the system by analyzing the log"""

    total_request=len(re.findall(r"\brequest_id\b",logfile,flags=re.IGNORECASE))
    errors=len(re.findall(r"\berror\b",logfile,flags=re.IGNORECASE))
    Warnings=len(re.findall(r"\bwarning\b",logfile,flags=re.IGNORECASE))

    error_rate=(errors/total_request)*100 if total_request > 0 else 0.0

    if error_rate == 0 and errors == 0:
        status = "Healthy"
    elif error_rate < 5.0:
        status = "Degraded"
    else:
        status = "Critical"

    data["health-result"]=[{
        "total-request":total_request,
        "erros":errors,
        "error-rate":round(error_rate,2),
        "status":status,
        "warnings":Warnings
    }]
    
    

def save_log_result(data):
    """ saves the log-analyzation result to a cvs file"""

    with open("/home/milan/Documents/PythonPJTS/log_file_analyzer/log_analyzed_result.json",'w') as file:
        json.dump(data,file,indent=4)

def main():

    raw_log=read_log_file()
    analyzation_result=generate_log_data(raw_log)
    save_log_result(analyzation_result)
    health_overview(raw_log,analyzation_result)


if __name__=="__main__":
    main()

