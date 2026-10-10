// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from my_robot_interface:msg/HardwareStatus.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_robot_interface/msg/hardware_status.hpp"


#ifndef MY_ROBOT_INTERFACE__MSG__DETAIL__HARDWARE_STATUS__TRAITS_HPP_
#define MY_ROBOT_INTERFACE__MSG__DETAIL__HARDWARE_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <array>
#include <cstddef>
#include <sstream>
#include <string>
#include <string_view>
#include <tuple>
#include <type_traits>
#include <utility>

#include "my_robot_interface/msg/detail/hardware_status__struct.hpp"
#include "rosidl_runtime_cpp/buffer__traits.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace my_robot_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const HardwareStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: temperature
  {
    out << "temperature: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature, out);
    out << ", ";
  }

  // member: are_motors_ready
  {
    out << "are_motors_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.are_motors_ready, out);
    out << ", ";
  }

  // member: debug_message
  {
    out << "debug_message: ";
    rosidl_generator_traits::value_to_yaml(msg.debug_message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const HardwareStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: temperature
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "temperature: ";
    rosidl_generator_traits::value_to_yaml(msg.temperature, out);
    out << "\n";
  }

  // member: are_motors_ready
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "are_motors_ready: ";
    rosidl_generator_traits::value_to_yaml(msg.are_motors_ready, out);
    out << "\n";
  }

  // member: debug_message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "debug_message: ";
    rosidl_generator_traits::value_to_yaml(msg.debug_message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const HardwareStatus & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

template<typename T, std::enable_if_t<std::is_same_v<std::decay_t<T>, my_robot_interface::msg::HardwareStatus>, int> = 0>
constexpr auto as_tuple_ref(T && msg)
{
  return std::forward_as_tuple(
    std::forward<T>(msg).temperature,
    std::forward<T>(msg).are_motors_ready,
    std::forward<T>(msg).debug_message);
}

}  // namespace msg

}  // namespace my_robot_interface

namespace rosidl_generator_traits
{

template<>
constexpr const char * data_type<my_robot_interface::msg::HardwareStatus>()
{
  return "my_robot_interface::msg::HardwareStatus";
}

template<>
constexpr const char * name<my_robot_interface::msg::HardwareStatus>()
{
  return "my_robot_interface/msg/HardwareStatus";
}

template<>
struct has_fixed_size<my_robot_interface::msg::HardwareStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<my_robot_interface::msg::HardwareStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<my_robot_interface::msg::HardwareStatus>
  : std::true_type {};

template<>
struct MessageTraits<my_robot_interface::msg::HardwareStatus>
{
  static constexpr std::size_t member_count = 3;
  static constexpr std::array<std::string_view, member_count> member_names = {
    "temperature",
    "are_motors_ready",
    "debug_message",
  };
};

}  // namespace rosidl_generator_traits

#endif  // MY_ROBOT_INTERFACE__MSG__DETAIL__HARDWARE_STATUS__TRAITS_HPP_
