import tkinter as tk
import random

class HangmanGame:
    def __init__(self, master):
        self.bg = 'light blue'
        self.word_font = ("Helvetica", 30)
        self.game_over_font = ("Helvetica", 18)
        self.button_bg = "#4a7a8c"
        self.button_fg = "white"
        self.button_font = ("Helvetica", 12, "bold")
        self.master = master
        self.master.title("Hangman Game")
        self.master.geometry("900x750")
        self.master.configure(bg=self.bg)
        self.word_list = ["PYTHON", "JAVASCRIPT", "KOTLIN", "JAVA", "RUBY", "SWIFT"]
        self.secret_word = self.choose_secret_word()
        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = 7
        self.initialize_gui()

    def choose_secret_word(self):
        return random.choice(self.word_list)
    
    def initialize_gui(self):
        self.hangman_canvas = tk.Canvas(self.master, width=300, height=300, bg="white")
        self.hangman_canvas.pack(pady=20)
        self.draw_rig()
        self.word_display = tk.Label(self.master, text="_ " * len(self.secret_word), font=self.word_font, bg=self.bg)
        self.word_display.pack(pady=(40, 20))
        self.buttons_frame = tk.Frame(self.master, bg=self.bg)
        self.buttons_frame.pack(pady=20)
        self.setup_alphabet_buttons()
        self.reset_button = tk.Button(self.master, text="Reset Game", command=self.reset_game, width=20, height=2, bg=self.button_bg, fg=self.button_fg, font=self.button_font)
        self.reset_button.pack(pady=(10, 0))

    def update_hangman_canvas(self):
        self.hangman_canvas.delete("all")  # Clear the canvas before redrawing
        self.draw_rig()
        stages = [self.draw_head, self.draw_body, self.draw_left_arm, self.draw_right_arm, self.draw_left_leg, self.draw_right_leg, self.draw_face]
        for i in range(len(self.incorrect_guesses)):
            if i < len(stages):
                stages[i]()

    def draw_rig(self):
        self.hangman_canvas.create_line(155, 25, 155, 50, fill="black")
        self.hangman_canvas.create_line(155, 25, 100, 25, fill="black")
        self.hangman_canvas.create_line(100, 25, 100, 250, fill="black")
        self.hangman_canvas.create_rectangle(50, 250, 250, 225, fill="black")

    def draw_head(self):
        self.hangman_canvas.create_oval(125, 50, 185, 110, outline="black")

    def draw_body(self):
        self.hangman_canvas.create_line(155, 110, 155, 170, fill="black")

    def draw_left_arm(self):
        self.hangman_canvas.create_line(155, 130, 125, 150, fill="black")

    def draw_right_arm(self):
        self.hangman_canvas.create_line(155, 130, 185, 150, fill="black")

    def draw_left_leg(self):
        self.hangman_canvas.create_line(155, 170, 125, 200, fill="black")

    def draw_right_leg(self):
        self.hangman_canvas.create_line(155, 170, 185, 200, fill="black")

    def draw_face(self):
        self.hangman_canvas.create_line(140, 70, 150, 80, fill="black") # Left eye
        self.hangman_canvas.create_line(160, 70, 170, 80, fill="black") # Right eye
        # Draw a sad mouth
        self.hangman_canvas.create_arc(140, 85, 170, 105, start=0, extent=180, fill="black")
    
    def setup_alphabet_buttons(self):        
        upper_row = "QWERTYUIOP"
        middle_row = "ASDFGHJKL"
        lower_row = "ZXCVBNM"
        
        upper_frame = tk.Frame(self.buttons_frame, bg=self.bg)
        upper_frame.pack()
        middle_frame = tk.Frame(self.buttons_frame, bg=self.bg)
        middle_frame.pack()
        lower_frame = tk.Frame(self.buttons_frame, bg=self.bg)
        lower_frame.pack()

        for letter in upper_row:
            button = tk.Button(upper_frame, text=letter, command=lambda l=letter: self.guess_letter(l), width=4, height=2, bg=self.button_bg, fg=self.button_fg, font=self.button_font)
            button.pack(side="left", padx=2, pady=2)

        for letter in middle_row:
            button = tk.Button(middle_frame, text=letter, command=lambda l=letter: self.guess_letter(l), width=4, height=2, bg=self.button_bg, fg=self.button_fg, font=self.button_font)
            button.pack(side="left", padx=2, pady=2)

        for letter in lower_row:
            button = tk.Button(lower_frame, text=letter, command=lambda l=letter: self.guess_letter(l), width=4, height=2, bg=self.button_bg, fg=self.button_fg, font=self.button_font)
            button.pack(side="left", padx=2, pady=2)

    def guess_letter(self, letter):
        if letter in self.secret_word and letter not in self.correct_guesses:
            self.correct_guesses.add(letter)
        elif letter not in self.incorrect_guesses:
            self.incorrect_guesses.add(letter)
            self.attempts_left -= 1
            self.update_hangman_canvas()
 
        self.update_word_display()
        self.check_game_over()

    def update_word_display(self):
        displayed_word = " ".join([letter if letter in self.correct_guesses else "_" for letter in self.secret_word])
        self.word_display.config(text=displayed_word)

    def check_game_over(self):
        if set(self.secret_word).issubset(self.correct_guesses):
            self.display_game_over_message("Congratulations, you've won!")
        elif self.attempts_left == 0:
            self.display_game_over_message(f"Game over! The word was: {self.secret_word}")
    
    def display_game_over_message(self, message):
        # Hide the reset button
        self.reset_button.pack_forget()
        
        # Hide the alphabet buttons by hiding the entire buttons_frame
        self.buttons_frame.pack_forget()
        
        # Display the game over message in the now-empty area
        self.game_over_label = tk.Label(self.master, text=message, font=self.game_over_font, fg="red", bg=self.bg)
        self.game_over_label.pack(pady=(10, 20))
        
        # Display the Restart button
        self.restart_button = tk.Button(self.master, text="Restart Game", command=self.reset_game, width=20, height=2, bg=self.button_bg, fg=self.button_fg, font=self.button_font)
        self.restart_button.pack(pady=(10, 20))

    def reset_game(self):
        # Re-show the reset button
        self.reset_button.pack(pady=(10, 0))
        
        # Reset game state and GUI elements
        self.secret_word = self.choose_secret_word()
        self.correct_guesses = set()
        self.incorrect_guesses = set()
        self.attempts_left = 7
        self.hangman_canvas.delete("all")
        self.draw_rig()
        self.update_word_display()
        for frame in self.buttons_frame.winfo_children():
            for button in frame.winfo_children():
                button.configure(state=tk.NORMAL)
        
        # Hide the game over label and the Restart button when the game is reset
        if hasattr(self, 'game_over_label') and self.game_over_label.winfo_exists():
            self.game_over_label.pack_forget()
        if hasattr(self, 'restart_button') and self.restart_button.winfo_exists():
            self.restart_button.pack_forget()

        # Ensure the alphabet buttons frame and other interactive elements are visible again
        self.buttons_frame.pack()

def main():
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()