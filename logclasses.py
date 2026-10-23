import re
import json

class Log_Analyzer:
    def __init__(self,log_path,output_path):
        self.log_path=log_path
        self.output_path=output_path
        self.content=""
        self.result={}

    def read(self):
        with open(self.log_path,"r") as f:
            self.content=f.read()

    def count_levels(self):
        """ analzyes the lof content and returns the ouput to stored """

        activity_counter={}
        activity_data={}
        common_activiys=["ERROR","INFO","WARN"]

        for activity in common_activiys:

            pattern=r"\bWARN(:?ING)?\b" if activity=="WARN" else rf"\b{activity}\b"
            match=re.findall(pattern,self.content,re.IGNORECASE)

            activity_counter[activity]=len(match)
            activity_data[activity]=match

            self.result["activity_counter"]=activity_counter
            self.result["activity_data"]=activity_data


    def extract_ids(self):
        user_ids = re.findall(r"\buser_id[:=]([^\s]+)", self.content)
        usernames = re.findall(r"\busername[:=]([^\s]+)", self.content)
        request_ids = re.findall(r"\brequest_id[:=]([^\s]+)", self.content)


        self.result["activity_data"].update({
            "user_ids": list(set(user_ids)),
            "usernames": list(set(usernames)),
            "request_ids": list(set(request_ids)),
})

    def health_overview(self):
        """makes a report of the entire health of the system by analyzing the log"""

        total_request=len(re.findall(r"\brequest_id\b",self.content,flags=re.IGNORECASE))
        errors=len(re.findall(r"\berror\b",self.content,flags=re.IGNORECASE))
        Warnings=len(re.findall(r"\bwarning\b",self.content,flags=re.IGNORECASE))

        error_rate=(errors/total_request)*100 if total_request > 0 else 0.0

        if error_rate == 0 and errors == 0:
            status = "Healthy"
        elif error_rate < 5.0:
            status = "Degraded"
        else:
            status = "Critical"

        self.result["health-result"]={
            "total-request":total_request,
            "erros":errors,
            "error-rate":round(error_rate,2),
            "status":status,
            "warnings":Warnings
        }


    def summary(self):
        self.result["summary"] = {
        "number of warnings": self.result["health-result"]["warnings"],
            "evidence": re.findall(
                r"^.*\bWARNING\b.*$",
                self.content,
                re.IGNORECASE | re.MULTILINE
            )
        }

    def save_log_result(self):
        """ saves the log-analyzation result to a cvs file"""

        with open(self.output_path,'w') as file:
            json.dump(self.result,file,indent=4)

    def run(self):
        self.read()
        self.count_levels()
        self.extract_ids()
        self.health_overview()
        self.summary()
        self.save_log_result()


if __name__ == "__main__":
    analyzer = Log_Analyzer("path/to/logfile.log", "path/to/output.json")
    analyzer.run()