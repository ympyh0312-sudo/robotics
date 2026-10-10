// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from my_robot_interface:srv/AddTwoInts.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "my_robot_interface/srv/add_two_ints.hpp"


#ifndef MY_ROBOT_INTERFACE__SRV__DETAIL__ADD_TWO_INTS__BUILDER_HPP_
#define MY_ROBOT_INTERFACE__SRV__DETAIL__ADD_TWO_INTS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "my_robot_interface/srv/detail/add_two_ints__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace my_robot_interface
{

namespace srv
{

namespace builder
{

class Init_AddTwoInts_Request_b
{
public:
  explicit Init_AddTwoInts_Request_b(::my_robot_interface::srv::AddTwoInts_Request & msg)
  : msg_(msg)
  {}
  ::my_robot_interface::srv::AddTwoInts_Request b(::my_robot_interface::srv::AddTwoInts_Request::_b_type arg)
  {
    msg_.b = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interface::srv::AddTwoInts_Request msg_;
};

class Init_AddTwoInts_Request_a
{
public:
  Init_AddTwoInts_Request_a()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AddTwoInts_Request_b a(::my_robot_interface::srv::AddTwoInts_Request::_a_type arg)
  {
    msg_.a = std::move(arg);
    return Init_AddTwoInts_Request_b(msg_);
  }

private:
  ::my_robot_interface::srv::AddTwoInts_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interface::srv::AddTwoInts_Request>()
{
  return my_robot_interface::srv::builder::Init_AddTwoInts_Request_a();
}

}  // namespace my_robot_interface


namespace my_robot_interface
{

namespace srv
{

namespace builder
{

class Init_AddTwoInts_Response_sum
{
public:
  Init_AddTwoInts_Response_sum()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::my_robot_interface::srv::AddTwoInts_Response sum(::my_robot_interface::srv::AddTwoInts_Response::_sum_type arg)
  {
    msg_.sum = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interface::srv::AddTwoInts_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interface::srv::AddTwoInts_Response>()
{
  return my_robot_interface::srv::builder::Init_AddTwoInts_Response_sum();
}

}  // namespace my_robot_interface


namespace my_robot_interface
{

namespace srv
{

namespace builder
{

class Init_AddTwoInts_Event_response
{
public:
  explicit Init_AddTwoInts_Event_response(::my_robot_interface::srv::AddTwoInts_Event & msg)
  : msg_(msg)
  {}
  ::my_robot_interface::srv::AddTwoInts_Event response(::my_robot_interface::srv::AddTwoInts_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::my_robot_interface::srv::AddTwoInts_Event msg_;
};

class Init_AddTwoInts_Event_request
{
public:
  explicit Init_AddTwoInts_Event_request(::my_robot_interface::srv::AddTwoInts_Event & msg)
  : msg_(msg)
  {}
  Init_AddTwoInts_Event_response request(::my_robot_interface::srv::AddTwoInts_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_AddTwoInts_Event_response(msg_);
  }

private:
  ::my_robot_interface::srv::AddTwoInts_Event msg_;
};

class Init_AddTwoInts_Event_info
{
public:
  Init_AddTwoInts_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AddTwoInts_Event_request info(::my_robot_interface::srv::AddTwoInts_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_AddTwoInts_Event_request(msg_);
  }

private:
  ::my_robot_interface::srv::AddTwoInts_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::my_robot_interface::srv::AddTwoInts_Event>()
{
  return my_robot_interface::srv::builder::Init_AddTwoInts_Event_info();
}

}  // namespace my_robot_interface

#endif  // MY_ROBOT_INTERFACE__SRV__DETAIL__ADD_TWO_INTS__BUILDER_HPP_
