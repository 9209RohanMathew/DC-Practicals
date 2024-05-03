from threading import Thread, Lock
import time

class SuzukiKasami:
    def __init__(self, num_sites):
        self.num_sites = num_sites
        self.token = False
        self.RN = [0] * num_sites
        self.LN = [0] * num_sites
        self.token_queue = []
        self.lock = Lock()

    def request_critical_section(self, site_id):
        with self.lock:
            self.RN[site_id] += 1
            sn = self.RN[site_id]
            for j in range(self.num_sites):
                if j != site_id:
                    # Send request message to all other sites
                    self.send_request(site_id, j, sn)

    def send_request(self, site_id, receiver_id, sn):
        # Simulate sending request message
        time.sleep(0.1)
        self.receive_request(site_id, receiver_id, sn)

    def receive_request(self, site_id, sender_id, sn):
        with self.lock:
            self.RN[sender_id] = max(self.RN[sender_id], sn)
            if self.token and all(self.RN[j] == self.LN[j] + 1 for j in range(self.num_sites)):
                self.token = False
                self.LN[site_id] = self.RN[site_id]
                self.token_queue.append(site_id)
                if self.token_queue:
                    next_site_id = self.token_queue.pop(0)
                    self.token = True
                    print(f"Token sent to Site {next_site_id}")
                else:
                    self.token = True

    def execute_critical_section(self, site_id):
        with self.lock:
            if self.token:
                print(f"Site {site_id} is executing the critical section.")
            else:
                print(f"Site {site_id} is waiting for the token to execute the critical section.")

    def release_critical_section(self, site_id):
        with self.lock:
            self.LN[site_id] = self.RN[site_id]
            for j in range(self.num_sites):
                if j not in self.token_queue and self.RN[j] == self.LN[j] + 1:
                    self.token_queue.append(j)
            if self.token_queue:
                next_site_id = self.token_queue.pop(0)
                self.token = True
                print(f"Token sent to Site {next_site_id}")
            else:
                self.token = True

# Example usage
def simulate_execution(site_id, sk):
    sk.request_critical_section(site_id)
    sk.execute_critical_section(site_id)
    time.sleep(1)  # Simulating critical section execution
    sk.release_critical_section(site_id)

if __name__ == "__main__":
    num_sites = 5
    sk = SuzukiKasami(num_sites)
    threads = []

    for i in range(num_sites):
        thread = Thread(target=simulate_execution, args=(i, sk))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
