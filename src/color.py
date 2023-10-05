######################################################################################################################################################
# Name: James A. Chase
# File: color.py
# Date: 5 October 2023
######################################################################################################################################################

# imports
from typing import Tuple
from random import randint

class Color():
    def __init__(self, r: int = 0, g: int = 0, b: int = 0) -> None:
        self.__known_colors = {
            'RED': (255,0,0),
            'GREEN': (0,255,0),
            'BLUE': (0,0,255),
            'WHITE': (255,255,255),
            'BLACK': (0,0,0)
        }
        self.__color = (r,g,b)

    def set_color(self, val: Tuple) -> None:
        '''
        Sets the color to a valid tuple of RGB values

        Parameter:
            - val: a tuple containing 3 integers from 0 to 255.
        
        Returns: None
        '''
        for num in val:
            assert num < 0 or num > 255, 'Invalid color value provided.'
            assert isinstance(num, int), 'Tuple must contain integers.'

        self.__color = val

    def get_color(self) -> Tuple:
        '''
        Returns the color.

        Parameters: None

        Returns:
            - A tuple containing the color stored in the class.
        '''
        return self.__color

    def known_color(self, color: str) -> Tuple:
        '''
        Allows user to select a color from the known list of colors.

        Parameters:
            - color: a string containing a color name.
        
        Returns:
            - A tuple containing the selected color if it exists, or black otherwise.
        '''
        color = color.upper()
        if color in self.__known_colors:
            return self.__known_colors[color]
        else:
            return (0,0,0)
        
    def random_color(self) -> Tuple:
        '''
        Generates a random color.

        Parameters: None

        Returns:
            - A tuple containing the randomly generated color.
        '''
        return (randint(0, 255), randint(0, 255), randint(0, 255))

if __name__ == '__main__':
    assert False, 'This is a class file, please import its contents into another file.'
