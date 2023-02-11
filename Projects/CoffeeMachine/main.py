
"""Coffee Machine program

    Emulates a coffee machine.

    ```json
    {
        "espresso": {
            "ingredients": {
                "water": 50,
                "milk": 0,
                "coffee": 18,
            },
            "cost": 1.5,
        },
        "latte": {
            "ingredients": {
                "water": 200,
                "milk": 150,
                "coffee": 24,
            },
            "cost": 2.5,
        },
        "cappuccino": {
            "ingredients": {
                "water": 250,
                "milk": 100,
                "coffee": 24,
            },
            "cost": 3.0,
        }
    }
    ```
    Available choices:
        - espresso: serves a espresso
        - latte: serves a latte
        - cappuccino: serves a cappuccino
        - report: give a detailed report on resources available inside the machine
        - off: turns off the machine
        - refill: refills resources inside the machine
"""
import coffee_machine
import coin

MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "milk": 0,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

q = coin.Coin(0.25) # Quarter
d = coin.Coin(0.10) # Dime
n = coin.Coin(0.05) # Nickel
p = coin.Coin(0.01) # Penny

cm = coffee_machine.CoffeeMachine(
    resources["water"], resources["milk"], resources["coffee"], money=0)


def check_resources(drink: str) -> tuple:
    """Check if there are enough resources on the machine for selected drink.

    Returns True if there are enough resources, False if not.

    Args:
        drink (string): selected drink
    """
    water: bool = cm.water() >= MENU[drink]["ingredients"]["water"]
    milk: bool = cm.milk() >= MENU[drink]["ingredients"]["milk"]
    coffee: bool = cm.coffee() >= MENU[drink]["ingredients"]["coffee"]
    missing_resources: str = ("water," if not water else "") +\
        ("milk," if not milk else "") +\
        ("coffee," if not coffee else "")
    return water and milk and coffee, missing_resources


def get_coins() -> float:
    """Get coins from user input

    Returns:
        float: total value inserted
    """
    print("Please insert coins.")
    q.setCount(int(input("How many quarters?: ")))
    d.setCount(int(input("How many dimes?: ")))
    n.setCount(int(input("How many nickles?: ")))
    p.setCount(int(input("How many pennies?: ")))

    return q.total_value() + d.total_value() + n.total_value() + p.total_value()


def serve_coffee(drink: str):
    """Serve selected drink

    Args:
        drink (string): selected drink
    """
    # Check resources sufficient to make drink order.
    check, missing_resources = check_resources(drink)
    if check:
        # Get coins
        total = get_coins()
        drink_cost = MENU[drink]["cost"]
        if total >= drink_cost:
            # Give change, add profit
            change = total - drink_cost
            cm.add_money(drink_cost)
            if change > 0:
                print(f"Here is ${change:.2f} in change.")
            # Deduct resources
            cm.sub_water(MENU[drink]["ingredients"]["water"])
            cm.sub_milk(MENU[drink]["ingredients"]["milk"])
            cm.sub_coffee(MENU[drink]["ingredients"]["coffee"])
            # Return coffee
            print(f"Here is your {drink} ☕ Enjoy!")
        else:
            print("Sorry, that's not enough money. Money refunded.")
    else:
        print(f"Sorry, there is not enough resources ({missing_resources}).")


def refill_machine():
    resource = input(
        "What resource would you like to refill? (water|milk|coffee):")
    if resource == "water":
        value = float(input("How much water (in ml) would you like to add?: "))
        cm.add_water(value)
    elif resource == "milk":
        value = float(input("How much milk (in ml) would you like to add?: "))
        cm.add_milk(value)
    elif resource == "coffee":
        value = float(input("How much coffee (in g) would you like to add?: "))
        cm.add_coffee(value)
    else:
        print('Resource not available, please select another one.')


off = False
while not off:
    choice = input("What would you like? (espresso|latte|cappuccino): ")
    if (choice == "report"):
        # Print report of all coffee machine resources
        print(cm.report())
    elif (choice == "off"):
        # Turn off machine
        off = True
    elif (choice in ("espresso", "latte", "cappuccino")):
        serve_coffee(choice)
    elif (choice == "refill"):
        refill_machine()
    else:
        print('Wrong choice, please try again')
