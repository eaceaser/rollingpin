import random

from twisted.internet.defer import inlineCallbacks, returnValue, succeed

from ..transports import (
    Transport,
    TransportConnection,
    CommandFailed,
)
from ..utils import sleep


class MockTransport(Transport):
    def __init__(self, config):
        pass

    @inlineCallbacks
    def connect_to(self, host):
        yield sleep(random.random())

        connection = MockTransportConnection()
        returnValue(connection)


class MockTransportConnection(TransportConnection):
    @inlineCallbacks
    def execute(self, log, command):
        command, args = command[0], command[1:]
        result = {}

        if command == "synchronize":
            log.debug("MOCK: git fetch")
        elif command == "build":
            log.debug("MOCK: build stuff")
            for arg in args:
                result[arg] = "build-token"
        elif command == "deploy":
            log.debug("MOCK: git fetch origin")
            if random.random() < .2:
                raise CommandFailed("remote command exited with status 127")
            log.debug("MOCK: git checkout origin/master")
        elif command == "restart":
            log.debug("MOCK: /sbin/initctl emit restart")
        elif command == "wait-until-components-ready":
            log.debug("MOCK: /sbin/initctl emit wait-until-components-ready")
            yield sleep(random.random() * 1)
        elif command == "components":
            result["components"] = {
                "example": {
                    "fbcedda5b56618db18426f90a06f1f62984b95e8": 3,
                    "7af8fe6294eab579c022b200388e886a348f05ac": 5,
                },
            }
        else:
            raise CommandFailed("unknown command %r" % command)

        returnValue(result)

    def disconnect(self):
        return succeed(None)
