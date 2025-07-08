# Example courtesey of Claude.

from abc import ABC, abstractmethod

# Base layer ABC
class Flyable(ABC):
    @abstractmethod
    def fly(self):
        pass
    
    @abstractmethod
    def land(self):
        pass

# Another base layer ABC  
class Speakable(ABC):
    @abstractmethod
    def speak(self):
        pass
    
    @abstractmethod
    def be_quiet(self):
        pass

# Multi-layered ABC that requires BOTH previous ABCs
class MagicalCreature(Flyable, Speakable, ABC):
    @abstractmethod
    def cast_spell(self):
        pass
    
    @abstractmethod
    def get_mana(self):
        pass
    
    # You can also add concrete methods that use the abstract ones
    def introduce_self(self):
        self.speak()
        print("I am a magical creature!")
        self.fly()

# Even more layers! An ABC that requires the multi-layered ABC
class DragonLike(MagicalCreature, ABC):
    @abstractmethod
    def breathe_fire(self):
        pass
    
    @abstractmethod
    def hoard_treasure(self):
        pass

# This won't work - missing implementations
# class BrokenDragon(DragonLike):
#     def fly(self):
#         return "Soaring!"

# This works - implements ALL required methods from the entire hierarchy
class FriendlyDragon(DragonLike):
    def fly(self):
        return "Soaring through clouds!"
    
    def land(self):
        return "Landing gracefully"
    
    def speak(self):
        print("Hello there, tiny human!")
    
    def be_quiet(self):
        print("*whispers*")
    
    def cast_spell(self):
        return "✨ Magic sparkles ✨"
    
    def get_mana(self):
        return 100
    
    def breathe_fire(self):
        return "🔥 WHOOSH! 🔥"
    
    def hoard_treasure(self):
        return "Adding gold to my pile!"

# Let's test it
if __name__ == "__main__":
    dragon = FriendlyDragon()
    
    print(f"Flying: {dragon.fly()}")
    dragon.speak()
    print(f"Spell: {dragon.cast_spell()}")
    print(f"Fire: {dragon.breathe_fire()}")
    print(f"Mana: {dragon.get_mana()}")
    
    # The inherited method works too
    dragon.introduce_self()
    
    # Check the MRO (Method Resolution Order)
    print(f"\nMRO: {[cls.__name__ for cls in FriendlyDragon.__mro__]}")
    
    # Verify it's an instance of all the ABCs
    print(f"Is Flyable: {isinstance(dragon, Flyable)}")
    print(f"Is Speakable: {isinstance(dragon, Speakable)}")
    print(f"Is MagicalCreature: {isinstance(dragon, MagicalCreature)}")
    print(f"Is DragonLike: {isinstance(dragon, DragonLike)}")