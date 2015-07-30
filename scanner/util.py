import time
import uuid
import subprocess
import logging


log = logging.getLogger(__name__)


def check_call(*args, **kwargs):
    start = time.time()
    command_uuid = uuid.uuid4()
    command_line = subprocess.list2cmdline(args[0])
    log.debug("%s: Executing: %s" % (command_uuid, command_line))

    data = None
    if "data" in kwargs:
        data = kwargs["data"]
        del(kwargs["data"])

    kwargs.setdefault("close_fds", True)

    proc = subprocess.Popen(
        *args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
        stderr=subprocess.PIPE, **kwargs
    )
    (stdout_data, stderr_data) = proc.communicate(input=data)

    if stdout_data.strip():
        log.debug("OUT: %s" % stdout_data.strip().replace('\n', ' -- '))
    if stderr_data.strip():
        log.debug("ERR: %s" % stderr_data.strip().replace('\n', ' -- '))

    log.debug("%s: %s: [code=%s, duration=%.1fs]" % (command_uuid, command_line, proc.returncode, time.time() - start))

    if proc.returncode != 0:
        return stderr_data.strip()

    return stdout_data.strip()
