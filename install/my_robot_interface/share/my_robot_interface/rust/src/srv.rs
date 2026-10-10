#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to my_robot_interface__srv__AddTwoInts_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AddTwoInts_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub a: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub b: i64,

}



impl Default for AddTwoInts_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AddTwoInts_Request::default())
  }
}

impl rosidl_runtime_rs::Message for AddTwoInts_Request {
  type RmwMsg = super::srv::rmw::AddTwoInts_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        a: msg.a,
        b: msg.b,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      a: msg.a,
      b: msg.b,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      a: msg.a,
      b: msg.b,
    }
  }
}


// Corresponds to my_robot_interface__srv__AddTwoInts_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AddTwoInts_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub sum: i64,

}



impl Default for AddTwoInts_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::AddTwoInts_Response::default())
  }
}

impl rosidl_runtime_rs::Message for AddTwoInts_Response {
  type RmwMsg = super::srv::rmw::AddTwoInts_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        sum: msg.sum,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      sum: msg.sum,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      sum: msg.sum,
    }
  }
}


// Corresponds to my_robot_interface__srv__SetLed_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLed_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub led_number: i64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub state: bool,

}



impl Default for SetLed_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetLed_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SetLed_Request {
  type RmwMsg = super::srv::rmw::SetLed_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        led_number: msg.led_number,
        state: msg.state,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      led_number: msg.led_number,
      state: msg.state,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      led_number: msg.led_number,
      state: msg.state,
    }
  }
}


// Corresponds to my_robot_interface__srv__SetLed_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SetLed_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SetLed_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SetLed_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SetLed_Response {
  type RmwMsg = super::srv::rmw::SetLed_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
    }
  }
}






#[link(name = "my_robot_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__my_robot_interface__srv__AddTwoInts() -> *const std::ffi::c_void;
}

// Corresponds to my_robot_interface__srv__AddTwoInts
#[allow(missing_docs, non_camel_case_types)]
pub struct AddTwoInts;

impl rosidl_runtime_rs::Service for AddTwoInts {
    type Request = AddTwoInts_Request;
    type Response = AddTwoInts_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__my_robot_interface__srv__AddTwoInts() }
    }
}




#[link(name = "my_robot_interface__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__my_robot_interface__srv__SetLed() -> *const std::ffi::c_void;
}

// Corresponds to my_robot_interface__srv__SetLed
#[allow(missing_docs, non_camel_case_types)]
pub struct SetLed;

impl rosidl_runtime_rs::Service for SetLed {
    type Request = SetLed_Request;
    type Response = SetLed_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__my_robot_interface__srv__SetLed() }
    }
}


