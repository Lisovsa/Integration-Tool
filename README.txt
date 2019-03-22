Tool to support continuous integration for automated test suites.
Version 1.0.

Runs test suites and creates zip output.
After running the tests, downloads the logs from PCU.

Before running the tool, edit the configuration file: src/config.yml

Please specify:
- test suites to run (suites_list)
- path to find tests (test_suites_path)
- desired path for the output (output_path)
- console_redirect 

console_redirect: set this parameter to 'true' to redirect the console log
to file '<Test_name>_console_log.txt'. The file will appear in the output folder for each test suite.
When set to 'false', console log will appear in console window.

Go to src folder to find PCU_logs.robot.
Open the test suite and change the path in scalar variable 'logOutputPath'.
Set path to the folder where you would like to get the tests results.
Refer to "Integration_Tool_Tutorial" for further information.

Run 'start.bat' file from Windows Prompt(cmd).

In case you would like to create several configuration files,
you can run the tool with -c parameter and set the path to the config file you need to use.
By default, src/config.yml is used as a configuration file. 

Example of command when configuration file is defined by user:

start.bat -c C:\work\tests\config.yml

Note: The tool needs established cable connection with the PCU,
but Connect to Pump will be executed by the test suite.