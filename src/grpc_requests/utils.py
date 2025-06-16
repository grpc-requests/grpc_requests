from pathlib import Path
from typing import Dict, Any

from google.protobuf.descriptor import (
    Descriptor,
    EnumDescriptor,
    OneofDescriptor,
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


def descriptor_to_json(descriptor: Descriptor, use_full_name: bool = False) -> Dict[str, Any]:
    json_data = {}
    for field in descriptor.fields:
        field_name = field.full_name if use_full_name else field.name
        field_value = get_default_value(field.type)
        print_value = [field_value] if field.label == 3 else field_value
        json_data[field_name] = print_value
    for descriptor in descriptor.nested_types:
        json_data[descriptor.name] = descriptor_to_json(descriptor)
    for enum in descriptor.enum_types:
        json_data[enum.name] = enum.values[0].name
    for oneof in descriptor.oneofs:
        json_data[oneof.name] = descriptor_to_json(oneof)
    for extension in descriptor.extensions:
        json_data[extension.name] = descriptor_to_json(extension, use_full_name=True)
    return json_data

def enum_descriptor_to_json(enum_descriptor: EnumDescriptor) -> Dict[str, int]:
    json_data = {}
    for value in enum_descriptor.values:
        json_data[value.name] = value.number
    return json_data

def get_default_value(field_type:int) -> Any:
    if field_type in [1, 2]:
        return 0.0
    elif field_type in [3,4,5,6,7,13,14,15,16,17]:
        return 0
    elif field_type == 5:
        return False
    elif field_type == 6:
        return "string"
    elif field_type == 7:
        return b"bytes"
    else:
        return None

def describe_descriptor(descriptor: Descriptor, indent: int = 0) -> str:
    """
    Prints a human readable description of a protobuf descriptor.
    :param descriptor: Descriptor - a protobuf descriptor
    :return: str - a human readable description of the descriptor
    """
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
