import json
from b_e.config import config


class ActionLogger(object):
    def __init__(self, config=None, logger=None):
        self.logger = None
        self.action_log_default_actor = None
        self.enable = None
        if config is not None and logger is not None:
            self.init_app(config, logger)

    def init_app(self, config, logger):
        self.logger = logger
        self.enable = config.get("ACTION_LOG_ENABLED", True)
        self.action_log_default_actor = config.get("ACTION_LOG_DEFAULT_ACTOR", "action_logger")

    def bin_data(self, kwargs, request):
        record = {}
        record.update(kwargs)

        record['System'] = config.get('SYSTEM')
        if request:
            record['ClientIP'] = request.client.host
            record['IpPortCurrentNode'] = request.scope['server']
        # record['IPPortCurrentNode'] = request
        for key in record:
            data = record[key]
            if isinstance(data, int) or isinstance(data, str) or isinstance(data, bool):
                continue
            if isinstance(data, list):
                for i in range(0, len(record[key])):
                    if isinstance(record[key][i], int) or isinstance(record[key][i], str) or isinstance(record[key][i],
                                                                                                        bool):
                        continue
                    record[key][i] = str(record[key][i]).replace("\n", "").replace("\r", "")
            elif isinstance(data, dict):
                try:
                    record[key] = json.dumps(record[key])
                except Exception as e:
                    record[key] = str(record[key]).replace("\n", "").replace("\r", "")
            else:
                record[key] = str(record[key]).replace("\n", "").replace("\r", "")
        return record

    def info_log(self, action, request, **kwargs):
        """
        Log action by actor
        """
        record = {}
        record.update(kwargs)
        try:
            if self.enable:
                record['ActionType'] = action
                record = self.bin_data(record, request)
                with open(f"{config['LOG_FILE']}/logs.txt", 'a') as log_file:
                    log_file.write("\n")
                    log_file.write(json.dumps(record))
                    log_file.close()
        except Exception as ex:
            with open(f"{config['LOG_FILE']}/logs.txt", 'a') as log_file:
                log_file.write("\n")
                log_file.write('Error log action {0}: {1}'.format(record, ex))
                log_file.close()

    def info_log_service(self, action, **kwargs):
        """
        Log action by actor
        """
        record = {}
        record.update(kwargs)
        try:
            if self.enable:
                record['ActionType'] = action
                record = self.bin_data(record, request=None)
                with open(f"{config['LOG_FILE']}/logs.txt", 'a') as log_file:
                    log_file.write("\n")
                    log_file.write(json.dumps(record))
                    log_file.close()
        except Exception as ex:
            with open(f"{config['LOG_FILE']}/logs.txt", 'a') as log_file:
                log_file.write("\n")
                log_file.write('Error log action {0}: {1}'.format(record, ex))
                log_file.close()

    def info_log_send_mail(self, action, request, **kwargs):
        """
        Log send mail by actor
        """
        record = {}
        record.update(kwargs)
        try:
            if self.enable:
                record['ActionType'] = action
                record = self.bin_data(record, request)
                with open(f"{config['LOG_FILE']}/logs_send_mail.txt", 'a') as log_file:
                    log_file.write("\n")
                    log_file.write(json.dumps(record))
                    log_file.close()
        except Exception as ex:
            with open(f"{config['LOG_FILE']}/logs_send_mail.txt", 'a') as log_file:
                log_file.write("\n")
                log_file.write('Error log action {0}: {1}'.format(record, ex))
                log_file.close()