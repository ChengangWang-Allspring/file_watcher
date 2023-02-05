REGEX_S3_URI: str = '^s3://([^/]+)/(.*?[^/]+/?)$'
REGEX_UNC: str = '^\\\\([a-zA-Z0-9_.$-]+\\[a-zA-Z0-9_.$-\\]+)$'
REGEX_LOCAL: str = ''

LOGGING_YML = """
version: 1
disable_existing_loggers: true
formatters:
    simple:
        format: '%(asctime)s - %(levelname)s - %(message)s'
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
    filename: <job-name_YYYYMMDD.log> 
loggers:
  fileWatchLogger:
    level: DEBUG
    handlers: [console]
    propagate: yes
root:
  level: DEBUG
  handlers: [console,file]
"""
