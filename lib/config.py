from ConfigParser import SafeConfigParser
import threading
import os
import time
import lib.utils as utils


class CheckConfigFileModification(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self._cached_stamp_core = 0
        self._cached_stamp_user = 0
        self.core_conf_file = 'config.ini'
        self.user_conf_file = 'html/user_config.ini'

    def run(self):
        global homenet
        global lock

        counter = 0
        while 1:
            flag = False
            stamp = os.stat(self.core_conf_file).st_mtime
            if stamp != self._cached_stamp_core:
                flag = True
                self._cached_stamp_core = stamp
                # Reading core configuration file
                core_config = SafeConfigParser()
                core_config.read('config.ini')

                # main section
                with lock:
                    homenet.interface = core_config.get('main', 'iface')
                    homenet.vt_api_domain_url = core_config.get('virustotal', 'vt_api_domain_url')
                    homenet.vt_api_ip_url = core_config.get('virustotal', 'vt_api_ip_url')
                    homenet.vt_api_file_url = core_config.get('virustotal', 'vt_api_file_url')

            stamp = os.stat(self.user_conf_file).st_mtime
            if stamp != self._cached_stamp_user:
                flag = True
                self._cached_stamp_user = stamp
                # Reading user configuration file
                user_config = SafeConfigParser()
                user_config.read('html/user_config.ini')

                # main section
                homenet.dst_emails = (user_config.get('main', 'dst_emails').translate(None, '"\n\r ')).split(",")
                homenet.vt_api_key = user_config.get('main', 'vt_api_key').translate(None, '"\n\r ')
                homenet.blacklist = (user_config.get('main', 'blacklist').translate(None, '"\n\r ')).split(",")
                homenet.whitelist = (user_config.get('main', 'whitelist').translate(None, '"\n\r ')).split(",")

            if flag:
                counter += 1

            if counter > 1:
                utils.kill_falcongate(homenet.pid)

            time.sleep(5)
