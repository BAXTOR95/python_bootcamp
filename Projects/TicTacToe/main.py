from game import Game


def main():
    """
    The main entry point of the application. Manages game sessions and prompts the user
    whether they want to play again after a game finishes.
    """
    starting_player = 'X'  # Initial starting player
    while True:
        game = Game(starting_player)
        game.play()

        # Determine next starting player
        starting_player = 'O' if starting_player == 'X' else 'X'

        play_again = input('Do you want to play again? (y/n): ').lower()
        if play_again == 'n':
            print('Thank you for playing!')
            break
        elif play_again != 'y':
            print("I didn't catch that, but let's play again!")
            # If the input is neither 'y' nor 'n', default to playing again


if __name__ == "__main__":
    main()
