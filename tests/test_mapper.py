from custom_components.wink_local.device_mapper import WinkDeviceMapper
def test_light_mapping():
 d=WinkDeviceMapper().map_device({"hub_device_id":"28","local_id":28,"name":"Lamp","last_reading":{"connection":True,"powered":True,"brightness":0.5}})
 assert WinkDeviceMapper().platform_for(d)=="light"
