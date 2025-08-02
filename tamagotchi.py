import tkinter as tk
from tkinter import messagebox
import threading
import time

class Tamagotchi:
    def __init__(self):
        self.name = "Tama"
        self.hunger = 50
        self.happiness = 50
        self.health = 50
        self.age = 0
        self.alive = True
        
    def feed(self):
        if self.alive:
            self.hunger = min(100, self.hunger + 20)
            self.health = min(100, self.health + 5)
    
    def play(self):
        if self.alive:
            self.happiness = min(100, self.happiness + 25)
            self.hunger = max(0, self.hunger - 10)
    
    def heal(self):
        if self.alive:
            self.health = min(100, self.health + 30)
            self.hunger = max(0, self.hunger - 5)
    
    def update_stats(self):
        if self.alive:
            self.hunger = max(0, self.hunger - 2)
            self.happiness = max(0, self.happiness - 1)
            self.health = max(0, self.health - 1)
            self.age += 1
            
            if self.hunger == 0 or self.happiness == 0 or self.health == 0:
                self.alive = False

class TamagotchiGUI:
    def __init__(self):
        self.pet = Tamagotchi()
        self.root = tk.Tk()
        self.root.title("Tamagotchi Game")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_ui()
        self.start_game_loop()
    
    def setup_ui(self):
        # Pet display
        self.pet_frame = tk.Frame(self.root, bg="#e6f3ff", relief="raised", bd=2)
        self.pet_frame.pack(pady=20, padx=20, fill="x")
        
        self.pet_label = tk.Label(self.pet_frame, text="🐾", font=("Arial", 60), bg="#e6f3ff")
        self.pet_label.pack(pady=20)
        
        self.name_label = tk.Label(self.pet_frame, text=f"Name: {self.pet.name}", 
                                  font=("Arial", 14), bg="#e6f3ff")
        self.name_label.pack()
        
        # Stats display
        self.stats_frame = tk.Frame(self.root, bg="#fff", relief="sunken", bd=2)
        self.stats_frame.pack(pady=10, padx=20, fill="x")
        
        self.hunger_label = tk.Label(self.stats_frame, text="", font=("Arial", 12), bg="#fff")
        self.hunger_label.pack(anchor="w", padx=10, pady=2)
        
        self.happiness_label = tk.Label(self.stats_frame, text="", font=("Arial", 12), bg="#fff")
        self.happiness_label.pack(anchor="w", padx=10, pady=2)
        
        self.health_label = tk.Label(self.stats_frame, text="", font=("Arial", 12), bg="#fff")
        self.health_label.pack(anchor="w", padx=10, pady=2)
        
        self.age_label = tk.Label(self.stats_frame, text="", font=("Arial", 12), bg="#fff")
        self.age_label.pack(anchor="w", padx=10, pady=2)
        
        # Action buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)
        
        tk.Button(self.button_frame, text="🍎 Feed", command=self.feed_pet, 
                 font=("Arial", 12), bg="#90EE90", width=10).pack(side="left", padx=5)
        
        tk.Button(self.button_frame, text="🎮 Play", command=self.play_with_pet, 
                 font=("Arial", 12), bg="#FFB6C1", width=10).pack(side="left", padx=5)
        
        tk.Button(self.button_frame, text="💊 Heal", command=self.heal_pet, 
                 font=("Arial", 12), bg="#87CEEB", width=10).pack(side="left", padx=5)
        
        # Status message
        self.status_label = tk.Label(self.root, text="Your pet is waiting for you!", 
                                   font=("Arial", 10), bg="#f0f0f0", fg="#666")
        self.status_label.pack(pady=10)
    
    def update_display(self):
        if self.pet.alive:
            # Update pet emoji based on stats
            if self.pet.happiness > 70:
                emoji = "😊"
            elif self.pet.health < 30:
                emoji = "🤒"
            elif self.pet.hunger < 30:
                emoji = "😋"
            else:
                emoji = "🐾"
            
            self.pet_label.config(text=emoji)
            
            # Update stats with color coding
            self.hunger_label.config(text=f"Hunger: {self.pet.hunger}%", 
                                   fg="red" if self.pet.hunger < 30 else "green")
            self.happiness_label.config(text=f"Happiness: {self.pet.happiness}%", 
                                      fg="red" if self.pet.happiness < 30 else "green")
            self.health_label.config(text=f"Health: {self.pet.health}%", 
                                   fg="red" if self.pet.health < 30 else "green")
            self.age_label.config(text=f"Age: {self.pet.age} hours")
        else:
            self.pet_label.config(text="💀")
            self.status_label.config(text="Your pet has died! Game Over.", fg="red")
            messagebox.showinfo("Game Over", "Your Tamagotchi has died!")
    
    def feed_pet(self):
        if self.pet.alive:
            self.pet.feed()
            self.status_label.config(text="Yummy! Your pet feels better!", fg="green")
            self.update_display()
    
    def play_with_pet(self):
        if self.pet.alive:
            self.pet.play()
            self.status_label.config(text="Fun time! Your pet is happier!", fg="blue")
            self.update_display()
    
    def heal_pet(self):
        if self.pet.alive:
            self.pet.heal()
            self.status_label.config(text="Medicine taken! Health improved!", fg="purple")
            self.update_display()
    
    def start_game_loop(self):
        def game_loop():
            while True:
                time.sleep(5)  # Update every 5 seconds
                if self.pet.alive:
                    self.pet.update_stats()
                    self.root.after(0, self.update_display)
                else:
                    break
        
        thread = threading.Thread(target=game_loop, daemon=True)
        thread.start()
    
    def run(self):
        self.update_display()
        self.root.mainloop()

if __name__ == "__main__":
    game = TamagotchiGUI()
    game.run()