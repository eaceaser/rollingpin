import logging
import unittest

from rollingpin.deploy import Deployer
from mock import MagicMock, ANY


class MockHost(object):

    def __init__(self, name, address):
        self.name = name
        self.address = address


class TestDeployer(unittest.TestCase):
    def test_constructor(self):
        config = {
            'hostsource': 'hostsrc',
            'transport': object(),
            'deploy': {
                'code-host': object()
            }
        }
        event_bus = object()
        deployer = Deployer(config, event_bus,
                            deploy_id='test-deploy',
                            parallel=10,
                            timeout=11,
                            sleeptime=12,
                            dangerously_fast=True
                            )
        self.assertEquals(deployer.code_host, config['deploy']['code-host'])
        self.assertEquals(deployer.host_source, 'hostsrc')
        self.assertEquals(deployer.transport, config['transport'])
        self.assertEquals(deployer.event_bus, event_bus)
        self.assertEquals(deployer.deploy_id, 'test-deploy')
        self.assertEquals(deployer.parallel, 10)
        self.assertEquals(deployer.execution_timeout, 11)
        self.assertEquals(deployer.sleeptime, 12)
        self.assertEquals(deployer.dangerously_fast, True)

    def test_process_host(self):
        transport = MagicMock()
        connection = MagicMock()
        transport.connect_to.return_value = connection
        event_bus = MagicMock()
        host = MockHost("test_host", "test_addr")

        config = {
            'hostsource': 'hostsrc',
            'transport': transport,
            'deploy': {
                'code-host': object()
            }
        }

        deployer = Deployer(config, event_bus,
                            deploy_id='test-deploy',
                            parallel=10,
                            timeout=11,
                            sleeptime=12,
                            dangerously_fast=True
                            )

        deployer.process_host(host, ['test_command'], timeout=10)

        transport.connect_to.assert_called_with("test_addr")
        assert isinstance(connection.execute.call_args[0][0], logging.LoggerAdapter)
        connection.execute.assert_called_with(ANY, 'test_command', 10, {'ROLLINGPIN_DEPLOY_ID': 'test-deploy'})

        connection.disconnect.assert_called()
