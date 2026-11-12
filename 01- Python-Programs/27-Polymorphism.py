class Dog:
    def sound(self):
        print("Dog Barks")

class Cat:
    def sound(self):
        print("Cat meows")

def animal_sound(i):
    i.sound()

dog = Dog()
cat = Cat()

animal_sound(dog)
animal_sound(cat)