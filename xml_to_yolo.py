# -*- coding: utf-8 -*-
"""xml_to_yolo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qMmaHC-w4zEvVOMnzGN50DNC8_CR6SCt
"""

import os
import glob
import pandas as pd
import io
import xml.etree.ElementTree as ET
import argparse

def convert(size: tuple, box: list):
    """Takes as input:  (width, height) of an image
                        (xmin, ymin, xmax, ymax) of the bounding box
       and returns (x, y, w, h) of the bounding box in yolo format.
    """   
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[2] + box[0])/2.0
    y = (box[3] + box[1])/2.0
    w = abs(box[2] - box[0])
    h = abs(box[3] - box[1])
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh

    return (x, y, w, h)

def xml_to_txt(input_path: str, output_path: str):
    """Iterates through all .xml files (generated by labelImg) in the given directory,
    and generates .txt files that comply with yolo format for each .xml file.
    """ 
    class_mapping = {'with_mask' : '0',
                     'without_mask' : '1',
                     'mask_weared_incorrect' : '1'}

    if not glob.glob(input_path + '/*.xml'):
        raise(ValueError(f"Empty folder, there are no .xml files in {input_path}."))

    for xml_file in glob.glob(input_path + '/*.xml'):       
        tree = ET.parse(xml_file)
        root = tree.getroot()

        txt_list = []
        for member in root.findall("object"):
            f_name = root.find("filename").text
            width, height = int(root.find('size')[0].text), int(root.find("size")[1].text)
            c = member[0].text
            
            b = float(member[5][0].text), float(member[5][1].text), float(member[5][2].text), float(member[5][3].text)
            bb = convert((width, height), b)                     

            txt_list.append(class_mapping.get(c) + " " + " ".join([str(l) for l in bb]) + "\n")

        print(f"Building: {f_name.split('.')[0]}.txt")
        with open(output_path + "\\" + f_name.split(".")[0] + ".txt", "w") as writer:
            for obj in txt_list:
                writer.write(obj)
    
def parser() -> None:
    parser = argparse.ArgumentParser(description="Converts .xlm annotations into .txt files that conform to yolo format.")
    parser.add_argument("--input", type=str, default="", help="The path of the input folder that contains the .png images with their corresponding txt annotations.")
    parser.add_argument("--output", type=str, default="", help="The path of the output folder in which .txt annotations will be saved.")
    return parser.parse_args()

def check_arguments_errors(args : argparse.Namespace) -> None:
    if not os.path.exists(args.input):
        raise(ValueError(f"Invalid input folder path: {os.path.abspath(args.input)}"))
    if not os.path.exists(args.output):
        raise(ValueError(f"Invalid output folder path: {os.path.abspath(args.output)}"))

def main() -> None:
    args = parser()
    check_arguments_errors(args)   
    xml_to_txt(args.input, args.output)
         
if __name__ == "__main__":
    main()