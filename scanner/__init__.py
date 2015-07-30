from gevent import monkey; monkey.patch_all(subprocess=True)

import os
import re
import argparse

import gevent
from gevent.event import AsyncResult
from gevent.pool import Pool
from yapsy.PluginManager import PluginManager

from analyze import do_analyze

import logging

log = logging.getLogger(__name__)


def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--list", "-l", required=True, help="file with domain list",
    )
    parser.add_argument(
        "--debug", "-d", default=False, action="store_true",
    )
    options = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    if options.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Get the check plugins.
    checks = PluginManager()
    checks.setPluginPlaces([
        os.path.join(os.path.dirname(__file__), "checks")
    ])
    checks.collectPlugins()

    for plugin in checks.getAllPlugins():
        plugin.plugin_object.description()

    hosts = set([])
    with open(options.list) as hosts_file:
        for host in hosts_file:
            hosts.add(host.rstrip('\r\n'))

    # Cleanup.
    for host in hosts.copy():
        # Skip comments.
        if (re.search('^\s*#', host)):
            hosts.remove(host)
            continue
        if (re.search('^\s*https://', host)):
            host = re.sub('^\s*https://', '', host)
        elif (re.search('^\s*http://', host)):
            host = re.sub('^\s*http://', '', host)
        elif (re.search(r'//', host)):
            print "Invalid host {}".format(host)
            hosts.remove(host)

    def run_test(plugin, host, host_info):
        result = plugin.plugin_object.check(host, host_info=host_info)
        if result is True:
            log.debug("{} detected: {}".format(host, plugin.plugin_object.description()))

    # Run tests.
    pool = Pool(10)
    jobs = []
    host_info = {}

    for host in hosts:
        host_info[host] = {}
        host_info[host]["ssl checked"] = AsyncResult()
        for plugin in checks.getAllPlugins():
            jobs.append(pool.spawn(run_test, plugin, host, host_info[host]))

    gevent.joinall(jobs)

    do_analyze(hosts, host_info)
