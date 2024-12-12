from termcolor import colored


def report_function(items):
    print('---------------------------------------------------------------------------------------------------------------------------')
    print(   colored(f'Report for iteration {items["ID"]}:',"cyan", attrs=["bold", "underline"])   )
    print(colored("The following input was provided:", "yellow"   )    )
    print('Filename that is used: ' + colored(f'{items["input"]["Filename"]}.', 'green') )
    print(f'Target attribute for ML: ' + colored(f'{items["input"]["Target"]}.', 'green') )
    # print(f'Possible known attributes to the attacker for risk measurements: ' + colored(f'{items["input"]["Possible known attributes"]}.', 'green') )
    # print(f'Secret attribute that attacker is trying to guess for Inference risk measurement: ' + colored(f'{items["input"]["Secret attribute"]}.', 'green') )

    print('\n')
    for syn, data in items['results'].items():
        
        epsilon = data['epsilon']
        syn_energy = format(data['energy_synthesis'], ".6f")
        risks = data['risks']
        knn = data['knn']
        logres = data['logres']
        if epsilon == 0:
            print(colored('Synthetic Data without DP.', 'yellow'  ))
        else:
            print(colored('Synthetic Data with DP (epsilon value is ', 'yellow' ) + colored( f'{epsilon}', 'green', attrs=["bold", "underline"] ) + colored(').', 'yellow') )
        
        for name, value in risks.items():
            percent = value * 100
            if name == "Inference" and items["input"]["Secret attribute"] == None:
                print(f'Mean {name} risk is ' + colored(f'{percent:.4f}%.', 'green'))
            else:
                print(f'{name} risk is ' + colored(f'{percent:.4f}%.', 'green'))
        
        print(f'Energy for generating synthetic data is ' + colored(f'{syn_energy}J.', 'green'))

        for name, value in knn.items():
            if name != 'K-value':
                value = format(value, ".6f" )
            
            if name == "Energy":
                print(f'{name} is ' + colored(f'{value}J.', 'green'))
            elif name == "Total energy":
                # total_knn = float(syn_energy) + float(format(knn['Energy'], ".6f"))
                print('Total energy consumption with K-nearest neighbors is ' + colored(f'{value}J.', 'green'))
            else:
                print(f'{name} is ' + colored(f'{value}.', 'green'))
            

        for name, value in logres.items():
            if name != 'K-value':
                value = format(value, ".6f" )
            
            if name == "Energy":
                print(f'{name} is ' + colored(f'{value}J.', 'green'))
            elif name == "Total energy":
                # total_knn = float(syn_energy) + float(format(knn['Energy'], ".6f"))
                print('Total energy consumption with Logistic Regression is ' + colored(f'{value}J.', 'green'))
            else:
                print(f'{name} is ' + colored(f'{value}.', 'green'))
        # total_logres = float(syn_energy) + float(format(logres['Energy'], ".6f"))
        # print(f'Total energy consumption with Logistic Regression is ' + colored(f'{total_logres:.6f}J.', 'green'))
        print('\n')
    print('---------------------------------------------------------------------------------------------------------------------------')
    to_html(items)





def to_html(items):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report for Iteration {items['ID']}</title>
        <style>
            .results-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr); /* 2 columns */
                gap: 20px;
            }}
            .data-section {{
                border: 1px solid #ccc;
                padding: 20px;
                background-color: #f8f8f8;
            }}
            .color-changer {{ 
                background-color: #249418;
                font-weight: bold; 
            }} 
        </style>
    </head>
    <body>
        <h1>Report for iteration {items['ID']}:</h1>
        <h2>User Input</h2>
        <p>The following input was provided:</p>
        <ul>
            <li>Filename that is used: {items['input']['Filename']}</li>
            <li>Operating System: {items['input']['OS']}</li>
            <li>Tool used for energy measurements: {items['input']['Tool']}</li>
            <li>Categorical attributes: {items['input']['Categorical attributes']}</li>
            <li>Continuous attributes: {items['input']['Continuous attributes']}</li>
            <li>Target attribute for ML: {items['input']['Target']}</li>
            <li>Number of records: {items['input']['Number of records']}</li>
            <li>Number of attributes: {items['input']['Number of attributes']}</li>

        </ul>
        <div class="results-grid">
            {"".join(f'''
            <div class="data-section">
                <h2>{"Synthetic Data without DP" if data["epsilon"] == 0 else f"Synthetic Data with DP (epsilon value is {data['epsilon']})"}</h2>
                <p>Energy consumed for generating synthetic data is {data['energy_synthesis']:.4f}J.</p>
                <h3> Privacy Risks </h3>
                {"".join(f"<p>{name} risk is {value * 100:.4f}%.</p>" for name, value in data['risks'].items())}
                
                <h3>KNN Details</h3>
                <p>Accuracy: {data['knn']['Accuracy']:.4f} (Max is 1)</p>
                <p>K-value: {data['knn']['K-value']:.4f}</p>
                <h3>Logistic Regression Details</h3>
                <p>Accuracy: {data['logres']['Accuracy']:.4f} (Maximum is 1)</p>
            </div>
            ''' for syn, data in items['results'].items())}
        </div>
    </body>
    </html>
    """

    with open(f'reports/{items["ID"]}_{items["input"]["OS"]}_report.html', 'w') as file:
        file.write(html_content)



#f
"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report for Iteration {items['ID']}</title>
        <style>
            .results-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr); /* 2 columns */
                gap: 20px;
            }}
            .data-section {{
                border: 1px solid #ccc;
                padding: 20px;
                background-color: #f8f8f8;
            }}
            .color-changer {{ 
                background-color: #249418;
                font-weight: bold; 
            }} 
        </style>
    </head>
    <body>
        <h1>Report for iteration {items['ID']}:</h1>
        <h2>User Input</h2>
        <p>The following input was provided:</p>
        <ul>
            <li>Filename that is used: {items['input']['Filename']}</li>
            <li>Operating System: {items['input']['OS']}</li>
            <li>Tool used for energy measurements: {items['input']['Tool']}</li>
            <li>Categorical attributes: {items['input']['Categorical attributes']}</li>
            <li>Continuous attributes: {items['input']['Continuous attributes']}</li>
            <li>Target attribute for ML: {items['input']['Target']}</li>
            <li>Possible known attributes to the attacker for risk measurements: {items['input']['Possible known attributes']}</li>
            <li>Secret attribute that attacker is trying to guess for Inference risk measurement: {items['input']['Secret attribute']}</li>
            <li>Number of records: {items['input']['Number of records']}</li>
            <li>Number of attributes: {items['input']['Number of attributes']}</li>

        </ul>
        <div class="results-grid">
            {"".join(f'''
            <div class="data-section">
                <h2>{"Synthetic Data without DP" if data["epsilon"] == 0 else f"Synthetic Data with DP (epsilon value is {data['epsilon']})"}</h2>
                <p>Energy consumed for generating synthetic data is {data['energy_synthesis']:.4f}J.</p>
                <h3> Privacy Risks </h3>
                {"".join(f"<p>{name} risk is {value * 100:.4f}%.</p>" for name, value in data['risks'].items())}
                
                <h3>KNN Details</h3>
                <p>Accuracy: {data['knn']['Accuracy']:.4f} (Max is 1)</p>
                <p>K-value: {data['knn']['K-value']:.4f}</p>
                <p>Energy used: {data['knn']['Energy']:.4f}J</p>
                <p>Total Energy with K-Nearest Neighbors used: {data['knn']['Total energy']:.4f}J</p>
                <h3>Logistic Regression Details</h3>
                <p>Accuracy: {data['logres']['Accuracy']:.4f} (Maximum is 1)</p>
                <p>Energy used: {data['logres']['Energy']:.4f}J</p>
                <p>Total Energy with Logistic Regression used: {data['logres']['Total energy']:.4f}J</p>
            </div>
            ''' for syn, data in items['results'].items())}
        </div>
    </body>
    </html>
    """


