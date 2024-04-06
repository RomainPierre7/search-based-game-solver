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
    
    def alpha_beta(self, alpha, beta, maximizing_player):
        if self.is_leaf():
            return self.score

        if maximizing_player:
            max_eval = float('-inf')
            for child in self.children:
                eval = child.alpha_beta(alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for child in self.children:
                eval = child.alpha_beta(alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval


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
        if new_state is not None:
           new_state.depth = 0
           self.state = new_state
        else:
           print("Invalid move! Please choose a valid divisor.")
    
    def get_computer_play(self):
        if self.algorithm == "minimax":
            return self.minimax()
        elif self.algorithm == "alpha-beta":
            return self.state.alpha_beta(float('-inf'), float('inf'), True)
        
    @staticmethod
    def heuristic_measure(leaf_node, first_player):
        check_if_first_player_won = (leaf_node.score + leaf_node.game_bank)%2 == 0
        if first_player == "computer":
            if check_if_first_player_won:
                m = 1
            else:
                m = -1
        else:
            if check_if_first_player_won:
                m = -1
            else:
                m = 1
        return m



    def minimax(self):
        def max_value(node):
            if node.is_leaf():
                return Game.heuristic_measure(node, self.first_player)
            v = float('-inf')
            for child in node.children:
                v = max(v, min_value(child))
            return v

        def min_value(node):
            if node.is_leaf():
                return Game.heuristic_measure(node, self.first_player)
            v = float('inf')
            for child in node.children:
                v = min(v, max_value(child))
            return v

        best_score = float('-inf')
        best_move = None
        for child in self.state.children:
            score = min_value(child)
            if score > best_score:
                best_score = score
                best_move = self.state.number / child.number
        return best_move