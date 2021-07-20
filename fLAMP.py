import numpy as np
import argparse
import cv2
import os

class Editor(object):
    '''
    '''
    def __init__(self, image, positives, negatives):
        self.image = cv2.imread(image)

        self.positives = [int(i) for i in positives]
        self.negatives = [int(i) for i in negatives]

        print(f'\nImage to be analyzed: {image}')
        print(f'Indicies of positive samples: {positives}')
        print(f'Indicies of negative samples: {negatives}\n')

    def run(self):
        '''
        Main algorithm of the class. Given a LightCycler fluorescence report,
        the method will find the colors of all of the samples and then recolor
        them either red or black depending on the user's input
        '''
        self.colors = self.findSampleColors(self.image)

        negativeColors = []
        positiveColors = []
        for i in self.negatives:
            negativeColors.append(self.colors[i - 1])
        for i in self.positives:
            positiveColors.append(self.colors[i - 1])

        for row in range(50, 405):
            for col in range(267, 961):
                if list(self.image[row, col]) in negativeColors:
                    self.image[row, col] = np.array([0, 0, 1])
                elif list(self.image[row, col]) in positiveColors:
                    self.image[row, col] = np.array([0, 0, 254])
        cv2.imwrite('output.png', self.image)

    def findSampleColors(self, image):
        '''
        Iterates down the pixels where the sample colors are and
        saves the RGB pixels that aren't white
        '''
        colors = []
        for i in range(400):
            color = list(image[50 + i, 140])

            # if the color is not white, save it
            if color != [255, 255, 255]:
                colors.append(color)
        
        print(f'Number of colors identified in the report: {len(colors)}')
        return colors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Edit a LightCycler report image'
    )

    parser.add_argument('-i', '--image', required=True, help='Image file name')
    parser.add_argument('-p', '--positive', nargs='+', required=True,
                    help='List containing sample #s of positive samples')
    parser.add_argument('-n', '--negative', nargs='+', required=True,
                    help='List containing sample #s of negative samples')

    args = parser.parse_args()

    editor = Editor(
        args.image,
        args.samples, 
        args.positive, 
        args.negative
        )
    editor.run()