clear()
plant(Entities.Grass)
plant_type, (x, y) = get_companion()
print(plant_type, (x, y))

move(East)

plant(Entities.Tree)
plant_type, (x, y) = get_companion()
print(plant_type, (x, y))

move(East)

plant(Entities.Carrot)
plant_type, (x, y) = get_companion()
print(plant_type, (x, y))

move(East)

plant(Entities.Pumpkin)
plant_type, (x, y) = get_companion()
print(plant_type, (x, y))

move(East)

plant(Entities.Sunflower)
plant_type, (x, y) = get_companion()
print(plant_type, (x, y))

print("Cost of Sunflower: ", get_cost(Entities.Sunflower))
