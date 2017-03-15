
LOG_FILE='/log'

def log(message):
    f = open(LOG_FILE, 'a')
    f.write(message)
    f.write("\n")
    f.close()

def log_exception(exc):
    f = open(LOG_FILE, 'a')
    sys.print_exception(exc, f)
    f.close()
