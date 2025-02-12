# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=unused-argument,no-self-use


import ssl
import os
import six

from time import time, sleep
from paho.mqtt import client as mqtt

from azext_iot._constants import EXTENSION_ROOT
from azext_iot.common.sas_token_auth import SasTokenAuthentication

connection_result = {0: "success", 1: "refused - incorrect protocol version", 2: "refused - invalid client id",
                     3: "refused - server unavailable", 4: "refused - bad username or password", 5: "refused - not authorized"}


class mqtt_client_wrap(object):

    def __init__(self, target, device_id):
        self.target = target
        self.device_id = device_id

        sas = SasTokenAuthentication(target['entity'], target['policy'], target['primarykey'], time() + 360).generate_sas_token()
        cwd = EXTENSION_ROOT
        cert_path = os.path.join(cwd, 'digicert.pem')
        auth = {'username': '{}/{}/api-version=2016-11-14'.format(target['entity'], device_id), 'password': sas}
        tls = {'ca_certs': cert_path, 'tls_version': ssl.PROTOCOL_SSLv23}
        self.topic_publish = 'devices/{}/messages/events/'.format(device_id)
        self.topic_receive = 'devices/{}/messages/devicebound/#'.format(device_id)
        self.connected = False

        self.client = mqtt.Client(protocol=mqtt.MQTTv311, client_id=device_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.tls_set(ca_certs=tls['ca_certs'], tls_version=tls['tls_version'])
        self.client.username_pw_set(username=auth['username'], password=sas)
        self.client.connect(host=self.target['entity'], port=8883)

    def on_connect(self, client, userdata, flags, rc):
        six.print_("Connected to target IoT Hub MQTT broker with result: {}".format(connection_result[rc]))
        self.client.subscribe(self.topic_receive)
        six.print_("Subscribed to device bound message queue")
        self.connected = True

    def on_message(self, client, userdata, msg):
        six.print_()
        six.print_("_Received C2D message with topic_: {}".format(msg.topic))
        six.print_("_Payload_: {}".format(msg.payload))

    def on_publish(self, client, userdata, mid):
        six.print_('.', end='', flush=True)

    def is_connected(self):
        return self.connected

    def execute(self, data, publish_delay=2, msg_count=100):
        try:
            msgs = 0
            self.client.loop_start()
            while True:
                if self.is_connected():
                    if msgs < msg_count:
                        msgs += 1
                        self.client.publish(self.topic_publish, data.generate(True))
                    else:
                        break
                sleep(publish_delay)
        except Exception as x:
            raise x
        finally:
            self.client.loop_stop()
