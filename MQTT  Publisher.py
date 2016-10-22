import os
import logging
import sys
import getopt
import paho.mqtt.publish as publish
from ConfigParser import SafeConfigParser

log = None

def initLogger(name):
    global log
    logging.basicConfig(filename=os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + "/" + name + ".log"), level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    log = logging.getLogger(__name__)
    soh = logging.StreamHandler(sys.stdout)
    soh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.addHandler(soh)
    log.setLevel(logging.DEBUG)

def main(argv):
    initLogger("MQTT Publisher")
    log.info("Initializing MQTT Publisher...")

    try:
        opts, args = getopt.getopt(argv, "h:", ["Config=", "Topic=", "Message="])
    except getopt.GetoptError:
        print("MQTTPublish.py -h --Config --Topic --Message")
        sys.exit(1)


    for opt, arg in opts:
        if opt in '-h':
            print("MQTTPublish.py -h --Config --Topic --Message")
            sys.exit(2)
        elif (opt == "--Config"):
            configFile = arg
        elif (opt == "--Topic"):
            topic = arg
        elif (opt == "--Message"):
            message = arg

    cfg = SafeConfigParser(
            {"client_id": "smappee-mqtt-" + str(os.getpid()), "hostname": "localhost", "port": "1883", "auth": "False",
             "retain": "False", "qos": "0"})
    cfg.optionxform = str
    cfg.read(configFile)
    client_id = cfg.get("mqtt", "client_id")
    host = cfg.get("mqtt", "hostname")
    port = eval(cfg.get("mqtt", "port"))
    qos = eval(cfg.get("mqtt", "qos"))
    retain = eval(cfg.get("mqtt", "retain"))
    if eval(cfg.get("mqtt", "auth")):
        auth = {"username": cfg.get("mqtt", "user"), "password": cfg.get("mqtt", "password")}
    else:
        auth = None

    log.info("Connecting to MQTT Broker on " + host + " port " + str(port))

    msgs = [{"topic": topic, "payload": message, "qos": qos, "retain": retain}]

    log.debug("msgs = " + str(msgs))

    publish.multiple(msgs, hostname=host, port=port, client_id=client_id, auth=auth)

main(sys.argv[1:])