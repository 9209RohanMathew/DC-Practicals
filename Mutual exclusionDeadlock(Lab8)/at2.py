import keyboard
import time
import threading

runningP = -1

# RN arrays of processes
RN = {
    0: [0, 0, 0, 0, 0],
    1: [0, 0, 0, 0, 0],
    2: [0, 0, 0, 0, 0],
    3: [0, 0, 0, 0, 0],
    4: [0, 0, 0, 0, 0]
}

token = {
    "token_owner": 2,
    "Q": [],
    "LN": [0, 0, 0, 0, 0],
    "isRunning": False
}

def dispCurrentRNState():
    print("Current RN Arrays:")
    for key, value in RN.items():
        print(f"{key} : {value}")

def updateRN(processNo, sequenceNumber):
    for key, value in RN.items():
        value[processNo] = max(value[processNo], sequenceNumber)

# Execute cs and remaining tasks
def executeCS(processForCS):
    global token, runningP
    print("\n******************************\n")
    print(f"Process {processForCS} executing CS...")
    print('Token owner is: {}'.format(token["token_owner"]))
    time.sleep(2)  # Simulating critical section execution
    print(f'\nProcess {processForCS} has completed running CS')
    # Process completed CS
    token["isRunning"] = False
    # Update LN
    token["LN"][processForCS] = RN[processForCS][processForCS]
    # Handle outstanding requests
    check_outstanding_requests()
    # Handing out the token
    if len(token["Q"]) != 0:
        # Pop a process from the queue and give it the token
        poppedPs = token["Q"].pop(0)
        token["token_owner"] = poppedPs
        token["isRunning"] = True
        print(f"Token sent to Process {poppedPs} from queue.")
        runningP = poppedPs
        thread = threading.Thread(target=executeCS, args=(poppedPs,))
        thread.start()

# Check for outstanding requests
def check_outstanding_requests():
    global token
    token_owner = token["token_owner"]
    for index, val in enumerate(RN[token_owner]):
        if val == token["LN"][index] + 1 and index not in token["Q"]:
            # Outstanding Requests
            print(f'Process {index}\'s request is outstanding, it will be added to Token\'s Queue')
            token["Q"].append(index)
            print(f'Queue: {token["Q"]}')

if __name__ == "__main__":
    # Display Current State of RN Arrays
    dispCurrentRNState()
    print("Token owner is:", token["token_owner"])
    print("\n")
    
    while True:
        if token["isRunning"]:
            processes = input("Enter Process Numbers which want to access C.S separated by space (Click N for None): ")
            if processes != 'N':
                psList = processes.strip().split(" ")
                print("\n")
                for ps in psList:
                    processForCS = int(ps)
                    print(f"***** Process {processForCS} *****")
                    seqNo = RN[processForCS][processForCS] + 1
                    # Broadcasting Request
                    print(f"Process No.: {processForCS}")
                    print(f"Sequence No.: {seqNo}")
                    print(f"Broadcasting Request ({processForCS}, {seqNo}) .......")
                    time.sleep(2)  # Simulating message broadcasting
                    print("Broadcast complete\n")
                    # Updating RN Arrays
                    print("Updating RN Arrays at all process sites")
                    updateRN(processForCS, seqNo)
                    dispCurrentRNState()
                    print("\n")

            else:
                processForCS = int(input("Enter Process No. which wants to access C.S: "))
                seqNo = RN[processForCS][processForCS] + 1
                # Broadcasting Request
                print(f"Process No.: {processForCS}")
                print(f"Sequence No.: {seqNo}")
                print(f"Broadcasting Request ({processForCS}, {seqNo}) .......")
                time.sleep(2)  # Simulating message broadcasting
                print("Broadcast complete\n")
                # Updating RN Arrays
                print("Updating RN Arrays at all process sites")
                updateRN(processForCS, seqNo)
                dispCurrentRNState()
                print("\n")
                # Check condition of sending token: RNj[i] = LN[i] + 1
                if RN[token["token_owner"]][processForCS] == token["LN"][processForCS] + 1:
                    # Give the token
                    print(f"Conditions met, giving token to {processForCS}...")
                    token["token_owner"] = processForCS
                    print('Token owner is:', token["token_owner"])
                    token["isRunning"] = True
                    runningP = processForCS
                    thread = threading.Thread(target=executeCS, args=(processForCS,))
                    thread.start()
                    
        if keyboard.is_pressed('E'):
            break
