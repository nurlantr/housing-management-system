from block import Block
class Dormitory:

    def __init__(self):
        self.blocks = {}
        self.num_blocks = 2
        for i in range(1, self.num_blocks + 1):
            self.blocks[i] = Block(f"D{i}")

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

