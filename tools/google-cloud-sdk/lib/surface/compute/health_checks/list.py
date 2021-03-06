# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for listing health checks."""
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import lister
from googlecloudsdk.calliope import exceptions


class List(base_classes.BaseLister):
  """List health checks."""

  @staticmethod
  def Args(parser):
    base_classes.BaseLister.Args(parser)

    protocol = parser.add_argument(
        '--protocol',
        help='The health check protocol to be listed. Default is all listed.')
    protocol.detailed_help = """\
        If protocol is specified, only health checks for that protocol are
        listed, and protocol-specific columns are added to the output. By
        default, health checks for all protocols are listed.
        """

  def _ConvertProtocolArgToValue(self, args):
    # Get the dictionary that maps strings to numbers, e.g. "HTTP" to 0.
    protocol_dict = self.messages.HealthCheck.TypeValueValuesEnum.to_dict()
    return protocol_dict.get(args.protocol.upper())

  def Format(self, args):
    # Start with the columns that apply to all protocols.
    columns = ['name:label=NAME', 'type:label=PROTOCOL']

    # Add protocol-specific columns. Note that we only need to worry about
    # protocols that were whitelisted in our GetResources method below.
    if args.protocol is not None:
      protocol_value = self._ConvertProtocolArgToValue(args)
      if (protocol_value ==
          self.messages.HealthCheck.TypeValueValuesEnum.HTTP.number):
        columns.extend(['httpHealthCheck.host:label=HOST'])
        columns.extend(['httpHealthCheck.port:label=PORT'])
        columns.extend(['httpHealthCheck.requestPath:label=REQUEST_PATH'])
      elif (protocol_value ==
            self.messages.HealthCheck.TypeValueValuesEnum.HTTPS.number):
        columns.extend(['httpsHealthCheck.host:label=HOST'])
        columns.extend(['httpsHealthCheck.port:label=PORT'])
        columns.extend(['httpsHealthCheck.requestPath:label=REQUEST_PATH'])
      elif (protocol_value ==
            self.messages.HealthCheck.TypeValueValuesEnum.HTTP2.number):
        columns.extend(['http2HealthCheck.host:label=HOST'])
        columns.extend(['http2HealthCheck.port:label=PORT'])
        columns.extend(['http2HealthCheck.requestPath:label=REQUEST_PATH'])
      elif (protocol_value ==
            self.messages.HealthCheck.TypeValueValuesEnum.TCP.number):
        columns.extend(['tcpHealthCheck.port:label=PORT'])
        columns.extend(['tcpHealthCheck.request:label=REQUEST'])
        columns.extend(['tcpHealthCheck.response:label=RESPONSE'])
      elif (protocol_value ==
            self.messages.HealthCheck.TypeValueValuesEnum.SSL.number):
        columns.extend(['sslHealthCheck.port:label=PORT'])
        columns.extend(['sslHealthCheck.request:label=REQUEST'])
        columns.extend(['sslHealthCheck.response:label=RESPONSE'])

    return 'table[]({columns})'.format(columns=','.join(columns))

  @property
  def service(self):
    return self.compute.healthChecks

  @property
  def resource_type(self):
    return 'healthChecks'

  def GetResources(self, args, errors):
    health_checks = lister.GetGlobalResources(
        service=self.service,
        project=self.project,
        filter_expr=self.GetFilterExpr(args),
        http=self.http,
        batch_url=self.batch_url,
        errors=errors)

    # If a protocol is specified, check that it is one we support, and convert
    # it to a number.
    protocol_value = None
    if args.protocol is not None:
      protocol_whitelist = [
          self.messages.HealthCheck.TypeValueValuesEnum.HTTP.number,
          self.messages.HealthCheck.TypeValueValuesEnum.HTTPS.number,
          self.messages.HealthCheck.TypeValueValuesEnum.HTTP2.number,
          self.messages.HealthCheck.TypeValueValuesEnum.TCP.number,
          self.messages.HealthCheck.TypeValueValuesEnum.SSL.number
          ]
      protocol_value = self._ConvertProtocolArgToValue(args)
      if protocol_value not in protocol_whitelist:
        raise exceptions.ToolException(
            'Invalid health check protocol ' + args.protocol + '.')

    for health_check in health_checks:
      if protocol_value is None or health_check.type.number == protocol_value:
        yield health_check


List.detailed_help = base_classes.GetGlobalListerHelp('health checks')
