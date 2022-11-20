// Generated by gencpp from file astra_camera/SetUVCGainResponse.msg
// DO NOT EDIT!


#ifndef ASTRA_CAMERA_MESSAGE_SETUVCGAINRESPONSE_H
#define ASTRA_CAMERA_MESSAGE_SETUVCGAINRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace astra_camera
{
template <class ContainerAllocator>
struct SetUVCGainResponse_
{
  typedef SetUVCGainResponse_<ContainerAllocator> Type;

  SetUVCGainResponse_()
    {
    }
  SetUVCGainResponse_(const ContainerAllocator& _alloc)
    {
  (void)_alloc;
    }







  typedef boost::shared_ptr< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> const> ConstPtr;

}; // struct SetUVCGainResponse_

typedef ::astra_camera::SetUVCGainResponse_<std::allocator<void> > SetUVCGainResponse;

typedef boost::shared_ptr< ::astra_camera::SetUVCGainResponse > SetUVCGainResponsePtr;
typedef boost::shared_ptr< ::astra_camera::SetUVCGainResponse const> SetUVCGainResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::astra_camera::SetUVCGainResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


} // namespace astra_camera

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const ::astra_camera::SetUVCGainResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd41d8cd98f00b204ULL;
  static const uint64_t static_value2 = 0xe9800998ecf8427eULL;
};

template<class ContainerAllocator>
struct DataType< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "astra_camera/SetUVCGainResponse";
  }

  static const char* value(const ::astra_camera::SetUVCGainResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "\n"
;
  }

  static const char* value(const ::astra_camera::SetUVCGainResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream&, T)
    {}

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SetUVCGainResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::astra_camera::SetUVCGainResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream&, const std::string&, const ::astra_camera::SetUVCGainResponse_<ContainerAllocator>&)
  {}
};

} // namespace message_operations
} // namespace ros

#endif // ASTRA_CAMERA_MESSAGE_SETUVCGAINRESPONSE_H
