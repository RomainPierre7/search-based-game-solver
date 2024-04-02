import random

class Node:
    def __init__(self, number, score, game_bank, depth, player):
        self.number = number
        self.score = score
        self.game_bank = game_bank

        self.depth = depth
        self.player = player

        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def is_leaf(self):
        return self.number % 3 != 0 and self.number % 4 != 0 and self.number % 5 != 0

    def other_player(self):
        return "human" if self.player == "computer" else "computer"
    
    def divide_by_3(self):
        if self.number % 3 == 0:
            new_number = self.number // 3
            new_score = self.score + 1 if new_number % 2 == 0 else self.score - 1
            new_game_bank = self.game_bank + 1 if new_number % 5 == 0 else self.game_bank
            return Node(new_number, new_score, new_game_bank, self.depth + 1, self.other_player())
        return None

    def divide_by_4(self):
        if self.number % 4 == 0:
            new_number = self.number // 4
            new_score = self.score + 1 if new_number % 2 == 0 else self.score - 1
            new_game_bank = self.game_bank + 1 if new_number % 5 == 0 else self.game_bank
            return Node(new_number, new_score, new_game_bank, self.depth + 1, self.other_player())
        return None

    def divide_by_5(self):
        if self.number % 5 == 0:
            new_number = self.number // 5
            new_score = self.score + 1 if new_number % 2 == 0 else self.score - 1
            new_game_bank = self.game_bank + 1 if new_number % 5 == 0 else self.game_bank
            return Node(new_number, new_score, new_game_bank, self.depth + 1, self.other_player())
        return None


class Game:
    @staticmethod
    def generate_start_numbers():
        numbers = []
        for _ in range(5):
            number = random.randint(40000, 50000)
            while (number in numbers) or (number % 3 != 0) or (number % 4 != 0) or (number % 5 != 0):
                number = random.randint(40000, 50000)
            numbers.append(number)
        return numbers
    
    def __init__(self, first_player, algorithm, initial_selected_number):
        self.first_player = first_player
        other_player = "computer" if first_player == "human" else "human"
        self.algorithm = algorithm
        self.state = Node(initial_selected_number, 0, 0, 0, other_player)

    def create_tree(self):
        queue = [self.state]
        while queue:
            current_node = queue.pop(0)
            children = [current_node.divide_by_3(), current_node.divide_by_4(), current_node.divide_by_5()]
            for child in children:
                if child:
                    current_node.add_child(child)
                    queue.append(child)

    def print_tree(self):
        queue = [self.state]
        current_depth = 0
        print("Depth 0 (root):     ", end="")
        while queue:
            current_node = queue.pop(0)
            if current_node.depth > current_depth:
                current_depth = current_node.depth
                print(f"\nDepth {current_depth} ({current_node.player}): ", end="")
                if current_node.player == "human":
                    print("   ", end="")
            print(f"({current_node.number}|{current_node.score}|{current_node.game_bank}) ", end="")
            for child in current_node.children:
                queue.append(child)
        print()

    def play(self, number):
        new_state = None
        if number == 3:
            new_state = self.state.divide_by_3()
        elif number == 4:
            new_state = self.state.divide_by_4()
        elif number == 5:
            new_state = self.state.divide_by_5()
        new_state.depth = 0
        self.state = new_state
    
    def get_computer_play(self):
        if self.algorithm == "minimax":
            return self.minimax()
        elif self.algorithm == "alpha-beta":
            return self.alpha_beta()
        
    def minimax(self):
        pass # TO IMPLEMENT Zehra | Has to return the number to divide by

    def alpha_beta(self):
        pass # TO IMPLEMENT Phu | Has to return the number to divide by