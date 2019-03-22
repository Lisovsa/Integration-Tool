*** Settings ***
Suite Setup       Initialize Test Suite
Test Setup        DEFAULT SETUP
Library           C:/Robot Framework/libraries/DataModelControl.py
Library           C:/Robot Framework/libraries/InfusionReportsVer.py
Library           C:/Robot Framework/libraries/KeypressControl.py
Library           C:/Robot Framework/libraries/MedleyUIVer.py
Library           C:/Robot Framework/libraries/PcuUtilitiesControl.py
Library           C:/Robot Framework/libraries/RemoteOrdersControl.py
Library           C:/Robot Framework/libraries/TestVer.py
Library           C:/Robot Framework/libraries/UIInfoControl.py
Resource          C:/Robot Framework/resource/RF files/BD8_Regression_resource.robot
Library           C:/Robot Framework/Python27/Lib/site-packages/robot/libraries/OperatingSystem.py
Library           C:/Robot Framework/Python27/Lib/site-packages/robot/libraries/DateTime.py
Library           C:/Robot Framework/Python27/Lib/site-packages/robot/libraries/String.py

*** Variables ***
${path}           ${EMPTY}

*** Test Cases ***
Set path
    [Documentation]    Set the path for the output file where all downloaded logs will be stored.
    ${current_date}    Get Current Date
    ${date}=    Convert Date    ${current_date}    result_format=%d%m%Y%H%M
    # Specify file_path: type in the path to the folder where you would like to see tests results, but leave file name "PCU_logs_{}.txt" unchaged.
    ${file_path}=    Replace String    C:/Robot Framework/Output/PCU_logs_{}.txt    {}    ${date}
    Set Suite Variable    ${path}    ${file_path}

Battery/Error/Event Logs
    [Documentation]    Download Battery/Error/Event Logs.
    ${battery_logs}=    Log Download    BATTERY
    ${error_logs}=    Log Download    ERROR
    ${event_logs}=    Log Download    EVENT
    Append To File    ${path}    ${battery_logs}
    Append To File    ${path}    '\n\n'
    Append To File    ${path}    ${error_logs}
    Append To File    ${path}    '\n\n'
    Append To File    ${path}    ${event_logs}
    Append To File    ${path}    '\n\n'

CQI Logs
    [Documentation]    Download CQI Logs.
    ${cqi_logs}=    CQI Log Request
    Append To File    ${path}    ${cqi_logs}
    Append To File    ${path}    '\n\n'

Historical Logs
    [Documentation]    Download Historical Logs.
    ...
    ...    Historical Logs usually are very large so Current sequence number of Historical logs is stored in a separate file and used for second call of Historical logs in order to collect only relevant logs.
    ${status}=    Run Keyword And Return Status    File Should Exist    C:/Robot Framework/Output/Current_sequence.txt
    ${current_number}=    Current Sequence Number
    ${sequence_number}=    Run Keyword If    ${status}    Get Binary File    C:/Robot Framework/Output/Current_sequence.txt
    ${historical_logs_rest}=    Run Keyword If    ${status} and ${current_number} > ${sequence_number}    Historical Logs    ${sequence_number}
    ${historical_logs_all}=    Run Keyword If    not ${status} or ${current_number} <= ${sequence_number}    Historical Logs    0
    Run Keyword If    '${historical_logs_rest}' != 'None'    Append To File    ${path}    ${historical_logs_rest}
    Run Keyword If    '${historical_logs_all}' != 'None'    Append To File    ${path}    ${historical_logs_all}
    # Remember current sequence number
    Remove File    C:/Robot Framework/Output/Current_sequence.txt
    Append To File    C:/Robot Framework/Output/Current_sequence.txt    ${current_number}

*** Keywords ***
Initialize Test Suite
    Load From    C:\\Robot Framework\\Resource\\RF Files\\startup_values.xml
    Load from    C:\\Robot Framework\\resource\\RF files\\log_entries.xml
    Connect To Pump
    DEFAULT CONFIGURATION    02181c6ef-R
