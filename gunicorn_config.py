from os import environ

bind = "0.0.0.0:5000"
errorlog = "-"
accesslog = "-"
name = "article12"
script_name = environ.get("SCRIPT_NAME", "")
worker_refresh_batch_size = 0
worker_class = "gevent"
lmit_request_line = 0
limit_request_fields = 1000
limit_request_field_size = 0
