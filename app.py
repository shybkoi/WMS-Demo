# -*- coding: cp1251 -*-

import pprint
pPrinter = pprint.PrettyPrinter(indent=1) #before importing cp_utils

mappings = None #объект, инкапсулирующий маппинг

def init(basepath):
    "initialization of web-server"

    global mappings
    import hot_conf as hc
    import conf.engine_conf as cfg
    import db
    import cp_utils as cpu
    import py_utils as pu
    import system_init as si
    import api.version as version

    server = cpu.init_server(basepath=basepath)

    print "\n    FirePy Engine v. " + version.get_full_version()
    print

    print "\nInit hot config..."
    print
    hc.init_hot_conf(cfg.hot_conf_location)

    print "\nInit database engine..."
    print

    db.init()

    print "\nReading db version..."
    (version_from_db, date_from_db) = version.get_version_from_db()
    db_version_matched = version.check_db_versions(version_from_db)
    print "\n    Db v. %s %s %s" % (version_from_db, pu.convToConsole('from'), date_from_db) + pu.iif(db_version_matched, '   ...OK', '   ...MISMATCH!!!')

    if not db_version_matched:
        print "\nWARNING!!! Db version mismatch!!! Expected %s, really %s" % (version.accepted_db_version, version.extract_major_minor_db_version(version_from_db))
        print

    # проверка, правильно ли установлены параметры запуска веб-сервера
    server.check_config()

    print
    print "\nReading engine params..."
    print

    si.read_engine_params()

    print
    print "\nReading bases params..."
    print

    si.read_bases_params()

    print
    print "\nReading systems params..."
    print

    si.read_systems_params()

    print
    print "\nMapping of a tree..."
    print

    mappings = si.Mappings(basepath,
        pu.iif('/' in cfg.error_log_file or '\\' in cfg.error_log_file,
          cfg.error_log_file,
          basepath + '/log/' + cfg.error_log_file))
    root, cntSystems, cntSuccessSystems = mappings.mapAll()

    print
    print "TOTAL: %s of %s systems are mounted successfully." % (cntSuccessSystems, cntSystems)

    #Close Main Thread connection to db
    db.main_th_connect_close()

    print
    print "\nStarting webserver..."
    print

    #may be 2 servers on different ports
    if cfg.server1:
        print "Server #1 starts at %s://%s:%s" % (cfg.server1, cfg.socket_host1, cfg.socket_port1)

    if cfg.server2:
        print "Server #2 starts at %s://%s:%s" % (cfg.server2, cfg.socket_host2, cfg.socket_port2)

    server.start(root)
