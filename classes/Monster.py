class Monster:
    def __init__(self, name, type_, level=1, max_health=100, attack=10, defense=10, speed=10, special_attack=10, special_defense=10):
        self.name = name
        self.type = type_
        self.level = level
        self.max_health = max_health
        self.current_health = max_health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.special_attack = special_attack
        self.special_defense = special_defense
        

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.attack += 2
        self.defense += 2
        self.current_health = self.max_health

    def take_damage(self, damage):
        reduced_damage = max(damage - self.defense, 0)
        self.current_health -= reduced_damage
        if self.current_health < 0:
            self.current_health = 0

    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health

    def is_fainted(self):
        return self.current_health <= 0

    def __str__(self):
        return (f"{self.name} (Type: {self.type}, Level: {self.level})\n"
                f"HP: {self.current_health}/{self.max_health}\n"
                f"Attack: {self.attack}, Defense: {self.defense}"
                f"Speed: {self.speed}, Special Attack: {self.special_attack}, Special Defense: {self.special_defense}")