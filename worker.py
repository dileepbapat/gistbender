from time import sleep
from pymongo import MongoClient
import subprocess

client = MongoClient('localhost',27017)
db = client['devday']
[i for i in db.get_collection("sketches").find()]



def update_status(docid, status, output=""):
    db.sketches.update_one({"_id":docid}, {"$set":{"status":status, "output":output}})

def runProcess(exe):
    p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
      retcode = p.poll() #returns None while subprocess is running
      line = p.stdout.readline()
      yield line
      if(retcode is not None):
        break


def run_it(first_doc):
    try:
        print "writing file"
        with open("/Users/dileepb/data/extsrc/Arduino-Makefile/examples/Blink/Blink.ino", "w") as f:
            f.write(first_doc["code"])
            f.close()
        result = [line for line in runProcess("/Users/dileepb/data/extsrc/Arduino-Makefile/examples/Blink/upload.sh")]
        print "completed upload"
        output = "".join(result)
        print result
        status = "Success" if "avrdude done.  Thank you." in "".join(result[-4:]) else "Failed"
        update_status(first_doc["_id"], status, output)
    except Exception as e:
        print "Error"
        update_status(first_doc["_id"], "failed")

while 1:
    docs = db.sketches.find({"status":"waiting"}).sort("date")
    try:
        first_doc = docs.next()
        first_id = first_doc["_id"]
        update_status(first_id, "running")
        run_it(first_doc)
    except StopIteration as e:
        sleep(2)
