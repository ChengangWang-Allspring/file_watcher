class LogConfigError(Exception):
    pass

class JobConfigError(Exception):
    pass

class S3ConfigError(Exception):
    pass

class HolidayConfigError(Exception):
    pass


class FileWatchTimeOutError(Exception):
    pass

class FileWatchError(Exception):
    pass


LOGGING_YML = """
version: 1
disable_existing_loggers: true
formatters:
    simple:
        format: "%(asctime)s - %(levelname)s - %(message)s"
handlers:
  console:
    class: logging.StreamHandler
    level: INFO
    formatter: simple
    stream: ext://sys.stdout
  file:
    class: logging.FileHandler
    level: DEBUG
    formatter: simple
    filename: <to-be-defined-in-job-config>
loggers:
  fileWatchLogger:
    level: DEBUG
    handlers: [console]
    propagate: yes
root:
  level: DEBUG
  handlers: [console,file]
"""