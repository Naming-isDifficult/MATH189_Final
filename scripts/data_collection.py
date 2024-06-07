from data_extraction import *
from categories import *

import pandas as pd
import re as regex
import numpy as np
import argparse
import os
import glob


RAW_FOLDER = '../data/raw/'
PREPROCESSED_FOLDER = '../data/preprocessed/'
FINALIZED_FOLDER = '../data/finalized/'
TABLE_XPATH = '/html/body/main/div/section/form/div[4]/div[2]/table'

def save(df, folder, name):
    df.to_csv(f'{folder}{name}', index=False)
    

def extract_year(term):
    year = regex.search(r'\d+', term)
    if year:
        return int(year[0])
    else:
        raise RuntimeWarning(f'Improper term: {term}, setting value to nan')
        return np.nan
    
    
def extract_course_number(course):
    course_number = regex.search(r'\d+', course)
    if course_number:
        return int(course_number[0])
    else:
        raise RuntimeWarning(f'Improper course name: {course}, setting value to nan')
        return np.nan
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    args = parser.parse_args()
    
    path = args.path
    files = []
    
    if os.path.isdir(path):
        # take in all files under given foloder
        # ignore files under sub-folder
        temp = glob.glob(os.path.join(path, '*'))
        
        for file in temp:
            if os.path.isfile(file):
                files.append(file)
                
    elif os.path.isfile(path):
        # simply store the path
        files.append(path)
        
    else:
        raise FileNotFoundError(f'{path} is not a file or directory')
    
    for file in files:
        # extract file name first
        filename = os.path.basename(file)
        filename = os.path.splitext(filename)[0]
        filename = filename + '.csv'
        
        # extract raw data
        tree = read_html(file)
        table = tree.xpath(TABLE_XPATH)[0]
        rows = table.xpath('.//tr')

        header = interpret_header(rows[0])
        data = interpret_table(rows[1:], header)

        save(pd.DataFrame(data), RAW_FOLDER, filename)
        
        # Preprocess data
        final_process(data)
        data = pd.DataFrame(data)
        data = data.dropna() # remove courses from summer sessions
                            # and/or courses that contain missing values

        save(data, PREPROCESSED_FOLDER, filename)
        
        # Pre/Post-GPT tagging
        data['isPreGPT'] = data['Term'].apply(extract_year)
        data['isPreGPT'] = data['isPreGPT'] < 22
        
        # STEM tagging
        data['isSTEM'] = data['Course'].apply(
            lambda x: False if 'LT' in x or 'PHIL' in x\
                            or 'VIS' in x or 'MUS' in x\
                            else True
        )
        
        # for STEM courses
        data['isAbstract'] = data['Course'].apply(
            # note STEM_ABSTRACT stores course number
            lambda x: True if x in STEM_ABSTRACT else False
        )

        # for Arts courses
        data['isWritten'] = data['Course'].apply(
            lambda x: True if 'LT' in x or 'PHIL' in x else False
        )
            
        # Upper Division tagging
        data['isUD'] = data['Course'].apply(extract_course_number)
        data['isUD'] = data['isUD'] >= 100
        
        save(data, FINALIZED_FOLDER, filename)