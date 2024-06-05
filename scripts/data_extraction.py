from lxml import html

from typing import *

import numpy as np
import re as regex

def read_html(file_path: str) -> html.HtmlElement:
    """
        Read an html file and convert it to an `html.HtmlElement` object

    Args:
        file_path (str): Path to html file

    Returns:
        html.HtmlElement: An `html.HtmlElement` object representing the page
    """
    with open(file_path, 'r') as file:
        content = file.read()
        
    return html.fromstring(content)


def interpret_header(row: html.HtmlElement, xpath='.//th') -> List[str]:
    """
        Extract the header from given row

    Args:
        row (html.HtmlElement): Header row
        xpath (str, optional): xpath to elements in a row. Defaults to './/th'.

    Returns:
        List[str]: List of headers.
    """
    result = []
    header: html.HtmlElement = None
    
    for header in row.xpath(xpath):
        result.append(header.text_content().strip())
        
    return result


def interpret_table(table: List[html.HtmlElement], headers:list, xpath='.//td')\
    -> Dict[str, List[str]]:
    """
        Interpret the given table. The table should be a `list` of `html.HtmlElement` objects where each element represents a row of the table.
        
        Each row is expected to have the same number of elements as headers. If a row contains more or less elements, it will be ignored

    Args:
        table (List[html.HtmlElement]): List of html table rows.
        header (list): List of headers.
        xpath (str, optional): xpath to elements in a row. Defaults to './/td'.

    Returns:
        Dict[str, List[str]]: A diction representing the table
    """
    result: Dict[str, List[str]] = {}
    for header in headers:
        result[header] = []
        
    row: html.HtmlElement = None
    for row in table:
        elements = row.xpath(xpath)
        if len(elements) != len(headers):
            # skip broken rows
            continue
        
        element: html.HtmlElement = None
        for (element, header) in zip(elements, headers):
            content = element.text_content().strip()
            result[header].append(content)
            
    return result

###########################################################
# ------------------------------------------------------- #
###########################################################

FINAL_PROCESS_KEYS = [
    'Course',
    'Term',
    'Enroll',
    'Evals Made',
    'Rcmnd Class',
    'Rcmnd Instr',
    'Study Hrs/wk',
    'Avg Grade Expected',
    'Avg Grade Received'
]

def final_process(data: Dict[str, List[str]]):
    """
        Final Process before the data is usable.
        
        
    Args:
        data (Dict[str, List[str]]): Original data extracted from html

    Raises:
        RuntimeError: if some keys are missing
    """
    
    for key in FINAL_PROCESS_KEYS:
        if key not in data:
            raise RuntimeError(f'Key "{key}" not found')
    
    # handle course name, only keeps department and code (i.e. MATH 140A)
    data['Course'] = list(
        map(
            lambda name: name.split(' - ')[0],
            data['Course']
        )
    )
    
    # handle Term, remove all summer sessions
    data['Term'] = list(
        map(
            lambda term: term if\
                                'SP' in term\
                             or 'WI' in term\
                             or 'FA' in term\
                         else np.nan,
            data['Term']
        )
    )
    
    # handle Enroll, Evals Made, Study Hrs/wk
    data['Enroll'] = list(
        map(
            lambda x: int(x),
            data['Enroll']
        )
    )
    data['Evals Made'] = list(
        map(
            lambda x: int(x),
            data['Evals Made']
        )
    )
    data['Study Hrs/wk'] = list(
        map(
            lambda x: float(x),
            data['Study Hrs/wk']
        )
    )
    
    # handle Rcmnd class and Rcmnd Instr
    data['Rcmnd Class'] = list(
        map(
            lambda x: float(x.strip('%'))/100,
            data['Rcmnd Class']
        )
    )
    data['Rcmnd Instr'] = list(
        map(
            lambda x: float(x.strip('%'))/100,
            data['Rcmnd Instr']
        )
    )
    
    # handle grade
    pattern = r'\((.*?)\)'
    def _extract_gpa(grade:str):
        result = regex.findall(pattern, grade)
        if len(result) != 1:
            return np.nan
        else:
            return float(result[0])
    
    data['Avg Grade Expected'] = list(
        map(
            _extract_gpa,
            data['Avg Grade Expected']
        )
    )
    data['Avg Grade Received'] = list(
        map(
            _extract_gpa,
            data['Avg Grade Received']
        )
    )