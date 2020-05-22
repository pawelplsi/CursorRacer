from __future__ import print_function

import hid
import time

# enumerate USB devices

# for d in hid.enumerate():
#     keys = list(d.keys())
#     keys.sort()
#     for key in keys:
#         print("%s : %s" % (key, d[key]))
#     print()

# try opening a device, then perform write and read

try:
    print("Opening the device")

    device_info = hid.enumerate()[2]
    print(device_info)
    device = hid.Device(device_info['vendor_id'], device_info['product_id']
                        )  # TREZOR VendorID/ProductID

    # print(device.read(69)) # co to?
    # print("Manufacturer: %s" % device.get_feature_report())
    print("Read the data")
    while True:
        data = device.read(64)
        if data:
            print(data[0] & 1)
            print(data[0] & 2)
            print(data[0] & 4)
            print(data)
        else:
            break

    exit(69)
    print("Product: %s" % device.get_product_string())
    print("Serial No: %s" % device.get_serial_number_string())

    # enable non-blocking mode
    device.set_nonblocking(1)

    # write some data to the device
    # print("Write the data")
    # device.write([0, 63, 35, 35] + [0] * 61) +

    # wait
    time.sleep(0.05)

    # read back the answer

    print("Closing the device")
    device.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard coded device. Update the hid.device line")
    print("in this script with one from the enumeration list output above and try again.")

print("Done")
