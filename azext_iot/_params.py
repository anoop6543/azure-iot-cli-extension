# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
CLI parameter definitions.
"""

from knack.arguments import CLIArgumentType, CaseInsensitiveList
from azure.cli.core.commands.parameters import (
    resource_group_name_type,
    get_enum_type,
    get_resource_name_completion_list,
    get_three_state_flag
)
from azext_iot.common.shared import (
    EntityStatusType,
    SettleType,
    DeviceAuthType,
    KeyType,
    AttestationType,
    ProtocolType,
    AckType,
    MetricType,
    ReprovisionType,
    AllocationType,
    DistributedTracingSamplingModeType,
    ModelSourceType
)
from azext_iot._validators import mode2_iot_login_handler

hub_name_type = CLIArgumentType(
    completer=get_resource_name_completion_list('Microsoft.Devices/IotHubs'),
    help='IoT Hub name.')

event_msg_prop_type = CLIArgumentType(
    nargs='*',
    choices=CaseInsensitiveList(['sys', 'app', 'anno', 'all']),
    help='Indicate key message properties to output. '
    'sys = system properties, app = application properties, anno = annotations'
)


# pylint: disable=too-many-statements
def load_arguments(self, _):
    """
    Load CLI Args for Knack parser
    """
    with self.argument_context('iot') as context:
        context.argument('login', options_list=['--login', '-l'],
                         validator=mode2_iot_login_handler,
                         help='This command supports an entity connection string with rights to perform action. '
                         'Use to avoid session login via "az login". '
                         'If both an entity connection string and name are provided the connection string takes priority.')
        context.argument('resource_group_name', arg_type=resource_group_name_type)
        context.argument('hub_name', options_list=['--hub-name', '-n'], arg_type=hub_name_type)
        context.argument('device_id', options_list=['--device-id', '-d'], help='Target Device.')
        context.argument('module_id', options_list=['--module-id', '-m'], help='Target Module.')
        context.argument('key_type', options_list=['--key-type', '--kt'],
                         arg_type=get_enum_type(KeyType),
                         help='Shared access policy key type for auth.')
        context.argument('policy_name', options_list=['--policy-name', '--pn'],
                         help='Shared access policy to use for auth.')
        context.argument('duration', options_list=['--duration', '--du'], type=int,
                         help='Valid token duration in seconds.')
        context.argument('etag', options_list=['--etag', '-e'], help='Entity tag value.')
        context.argument('top', type=int, options_list=['--top'],
                         help='Maximum number of elements to return. Use -1 for unlimited.')
        context.argument('method_name', options_list=['--method-name', '--mn'],
                         help='Target method for invocation.')
        context.argument('method_payload', options_list=['--method-payload', '--mp'],
                         help='Json payload to be passed to method. Must be file path or raw json.')
        context.argument('timeout', options_list=['--timeout', '--to'], type=int,
                         help='Maximum number of seconds to wait for method result.')
        context.argument('auth_method', options_list=['--auth-method', '--am'],
                         arg_type=get_enum_type(DeviceAuthType),
                         help='The authorization type an entity is to be created with.')
        context.argument('metric_type', options_list=['--metric-type', '--mt'], arg_type=get_enum_type(MetricType),
                         help='Indicates which metric collection should be used to lookup a metric.')
        context.argument('metric_id', options_list=['--metric-id', '-m'],
                         help='Target metric for evaluation.')
        context.argument('yes', options_list=['--yes', '-y'],
                         arg_type=get_three_state_flag(),
                         help='Skip user prompts. Indicates acceptance of dependency installation (if required). '
                         'Used primarily for automation scenarios. Default: false')
        context.argument('repair', options_list=['--repair', '-r'],
                         arg_type=get_three_state_flag(),
                         help='Reinstall uamqp dependency compatible with extension version. Default: false')
        context.argument('repo_endpoint', options_list=['--endpoint', '-e'], help='IoT Plug and Play endpoint.')
        context.argument('repo_id', options_list=['--repo-id', '-r'], help='IoT Plug and Play repository Id.')

    with self.argument_context('iot hub') as context:
        context.argument('target_json', options_list=['--json', '-j'],
                         help='Json to replace existing twin with. Provide file path or raw json.')
        context.argument('policy_name', options_list=['--policy-name', '--pn'],
                         help='Shared access policy with operation permissions for target IoT Hub entity.')
        context.argument('primary_thumbprint', arg_group='X.509',
                         options_list=['--primary-thumbprint', '--ptp'],
                         help='Explicit self-signed certificate thumbprint to use for primary key.')
        context.argument('secondary_thumbprint', arg_group='X.509',
                         options_list=['--secondary-thumbprint', '--stp'],
                         help='Explicit self-signed certificate thumbprint to '
                         'use for secondary key.')
        context.argument('valid_days', arg_group='X.509', options_list=['--valid-days', '--vd'],
                         type=int,
                         help='Generate self-signed cert and use its thumbprint. Valid '
                         'for specified number of days. Default: 365.')
        context.argument('output_dir', arg_group='X.509', options_list=['--output-dir', '--od'],
                         help='Generate self-signed cert and use its thumbprint. '
                         'Output to specified target directory')

    with self.argument_context('iot hub monitor-events') as context:
        context.argument('timeout', options_list=['--timeout', '--to', '-t'], type=int,
                         help='Maximum seconds to maintain connection without receiving message. Use 0 for infinity. ')
        context.argument('consumer_group', options_list=['--consumer-group', '--cg', '-c'],
                         help='Specify the consumer group to use when connecting to event hub endpoint.')
        context.argument('enqueued_time', options_list=['--enqueued-time', '--et', '-e'], type=int,
                         help='Indicates the time that should be used as a starting point to read messages from the partitions. '
                         'Units are milliseconds since unix epoch. '
                         'If no time is indicated "now" is used.')
        context.argument('properties', options_list=['--properties', '--props', '-p'], arg_type=event_msg_prop_type)
        context.argument('content_type', options_list=['--content-type', '--ct'],
                         help='Specify the Content-Type of the message payload to automatically format the output to that type.')
        context.argument('device_query', options_list=['--device-query', '-q'], help='Specify a custom query to filter devices.')

    with self.argument_context('iot hub monitor-feedback') as context:
        context.argument('wait_on_id', options_list=['--wait-on-msg', '-w'],
                         help='Feedback monitor will block until a message with specific id (uuid) is received.')

    with self.argument_context('iot hub device-identity') as context:
        context.argument('edge_enabled', options_list=['--edge-enabled', '--ee'],
                         arg_type=get_three_state_flag(),
                         help='Flag indicating edge enablement.')
        context.argument('status', options_list=['--status', '--sta'],
                         arg_type=get_enum_type(EntityStatusType),
                         help='Set device status upon creation.')
        context.argument('status_reason', options_list=['--status-reason', '--star'],
                         help='Description for device status.')

    with self.argument_context('iot hub device-identity create') as context:
        context.argument('force', options_list=['--force', '-f'],
                         help='Overwrites the non-edge device\'s parent device.')
        context.argument('set_parent_id', options_list=['--set-parent', '--pd'], help='Id of edge device.')
        context.argument('add_children', options_list=['--add-children', '--cl'],
                         help='Child device list (comma separated) includes only non-edge devices.')

    with self.argument_context('iot hub device-identity export') as context:
        context.argument('blob_container_uri',
                         options_list=['--blob-container-uri', '--bcu'],
                         help='Blob Shared Access Signature URI with write access to '
                         'a blob container. This is used to output the status of the '
                         'job and the results.')
        context.argument('include_keys',
                         options_list=['--include-keys', '--ik'],
                         arg_type=get_three_state_flag(),
                         help='If set, keys are exported normally. Otherwise, keys are '
                         'set to null in export output.')

    with self.argument_context('iot hub device-identity import') as context:
        context.argument('input_blob_container_uri',
                         options_list=['--input-blob-container-uri', '--ibcu'],
                         help='Blob Shared Access Signature URI with read access to a blob '
                         'container. This blob contains the operations to be performed on '
                         'the identity registry ')
        context.argument('output_blob_container_uri',
                         options_list=['--output-blob-container-uri', '--obcu'],
                         help='Blob Shared Access Signature URI with write access '
                         'to a blob container. This is used to output the status of '
                         'the job and the results.')

    with self.argument_context('iot hub device-identity get-parent') as context:
        context.argument('device_id', help='Id of non-edge device.')

    with self.argument_context('iot hub device-identity set-parent') as context:
        context.argument('device_id', help='Id of non-edge device.')
        context.argument('parent_id', options_list=['--parent-device-id', '--pd'], help='Id of edge device.')
        context.argument('force', options_list=['--force', '-f'],
                         help='Overwrites the non-edge device\'s parent device.')

    with self.argument_context('iot hub device-identity add-children') as context:
        context.argument('device_id', help='Id of edge device.')
        context.argument('child_list', options_list=['--child-list', '--cl'],
                         help='Child device list (comma separated) includes only non-edge devices.')
        context.argument('force', options_list=['--force', '-f'],
                         help='Overwrites the non-edge device\'s parent device.')

    with self.argument_context('iot hub device-identity remove-children') as context:
        context.argument('device_id', help='Id of edge device.')
        context.argument('child_list', options_list=['--child-list', '--cl'],
                         help='Child device list (comma separated) includes only non-edge devices.')
        context.argument('remove_all', options_list=['--remove-all', '-a'], help='To remove all children.')

    with self.argument_context('iot hub distributed-tracing update') as context:
        context.argument('sampling_mode', options_list=['--sampling-mode', '--sm'],
                         help='Turns sampling for distributed tracing on and off. 1 is On and, 2 is Off.',
                         arg_type=get_enum_type(DistributedTracingSamplingModeType))
        context.argument('sampling_rate', options_list=['--sampling-rate', '--sr'],
                         help='Controls the amount of messages sampled for adding trace context. This value is'
                              'a percentage. Only values from 0 to 100 (inclusive) are permitted.')

    with self.argument_context('iot hub device-identity list-children') as context:
        context.argument('device_id', help='Id of edge device.')

    with self.argument_context('iot hub query') as context:
        context.argument('query_command', options_list=['--query-command', '-q'],
                         help='User query to be executed.')
        context.argument('top', options_list=['--top'], type=int,
                         help='Maximum number of elements to return. By default query has no cap.')

    with self.argument_context('iot device') as context:
        context.argument('data', options_list=['--data', '--da'], help='Message body.')
        context.argument('properties', options_list=['--properties', '--props', '-p'],
                         help='Message property bag in key-value pairs with the '
                         'following format: a=b;c=d')
        context.argument('msg_count', options_list=['--msg-count', '--mc'], type=int,
                         help='Number of device messages to send to IoT Hub.')
        context.argument('msg_interval', options_list=['--msg-interval', '--mi'], type=int,
                         help='Delay in seconds between device-to-cloud messages.')
        context.argument('receive_settle', options_list=['--receive-settle', '--rs'],
                         arg_type=get_enum_type(SettleType),
                         help='Indicates how to settle received cloud-to-device messages. '
                         'Supported with HTTP only.')
        context.argument('protocol_type', options_list=['--protocol', '--proto'],
                         arg_type=get_enum_type(ProtocolType),
                         help='Indicates device-to-cloud message protocol')

    with self.argument_context('iot device c2d-message') as context:
        context.argument('ack', options_list=['--ack'], arg_type=get_enum_type(AckType),
                         help='Request the delivery of per-message feedback regarding the final state of that message. '
                         'The description of ack values is as follows. '
                         'Positive: If the c2d message reaches the Completed state, IoT Hub generates a feedback message. '
                         'Negative: If the c2d message reaches the Dead lettered state, IoT Hub generates a feedback message. '
                         'Full: IoT Hub generates a feedback message in either case. '
                         'By default, no ack is requested.')
        context.argument('correlation_id', options_list=['--correlation-id', '--cid'],
                         help='Correlation Id associated with message.')
        context.argument('lock_timeout', options_list=['--lock-timeout', '--lt'], type=int,
                         help='Specifies the amount of time a message will be invisible to other receive calls.')

    with self.argument_context('iot device c2d-message send') as context:
        context.argument('wait_on_feedback', options_list=['--wait', '-w'],
                         arg_type=get_three_state_flag(),
                         help='If set the c2d send operation will block until device feedback has been received.')

    with self.argument_context('iot device upload-file') as context:
        context.argument('file_path', options_list=['--file-path', '--fp'],
                         help='Path to file for upload.')
        context.argument('content_type', options_list=['--content-type', '--ct'],
                         help='MIME Type of file.')

    # Remove after deprecation
    with self.argument_context('iot hub apply-configuration') as context:
        context.argument('content', options_list=['--content', '-k'],
                         help='Configuration content. Provide file path or raw json.')

    with self.argument_context('iot hub configuration') as context:
        context.argument('config_id', options_list=['--config-id', '-c'],
                         help='Target device configuration.')
        context.argument('target_condition', options_list=['--target-condition', '--tc', '-t'],
                         help='Target condition in which a device configuration applies to.')
        context.argument('priority', options_list=['--priority', '--pri'],
                         help='Weight of the device configuration in case of competing rules (highest wins).')
        context.argument('content', options_list=['--content', '-k'],
                         help='Device configuration content. Provide file path or raw json.')
        context.argument('metrics', options_list=['--metrics', '-m'],
                         help='Device configuration metric definitions. Provide file path or raw json.')
        context.argument('labels', options_list=['--labels', '--lab'],
                         help="Map of labels to be applied to target configuration. "
                              "Format example: {\"key0\":\"value0\", \"key1\":\"value1\"}")
        context.argument('top', options_list=['--top'], type=int,
                         help='Maximum number of configurations to return.')

    with self.argument_context('iot edge') as context:
        context.argument('config_id', options_list=['--deployment-id', '-d', '--config-id', '-c'],
                         help='Target deployment. --config-id/-c is deprecated for deployments. Use --deployment-id/-d instead.')
        context.argument('target_condition', options_list=['--target-condition', '--tc', '-t'],
                         help='Target condition in which an Edge deployment applies to.')
        context.argument('priority', options_list=['--priority', '--pri'],
                         help='Weight of deployment in case of competing rules (highest wins).')
        context.argument('content', options_list=['--content', '-k'],
                         help='IoT Edge deployment content. Provide file path or raw json.')
        context.argument('metrics', options_list=['--metrics', '-m'],
                         help='IoT Edge deployment metric definitions. Provide file path or raw json.')
        context.argument('labels', options_list=['--labels', '--lab'],
                         help="Map of labels to be applied to target deployment. "
                              "Use the following format: '{\"key0\":\"value0\", \"key1\":\"value1\"}'")
        context.argument('top', options_list=['--top'], type=int,
                         help='Maximum number of deployments to return.')

    with self.argument_context('iot dps') as context:
        context.argument('dps_name', help='Name of the Azure IoT Hub device provisioning service')
        context.argument('initial_twin_properties',
                         options_list=['--initial-twin-properties', '--props'],
                         help='Initial twin properties')
        context.argument('initial_twin_tags', options_list=['--initial-twin-tags', '--tags'],
                         help='Initial twin tags')
        context.argument('iot_hub_host_name', options_list=['--iot-hub-host-name', '--hn'],
                         help='Host name of target IoT Hub')
        context.argument('provisioning_status', options_list=['--provisioning-status', '--ps'],
                         arg_type=get_enum_type(EntityStatusType),
                         help='Enable or disable enrollment entry')
        context.argument('certificate_path',
                         options_list=['--certificate-path', '--cp'],
                         help='The path to the file containing the primary certificate.')
        context.argument('secondary_certificate_path',
                         options_list=['--secondary-certificate-path', '--scp'],
                         help='The path to the file containing the secondary certificate')
        context.argument('remove_certificate',
                         options_list=['--remove-certificate', '--rc'],
                         help='Remove current primary certificate',
                         arg_type=get_three_state_flag())
        context.argument('remove_secondary_certificate',
                         options_list=['--remove-secondary-certificate', '--rsc'],
                         help='Remove current secondary certificate',
                         arg_type=get_three_state_flag())
        context.argument('reprovision_policy', options_list=['--reprovision-policy', '--rp'],
                         arg_type=get_enum_type(ReprovisionType),
                         help='Device data to be handled on re-provision to different Iot Hub.')
        context.argument('allocation_policy', options_list=['--allocation-policy', '--ap'],
                         arg_type=get_enum_type(AllocationType),
                         help='Type of allocation for device assigned to the Hub.')
        context.argument('iot_hubs', options_list=['--iot-hubs', '--ih'],
                         help='Host name of target IoT Hub. Use space-separated list for multiple IoT Hubs.')

    with self.argument_context('iot dps enrollment') as context:
        context.argument('enrollment_id', help='ID of device enrollment record')
        context.argument('device_id', help='IoT Hub Device ID')
        context.argument('primary_key', options_list=['--primary-key', '--pk'],
                         help='The primary symmetric shared access key stored in base64 format. ')
        context.argument('secondary_key', options_list=['--secondary-key', '--sk'],
                         help='The secondary symmetric shared access key stored in base64 format. ')

    with self.argument_context('iot dps enrollment create') as context:
        context.argument('attestation_type', options_list=['--attestation-type', '--at'],
                         arg_type=get_enum_type(AttestationType), help='Attestation Mechanism')
        context.argument('certificate_path',
                         options_list=['--certificate-path', '--cp'],
                         help='The path to the file containing the primary certificate. '
                         'When choosing x509 as attestation type, '
                         'one of the certificate path is required.')
        context.argument('secondary_certificate_path',
                         options_list=['--secondary-certificate-path', '--scp'],
                         help='The path to the file containing the secondary certificate. '
                         'When choosing x509 as attestation type, '
                         'one of the certificate path is required.')
        context.argument('endorsement_key', options_list=['--endorsement-key', '--ek'],
                         help='TPM endorsement key for a TPM device. '
                         'When choosing tpm as attestation type, endorsement key is required.')

    with self.argument_context('iot dps enrollment update') as context:
        context.argument('endorsement_key', options_list=['--endorsement-key', '--ek'],
                         help='TPM endorsement key for a TPM device.')

    with self.argument_context('iot dps enrollment-group') as context:
        context.argument('enrollment_id', help='ID of enrollment group')
        context.argument('primary_key', options_list=['--primary-key', '--pk'],
                         help='The primary symmetric shared access key stored in base64 format. ')
        context.argument('secondary_key', options_list=['--secondary-key', '--sk'],
                         help='The secondary symmetric shared access key stored in base64 format. ')
        context.argument('certificate_path',
                         options_list=['--certificate-path', '--cp'],
                         help='The path to the file containing the primary certificate. '
                         'If attestation with an intermediate certificate is desired then a certificate path must be provided.')
        context.argument('secondary_certificate_path',
                         options_list=['--secondary-certificate-path', '--scp'],
                         help='The path to the file containing the secondary certificate. '
                         'If attestation with an intermediate certificate is desired then a certificate path must be provided.')
        context.argument('root_ca_name',
                         options_list=['--root-ca-name', '--ca-name', '--cn'],
                         help='The name of the primary root CA certificate. '
                         'If attestation with a root CA certificate is desired then a root ca name must be provided.')
        context.argument('secondary_root_ca_name',
                         options_list=['--secondary-root-ca-name', '--secondary-ca-name', '--scn'],
                         help='The name of the secondary root CA certificate. '
                         'If attestation with a root CA certificate is desired then a root ca name must be provided.')

    with self.argument_context('iot dps registration') as context:
        context.argument('registration_id', help='ID of device registration')

    with self.argument_context('iot dps registration list') as context:
        context.argument('enrollment_id', help='ID of enrollment group')

    with self.argument_context('iot dt') as context:
        context.argument('repo_login', options_list=['--repo-login', '--rl'],
                         help='This command supports an entity connection string with rights to perform action. '
                         'Use to avoid PnP endpoint and repository name if repository is private. '
                         'If both an entity connection string and name are provided the connection string takes priority.')
        context.argument('interface', options_list=['--interface', '-i'],
                         help='Target interface name. This should be the name of the interface not the urn-id.')
        context.argument('command_name', options_list=['--command-name', '--cn'],
                         help='IoT Plug and Play interface command name.')
        context.argument('command_payload', options_list=['--command-payload', '--cp', '--cv'],
                         help='IoT Plug and Play interface command payload. '
                         'Content can be directly input or extracted from a file path.')
        context.argument('interface_payload', options_list=['--interface-payload', '--ip', '--iv'],
                         help='IoT Plug and Play interface payload. '
                         'Content can be directly input or extracted from a file path.')
        context.argument('source_model', options_list=['--source', '-s'],
                         help='Choose your option to get model definition from specified source. ',
                         arg_type=get_enum_type(ModelSourceType))
        context.argument('schema', options_list=['--schema'],
                         help='Show interface with entity schema.')

    with self.argument_context('iot dt monitor-events') as context:
        context.argument('consumer_group', options_list=['--consumer-group', '--cg'],
                         help='Specify the consumer group to use when connecting to event hub endpoint.')
        context.argument('properties', options_list=['--properties', '--props', '-p'], arg_type=event_msg_prop_type)
        context.argument('repair', options_list=['--repair'],
                         arg_type=get_three_state_flag(),
                         help='Reinstall uamqp dependency compatible with extension version. Default: false')

    with self.argument_context('iot pnp') as context:
        context.argument('model', options_list=['--model', '-m'],
                         help='Target capability-model urn-id. Example: urn:example:capabilityModels:Mxchip:1')
        context.argument('interface', options_list=['--interface', '-i'],
                         help='Target interface urn-id. Example: urn:example:interfaces:MXChip:1')

    with self.argument_context('iot pnp interface') as context:
        context.argument('interface_definition', options_list=['--definition', '--def'],
                         help='IoT Plug and Play interface definition written in PPDL (JSON-LD). '
                         'Can be directly input or a file path where the content is extracted.')

    with self.argument_context('iot pnp interface list') as context:
        context.argument('search_string', options_list=['--search', '--ss'],
                         help='Searches IoT Plug and Play interfaces for given string in the'
                              ' \"Description, DisplayName, comment and Id\".')
        context.argument('top', type=int, options_list=['--top'],
                         help='Maximum number of interface to return.')

    with self.argument_context('iot pnp capability-model') as context:
        context.argument('model_definition', options_list=['--definition', '--def'],
                         help='IoT Plug and Play capability-model definition written in PPDL (JSON-LD). '
                         'Can be directly input or a file path where the content is extracted.')

    with self.argument_context('iot pnp capability-model show') as context:
        context.argument('expand', options_list=['--expand'],
                         help='Indicates whether to expand the device capability model\'s'
                              ' interface definitions or not.')

    with self.argument_context('iot pnp capability-model list') as context:
        context.argument('search_string', options_list=['--search', '--ss'],
                         help='Searches IoT Plug and Play models for given string in the'
                              ' \"Description, DisplayName, comment and Id\".')
        context.argument('top', type=int, options_list=['--top'],
                         help='Maximum number of capability-model to return.')
