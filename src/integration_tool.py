import shutil
import sys
from config import create_config
from test_suite import TestSuite


def run_tool(conf):
    """
    Runs the regression test suits, zips the output folder.
    """
    # Creating a list of suites to run
    test_suites = [TestSuite(test, conf) for test in conf.tests]

    # Launching test suites
    try:
        for index, suite in enumerate(test_suites, start=1):
            print '\nStarting Test Suite {0}: {1}...\n'.format(index, suite.name)
            suite.process_tests()
    except Exception as e:
        sys.stderr.write('Failed to run tests: {}'.format(e))
        sys.exit(1)

    # Zipping results
    print('Zipping all test results...\n')
    try:
        shutil.make_archive('Tests_results', 'zip', base_dir=config.output_path.split('\\')[-1])
        shutil.rmtree(config.output_path)

    except Exception as e:
        sys.stderr.write('Error: {}'.format(e))
        sys.exit(1)


if __name__ == '__main__':
    config = create_config(sys.argv[1:])
    if not config:
        sys.exit(1)

    run_tool(config)
