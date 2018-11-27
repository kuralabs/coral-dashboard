from shutil import which
from pathlib import Path
from time import time, sleep
from os import environ, chmod
from contextlib import closing
from subprocess import Popen, PIPE
from logging import getLogger as get_logger
from socket import socket, AF_INET, SOCK_STREAM

from pytest import fixture
from pprintpp import pformat


log = get_logger(__name__)


BOOTSTRAP_SCRIPT_TPL = """\
#!/usr/bin/env bash

set -o errexit

echo "Executing dashboard.sh script ..."
source {root}/.tox/test/bin/activate
cd {workdir}
python3 -m coral_dashboard -vvv --port {port} --log {logfile}
"""


class Dashboard:
    def __init__(self, port=None, logfile='coral.log'):

        self.root = Path(__file__).resolve().parent.parent
        self.port = port or self._find_free_tcp_port()
        self.workdir = Path.cwd()
        self.logfile = logfile

        self._bootstrap = self.workdir / 'bootstrap.sh'
        self._logs = self.workdir / logfile

        self._process = None

        # Log basic information
        log.info('Project root: {}'.format(
            self.root,
        ))

        log.info('Environment:\n{}'.format(
            pformat(dict(environ)),
        ))

    def _find_free_tcp_port(self):
        with closing(socket(AF_INET, SOCK_STREAM)) as sock:
            sock.bind(('', 0))
            addr, port = sock.getsockname()
        return port

    def _server_is_listening(self):
        with closing(socket(AF_INET, SOCK_STREAM)) as sock:
            return sock.connect_ex(('localhost', self.port)) == 0

    def is_alive(self):
        return self._process.poll() is None

    def start(self):

        # Find xterm before trying anything
        xterm = which('xterm')
        if xterm is None:
            raise RuntimeError('Unable to find xterm')

        # Create bootstrap script
        self._bootstrap.write_text(
            BOOTSTRAP_SCRIPT_TPL.format(
                root=self.root,
                workdir=self.workdir,
                port=self.port,
                logfile=self.logfile,
            ),
            encoding='utf-8',
        )
        chmod(str(self._bootstrap), 0o775)

        # Spawn subprocess
        command = [
            xterm,
            '-fa', 'Monospace',
            '-fs', '10',
            '-geometry', '80x48',
            '-e', '{} || read'.format(self._bootstrap)
        ]

        log.info('Command: {}'.format(' '.join(command)))
        process = Popen(command, env=dict(environ), stdout=PIPE, stderr=PIPE)
        log.info(
            'Spawn dashboard subprocess with PID {} ...'.format(
                process.pid
            )
        )
        self._process = process

    def wait_ready(self):
        assert self._process is not None

        log.info('Waiting for dashboard to be ready ...')

        start = time()
        while (time() - start < 20) and self.is_alive():
            if self._server_is_listening():
                log.info(
                    'Dashboard up and ready at port {}'.format(self.port)
                )
                return
            sleep(0.5)

        self.wait_done()
        self.show_logs()
        raise RuntimeError(
            'Dashboard didn\'t started after {:.2f} seconds. '
            'Current return code: {}'.format(
                time() - start,
                self._process.poll(),
            )
        )

    def wait_done(self):
        assert self._process is not None

        if self.is_alive():
            log.info(
                'Waiting for dashboard terminal PID {} to finish ... '
                'Timeout 15 seconds ...'.format(
                    self._process.pid,
                )
            )
            self._process.kill()
            self._process.wait(timeout=15)

        # Log terminal emulator stdout and stderr
        # These are usually empty
        stdout, stderr = (
            stream.decode('utf-8')
            for stream in self._process.communicate(timeout=15)
        )
        for name, stream in [
            ('stdout', stdout),
            ('stderr', stderr),
        ]:
            if stream:
                log.info('Terminal emulator {}:\n{}'.format(
                    name, stream,
                ))
                continue
            log.info(
                'As expected, terminal emulator didn\'t '
                'reported any {}'.format(name)
            )

        log.info(
            'Terminal emulator returned code {} ...'.format(
                self._process.poll(),
            )
        )

    def show_logs(self):
        if self._logs.is_file():
            log.info('Log file at {} :\n{}'.format(
                self._logs,
                self._logs.read_text(encoding='utf-8'),
            ))
        else:
            log.info('No logfile found!')


@fixture(scope='session')
def dashboard():

    # Create user facing object
    dashboard = Dashboard()
    dashboard.start()
    dashboard.wait_ready()

    # Pass dashboard to user
    yield dashboard

    # Wait until terminal is closed
    dashboard.wait_done()
    dashboard.show_logs()
