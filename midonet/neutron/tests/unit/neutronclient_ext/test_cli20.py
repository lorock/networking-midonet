# Copyright (C) 2016 Midokura SARL
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import mock
from mox3 import mox

from neutronclient import shell
from neutronclient.tests.unit import test_cli20

TOKEN = test_cli20.TOKEN


class MyResp(test_cli20.MyResp):

    pass


class MyApp(test_cli20.MyApp):

    pass


class MyComparator(test_cli20.MyComparator):

    pass


class CLIExtTestV20Base(test_cli20.CLITestV20Base):

    def setUp(self, plurals=None):
        super(CLIExtTestV20Base, self).setUp(plurals=plurals)

    def _setup_mock_patch(self, name):
        patcher = mock.patch(name)
        thing = patcher.start()
        return thing

    def _mock_load_extensions(self, resource):
        load_method = ('neutronclient.common.extension.' +
                       '_discover_via_entry_points')
        load_ext_mock = self._setup_mock_patch(load_method)
        load_ext_mock.return_value = [resource]
        return load_ext_mock

    def _test_update_ext_resource(self, resource, cmd, myid, args,
                                  extrafields,
                                  cmd_resource=None, parent_id=None):
        self.mox.StubOutWithMock(cmd, "get_client")
        self.mox.StubOutWithMock(self.client.httpclient, "request")
        cmd.get_client().MultipleTimes().AndReturn(self.client)
        if not cmd_resource:
            cmd_resource = resource

        body = {resource: extrafields}
        path = getattr(self.client, cmd_resource + "_path")
        if parent_id:
            path = path % parent_id
        path = path % myid
        mox_body = MyComparator(body, self.client)

        self.client.httpclient.request(
            test_cli20.MyUrlComparator(
                test_cli20.end_url(path), self.client),
            'PUT',
            body=mox_body,
            headers=mox.ContainsKeyValue(
                'X-Auth-Token', TOKEN)).AndReturn((MyResp(204), None))
        self.mox.ReplayAll()
        cmd_parser = cmd.get_parser("update_" + cmd_resource)
        shell.run_command(cmd, cmd_parser, args)
        self.mox.VerifyAll()
        self.mox.UnsetStubs()
        _str = self.fake_stdout.make_string()
        self.assertIn(myid, _str)

    def _test_show_ext_resource(self, resource, cmd, myid, args, fields=(),
                                cmd_resource=None, parent_id=None):
        self.mox.StubOutWithMock(cmd, "get_client")
        self.mox.StubOutWithMock(self.client.httpclient, "request")
        cmd.get_client().MultipleTimes().AndReturn(self.client)
        if not cmd_resource:
            cmd_resource = resource

        query = "&".join(["fields=%s" % field for field in fields])
        expected_res = {resource:
                        {self.id_field: myid,
                         'name': 'myname', }, }
        resstr = self.client.serialize(expected_res)
        path = getattr(self.client, cmd_resource + "_path")
        if parent_id:
            path = path % parent_id
        path = path % myid
        self.client.httpclient.request(
            test_cli20.end_url(path, query), 'GET',
            body=None,
            headers=mox.ContainsKeyValue(
                'X-Auth-Token', TOKEN)).AndReturn((MyResp(200), resstr))
        self.mox.ReplayAll()
        cmd_parser = cmd.get_parser("show_" + cmd_resource)
        shell.run_command(cmd, cmd_parser, args)
        self.mox.VerifyAll()
        self.mox.UnsetStubs()
        _str = self.fake_stdout.make_string()
        self.assertIn(myid, _str)
        self.assertIn('myname', _str)

    def _test_delete_ext_resource(self, resource, cmd, myid, args,
                                  cmd_resource=None, parent_id=None):
        self.mox.StubOutWithMock(cmd, "get_client")
        self.mox.StubOutWithMock(self.client.httpclient, "request")
        cmd.get_client().MultipleTimes().AndReturn(self.client)
        if not cmd_resource:
            cmd_resource = resource
        path = getattr(self.client, cmd_resource + "_path")
        if parent_id:
            path = path % parent_id
        path = path % myid
        self.client.httpclient.request(
            test_cli20.end_url(path), 'DELETE',
            body=None,
            headers=mox.ContainsKeyValue(
                'X-Auth-Token', TOKEN)).AndReturn((MyResp(204), None))
        self.mox.ReplayAll()
        cmd_parser = cmd.get_parser("delete_" + cmd_resource)
        shell.run_command(cmd, cmd_parser, args)
        self.mox.VerifyAll()
        self.mox.UnsetStubs()
        _str = self.fake_stdout.make_string()
        self.assertIn(myid, _str)
