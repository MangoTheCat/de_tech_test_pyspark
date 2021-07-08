import random
from functools import partial
import csv
from itertools import product
import string
import csv
from datetime import datetime
import os

def generate_data(size=1000000):
    """
    Generates csvs in root directory. The csvs are:
        main/test_data.csv
            - field1, field2, field3, field4 are random ints in range(1,20)
            - val1, val2, val3 are random floats

    Args:
        size (int, optional): The number of rows required in the 
            main test data csv.

    Raises:
        FileExistsError: Raised if a file has already been generated
            with today's date.
    """
    def _randomly_nullify(series, n):
        "Replaces n entires in series with None"
        indices = random.choices(range(size),k=n)
        return [v if i not in indices else None for i,v in enumerate(series)]

    date = datetime.today().strftime('%Y-%m-%d')

    part_choices = partial(random.choices, range(1,20), k=size)

    field1 = _randomly_nullify(
        part_choices(weights=[i**2/2 for i in range(1,20)]), 5
     ) # end weighted

    field2 = _randomly_nullify(
        part_choices(weights=[(20-i)/i for i in range(1,20)]), 30
    ) # start weighted

    field3 = part_choices(weights=[1/(1+abs(i - 10)) for i in range(1,20)]) # mid weighted
    field4 = part_choices() # uniform

    val1 = (random.gauss(1000, 100) for i in range(size)) # normal random
    val2 = (random.random()*1000*i if i else 0 for i in field1) # random correlated with field1
    val3 = _randomly_nullify(
        [random.random()*1000*i for i in field4],10
        ) # random correlated with field4

    combined = zip(field1, field2, field3, field4, val1, val2, val3)

    path = os.path.join(os.getcwd(), f'data/main/{date}/test_data.csv')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['field1','field2','field3','field4','val1','val2','val3'])
        writer.writerows(combined)

    # lookup csv
    field = [i for i in range(1,20) if i != 10]
    group = product(field, field)
    lookup = list([x, y, random.choice(string.ascii_letters)] for x,y in group)
    try:
        with open('data/lookup.csv', 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['field1','f2','lookup_val'])
            writer.writerows(lookup)
    except FileExistsError:
        pass
