from os import environ

bind = "0.0.0.0:5000"
errorlog = "-"
accesslog = "-"
name = "article12"
script_name = environ.get("SCRIPT_NAME", "")
worker_refresh_batch_size = 0
worker_class = "gevent"
