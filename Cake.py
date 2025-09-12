class Cake:
    recipe_type = "Basic Cake"
    baking_temperature = 180
    baking_time = 30

    def __init__(self, flour, sugar, milk, eggs):
        self.cake_flour = flour
        self.cake_sugar = sugar
        self.cake_milk = milk
        self.cake_eggs = eggs

    def mix_ingredients(self):
        print(
            f"Mixing {self.cake_flour} grams of flour, {self.cake_sugar} grams of sugar, {self.cake_milk} ml of milk, and {self.cake_eggs} eggs."
        )

    def bake(self):
        print(f"Baking the cake at {self.__class__.baking_temperature}°C for {self.__class__.baking_time} minutes.")

    def serve(self):
        print("Serving the cake with decoration.")


# flour, sugar, milk, eggs in order
cake_1 = Cake(flour=200, sugar=200, milk=240, eggs=2)
cake_2 = Cake(flour=200, sugar=150, milk=220, eggs=2)
cake_3 = Cake(flour=170, sugar=170, milk=200, eggs=2)

print(cake_1.cake_flour)
print(cake_2.baking_time)
