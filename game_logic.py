import random

class Node:
    def __init__(self, number, score, game_bank, depth, player, divided_by=None):
        # Parameters
        self.number = number
        self.score = score
        self.game_bank = game_bank

        # Useful for printing and the program
        self.depth = depth 
        self.player = player
        self.divided_by = divided_by

        # Useful for alpha_beta
        self.intermediate_heuristic = None
        self.heuristic = None

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
            return Node(new_number, new_score, new_game_bank, self.depth + 1, self.other_player(), 3)
        return None

    def divide_by_4(self):
        if self.number % 4 == 0:
            new_number = self.number // 4
            new_score = self.score + 1 if new_number % 2 == 0 else self.score - 1
            new_game_bank = self.game_bank + 1 if new_number % 5 == 0 else self.game_bank
            return Node(new_number, new_score, new_game_bank, self.depth + 1, self.other_player(), 4)
        return None

    def divide_by_5(self):
        if self.number % 5 == 0:
            new_number = self.number // 5
            new_score = self.score + 1 if new_number % 2 == 0 else self.score - 1
            new_game_bank = self.game_bank + 1 if new_number % 5 == 0 else self.game_bank
            return Node(new_number, new_score, new_game_bank, self.depth + 1, self.other_player(), 5)
        return None
    
    def leaf_heuristic_eval(self, player, first_player, type):
        result = self.score
        if self.score % 2 == 0:
            result -= self.game_bank
        else:
            result += self.game_bank
        if result % 2 == 0: # winner is the first player
            if first_player == player:
                if type == 'max':
                    return 1
                else:
                    return -1
            else:
                if type == 'max':
                    return -1
                else:
                    return 1
        else: # winner is the second player
            if first_player == player:
                if type == 'max':
                    return -1
                else:
                    return 1
            else:
                if type == 'max':
                    return 1
                else:
                    return -1
                      
    def minimax(self, player, first_player, type):
        if self.is_leaf():
            return self.leaf_heuristic_eval(player, first_player, type)
        
        other_player = "computer" if player == "human" else "human"
        
        if type == 'max':
            max_eval = float('-inf')
            best_child = None
            for child in self.children:
                eval = child.minimax(other_player, first_player, 'min')
                if eval > max_eval:
                    max_eval = eval
                    best_child = child
            return best_child.divided_by
        
        else:
            min_eval = float('inf')
            best_child = None
            for child in self.children:
                eval = child.minimax(other_player, first_player, 'max')
                if eval < min_eval:
                    min_eval = eval
                    best_child = child
            return best_child.divided_by
            
    def alpha_beta(self, ancestor_intermediate_value, player, first_player, type):
        if self.is_leaf():
            self.heuristic = self.leaf_heuristic_eval(player, first_player, type)
            return self.heuristic
        
        #Check if we can give an intermediate heuristic
        no_heuristic_child = False
        heuristic_child = False
        heuristics = []
        for child in self.children:
            if child.heuristic != None:
                heuristic_child = True
                heuristics.append(child.heuristic)
            else:
                no_heuristic_child = True
        if no_heuristic_child and heuristic_child:
            #Give an intermediate heuristic
            if type == 'max':
                self.intermediate_heuristic = max(heuristics)
            else:
                self.intermediate_heuristic = min(heuristics)

        # Check if we can cut off
        if type == 'max':
            if self.intermediate_heuristic != None and ancestor_intermediate_value != None:
                if self.intermediate_heuristic >= ancestor_intermediate_value:
                    self.heuristic = self.intermediate_heuristic
                    return self.heuristic
        else:
            if self.intermediate_heuristic != None and ancestor_intermediate_value != None:
                if self.intermediate_heuristic <= ancestor_intermediate_value:
                    self.heuristic = self.intermediate_heuristic
                    return self.heuristic

        other_player = "computer" if player == "human" else "human"

        if type == 'max':
            max_eval = float('-inf')
            best_child = None
            for child in self.children:
                eval = child.alpha_beta(self.intermediate_heuristic, other_player, first_player, 'min')
                if eval > max_eval:
                    max_eval = eval
                    best_child = child
            self.heuristic = max_eval
            return best_child.divided_by
        
        else:
            min_eval = float('inf')
            best_child = None
            for child in self.children:
                eval = child.alpha_beta(self.intermediate_heuristic, other_player, first_player, 'max')
                if eval < min_eval:
                    min_eval = eval
                    best_child = child
            self.heuristic = min_eval
            return best_child.divided_by


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
            print(f"({current_node.number}|{current_node.score}|{current_node.game_bank})", end="")
            if current_depth > 0:
                print(f"[{current_node.divided_by}] ", end="")
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
            return self.state.minimax(player='computer', first_player=self.first_player, type='max')
        elif self.algorithm == "alpha-beta":
            return self.state.alpha_beta(ancestor_intermediate_value=None, player='computer', first_player=self.first_player, type='max')
