from room import Room
from typing import Dict
class Dormitory:

    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.num_blocks = 1
        for block_idx in range(1, self.num_blocks + 1):
            for i in range(10, 12):
                for j in range(1, 29):
                    self.rooms[f"D{block_idx}{i*100 + j}"] = Room(f"D{block_idx}{i*100 + j}")

    def __str__(self):
        result = "Dormitory:\n"
        for i in self.rooms.values():
            result += f"{i}\n"

        return result

    def num_students(self):
        res = 0
        for room in self.rooms.values():
                res += len(room.students)

        return res

