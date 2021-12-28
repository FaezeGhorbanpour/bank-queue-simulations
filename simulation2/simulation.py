from random import expovariate, seed
import math
import random
from numpy import arange
from heap import Heap


def next_time(landa):
    # t = expovariate(1.0/landa)
    # return expovariate(1.0/landa)
    return -math.log(1.0 - random.random()) / landa


class EventType:
    ENTRANCE = 1
    DEADLINE = 2


class Event:
    def __init__(self, type, event_time, customer_number):
        self.type = type
        self.time = event_time
        self.customer = customer_number


class EventCreator:
    def __init__(self):
        self.deleted_customers = set()
        self.times = Heap()

    def get_events(self):
        next_event = self.times.heappop()
        while next_event and (next_event.type == EventType.DEADLINE and next_event.customer in self.deleted_customers):
            self.deleted_customers.remove(next_event.customer)
            next_event = self.times.heappop()
        return next_event

    def make_event(self, type, event_time, customer_number):
        new_event = Event(type, event_time, customer_number)
        self.times.heappush(new_event)


class Customer:
    def __init__(self, id, entrance_time, waiting_time, service_time, left_service_time, class_):
        self.id = id
        self.entrance_time = entrance_time
        self.waiting_time = waiting_time
        self.service_time = service_time
        self.time = left_service_time
        self.class_ = class_


class CustomerCreator:
    def __init__(self, type, landa, mu, teta):
        self.customer_number = 0
        self.type = type
        self.landa = landa
        self.mu = mu
        self.teta = teta
        self.customers = list()
        self.maximum_customer_number = 10**5
        self.create_customers()

    def create_customer(self, previous_time):
        if previous_time == -1:
            entrance_time = 0
        else:
            entrance_time = next_time(self.landa) + previous_time
        service_time = next_time(self.mu)
        if self.type == 'fixed':
            waiting_time = self.teta
        else:
            waiting_time = next_time(1 / self.teta)
        new_class = random.randint(1, 2)
        new_customer = Customer(self.customer_number, entrance_time=entrance_time, waiting_time=waiting_time,
                                service_time=service_time, left_service_time=service_time, class_=new_class)
        return new_customer

    def create_customers(self):
        previous_time = -1
        while self.customer_number < self.maximum_customer_number:
            self.customer_number += 1
            new_customer = self.create_customer(previous_time)
            previous_time = new_customer.entrance_time
            self.customers.append(new_customer)

    def get_customer(self, index):
        return self.customers[index - 1]


class Server:
    def __init__(self, customer_creator):
        self.queue = list()
        self.time = 0
        self.blocked_customer_number = 0
        self.deadlined_customer_number = 0
        self.event_creator = EventCreator()
        self.customer_creator = customer_creator
        self.serviced_customer_number = 0

    def start(self):
        for i in range(self.customer_creator.maximum_customer_number):
            customer = self.customer_creator.customers[i]
            self.event_creator.make_event(EventType.ENTRANCE, customer.entrance_time, customer.id)
        new_event = self.event_creator.get_events()
        while len(self.event_creator.times) > 0:
            self.time = new_event.time
            self.check(new_event)
            next_event = self.event_creator.get_events()
            if next_event is None:
                break
            delta = next_event.time - self.time
            self.check_server(delta)
            new_event = next_event
        return self.deadlined_customer_number / self.customer_creator.maximum_customer_number, \
               self.blocked_customer_number / self.customer_creator.maximum_customer_number

    def add_queue(self, new_customer: Customer):
        new_queue = list()
        replaced = False
        for i, customer in enumerate(self.queue):
            if new_customer.time / new_customer.class_ <= customer.time / customer.class_:
                new_queue.append(new_customer)
                new_queue += self.queue[i:]
                replaced = True
                break
            new_queue.append(customer)
        if not replaced:
            new_queue.append(new_customer)
        self.queue = list(new_queue)

    def check(self, event: Event):
        current_customer = self.customer_creator.get_customer(event.customer)
        if event.type == EventType.ENTRANCE:
            if len(self.queue) < 12:
                self.add_queue(current_customer)
                deadline_time = self.time + current_customer.waiting_time
                self.event_creator.make_event(EventType.DEADLINE, deadline_time, current_customer.id)
            else:
                self.blocked_customer_number += 1
        elif event.type == EventType.DEADLINE and event.customer not in self.event_creator.deleted_customers:
            index = self.queue.index(current_customer)
            del self.queue[index]
            self.deadlined_customer_number += 1

    def check_server(self, delta):
        new_queue = list(self.queue)
        for i, customer in enumerate(new_queue):
            classes = [0, 0]
            for c in self.queue:
                classes[c.class_-1] += 1
            if classes == [0, 0]:
                unit = delta
                print('hi')
            else:
                unit = delta / (classes[0] + 2 * classes[1])
            if customer.time <= customer.class_ * unit:
                delta += unit - customer.time
                customer.time = 0
                self.queue.remove(customer)
                self.event_creator.deleted_customers.add(customer.id)
            else:
                customer.time -= customer.class_ * unit

def main():
    landas = [i for i in arange(0.1, 20.1, 0.1)]
    landas = [5, 10, 15]
    with open('parameters.conf', 'r') as f:
        teta = int(f.readline())
        mu = int(f.readline())
    # mu = 2
    # teta = 1
    string = ''
    print('fixed')
    for landa in landas:
        customer_creator = CustomerCreator('fixed', landa, mu, teta)
        service = Server(customer_creator)
        pd, pb = service.start()
        string += str(landa) + '\t' + str(pd) + '\t' + str(pb) + '\n'
    with open('3fixed6.txt', 'w') as f:
        f.write(string)
    print(string)
    print('exp')
    string = ''
    for landa in landas:
        customer_creator = CustomerCreator('exp', landa, mu, teta)
        service = Server(customer_creator)
        pd, pb = service.start()
        string += str(landa) + '\t' + str(pd) + '\t' + str(pb) + '\n'
    with open('3exp6.txt', 'w') as f:
        f.write(string)
    print(string)
