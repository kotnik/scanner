

def do_analyze(hosts, host_info):
    failures = {}
    for host, data in host_info.iteritems():
        for vuln, result in data.iteritems():
            if vuln == "ssl checked":
                continue
            if not result:
                continue
            if vuln == "POODLE":
                if data.get("TLS_FALLBACK_SCSV", None):
                    continue

            if not failures.get(vuln, None):
                failures[vuln] = []
            failures[vuln].append(host)

    print "{:20} {:>5}".format("Checked sites", len(hosts))

    for typ in ["SSL missing", "RC4", "FREAK", "Heartbleed", "Forward Secrecy", "POODLE"]:
        if typ in failures:
            percentage = float(len(failures[typ])) * 100 / len(hosts)
            print "{:20} {:>5} ({:.2f}%)".format(typ, len(failures[typ]), percentage)
