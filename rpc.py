import csv, json

#RPC
def processData(x):
    return x * 2

#RMI
class Server:
    def processData(self, x):
        return x * 2

server = Server()
choice = input("Enter 1 for RPC or 2 for RMI: ")

with open("rpc_calls_1.csv") as f:
    data = csv.reader(f)
    next(data)#skip header

    for r in data:
        #Client Annouces Call
        print("\n[DISPATCH]", r[1], "invoking", r[2], "at", r[4])

        #Client Packs the request
        packet = json.dumps({"method": r[2], "param": int(r[3])})  # marshal
        print("[MARSHAL]", packet)

        #Server unpacks the request
        d = json.loads(packet)
        x = d["param"]  # unmarshal on server
        print("[SERVER EXECUTION] Processing parameter:", x)

        #Execution
        if choice == "1":
            result = processData(x)
        else:
            result = server.processData(x)
        print("[RETURN] Result:", result)
