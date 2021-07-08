import numpy as np
import argparse
import cv2
import os

class Editor(object):
    '''
    '''
    def __init__(self, samples, positives, negatives):
        self.samples = samples
        self.positives = positives
        self.negatives = negatives
        print(samples)
        print(positives)
        print(negatives)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Edit a LightCycler report image'
    )
    parser.add_argument('-s', '--samples', type=int, help='Number of samples')
    parser.add_argument('-p', '--positive', type=list,
                    help='List containing sample #s of positive samples')
    parser.add_argument('-n', '--negative', type=list,
                    help='List containing sample #s of negative samples')
    args = parser.parse_args()
    args_dict = vars(args)
    print(args_dict)
    editor = Editor(**args_dict)