class Map:
        def __init__(self):
                self.rooms = {
                        1: [2, 5, 8],
                        2: [1, 3, 10],
                        3: [2, 4, 12],
                        4: [3, 5, 11],
                        5: [1, 4, 6],
                        6: [5, 7, 12],
                        7: [6, 8, 11],
                        8: [1, 7, 9],
                        9: [8, 10, 12],
                        10: [2, 9, 11],
                        11: [4, 7, 10],
                        12: [3, 6, 9]
                        }
                self.occupied = []
                self.player_occupied = []
                self.unoccupied = []
                self.player_unoccupied = []

        def set_unoccupied(self):
                self.unoccupied = [x for x in range(1, 12) if not x in self.occupied]
        def set_player_unoccupied(self):
                self.player_unoccupied = [x for x in range(1, 12) if not x in self.occupied and self.player_occupied]
