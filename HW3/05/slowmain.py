from sys import stdin, stdout

def slowmain(filein = stdin, fileout = stdout):
    class Knight:
        def __init__(self, health, ATK, position):
            self.__health = health
            self.__ATK = ATK
            self.__position = position
            self.__attack_times = 0

        def attack(self, positions, target):
            atk_pos, target_pos = self.__position, target.__position
            if self.__health == 0 or target.__health == 0 or atk_pos == target_pos:
                return
            dead_list = []
            total_ATK = positions[atk_pos][1]
            ATK_decrease = 0
            for ATKed_knight in positions[target_pos][0]:
                if ATKed_knight.__health <= total_ATK:
                    ATK_decrease += ATKed_knight.__ATK
                    ATKed_knight.__health = 0
                    dead_list.append(ATKed_knight)
                else:
                    ATKed_knight.__health -= total_ATK
            positions[target_pos][0].difference_update(dead_list)
            positions[target_pos][0].update(positions[atk_pos][0])
            positions[target_pos][1] += positions[atk_pos][1] - ATK_decrease
            for ATKing_knight in positions[atk_pos][0]:
                ATKing_knight.__position = target_pos
                ATKing_knight.__attack_times += 1
            positions[atk_pos][0].clear()
            positions[atk_pos][1] = 0

        @property
        def attack_times(self):
            return self.__attack_times

        @property
        def position(self):
            return self.__position
    
    if filein == stdin:
        n, m = map(int, input().strip().split())
        h = list(map(int, input().strip().split()))
        a = list(map(int, input().strip().split()))
    else:
        n, m = map(int, filein.readline().strip().split())
        h = list(map(int, filein.readline().strip().split()))
        a = list(map(int, filein.readline().strip().split()))
    knights = []
    positions = []
    for i, (health, ATK) in enumerate(zip(h, a)):
        knight = Knight(health, ATK, i)
        knights.append(knight)
        positions.append([{knight,}, ATK])
    for q in range(m):
        if filein == stdin:
            Ka, Ks = map(int, input().strip().split())
        else:
            Ka, Ks = map(int, filein.readline().strip().split())
        knights[Ka - 1].attack(positions, knights[Ks - 1])
    for knight in knights:
        print(knight.attack_times, end=" ", file=fileout)

if __name__ == "__main__":
    slowmain()