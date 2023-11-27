from pathlib import Path
from google.protobuf.descriptor import Descriptor, EnumDescriptor, MethodDescriptor, OneofDescriptor

import warnings

# String descriptions of protobuf field types
FIELD_TYPES = [
    'DOUBLE',
    'FLOAT',
    'INT64',
    'UINT64',
    'INT32',
    'FIXED64',
    'FIXED32',
    'BOOL',
    'STRING',
    'GROUP',
    'MESSAGE',
    'BYTES',
    'UINT32',
    'ENUM',
    'SFIXED32',
    'SFIXED64',
    'SINT32',
    'SINT64'
]

def load_data(_path):
    with open(Path(_path).expanduser(), 'rb') as f:
        data = f.read()
    return data

def describe_request(method_descriptor: MethodDescriptor) -> dict:
    """
    Provide a dictionary that describes the fields of a Method request
    with a string description of their types.
    :param method_descriptor: MethodDescriptor
    :return: dict - a mapping of field names to their types
    """
    warnings.warn(
        "This function is deprecated, and will be removed in a future release. Use describe_descriptor() instead.",
        DeprecationWarning
    )
    description = {}
    for field in method_descriptor.input_type.fields:
        description[field.name] = FIELD_TYPES[field.type-1]
    return description

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
            description += describe_enum_descriptor(enum, indent+1)

    if descriptor.fields:
        description += f"\n{padding}Fields:"
        for field in descriptor.fields:
            description += f"\n\t{padding}{field.name}: {FIELD_TYPES[field.type-1]}"

    if descriptor.oneofs:
        description += f"\n{padding}Oneofs:"
        for oneof in descriptor.oneofs:
            description += describe_oneof_descriptor(oneof, indent+1)

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

def describe_oneof_descriptor(oneof_descriptor: OneofDescriptor, indent: int = 0) -> str:
    """
    Prints a human readable description of a protobuf oneof descriptor.
    :param oneof_descriptor: OneofDescriptor - a protobuf oneof descriptor
    :return: str - a human readable description of the oneof descriptor
    """
    padding = "\t" * indent
    description = f"\n{padding}{oneof_descriptor.name}:"
    for field in oneof_descriptor.fields:
        description += f"\n{padding}{field.name}: {FIELD_TYPES[field.type-1]}"
    return description
