# healthcheck.py -- exits with an error if /health does not answer
import urllib.request
urllib.request.urlopen("http://localhost:8000/health", timeout=2)
