# Author: Katelyn Lindsey
# Date: 8/13/2020
# Description:  Represents an abstract board game called Black Box. Black Box has a 10x10 board
#               full of Atoms in certain locations, and the user guesses where the Atoms are based
#               off of how Rays interact with them when shot from the border squares. Rays will
#               deflect, reflect, hit, and miss Atoms depending on the placement of Atoms in
#               the Black Box. The user will use this information in order to make guesses on
#               where Atoms are on the board, and the goal is to do this by using the lowest amount
#               of Rays possible. The user starts with a score of 25 points, and each incorrect guess
#               will result in a 5 point deduction (though multiple incorrect guesses in the same
#               location will not deduct more than 5 points). When shooting Rays, each use of an
#               entry or exit location will result in a 1 point deduction per new entry and exit
#               point.


class BlackBoxGame:
    """
    Represents an abstract board game called Black Box. A BlackBoxGame object
    has a 10x10 board with Atoms in certain locations and the ability to shoot
    Rays from the boarder squares. Atoms locations can be guessed and the user
    will lose points for incorrect guesses (unless the same location is guessed
    more than once). Users will also lose points depending on how many entry
    and exit points their Rays use, 1 point per new entry and exit. The goal
    is to guess all of the Atom locations as accurately as possible with
    the least number of Rays possible.
    """

    def __init__(self, atom_locations):
        """
        Initializes a BlackBoxGame object with a 10x10 board that has Atoms in the
        locations specified by the tuples in the atom_locations list. It also initializes
        an empty list of the Atoms contained in the board, an empty list of entry and exit locations
        used by Rays, an empty list of incorrect guesses for Atom locations, the number of
        correct guesses made initialized to 0, and a starting score of 25.
        :param atom_locations: A list of tuples that are coordinates for atom locations.
        """

        # empty board
        self._board = [['', '', '', '', '', '', '', '', '', ''] for x in range(10)]

        # empty list of atoms
        self._atoms = []

        # a list of atoms that are in the board
        for location in atom_locations:
            self._atoms.append(Atom(location))

        # add atoms to board in locations requested in atom_locations
        for location in atom_locations:

            for atom in self._atoms:

                if atom.get_location() == location:
                    self._board[location[0]][location[1]] = atom

        # a list of entry_exit locations already traversed (for score-keeping)
        self._entry_exit_locations = []

        # a list of incorrect guesses for atom locations (for score-keeping)
        self._incorrect_guesses = []

        # the number of correct guesses made
        self._correct_guesses = 0

        # starting score
        self._score = 25

    def shoot_ray(self, row, column):
        """
        Takes a row, column and if it is a valid coordinate (somewhere on the border
        of the board and not a corner), a Ray is shot from that location. If the
        coordinate is invalid, False is returned. Else, an exit point is returned
        if there is one for that Ray, or None if the Ray hits an Atom.
        :param row: The row to shoot the Ray from.
        :param column: The column to shoot the Ray from.
        :return: False if the guess is not in a valid location, None if the Ray hits an Atom,
        or the (row, column) exited otherwise.
        """

        # if the guess is not somewhere on the border of the board, return False
        if row != 0 and row != 9 and column != 0 and column != 9:
            return False

        # else if the guess is in a corner of the board, return False
        elif (row, column) == (0, 0) or (row, column) == (9, 9) or (row, column) == (9, 0) or (row, column) == (0, 9):
            return False

        # if a ray has already been shot from there, return the exit point and don't deduct points
        if self._board[row][column] != '':
            return self._board[row][column].get_exit_point()

        # else, add a ray there and find the exit point - adjust points accordingly
        else:

            # create a ray at that border square
            self._board[row][column] = Ray((row, column))

            # add the entry point to the list of entry_exit_locations if it is not there already
            square_used = False
            for location in self._entry_exit_locations:

                if location == (row, column):
                    square_used = True

            if square_used is False:
                self._entry_exit_locations.append((row, column))

            # find the exit point
            self._board[row][column].find_exit_point(self._board)
            exit_point = self._board[row][column].get_exit_point()

            # if there was no exit point (there was a hit), deduct a point if the entry point
            # was not used already and return the exit point, else just return the exit point
            if exit_point is None:

                if square_used is True:
                    return exit_point

                self.update_score(1)
                return exit_point

            # else if there was an exit point, deduct two points if the exit point has not
            # been used yet, otherwise deduct one point
            else:

                for entry_exit in self._entry_exit_locations:

                    # if the exit point has been used and the entry point is used, deduct no points
                    if exit_point == entry_exit and square_used:
                        return exit_point

                    # else if the exit point has been used but the entry point hasn't, deduct one point
                    elif exit_point == entry_exit:
                        self.update_score(1)
                        return exit_point

                # else if the exit point and entry point have not been used, deduct two points
                self._entry_exit_locations.append(exit_point)
                self.update_score(2)
                return exit_point

    def update_score(self, deducted_points):
        """
        Updates the score by deducting points from the score.
        :param deducted_points: The amount of points to deduct.
        :return: None
        """

        self._score -= deducted_points

    def guess_atom(self, row, column):
        """
        Takes a coordinate (row, column) of a guess and, if it is a valid location for
        an Atom, it returns True. Otherwise, it returns False and deducts 5 points if
        that location has not been guessed yet.
        :param row: The row of the guess.
        :param column: The column of the guess.
        :return: True if there is an atom at the given coordinate, False otherwise.
        """

        # if there is no atom there, return False and deduct points depending on if
        # that spot has been guessed incorrectly before
        if self._board[row][column] == '':

            # if that spot has been guessed before, return False without deducting points
            for guess in self._incorrect_guesses:

                if guess == (row, column):
                    return False

            # else, add that coordinate to the list of incorrect guesses, deduct 5 points,
            # and return False
            self._incorrect_guesses.append((row, column))
            self.update_score(5)
            return False

        # else, update that Atoms' guess state and return True
        else:

            # if that Atom has not been guessed before, add 1 to the total number of correct guesses
            # and update the Atom's guess state
            if self._board[row][column].is_guessed() is False:
                self._correct_guesses += 1
                self._board[row][column].set_guess_state()

            return True

    def get_score(self):
        """
        Returns the score of a BlackBoxGame.
        :return: self._score (an integer)
        """

        return self._score

    def atoms_left(self):
        """
        Returns the number of atoms left that haven't been guessed.
        :return: the number of atoms not guessed (an integer)
        """

        return len(self._atoms) - self._correct_guesses

    def display_board(self):
        """
        Displays the board of a BlackBoardGame.
        :return: None
        """

        for row in self._board:
            print(row)


class Atom:
    """
    Represents an Atom with a location and a guess state. Atoms can be guessed
    and their location can be returned.
    """

    def __init__(self, location):
        """
        Initializes an Atom with a location (row, column) and a guess state
        initialized to False.
        :param location: The coordinate location (row, column) of an Atom.
        """

        self._location = location
        self._guess_state = False

    def get_location(self):
        """
        Returns the location (row, column) of an Atom.
        :return: self._location
        """

        return self._location

    def is_guessed(self):
        """
        Returns True if the Atom has been guessed, False otherwise.
        :return: self._guess_state
        """

        return self._guess_state

    def set_guess_state(self):
        """
        Sets the guess state of an Atom to True if it is guessed.
        :return: None
        """

        self._guess_state = True


class Ray:
    """
    Represents a Ray with an entry point, an exit point, and whether or not the
    Ray has been shot. A Ray's exit point can be found by traversing through
    a board and changing direction depending on the Atoms encountered.
    """

    def __init__(self, entry_point):
        """
        Initializes a Ray with an entry point, an exit point set to 'UNKNOWN',
        and a ray_shot attribute initialized to False.
        :param entry_point: The coordinate (row, column) of the entry point.
        """

        self._entry_point = entry_point
        self._exit_point = "UNKNOWN"
        self._ray_shot = False

    def get_entry_point(self):
        """
        Returns the entry point of a Ray.
        :return: self._entry_point
        """

        return self._entry_point

    def get_exit_point(self):
        """
        Returns the exit point of a Ray.
        :return: self._exit_point
        """

        return self._exit_point

    def is_ray_shot(self):
        """
        Returns True if the ray has been shot, False otherwise.
        :return: self._ray_shot
        """

        return self._ray_shot

    def set_ray_shot(self):
        """
        Sets the ray_shot data member to True if the ray has been shot.
        :return: None
        """

        self._ray_shot = True

    def find_exit_point(self, board):
        """
        Finds the exit point of a Ray by traversing through the board and
        interacting with the Atoms it encounters. Once an exit point is found, the Ray's
        exit_point data member is set to that exit point.
        :param board: A list of lists representing a board of a BlackBoxGame with Atoms in it.
        :return: None
        """

        # if the exit point is already known, there is no need to find it again
        if self._exit_point != "UNKNOWN":
            return

        # else if it is not known, it is time to search for the exit point
        row = self._entry_point[0]
        column = self._entry_point[1]

        # if the ray is starting on the left boarder, start searching right
        if column == 0:
            return self.search_right(row, column, board)

        # else if the ray is starting on the right boarder, start searching left
        elif column == 9:
            return self.search_left(row, column, board)

        # else if the ray is starting on the top border, start searching down
        elif row == 0:
            return self.search_down(row, column, board)

        # else if the ray is starting on the bottom border, start searching up
        else:
            return self.search_up(row, column, board)

    def search_right(self, row, column, board):
        """
        Takes a row, column, and board of a BlackBoxGame with Atoms, and searches
        right through the board while testing for interactions with Atom objects.
        The purpose is to find the exit point of the Ray.
        :param row: The row coordinate of the starting point.
        :param column: The column coordinate of the starting point.
        :param board: The board of a BlackBoxGame which is a list of lists with Atoms.
        :return: None
        """

        # First, check for a reflection on the edge of the board if the ray is still at
        # its entry point.
        # check for a reflection if the ray is at the top edge of the board
        if column == 0 and row == 1 and board[row + 1][column + 1] != '':
            self._exit_point = (row, column)
            return

        # else, check for a reflection if the ray is at the bottom edge of the board
        elif column == 0 and row == 8 and board[row - 1][column + 1] != '':
            self._exit_point = (row, column)
            return

        # else, check for a reflection if the ray is not at the top or bottom edge
        elif column == 0 and (board[row + 1][column + 1] != '' or board[row - 1][column + 1] != ''):
            self._exit_point = (row, column)
            return

        # now, search to the right until either a hit or deflection happens
        while column < 8:

            # if a hit is found, there is no exit - return
            if board[row][column + 1] != '':
                self._exit_point = None
                return

            # if the ray is not along the top or bottom edge of the board, search for upper and lower atoms
            if row != 1 and row != 8:

                # if there is a deflection with two atoms at once, it results in a reflection -
                # start searching the opposite direction
                if board[row - 1][column + 1] != '' and board[row + 1][column + 1] != '':
                    # print("double deflection")
                    return self.search_left(row, column, board)

                # else if there is a deflection from an upper atom, the ray is deflected downwards
                elif board[row - 1][column + 1] != '':
                    return self.search_down(row, column, board)

                # else if there is a deflection from a lower atom, the ray is deflected upwards
                elif board[row + 1][column + 1] != '':
                    return self.search_up(row, column, board)

            # else if the ray is along the top edge of the board, only search for lower atoms
            elif row == 1:

                # if there is a deflection from a lower atom, the ray exits the top of the board
                if board[row + 1][column + 1] != '':
                    self._exit_point = (row - 1, column)
                    return

            # else if the ray is along the bottom edge of the board, only search for upper atoms
            elif row == 8:

                # if there is a deflection from an upper atom, the ray exits the top of the board
                if board[row - 1][column + 1] != '':
                    self._exit_point = (row + 1, column)
                    return

            # if no atoms are interacted with, 'move' the ray one column forwards
            column += 1

        # once the last column before the boarder is reached, this means the exit point is found
        self._exit_point = (row, column + 1)
        return

    def search_left(self, row, column, board):
        """
        Takes a row, column, and board of a BlackBoxGame with Atoms, and searches
        left through the board while testing for interactions with Atom objects.
        The purpose is to find the exit point of the Ray.
        :param row: The row coordinate of the starting point.
        :param column: The column coordinate of the starting point.
        :param board: The board of a BlackBoxGame which is a list of lists with Atoms.
        :return: None
        """

        # First, check for a reflection on the edge of the board if the ray is still at
        # its entry point.
        # check for a reflection if the ray is at the top edge of the board
        if column == 9 and row == 1 and board[row + 1][column - 1] != '':
            self._exit_point = (row, column)
            return

        # else, check for a reflection if the ray is at the bottom edge of the board
        elif column == 9 and row == 8 and board[row - 1][column - 1] != '':
            self._exit_point = (row, column)
            return

        # else, check for a reflection if the ray is not at the top or bottom edge
        elif column == 9 and (board[row + 1][column - 1] != '' or board[row - 1][column - 1] != ''):
            self._exit_point = (row, column)
            return

        # now, search to the left until either a hit or deflection happens
        while column > 1:

            # if a hit is found, there is no exit - return
            if board[row][column - 1] != '':
                self._exit_point = None
                return

            # if the ray is not along the top or bottom edge of the board, search for upper and lower atoms
            if row != 1 and row != 8:

                # if there is a deflection with two atoms at once, it results in a reflection -
                # start searching the opposite direction
                if board[row - 1][column - 1] != '' and board[row + 1][column - 1] != '':
                    # print("double deflection")
                    return self.search_right(row, column, board)

                # else if there is a deflection from an upper atom, the ray is deflected downwards
                elif board[row - 1][column - 1] != '':
                    return self.search_down(row, column, board)

                # else if there is a deflection from a lower atom, the ray is deflected upwards
                elif board[row + 1][column - 1] != '':
                    return self.search_up(row, column, board)

            # else if the ray is along the top edge of the board, only search for lower atoms
            elif row == 1:

                # if there is a deflection from a lower atom, the ray exits the top of the board
                if board[row + 1][column - 1] != '':
                    self._exit_point = (row - 1, column)
                    return

            # else if the ray is along the bottom edge of the board, only search for upper atoms
            elif row == 8:

                # if there is a deflection from an upper atom, the ray exits the top of the board
                if board[row - 1][column - 1] != '':
                    self._exit_point = (row + 1, column)
                    return

            # if no atoms are interacted with, 'move' the ray one column forwards
            column -= 1

        # once the last column before the boarder is reached, this means the exit point is found
        self._exit_point = (row, column - 1)
        return

    def search_up(self, row, column, board):
        """
        Takes a row, column, and board of a BlackBoxGame with Atoms, and searches
        up through the board while testing for interactions with Atom objects.
        The purpose is to find the exit point of the Ray.
        :param row: The row coordinate of the starting point.
        :param column: The column coordinate of the starting point.
        :param board: The board of a BlackBoxGame which is a list of lists with Atoms.
        :return: None
        """

        # First, check for a reflection on the edge of the board if the ray is still at
        # its entry point.
        # check for a reflection if the ray is at the left edge of the board
        if row == 9 and column == 1 and board[row - 1][column + 1] != '':
            self._exit_point = (row, column)
            return

        # else, check for a reflection if the ray is at the right edge of the board
        elif row == 9 and column == 8 and board[row - 1][column - 1] != '':
            self._exit_point = (row, column)
            return

        # else, check for a reflection if the ray is not at the left or right edge
        elif row == 9 and (board[row - 1][column + 1] != '' or board[row - 1][column - 1] != ''):
            self._exit_point = (row, column)
            return

        # now, search upwards until either a hit or deflection happens
        while row > 1:

            # if a hit is found, there is no exit - return
            if board[row - 1][column] != '':
                self._exit_point = None
                return

            # if the ray is not along the left or right edge of the board, search for atoms up to the left and right
            if column != 1 and column != 8:

                # if there is a deflection with two atoms at once, it results in a reflection -
                # start searching the opposite direction
                if board[row - 1][column - 1] != '' and board[row - 1][column + 1] != '':
                    # print("double deflection")
                    return self.search_down(row, column, board)

                # else if there is a deflection from an upper left atom, the ray is deflected to the right
                elif board[row - 1][column - 1] != '':
                    return self.search_right(row, column, board)

                # else if there is a deflection from an upper right atom, the ray is deflected to the left
                elif board[row - 1][column + 1] != '':
                    return self.search_left(row, column, board)

            # else if the ray is along the left edge of the board, only search for atoms up and right
            elif column == 1:

                # if there is a deflection from an upper right atom, the ray exits the top of the board
                if board[row - 1][column + 1] != '':
                    self._exit_point = (row, column - 1)
                    return

            # else if the ray is along the right edge of the board, only search for atoms up and left
            elif column == 8:

                # if there is a deflection from an upper left atom, the ray exits the top of the board
                if board[row - 1][column - 1] != '':
                    self._exit_point = (row, column + 1)
                    return

            # if no atoms are interacted with, 'move' the ray one row forwards
            row -= 1

        # once the last row before the boarder is reached, this means the exit point is found
        self._exit_point = (row - 1, column)
        return

    def search_down(self, row, column, board):
        """
        Takes a row, column, and board of a BlackBoxGame with Atoms, and searches
        down through the board while testing for interactions with Atom objects.
        The purpose is to find the exit point of the Ray.
        :param row: The row coordinate of the starting point.
        :param column: The column coordinate of the starting point.
        :param board: The board of a BlackBoxGame which is a list of lists with Atoms.
        :return: None
        """

        # First, check for a reflection on the edge of the board if the ray is still at
        # its entry point.
        # check for a reflection if the ray is at the left edge of the board
        if row == 0 and column == 1 and board[row + 1][column + 1] != '':
            self._exit_point = (row, column)
            return

        # else, check for a reflection if the ray is at the right edge of the board
        elif row == 0 and column == 8 and board[row + 1][column - 1] != '':
            self._exit_point = (row, column)
            return

        # else, check for a reflection if the ray is not at the left or right edge
        elif row == 0 and (board[row + 1][column + 1] != '' or board[row + 1][column - 1] != ''):
            self._exit_point = (row, column)
            return

        # now, search upwards until either a hit or deflection happens
        while row < 8:

            # if a hit is found, there is no exit - return
            if board[row + 1][column] != '':
                self._exit_point = None
                return

            # if the ray is not along the left or right edge of the board, search for atoms down to the left and right
            if column != 1 and column != 8:

                # if there is a deflection with two atoms at once, it results in a reflection -
                # start searching the opposite direction
                if board[row + 1][column - 1] != '' and board[row + 1][column + 1] != '':
                    # print("double deflection")
                    return self.search_up(row, column, board)

                # else if there is a deflection from a lower left atom, the ray is deflected to the right
                elif board[row + 1][column - 1] != '':
                    return self.search_right(row, column, board)

                # else if there is a deflection from a lower right atom, the ray is deflected to the left
                elif board[row + 1][column + 1] != '':
                    return self.search_left(row, column, board)

            # else if the ray is along the left edge of the board, only search for atoms up and right
            elif column == 1:

                # if there is a deflection from a lower right atom, the ray exits the top of the board
                if board[row + 1][column + 1] != '':
                    self._exit_point = (row, column - 1)
                    return

            # else if the ray is along the right edge of the board, only search for atoms up and left
            elif column == 8:

                # if there is a deflection from a lower left atom, the ray exits the top of the board
                if board[row + 1][column - 1] != '':
                    self._exit_point = (row, column + 1)
                    return

            # if no atoms are interacted with, 'move' the ray one row forwards
            row += 1

        # once the last row before the boarder is reached, this means the exit point is found
        self._exit_point = (row + 1, column)
        return
