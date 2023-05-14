from models_refactored import *

def build_dorm(excluded_rooms_file: str | None = None) -> Dormitory:
    blocks = {
            22: Dormitory.Block(22, [2, 12], [1, 28], 3),
            23: Dormitory.Block(23, [2, 12], [1, 28], 2),
            24: Dormitory.Block(24, [2, 12], [1, 28], 2),
            25: Dormitory.Block(25, [2, 12], [1, 28], 2),
            26: Dormitory.Block(26, [2, 12], [1, 28], 2),
            27: Dormitory.Block(27, [2, 12], [1, 28], 2),
    }

    nu = Dormitory(blocks, excluded_rooms_file)
    return nu