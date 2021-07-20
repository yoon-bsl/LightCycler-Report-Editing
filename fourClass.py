import numpy as np
import argparse

from numpy.lib.function_base import _parse_input_dimensions
import cv2
import os

from fLAMP import Editor

class Editor_Four_Class(Editor):
    '''
    '''

    def __init__(self, image, column, 
                fristclass, secondclass, thirdclass, lastclass):
        self.image = cv2.imread(image)
        
        self.column = int(column)

        self.fristclass  = [int(i) for i in fristclass ]
        self.secondclass = [int(i) for i in secondclass]
        self.thirdclass  = [int(i) for i in thirdclass ]
        self.lastclass   = [int(i) for i in lastclass  ]

        print(f'\nImage to be analyzed: {image}')
        print(f'Indicies of first class: {self.fristclass}')
        print(f'Indicies of second class: {self.secondclass}')
        print(f'Indicies of third class: {self.thirdclass}')
        print(f'Indicies of fourth class: {self.lastclass}')

    def run(self):
        '''
        Main algorithm of the class. Given a LightCycler fluorescence report,
        the method will find the colors of all of the samples and then recolor
        them different colors depending on the user's input
        '''
        self.colors = self.findSampleColors(self.image)

        colors1 = [self.colors[i - 1] for i in self.fristclass ] # Black
        colors2 = [self.colors[i - 1] for i in self.secondclass] # Blue
        colors3 = [self.colors[i - 1] for i in self.thirdclass ] # Green
        colors4 = [self.colors[i - 1] for i in self.lastclass  ] # Red

        for row in range(50, 405):
            for col in range(267, 961):
                # Remember that images are in BGR in OpenCV!
                if list(self.image[row, col]) in colors1:
                    # Change first sample class to black
                    self.image[row, col] = np.array([0, 0, 1])
                elif list(self.image[row, col]) in colors2:
                    # Change second sample class to blue
                    self.image[row, col] = np.array([254, 0, 0])
                elif list(self.image[row, col]) in colors3:
                    # Change third sample class to green
                    self.image[row, col] = np.array([0, 254, 0])
                elif list(self.image[row, col]) in colors4:
                    # Change fourth sample class to red
                    self.image[row, col] = np.array([0, 0, 254])
        cv2.imwrite('output.png', self.image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Edit a LightCycler report image'
    )

    parser.add_argument('-i', '--image', required=True, help='Image file name')
    parser.add_argument('-c', '--column', required=True,
                    help='Image column containing sample colors')
    parser.add_argument('-f', '--fristclass', nargs='+', required=True,
                    help='List containing sample #s of the first sample type')
    parser.add_argument('-s', '--secondclass', nargs='+', required=True,
                    help='List containing sample #s of the second sample type')
    parser.add_argument('-t', '--thirdclass', nargs='+', required=True,
                    help='List containing sample #s of the third sample type')
    parser.add_argument('-l', '--lastclass', nargs='+', required=True,
                    help='List containing sample #s of the fourth sample type')

    args = parser.parse_args()
    # print(args)

    editor = Editor_Four_Class(
        args.image,
        args.column,
        args.fristclass, 
        args.secondclass, 
        args.thirdclass,
        args.lastclass
        )
    editor.run()