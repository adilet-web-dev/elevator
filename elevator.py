import time
import os
from random import randint, choice


class Client:
    def __init__(self, max_floor, current_floor_number) -> None:
        floors = list(range(1, max_floor+1))
        floors.remove(current_floor_number)
        self.target_floor = choice(floors)

    def __repr__(self) -> str:
        return str(self.target_floor)

class Floor:
    def __init__(self, number, max_floor) -> None:
        self.waiting_clients = [Client(max_floor, number) for i in range(randint(1, 4))]
        self.finished_clients = []
        self.number = number

        self.floor_len = 12

    def present_clients(self, clients, aditional_space=0) -> str:
        result = ""

        result += " ".join(map(lambda client: str(client.target_floor), clients))
        # for client in clients:
        #     result += str(client.target_floor) + " "
            
        result += " " * (self.floor_len - len(result) - aditional_space)

        return result

    def present_waiting_clients(self):
        return self.present_clients(self.waiting_clients)
        
    def present_finished_clients(self):
        return self.present_clients(self.finished_clients)
        

class Direction:
    UP = +1
    DOWN = -1


class Elevator:
    def __init__(self) -> None:
        self.current_floor_number = 1
        self.nearest_target_floor_number = 0
        self.current_clients: Client = []
        self.max_floor = 20
        self.floors = [Floor(i, self.max_floor) for i in range(1, self.max_floor + 1)]
        self.direction = Direction.UP

        self.reprint_frequency = 0.3


    def run(self):
        self.load_clients()
        self.update_nearest_target_floor()

        while True:
            self.current_floor_number += self.direction
            self.update_direction()
            self.load_clients()
            self.update_nearest_target_floor()

            if self.nearest_target_floor_number == self.current_floor_number:
                self.drop_off_clients()
                self.update_direction()
                self.load_clients()

                if len(self.current_clients) == 0:
                    current_floor = self.get_current_floor()
                    if len(current_floor.waiting_clients) == 0:
                        self.next_floor_number = self.get_nearest_clients_floor()
                        if self.next_floor_number > self.current_floor_number: 
                            self.direction = Direction.UP
                        else:
                            self.direction = Direction.DOWN
                        self.present()
                        time.sleep(self.reprint_frequency)
                        continue

                    self.load_clients_without_condition()
                    
                    first_client = self.current_clients[0]
                    if first_client.target_floor > self.current_floor_number:
                        self.direction = Direction.UP
                    elif first_client.target_floor < self.current_floor_number:
                        self.direction = Direction.DOWN

                self.update_nearest_target_floor()


            self.present()
            time.sleep(self.reprint_frequency)

    def update_direction(self):
        if self.current_floor_number == self.max_floor:
            self.direction = Direction.DOWN

        elif self.current_floor_number == 1:
            self.direction = Direction.UP

    def load_clients(self):
        current_floor = self.get_current_floor()

        if current_floor is None or len(current_floor.waiting_clients) == 0:
            return

        for client in current_floor.waiting_clients:
            if len(self.current_clients) < 3:
                clients_target_floor_is_on_the_way = \
                    (self.direction == Direction.UP and client.target_floor > self.current_floor_number) \
                    or \
                    (self.direction == Direction.DOWN and client.target_floor < self.current_floor_number)

                if clients_target_floor_is_on_the_way:
                    self.current_clients.append(client)

        for client in self.current_clients:
            if client in current_floor.waiting_clients:
                current_floor.waiting_clients.remove(client)
                

    def load_clients_without_condition(self):
        current_floor = self.get_current_floor()

        for client in current_floor.waiting_clients:
            if len(self.current_clients) < 3:
                self.current_clients.append(
                        current_floor.waiting_clients.pop(current_floor.waiting_clients.index(client))
                    )

    def drop_off_clients(self):
        current_floor = self.get_current_floor()
        for client in self.current_clients:
            if client.target_floor == self.current_floor_number:
                current_floor.finished_clients.append(client)

        for client in current_floor.finished_clients:
            if client in self.current_clients:
                self.current_clients.remove(client)
            

    def update_nearest_target_floor(self):
        if self.direction == Direction.UP:
            nearest_floor = 100

            for client in self.current_clients:
                if client.target_floor < nearest_floor:
                    nearest_floor = client.target_floor

            self.nearest_target_floor_number = nearest_floor

        elif self.direction == Direction.DOWN:
            nearest_floor = 1

            for client in self.current_clients:
                if client.target_floor > nearest_floor:
                    nearest_floor = client.target_floor

            self.nearest_target_floor_number = nearest_floor

    def get_nearest_clients_floor(self):

        minimum = 100
        best_floor_number = 1

        for floor in self.floors:
            if len(floor.waiting_clients) > 0:
                if abs(self.current_floor_number - floor.number) < minimum:
                    minimum = abs(self.current_floor_number - floor.number)
                    best_floor_number = floor.number

        return best_floor_number


    def get_current_floor(self):
        current_floor = None

        for floor in self.floors:
            if floor.number == self.current_floor_number:
                current_floor = floor

        return current_floor

    def present(self):
        os.system("cls")
        print("current floor:  ", self.current_floor_number)
        for floor in reversed(self.floors):
            cabine = "|"
            

            if floor.number == self.current_floor_number:
                cabine += "=="
                cabine += floor.present_clients(self.current_clients, 4)
                cabine += "=="

            else:
                cabine += " " * floor.floor_len

            cabine += "|"

            print(floor.present_waiting_clients(), cabine, floor.present_finished_clients())

        print("=" * 45)



elevator = Elevator()
elevator.run()
