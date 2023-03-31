from room import Room
class Block:
    def __init__(self, block_number):
        self.block_number = block_number
        self.rooms = {}
        for i in range(2, 13):
            for j in range(1, 29):
                self.rooms[i*100 + j] = Room(block_number, i*100 + j)

    def __str__(self):
        result = f"Block {self.block_number}:\n"
        for i in self.rooms.values():
            result += f"    {i}\n"
        return result

    def __eq__(self, other):
        return self.block_number == other.block_number

    def __hash__(self):
        return hash(self.block_number)
