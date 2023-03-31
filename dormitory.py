from room import Room
class Dormitory:

    def __init__(self):
        self.rooms = {}
        self.num_blocks = 2
        for block_idx in range(1, self.num_blocks + 1):
            for i in range(2, 13):
                for j in range(1, 29):
                    self.rooms[f"D{block_idx}{i*100 + j}"] = Room(f"D{block_idx}{i*100 + j}")

    def __str__(self):
        result = "Dormitory:\n"
        for i in self.blocks.values():
            result += f"{i}\n"

        return result

    def num_students(self):
        res = 0
        for block in self.blocks.values():
            for room in block.rooms.values():
                res += len(room.students)

        return res

