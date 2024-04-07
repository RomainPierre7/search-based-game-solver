import game_logic

import tkinter as tk
import time

def create_gui():
    global root
    root = tk.Tk()
    root.title("Divide by 3, 4, 5 Game")
    root.geometry("700x700")
    root.resizable(False, False)
    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    position_right = int(root.winfo_screenwidth()/2 - window_width/2 - 700/2)
    position_down = int(root.winfo_screenheight()/2 - window_height/2 - 700/2)
    root.geometry("+{}+{}".format(position_right, position_down))
    return root

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def show_config(numbers):
    first_player = "human"
    algorithm = "minimax"
    initial_selected_number = numbers[0]

    def select_first_player(player):
        nonlocal first_player
        first_player = player
        if player == "human":
            button_config_human.config(highlightbackground="blue", highlightthickness=5)
            button_config_computer.config(highlightbackground="#d9d9d9", highlightthickness=5)
        else:
            button_config_human.config(highlightbackground="#d9d9d9", highlightthickness=5)
            button_config_computer.config(highlightbackground="blue", highlightthickness=5)

    def select_algorithm(algo):
        nonlocal algorithm
        algorithm = algo
        if algo == "minimax":
            button_config_minimax.config(highlightbackground="blue", highlightthickness=5)
            button_config_alpha.config(highlightbackground="#d9d9d9", highlightthickness=5)
        else:
            button_config_minimax.config(highlightbackground="#d9d9d9", highlightthickness=5)
            button_config_alpha.config(highlightbackground="blue", highlightthickness=5)

    def select_number(number):
        nonlocal initial_selected_number
        initial_selected_number = number
        for btn in buttons_config_number:
            if btn["text"] == str(number):
                btn.config(highlightbackground="blue", highlightthickness=5)
            else:
                btn.config(highlightbackground="#d9d9d9", highlightthickness=5)

    top_space = tk.Frame(root, height=75)
    top_space.pack()
    tk.Label(root, text="Select the first player:").pack()
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    button_config_human = tk.Button(button_frame, text="Human", highlightbackground="blue", highlightthickness=5, command=lambda: select_first_player("human"))
    button_config_human.pack(side=tk.LEFT, padx=5, pady=5)
    button_config_computer = tk.Button(button_frame, text="Computer", command=lambda: select_first_player("computer"))
    button_config_computer.pack(side=tk.LEFT, padx=5, pady=5)

    tk.Label(root, text="Select the algorithm:").pack()
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    button_config_minimax = tk.Button(button_frame, text="Minimax", highlightbackground="blue", highlightthickness=5, command=lambda: select_algorithm("minimax"))
    button_config_minimax.pack(side=tk.LEFT, padx=5, pady=5)
    button_config_alpha = tk.Button(button_frame, text="Alpha-beta", command=lambda: select_algorithm("alpha-beta"))
    button_config_alpha.pack(side=tk.LEFT, padx=5, pady=5)

    tk.Label(root, text="Select a number:").pack()
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    buttons_config_number = [tk.Button(button_frame, text=str(number), command=lambda num=number: select_number(num)) for number in numbers]
    for btn in buttons_config_number:
        btn.pack(side=tk.LEFT, padx=5, pady=5)
        if btn["text"] == str(initial_selected_number):
            btn.config(highlightbackground="blue", highlightthickness=5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    button_config_start = tk.Button(button_frame, text="Start", highlightbackground="green", highlightthickness=5, command=lambda: start_game(first_player, algorithm, initial_selected_number))
    button_config_start.pack(side=tk.LEFT, padx=5, pady=5)

def start_game(first_player, algorithm, initial_selected_number):
    global game
    game = game_logic.Game(first_player, algorithm, initial_selected_number)
    print("First player:", first_player)
    print("Algorithm:", algorithm)
    print("Initial selected number:", initial_selected_number)
    print("========== Initial game tree (number|score|game_bank)[divided_by] ==========")
    game.create_tree()
    game.print_tree()

    clear_frame()
    top_space = tk.Frame(root, height=50)
    top_space.pack()
    number_label = tk.Label(root, text=f"Number: {game.state.number}", font=("Arial", 20))
    number_label.pack()
    score_label = tk.Label(root, text=f"Score: {game.state.score}")
    score_label.pack()
    bank_label = tk.Label(root, text=f"Game bank: {game.state.game_bank}")
    bank_label.pack()
    top_space = tk.Frame(root, height=50)
    top_space.pack()
    button_divide_by_3 = tk.Button(root, text="Divide by 3", command=lambda: human_play(3, number_label, score_label, bank_label, button_divide_by_3, button_divide_by_4, button_divide_by_5, info_label))
    button_divide_by_3.pack(pady=20)
    if game.state.number % 3 != 0:
        button_divide_by_3.config(state=tk.DISABLED)
    button_divide_by_4 = tk.Button(root, text="Divide by 4", command=lambda: human_play(4, number_label, score_label, bank_label, button_divide_by_3, button_divide_by_4, button_divide_by_5, info_label))
    button_divide_by_4.pack(pady=20)
    if game.state.number % 4 != 0:
        button_divide_by_4.config(state=tk.DISABLED)
    button_divide_by_5 = tk.Button(root, text="Divide by 5", command=lambda: human_play(5, number_label, score_label, bank_label, button_divide_by_3, button_divide_by_4, button_divide_by_5, info_label))
    button_divide_by_5.pack(pady=20)
    if game.state.number % 5 != 0:
        button_divide_by_5.config(state=tk.DISABLED)
    top_space = tk.Frame(root, height=50)
    top_space.pack()
    info_label = tk.Label(root, text="")
    info_label.pack()
    if first_player == "computer":
        button_divide_by_3.config(state=tk.DISABLED)
        button_divide_by_4.config(state=tk.DISABLED)
        button_divide_by_5.config(state=tk.DISABLED)
        computer_play(number_label, score_label, bank_label, button_divide_by_3, button_divide_by_4, button_divide_by_5, info_label)

def human_play(divisor, number_label, score_label, bank_label, button_divide_by_3, button_divide_by_4, button_divide_by_5, info_label):
    global game
    game.play(divisor)
    number_label.config(text=f"Number: {game.state.number}")
    score_label.config(text=f"Score: {game.state.score}")
    bank_label.config(text=f"Game bank: {game.state.game_bank}")
    button_divide_by_3.config(state=tk.DISABLED)
    button_divide_by_4.config(state=tk.DISABLED)
    button_divide_by_5.config(state=tk.DISABLED)

    print(f"========== Game tree after human's move (divide by {divisor})==========")
    game.create_tree()
    game.print_tree()
    if game.state.is_leaf():
        game_over(game.state.score, game.state.game_bank)
        return
    computer_play(number_label, score_label, bank_label, button_divide_by_3, button_divide_by_4, button_divide_by_5, info_label)
    
def computer_play(number_label, score_label, bank_label, button_divide_by_3, button_divide_by_4, button_divide_by_5, info_label):
    global game
    info_label.config(text="Computer is thinking...")
    root.update()
    time.sleep(2)
    start = time.time()
    visited_nodes, divisor = game.get_computer_play()
    end = time.time()
    game.play(divisor)
    print(f"========== Game tree after computer's move (divide by {divisor})==========")
    number_label.config(text=f"Number: {game.state.number}")
    score_label.config(text=f"Score: {game.state.score}")
    bank_label.config(text=f"Game bank: {game.state.game_bank}")
    game.create_tree()
    game.print_tree()
    if game.state.is_leaf():
        game_over(game.state.score, game.state.game_bank, divisor, end - start, visited_nodes)
        return
    button_divide_by_3.config(state=tk.NORMAL if game.state.number % 3 == 0 else tk.DISABLED)
    button_divide_by_4.config(state=tk.NORMAL if game.state.number % 4 == 0 else tk.DISABLED)
    button_divide_by_5.config(state=tk.NORMAL if game.state.number % 5 == 0 else tk.DISABLED)
    info_label.config(text=f"Computer played {divisor} !\n* Real execution time: {end - start:.5f} seconds \n * Visited nodes: {visited_nodes} \n Your turn !")

def game_over(score, game_bank, divisor=None, execution_time=None, visited_nodes=None):
    global game
    winner = ''
    result = score
    if score % 2 == 0:
        result -= game_bank
    else:
        result += game_bank
    if result % 2 == 0:
        winner = game.first_player
    else:
        winner = "computer" if game.first_player == "human" else "human"
    print("========== Game over ! ==========")
    print(f"Score: {score}")
    print(f"Game bank: {game_bank}")
    print(f"Result: {result}")
    print(f"Winner: {winner}")
    print("=================================")
    clear_frame()
    top_space = tk.Frame(root, height=50)
    top_space.pack()
    tk.Label(root, text="Game Over !", font=("Arial", 20)).pack()
    tk.Label(root, text=f"Score: {score}").pack()
    tk.Label(root, text=f"Game bank: {game_bank}").pack()
    tk.Label(root, text=f"Result: {result}").pack()
    tk.Label(root, text=f"Winner: {winner}").pack()
    top_space = tk.Frame(root, height=50)
    top_space.pack()
    if divisor is not None and execution_time is not None and visited_nodes is not None:
        tk.Label(root, text=f"Computer played {divisor} !\n* Real execution time: {execution_time:.5f} seconds \n * Visited nodes: {visited_nodes}").pack()
    top_space = tk.Frame(root, height=50)
    top_space.pack()
    button_restart = tk.Button(root, text="Restart", command=restart_game)
    button_restart.pack()

def restart_game():
    clear_frame()
    start_numbers = game_logic.Game.generate_start_numbers()
    show_config(start_numbers)

def main():
    root = create_gui()
    start_numbers = game_logic.Game.generate_start_numbers()
    show_config(start_numbers)
    root.mainloop()

if __name__ == "__main__":
    main()