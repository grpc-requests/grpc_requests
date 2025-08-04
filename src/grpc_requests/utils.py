from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Any, Union
import grpc
import warnings

from google.protobuf.descriptor import (
    Descriptor,
    EnumDescriptor,
    OneofDescriptor,
)


@dataclass
class CredentialsInfo:
    root_certificates: Union[bytes, None]
    private_key: Union[bytes, None]
    certificate_chain: Union[bytes, None]

    def __post_init__(self):
        for attr in ["root_certificates", "private_key", "certificate_chain"]:
            value = getattr(self, attr)
            if isinstance(value, str):
                setattr(self, attr, load_data(value))

    # Hey Doofus - the act of making the class should do the loading, not every time you create creds
    def create_ssl_credentials(self) -> grpc.ChannelCredentials:
        return grpc.ssl_channel_credentials(
            self.root_certificates, self.private_key, self.certificate_chain
        )


# String descriptions of protobuf field types
FIELD_TYPES = [
    "DOUBLE",
    "FLOAT",
    "INT64",
    "UINT64",
    "INT32",
    "FIXED64",
    "FIXED32",
    "BOOL",
    "STRING",
    "GROUP",
    "MESSAGE",
    "BYTES",
    "UINT32",
    "ENUM",
    "SFIXED32",
    "SFIXED64",
    "SINT32",
    "SINT64",
]


def load_data(_path):
    with open(Path(_path).expanduser(), "rb") as f:
        data = f.read()
    return data


def descriptor_to_json(
    descriptor: Descriptor, use_full_name: bool = False
) -> Dict[str, Any]:
    """
    Converts a descriptor to a JSON object. Used to print an exemplar of given descriptor as
    a JSON object for user reference.
    :param descriptor: Descriptor - the descriptor to convert
    :param use_full_name: bool - whether to use full name or not
    :return: Dict[str, Any] - the JSON object representing the descriptor
    """
    json_data = {}
    for field in descriptor.fields:
        field_name = field.full_name if use_full_name else field.name
        field_value = (
            descriptor_to_json(field.message_type)
            if field.message_type
            else get_default_value(field.type)
        )
        print_value = [field_value] if field.label == 3 else field_value
        json_data[field_name] = print_value
    for n_type in descriptor.nested_types:
        json_data[n_type.name] = descriptor_to_json(n_type)
    for enum in descriptor.enum_types:
        json_data[enum.name] = enum.values[0].name
    for oneof in descriptor.oneofs:
        json_data[oneof.name] = descriptor_to_json(oneof)
    for extension in descriptor.extensions:
        json_data[extension.name] = descriptor_to_json(extension, use_full_name=True)
    return json_data


def enum_descriptor_to_json(enum_descriptor: EnumDescriptor) -> Dict[str, int]:
    """
    Converts an EnumDescriptor to a JSON object.
    :param enum_descriptor: EnumDescriptor - the enum descriptor to convert
    :return: Dict[str, int] - the JSON object representing the enum descriptor
    """
    json_data = {}
    for value in enum_descriptor.values:
        json_data[value.name] = value.number
    return json_data


def get_default_value(field_type: int) -> Any:
    """
    Returns the default value for a given field type.
    :param field_type: int - the field type
    :return: Any - the default value best describing the field type
    """
    # Floating point numbers
    if field_type in [1, 2]:
        return 0.0
    # Signed and Unsigned integers
    elif field_type in [3, 4, 5, 6, 7, 13, 14, 15, 16, 17]:
        return 0
    # Boolean
    elif field_type == 8:
        return False
    # String
    elif field_type == 9:
        return "string"
    # Bytes
    elif field_type == 12:
        return b"bytes"
    # Unhandled types
    else:
        return None


def describe_descriptor(descriptor: Descriptor, indent: int = 0) -> str:
    """
    Prints a human readable description of a protobuf descriptor.
    :param descriptor: Descriptor - a protobuf descriptor
    :return: str - a human readable description of the descriptor
    """
    warnings.warn(
        "describe_descriptor is deprecated and will be removed in version 0.1.23. Please use descriptor_as_json",
        DeprecationWarning,
        stacklevel=2,
    )
    description = descriptor.name
    padding = "\t" * indent

    if descriptor.enum_types:
        description += f"\n{padding}Enums:"
        for enum in descriptor.enum_types:
            description += describe_enum_descriptor(enum, indent + 1)

    if descriptor.fields:
        description += f"\n{padding}Fields:"
        for field in descriptor.fields:
            description += f"\n\t{padding}{field.name}: {FIELD_TYPES[field.type - 1]}"

    if descriptor.oneofs:
        description += f"\n{padding}Oneofs:"
        for oneof in descriptor.oneofs:
            description += describe_oneof_descriptor(oneof, indent + 1)

    return description


def describe_enum_descriptor(enum_descriptor: EnumDescriptor, indent: int = 0) -> str:
    """
    Prints a human readable description of a protobuf enum descriptor.
    :param enum_descriptor: EnumDescriptor - a protobuf enum descriptor
    :return: str - a human readable description of the enum descriptor
    """
    padding = "\t" * indent
    description = f"\n{padding}{enum_descriptor.name}:"
    for value in enum_descriptor.values:
        description += f"\n{padding}{value.name} = {value.number}"
    return description


def describe_oneof_descriptor(
    oneof_descriptor: OneofDescriptor, indent: int = 0
) -> str:
    """
    Prints a human readable description of a protobuf oneof descriptor.
    :param oneof_descriptor: OneofDescriptor - a protobuf oneof descriptor
    :return: str - a human readable description of the oneof descriptor
    """
    padding = "\t" * indent
    description = f"\n{padding}{oneof_descriptor.name}:"
    for field in oneof_descriptor.fields:
        description += f"\n{padding}{field.name}: {FIELD_TYPES[field.type - 1]}"
    return description
