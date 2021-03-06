from __future__ import print_function

import paho.mqtt.client as mqtt
import flow, gadgets
import json

SERVICE_PREFIX = "s/pyf-demo"
REGISTRY_TOPIC = "registry-" + SERVICE_PREFIX

circuits = {}
client = None

class ConnectedCircuit(flow.Circuit):
    def __init__(self, name):
        flow.Circuit.__init__(self)
        self.name = name
        circuits[name] = self

    def subscriptions(self):
        return [("%s/%s" % (SERVICE_PREFIX, self.name), 0),
                ("%s/%s/in/+" % (SERVICE_PREFIX, self.name), 0)]

    def control(self, msg):
        print("CONTROL:", self.name, msg)
        for ctrl in msg:
            assert(isinstance(ctrl, list) and len(ctrl) > 0)
            if isinstance(ctrl[0], int):
                self.wire(*ctrl)
            else:
                self.add(*ctrl)

    def emit(self, onum, msg):
        topic = "%s/%s/out/%d" % (SERVICE_PREFIX, self.name, onum)
        client.publish(topic, json.dumps(str(msg)))

def on_connect(client, userdata, flags, rc):
    print("Connected: code", rc)
    subs = [(SERVICE_PREFIX, 0)]
    for name in circuits:
        subs += circuits[name].subscriptions()
    client.subscribe(subs)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
        if msg.topic == SERVICE_PREFIX:
            print("CMD:", payload)
            assert(len(payload) == 2 and payload[0] == "create")
            name = payload[1]
            exists = name in circuits
            cob = ConnectedCircuit(name)
            if not exists:
                client.subscribe(cob.subscriptions())
        else:
            topic = msg.topic[len(SERVICE_PREFIX)+1:]
            parts = topic.split('/')
            cob = circuits[parts[0]]
            if len(parts) == 1:
                cob.control(payload)
            else:
                assert(len(parts) == 3 and parts[1] == 'in')
                cob.feed(int(parts[2]), payload)
    except Exception as e:
        if str(e) == '':
            e = 'error'
        print(e, (msg.topic, msg.payload))

# loop back test circuit: print msgs from inlet 0 and pass them to outlet 0
c = ConnectedCircuit('loop')
c.add('inlet')
c.add('pass')
c.add('print', 'got:')
c.add('outlet')
c.wire(0, 0, 1, 0)
c.wire(1, 0, 2, 0)
c.wire(1, 0, 3, 0)

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message
client.will_set(REGISTRY_TOPIC, retain=True)
client.connect("localhost")
client.publish(REGISTRY_TOPIC, json.dumps({}), retain=True)

client.loop_forever()
