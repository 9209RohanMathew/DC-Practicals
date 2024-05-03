import time
import threading

# Global variables
runningP = -1
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

# Display current state of RN arrays
def dispCurrentRNState():
    for key, value in RN.items():
        print(key, ": ", value)

# Update RN arrays
def updateRN(processNo, sequenceNumber):
    for key, value in RN.items():
        value[processNo] = max(value[processNo], sequenceNumber)

# Execute critical section and remaining tasks
def executeCS(processForCS):
    global token, runningP
    print("\n******************************\n")
    print(f"Process {processForCS} executing CS...")
    print('Token owner is: {}'.format(token["token_owner"]))
    time.sleep(10)
    print(f'\nProcess {processForCS} has completed running CS')
    # Process completed CS
    token["isRunning"] = False
    # Update LN
    token["LN"][processForCS] = RN[processForCS][processForCS]
    # Handle outstanding requests
    check_outstanding_requests()
    # Handing out the token
    if token["Q"]:
        # Pop a process from the queue and give it the token
        poppedPs = token["Q"].pop(0)
        token["token_owner"] = poppedPs
        token["isRunning"] = True
        print(f"Token sent to Process {poppedPs} from queue.")
        runningP = poppedPs
        thread = threading.Thread(target=executeCS, args=(poppedPs,))
        thread.start()

# Check for outstanding requests and update token queue
def check_outstanding_requests():
    global token
    token_owner = token["token_owner"]
    for index, val in enumerate(RN[token_owner]):
        if val == token["LN"][index] + 1 and index != runningP and index not in token["Q"]:
            # Outstanding Requests
            print(f'Process {index}\'s request is outstanding, it will be added to Token\'s Queue')
            token["Q"].append(index)
            print(f'Queue: {token["Q"]}')

if __name__ == "__main__":
    print("Running Main Again")
    # Display Current State of RN Arrays
    print("Current RN Arrays: ")
    dispCurrentRNState()
    print(" ")
    print('Token owner is: {}'.format(token["token_owner"]))

    while True:
        if token["isRunning"]:
            processes = input("Enter Process Numbers which want to access C.S separated by space (Click N for None): ")

            if processes != 'N':
                psList = processes.strip().split(" ")
                print(" ")
                for ps in psList:
                    processForCS = int(ps)
                    print(f"***** Process {processForCS} *****")
                    seqNo = RN[processForCS][processForCS] + 1
                    # Broadcasting Request
                    print(f"Process No.: {processForCS}")
                    print(f"Sequence No.: {seqNo}")
                    print(f"Broadcasting Request ({processForCS}, {seqNo}) .......")
                    time.sleep(2)
                    print("Broadcast complete")
                    print(" ")
                    # Updating RN Arrays
                    print("Updating RN Arrays at all process sites")
                    updateRN(processForCS, seqNo)
                    print("Current RN Arrays: ")
                    dispCurrentRNState()
                    print(" ")
            else:
                processForCS = int(input("Enter Process No. which wants to access C.S: "))
                seqNo = RN[processForCS][processForCS] + 1

                # Broadcasting Request
                print(f"Process No.: {processForCS}")
                print(f"Sequence No.: {seqNo}")
                print(f"Broadcasting Request ({processForCS}, {seqNo}) .......")
                time.sleep(2)
                print("Broadcast complete")
                print(" ")
                # Updating RN Arrays
                print("Updating RN Arrays at all process sites")
                updateRN(processForCS, seqNo)
                print("Current RN Arrays: ")
                dispCurrentRNState()
                print(" ")
                # Check condition of sending token: RNj[i] = LN[i] + 1
                if RN[token["token_owner"]][processForCS] == token["LN"][processForCS] + 1:
                    # give the token
                    print(f"Conditions met, giving token to {processForCS}...")
                    token["token_owner"] = processForCS
                    print('Token owner is: {}'.format(token["token_owner"]))
                    token["isRunning"] = True
                    runningP = processForCS
                    thread = threading.Thread(target=executeCS, args=(processForCS,))
                    thread.start()

            # Add an exit condition
            if input("Press 'E' to exit: ").lower() == 'e':
                break