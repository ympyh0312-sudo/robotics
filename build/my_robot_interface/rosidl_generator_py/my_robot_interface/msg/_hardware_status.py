# generated from rosidl_generator_py/resource/_idl.py.em
# with input from my_robot_interface:msg/HardwareStatus.idl
# generated code does not contain a copyright notice

from __future__ import annotations

import collections.abc
import os
import typing

import rosidl_pycommon.interface_base_classes

if typing.TYPE_CHECKING:
    from ctypes import Structure

    class PyCapsule(Structure):
        pass  # don't need to define the full structure


# This is being done at the module level and not on the instance level to avoid looking
# for the same variable multiple times on each instance. This variable is not supposed to
# change during runtime so it makes sense to only look for it once.
ros_python_check_fields = os.getenv('ROS_PYTHON_CHECK_FIELDS', default='')


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_HardwareStatus(rosidl_pycommon.interface_base_classes.MessageTypeSupportMeta):
    """Metaclass of message 'HardwareStatus'."""

    _CREATE_ROS_MESSAGE: typing.ClassVar[typing.Optional[PyCapsule]] = None
    _CONVERT_FROM_PY: typing.ClassVar[typing.Optional[PyCapsule]] = None
    _CONVERT_TO_PY: typing.ClassVar[typing.Optional[PyCapsule]] = None
    _DESTROY_ROS_MESSAGE: typing.ClassVar[typing.Optional[PyCapsule]] = None
    _TYPE_SUPPORT: typing.ClassVar[typing.Optional[PyCapsule]] = None

    class HardwareStatusConstants(typing.TypedDict):
        pass

    __constants: HardwareStatusConstants = {
    }

    @classmethod
    def __import_type_support__(cls) -> None:
        try:
            from rosidl_generator_py import import_type_support  # type: ignore[attr-defined]
            module = import_type_support('my_robot_interface')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'my_robot_interface.msg.HardwareStatus')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__hardware_status
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__hardware_status
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__hardware_status
            cls._TYPE_SUPPORT = module.type_support_msg__msg__hardware_status
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__hardware_status

    @classmethod
    def __prepare__(metacls, name: str, bases: tuple[type[typing.Any], ...], /, **kwds: typing.Any) -> collections.abc.MutableMapping[str, object]:
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class HardwareStatus(rosidl_pycommon.interface_base_classes.BaseMessage, metaclass=Metaclass_HardwareStatus):
    """Message class 'HardwareStatus'."""

    __slots__ = [
        '_temperature',
        '_are_motors_ready',
        '_debug_message',
        '_check_fields',
    ]

    _fields_and_field_types: dict[str, str] = {
        'temperature': 'int64',
        'are_motors_ready': 'boolean',
        'debug_message': 'string',
    }

    # This attribute is used to store an rosidl_parser.definition variable
    # related to the data type of each of the components the message.
    SLOT_TYPES: tuple[rosidl_parser.definition.AbstractType, ...] = (
        rosidl_parser.definition.BasicType('int64'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, *,
                 temperature: typing.Optional[int] = None,  # noqa: E501
                 are_motors_ready: typing.Optional[bool] = None,  # noqa: E501
                 debug_message: typing.Optional[str] = None,  # noqa: E501
                 check_fields: typing.Optional[bool] = None) -> None:
        if check_fields is not None:
            self._check_fields = check_fields
        else:
            self._check_fields = ros_python_check_fields == '1'
        self.temperature = temperature if temperature is not None else int()
        self.are_motors_ready = are_motors_ready if are_motors_ready is not None else bool()
        self.debug_message = debug_message if debug_message is not None else str()

    def __repr__(self) -> str:
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args: list[str] = []
        for s, t in zip(self.get_fields_and_field_types().keys(), self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    from rosidl_buffer import Buffer as _RosidlBuffer
                    if not isinstance(field, _RosidlBuffer):
                        if self._check_fields:
                            assert fieldstr.startswith('array(')
                        prefix = "array('X', "
                        suffix = ')'
                        fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HardwareStatus):
            return False
        if self.temperature != other.temperature:
            return False
        if self.are_motors_ready != other.are_motors_ready:
            return False
        if self.debug_message != other.debug_message:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls) -> dict[str, str]:
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def temperature(self) -> int:
        """Message field 'temperature'."""
        return self._temperature

    @temperature.setter
    def temperature(self, value: int) -> None:

        if self._check_fields:
            if False:  # Done for templating alignment
                pass
            else:
                assert \
                    isinstance(value, int), \
                    "The 'temperature' field must be of type 'int'"
                assert value >= -9223372036854775808 and value < 9223372036854775808, \
                    "The 'temperature' field must be an integer in [-9223372036854775808, 9223372036854775807]"

        self._temperature = value

    @builtins.property
    def are_motors_ready(self) -> bool:
        """Message field 'are_motors_ready'."""
        return self._are_motors_ready

    @are_motors_ready.setter
    def are_motors_ready(self, value: bool) -> None:

        if self._check_fields:
            if False:  # Done for templating alignment
                pass
            else:
                assert \
                    isinstance(value, bool), \
                    "The 'are_motors_ready' field must be of type 'bool'"

        self._are_motors_ready = value

    @builtins.property
    def debug_message(self) -> str:
        """Message field 'debug_message'."""
        return self._debug_message

    @debug_message.setter
    def debug_message(self, value: str) -> None:

        if self._check_fields:
            if False:  # Done for templating alignment
                pass
            else:
                assert \
                    isinstance(value, str), \
                    "The 'debug_message' field must be of type 'str'"

        self._debug_message = value
