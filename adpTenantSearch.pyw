import FreeSimpleGUI as sg
import webbrowser
import re
import os
import time

headers=['Tenant', 'Client Name', 'Entity']
rows=[]

layout = [
    [sg.Text("Search Criteria:"), sg.Input(key='-SEARCH_VALUE-')],
    [sg.Text('Tenant: '), sg.Text(key='tenant')],
    [sg.Text('Client: '), sg.Text(key='client')],
    [sg.Button('Search'), sg.Button('Open')],
    [sg.Table(values=[], headings=['Tenant', 'Client Name', 'Entity'], key='-SEARCHRESULTS-', justification='center', enable_click_events=True, expand_x=True, enable_events=False, num_rows=15, visible=False)]


]

window = sg.Window('ADP Tenant Search', layout)

design_artifacts = {
    'BTP_ADP_US1': 'https://adp-production-us-1-vmdabemk.integrationsuite.cfapps.us10-002.hana.ondemand.com/shell/design/contentpackage/',
    'BTP_ADP_US2': 'https://adp-production-us-2-hdjy1adt.integrationsuite.cfapps.us10-002.hana.ondemand.com/shell/design/contentpackage/',
    'BTP_ADP_US3': 'https://adp-production-us-3-3nbvenke.it-cpi019.cfapps.us10-002.hana.ondemand.com/itspaces/shell/design/contentpackage/',
    'BTP_ADP_US4': 'https://adp-production-us-4-ueg7o2ub.integrationsuite.cfapps.us10-002.hana.ondemand.com/shell/design/contentpackage/'
    }

def urlFormat(string):
    formatted = re.sub('[^A-Za-z0-9]+', '', string)
    return formatted

selected = []

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    if event == 'Search' :
        search_value = values['-SEARCH_VALUE-']
        window['tenant'].update('')
        window['client'].update('')
        window['-SEARCHRESULTS-'].update(values=[], visible=False)
    #    search_file = window['-SEARCHFILE-'].get()
        if os.path.exists('./ADP Packages.txt') != True:
            sg.popup('Unable to find ADP Packages file')
        else:
            search_file = os.getcwd() + '/ADP Packages.txt'
            result = []
            new_rows = []
            with open(search_file, 'r') as file:
                packages = file.readlines()
                for package in packages:
                    if search_value.lower() in package.lower():
                        temp = package.strip()
                        result.append(temp.split(','))


            if len(result) > 1:
                for x in result:
                    temp_package = re.sub(r'(ADPWFN|ADPVantage)','',x[2]).replace(x[1], '')
                    temp_tenant = x[3].replace('BTP_ADP_', '')
                    new_rows.append([temp_tenant, temp_package, x[1]])
                window['-SEARCHRESULTS-'].update(values=new_rows, visible=True)
            elif len(result) == 1 :
                selected = result[0]
                window['tenant'].update(selected[3].replace('BTP_ADP_', ''))
                window['client'].update(re.sub(r'(ADPWFN|ADPVantage)','',selected[2].strip()).replace(selected[1], '') + ' - ' + selected[1])
                window['-SEARCHRESULTS-'].update(values=new_rows, visible=False)
            else:
                sg.popup("Client not found!")
    
    if '+CLICKED+' in event:
        if((event[2][0] != None) & (event[2][1] != None)):
            selected = result[event[2][0]]
            window['tenant'].update(selected[3].replace('BTP_ADP_', ''))
            window['client'].update(re.sub(r'(ADPWFN|ADPVantage)','',selected[2].strip()).replace(selected[1], '') + ' - ' + selected[1])


    if event == 'Open':
        if (window['tenant'].get() != '') & (selected != []):
            webbrowser.open(design_artifacts[selected[3]] + urlFormat(selected[2]) + '?section=ARTIFACTS')
        #    time.sleep(10)
        #    webbrowser.open(design_artifacts[selected[3]] + 'monitoring/Overview')
        else:
            sg.popup("Please search/select for a client!")
        
window.close()
        