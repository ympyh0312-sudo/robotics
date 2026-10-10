// generated from rosidl_generator_c/resource/idl__type_support.h.em
// with input from my_robot_interface:srv/AddTwoInts.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_robot_interface/srv/add_two_ints.h"


#ifndef MY_ROBOT_INTERFACE__SRV__DETAIL__ADD_TWO_INTS__TYPE_SUPPORT_H_
#define MY_ROBOT_INTERFACE__SRV__DETAIL__ADD_TWO_INTS__TYPE_SUPPORT_H_

#include "rosidl_typesupport_interface/macros.h"

#include "my_robot_interface/msg/rosidl_generator_c__visibility_control.h"

#ifdef __cplusplus
extern "C"
{
#endif

#include "rosidl_runtime_c/message_type_support_struct.h"

// Forward declare the get type support functions for this type.
ROSIDL_GENERATOR_C_PUBLIC_my_robot_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  my_robot_interface,
  srv,
  AddTwoInts_Request
)(void);

// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"

// Forward declare the get type support functions for this type.
ROSIDL_GENERATOR_C_PUBLIC_my_robot_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  my_robot_interface,
  srv,
  AddTwoInts_Response
)(void);

// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"

// Forward declare the get type support functions for this type.
ROSIDL_GENERATOR_C_PUBLIC_my_robot_interface
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  my_robot_interface,
  srv,
  AddTwoInts_Event
)(void);

#include "rosidl_runtime_c/service_type_support_struct.h"

// Forward declare the get type support functions for this type.
ROSIDL_GENERATOR_C_PUBLIC_my_robot_interface
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
  rosidl_typesupport_c,
  my_robot_interface,
  srv,
  AddTwoInts
)(void);

// Forward declare the function to create a service event message for this type.
ROSIDL_GENERATOR_C_PUBLIC_my_robot_interface
void *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  my_robot_interface,
  srv,
  AddTwoInts
)(
  const rosidl_service_introspection_info_t * info,
  rcutils_allocator_t * allocator,
  const void * request_message,
  const void * response_message);

// Forward declare the function to destroy a service event message for this type.
ROSIDL_GENERATOR_C_PUBLIC_my_robot_interface
bool
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
  rosidl_typesupport_c,
  my_robot_interface,
  srv,
  AddTwoInts
)(
  void * event_msg,
  rcutils_allocator_t * allocator);

#ifdef __cplusplus
}
#endif

#endif  // MY_ROBOT_INTERFACE__SRV__DETAIL__ADD_TWO_INTS__TYPE_SUPPORT_H_
