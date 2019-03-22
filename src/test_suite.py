import os
import shutil
import subprocess
import sys

from datetime import datetime

class TestSuite(object):
    """Creates Test Suite object."""
    def __init__(self, name, config):
        self.name = name
        self.log_test = config.log_test
        self.path = config.path
        self.output_path = config.output_path
        self.console_redirect = config.console_redirect
        self.output_dir_path = '{0}\{1}_output'.format(self.output_path, name)

    def process_tests(self):
        """Runs test suites."""
        try:
            self._create_paths()
            logfile = self._create_logfile()

            if self.name == self.log_test.replace('.robot', ''):
                status = self._process_logs_download(logfile)
            else:
                status = self._process_test_suite(logfile)

            self._check_for_errors(status)

        except Exception as e:
            sys.stderr.write(e)

    def _create_paths(self):
        """Prepares directories for tests output.'"""

        # Copying the file 'PCU_logs.robot' to the folder with test suites.
        if not os.path.exists('\\'.join([self.path, self.log_test])):
            shutil.copy(self.log_test, self.path)

        # Moving to test suites directory
        os.chdir(self.path)

        # Create a directory for the test suite
        if not os.path.exists(self.output_dir_path):
            os.makedirs(self.output_dir_path)

    def _create_logfile(self):
        """Creates a file for console output if console redirection is chosen."""
        if not self.console_redirect:
            return None

        # PCU_logs.robot need a timestamp for console logs as can be run several times
        if self.name == self.log_test.replace('.robot', ''):
            return open('{0}\{1}_console_log_{2}'.format(
                self.output_dir_path, self.name, datetime.now().strftime("%m%d%H%M")), "w+")
        else:
            return open('{0}\{1}_console_log'.format(self.output_dir_path, self.name), "w+")

    def _process_logs_download(self, logfile):
        """Creates a command for the PCU download test suite and runs the test suite.
        The execution results are stored in 'C:\Robot Framework\Output\PCU_logs' folder.
        """

        print 'Downloading PCU logs'
        command = 'robot --outputdir "C:\Robot Framework\Output\PCU_logs" {}.robot'.format(self.name)

        return self._run_command(command, logfile)

    def _process_test_suite(self, logfile):
        """Creates a command for test suite execution and runs the test suite."""

        print '***' * 10
        print 'Output will be generated in folder {}\n'.format(self.output_dir_path)

        command = 'robot --outputdir {0} -r {1}_report.html -l {1}_log.html -o {1}_output.xml {1}.robot'.format(
                self.output_dir_path, self.name)

        return self._run_command(command, logfile)

    @staticmethod
    def _run_command(cmd, logfile=None):
        return subprocess.call(cmd, shell=True, stdout=logfile)

    def _check_for_errors(self, status):
        """Checking status for errors."""

        # Case when test suite name is misspelled or file doesn't exist
        if status == 252:
            sys.stderr.write('Test suite "{}" was not found in path {}\n'.format(self.name, self.path))
        print 'Return code is {}'.format(status)
