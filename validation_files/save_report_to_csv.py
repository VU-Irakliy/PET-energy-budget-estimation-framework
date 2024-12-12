import csv
import pandas as pd
from collections import defaultdict


def save_report_to_csv(items):

    items = check_for_nones(items)

    # print(items)
    # exit()
    
    def flatten_dict(d, parent_key='', sep='_'):
        new_dict = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                new_dict.update(flatten_dict(v, new_key, sep=sep))
            else:
                new_dict[new_key] = v
        return new_dict
    
    # df = pd.json_normalize(items['results'])
    # new_dict = defa
    with open(f'reports/{items["input"]["Filename"]}_{items["ID"]}_{items["input"]["OS"]}_output.csv', 'w', newline='') as file:
        writer = None
        for syn_key, syn_values in items['results'].items():
            flat_data = flatten_dict(syn_values)
            if not writer:
                # Initialize the CSV writer and write headers
                headers = flat_data.keys()
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
            # Write the flattened dictionary as a row in the CSV
            writer.writerow(flat_data)
            # Write an empty row
        writer.writerow({})

        # Writing second dataset with different structure
        new_headers = items['input'].keys()
        new_writer = csv.DictWriter(file, fieldnames=new_headers)
        new_writer.writeheader()
        new_writer.writerow(items['input'])
    # Save to CSV
    # df.to_csv(f'{items["ID"]}_output.csv', index=False)


def check_for_nones(items):
    for key, value in items.items():
        if isinstance(value, dict):
            items[key] = check_for_nones(value)
        
        elif value == None:
            items[key] = 'None'
    return items
        