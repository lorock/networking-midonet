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

from neutron_lib.api.definitions import router_interface_fip
from neutron_lib.api import extensions
from neutron_lib import exceptions as n_exc

from midonet.neutron._i18n import _


class RouterInterfaceInUseAsGatewayByFloatingIP(n_exc.InUse):
    message = _("Router interface for subnet %(subnet_id)s on router "
                "%(router_id)s cannot be deleted, as it is required "
                "by one or more floating IPs as a gateway.")


class Routerinterfacefip(extensions.ExtensionDescriptor):
    """Router interface FIP extension."""

    @classmethod
    def get_name(cls):
        return router_interface_fip.NAME

    @classmethod
    def get_alias(cls):
        return router_interface_fip.ALIAS

    @classmethod
    def get_description(cls):
        return router_interface_fip.DESCRIPTION

    @classmethod
    def get_updated(cls):
        return router_interface_fip.UPDATED_TIMESTAMP

    def get_required_extensions(self):
        return router_interface_fip.REQUIRED_EXTENSIONS

    def get_optional_extensions(self):
        return router_interface_fip.OPTIONAL_EXTENSIONS
