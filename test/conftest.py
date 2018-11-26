from os import environ
from pathlib import Path
from subprocess import Popen, PIPE

from pytest import fixture
from pprintpp import pprint


@fixture(scope='session')
def dashboard():

    root = Path(__file__).resolve().parent.parent

    print('Environment:')
    pprint(dict(environ))

    # FIXME: Allow to fetch stdout and stderr of the terminal emulator command
    command = [
        '/usr/bin/xterm',
        '-fa', 'Monospace',
        '-fs', '10',
        '-geometry', '80x48',
        '-e', 'cd {} && {}'.format(
            root,
            root / 'test' / 'dashboard.sh',
        )
    ]
    print('Command:')
    print(' '.join(command))

    dashboard = Popen(
        command,
        env=dict(environ),
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
    )
    print(
        'Spawn subprocess PID {} with dashboard ...'.format(
            dashboard.pid
        )
    )

    # FIXME: Poll for TCP socket
    from time import sleep
    sleep(5)

    yield dashboard

    dashboard.kill()
    print(
        'Waiting for dashboard terminal PID {} to finish ... '
        'Timeout 15 seconds ...'.format(
            dashboard.pid,
        )
    )

    dashboard.wait(timeout=15)

    # NOTE:
    #     Useless as the output of the command is not shown in the stdout of
    #     the terminal emulator.
    #
    # stdout, stderr = dashboard.communicate(timeout=15)
    # print('Standard output:\n'.format(
    #     stdout.decode('utf-8'))
    # )
    # print('Standard error:\n'.format(
    #     stderr.decode('utf-8'))
    # )

    print(
        'Terminal emulator returned code {} ...'.format(
            dashboard.returncode,
        )
    )

    logfile = root / '.tox' / 'test' / 'tmp' / 'coral.log'
    if logfile.is_file():
        print('Log file at {} :'.format(logfile))
        print(logfile.read_text(encoding='utf-8'))
    else:
        print('No logfile found!')
