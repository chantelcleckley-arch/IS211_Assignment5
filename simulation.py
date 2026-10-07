import csv
import argparse
from collections import deque


class Request:
    def __init__(self, arrival_time, file_name, processing_time):
        self.arrival_time = int(arrival_time)
        self.file_name = file_name
        self.processing_time = int(processing_time)
        self.start_time = None

    def wait_time(self, current_time):
        return current_time - self.arrival_time


class Server:
    def __init__(self):
        self.current_request = None
        self.time_remaining = 0

    def busy(self):
        return self.current_request is not None

    def start_next(self, request):
        self.current_request = request
        self.time_remaining = request.processing_time

    def tick(self):
        if self.current_request:
            self.time_remaining -= 1

            if self.time_remaining <= 0:
                self.current_request = None
def read_requests(filename):
    requests = []

    with open(filename, "r") as file:
        reader = csv.reader(file)

        for row in reader:
            if not row:
                continue

            arrival_time = row[0].strip()
            file_name = row[1].strip()
            processing_time = row[2].strip()

            requests.append(
                Request(arrival_time, file_name, processing_time)
            )

    return requests


def simulateOneServer(filename):
    requests = read_requests(filename)
    request_queue = deque()
    server = Server()
    wait_times = []

    current_time = 0
    request_index = 0

    while request_index < len(requests) or request_queue or server.busy():

        while (
            request_index < len(requests)
            and requests[request_index].arrival_time == current_time
        ):
            request_queue.append(requests[request_index])
            request_index += 1

        if not server.busy() and request_queue:
            next_request = request_queue.popleft()

            wait = next_request.wait_time(current_time)
            wait_times.append(wait)

            server.start_next(next_request)

        server.tick()
        current_time += 1

    if wait_times:
        average_wait = sum(wait_times) / len(wait_times)
    else:
        average_wait = 0

    print("Average wait time:", average_wait)

    return average_wait
def simulateManyServers(filename, number_of_servers):
    requests = read_requests(filename)

    servers = [Server() for _ in range(number_of_servers)]
    queues = [deque() for _ in range(number_of_servers)]

    wait_times = []
    current_time = 0
    request_index = 0
    next_server = 0

    while (
        request_index < len(requests)
        or any(queues)
        or any(server.busy() for server in servers)
    ):

        while (
            request_index < len(requests)
            and requests[request_index].arrival_time == current_time
        ):
            queues[next_server].append(requests[request_index])

            next_server = (next_server + 1) % number_of_servers
            request_index += 1

        for i in range(number_of_servers):

            if not servers[i].busy() and queues[i]:
                next_request = queues[i].popleft()

                wait = next_request.wait_time(current_time)
                wait_times.append(wait)

                servers[i].start_next(next_request)

        for server in servers:
            server.tick()

        current_time += 1

    if wait_times:
        average_wait = sum(wait_times) / len(wait_times)
    else:
        average_wait = 0

    print("Average wait time:", average_wait)

    return average_wait
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file",
        required=True,
        help="CSV file containing network requests"
    )

    parser.add_argument(
        "--servers",
        type=int,
        help="Number of servers to simulate"
    )

    args = parser.parse_args()

    if args.servers:
        simulateManyServers(args.file, args.servers)
    else:
        simulateOneServer(args.file)


if __name__ == "__main__":
    main()
