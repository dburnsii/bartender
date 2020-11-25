# OpenDrinks

OpenDrinks is a repository for fancy (or not so fancy) cocktail recipe, formatted for computers to use. These recipes contain metadata that is less valuable to a human, but can be useful for a machine attempting to pour a beverage. For instance: pouring Cranberry Juice is easy, but pouring Cola is made more complicated due to carbonation. Here we make note of that so our robots know how to handle it.

## Getting Started
To add a recipe to the repo, run the `drink_maker.py` utility, and it'll walk you through the process. Currently, for any ingredient that shouldn't be put through a pump (lemon wedges, salt, bitters, thick syrups), be sure to use either `dash` or `count` as the measure, since the robots may try to pour anything labeled `mL`.
## Formatting

### Images
 - Must be 200x200 px and in `.jpg` format
 - Must be named the same name as an existing drink (i.e. `rum_and_coke.jpg` for `Rum and Coke`)
 - Must be licensed under the `Creative Commons` License. https://search.creativecommons.org/ is a great resource for finding images, and credits must be added to the `images/credits.txt` file.

### JSON
The `drink_maker.py` utility should handle all formatting, but as a reference, the format of all JSON files is as described below:
#### Ingredients
Ingredients are individual components of a drink, such as Rum or Limes
```
  {
    name: Name of the ingredient
      (type: string, required: true),
    measure: One of ["mL", "dash", "count"],
      used to determine how to measure this ingredient
      (type: string, required: true),
    carbonated: Whether or not this ingredient is even slightly carbonated
      (type: boolean, required: true)
  }
```

#### Drinks
Drinks are recipes for cocktails that incorporate multiple ingredients. The ingredients must be present for the drink to be valid, and the `drink_maker.py` utility will establish a new ingredient for you if one does not exist. Unless a drink has a hard requirement for a type of ingredient (i.e. Jager for a Jagerbomb), err on the side of being as agnostic as possible (`Vodka` vs `Smirinoff`).
```
  {
    name: Name of the drink
      (type: string, required: true),
    ingredients: List of ingredients, quantities, and whether each is required
      (type: array(object), required: true):
      [
        {
          ingredient: Name of the ingredient
            (type: string, required: true),
          quantity: Measure of how much of this ingredient we need
            (type: float, required: true),
          required: Whether or not this drink can be made without this ingredient
            (type: boolean, required: false, default: true)
        }
      ],
    alias: List of alternative names a drink could be called (i.e. `Adios` vs `AMF`).
      Used for searching for the drink.  
      (type: array(string), required: false, default: []),
    image: String to locate the image associated with this drink.
      (type: string, required: true)
  }
```
