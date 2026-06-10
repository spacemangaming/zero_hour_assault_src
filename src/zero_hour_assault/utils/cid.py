import hashlib
import platform
import psutil
import uuid
import os

def hash_mac_address(mac_address_bytes):
    hash_val = 0
    for i in range(len(mac_address_bytes)):
        hash_val += (mac_address_bytes[i] << ((i & 1) * 8))
    return hash_val

def get_mac_hash():
    mac1 = 0
    mac2 = 0
    mac_addresses = []
    for interface_name, interface_addresses in psutil.net_if_addrs().items():
        for addr in interface_addresses:
            if addr.family == psutil.AF_LINK:
                mac_bytes = addr.address.replace('-', '').replace(':', '').lower()
                if mac_bytes != '000000000000': #ignore all zero mac address
                    mac_addresses.append(bytes.fromhex(mac_bytes))

    if mac_addresses:
        mac1 = hash_mac_address(mac_addresses[0])
    if len(mac_addresses) > 1:
        mac2 = hash_mac_address(mac_addresses[1])

    if mac1 > mac2:
        mac1, mac2 = mac2, mac1
    return mac1, mac2

def get_volume_hash():
    vol_hash = 0
    system_platform = platform.system()
    if system_platform == "Windows":
        import ctypes
        serial = ctypes.c_ulong(0)
        ctypes.windll.kernel32.GetVolumeInformationW(
            ctypes.c_wchar_p("C:\\"), None, 0,
            ctypes.byref(serial), None, None, None, 0
        )
        serial_num = serial.value
        vol_hash = (serial_num + (serial_num >> 16)) & 0xFFFF
        return vol_hash
    elif system_platform == "Darwin": # macOS
        try:
            serial_number = get_system_serial_number_mac()
            if serial_number:
                for i, char in enumerate(serial_number):
                    vol_hash += ord(char) << ((i & 1) * 8)
                return vol_hash
        except Exception:
            pass # Fallback to machine name if serial number fails
        machine_name = platform.node()
        for i, char in enumerate(machine_name):
            vol_hash += ord(char) << ((i & 1) * 8)
        return vol_hash

    else: # Linux and other Unix-like
        machine_name = platform.node()
        for i, char in enumerate(machine_name):
            vol_hash += ord(char) << ((i & 1) * 8)
        return vol_hash
    return vol_hash

def get_cpu_hash():
    cpu_info_string = platform.processor()
    if not cpu_info_string:
        cpu_info_string = str(psutil.cpu_count(logical=False)) + "_" + str(psutil.cpu_count(logical=True)) #Fallback if processor name is empty

    cpu_hash_val = 0
    for i, char in enumerate(cpu_info_string):
        cpu_hash_val += ord(char) << ((i & 1) * 8)
    return cpu_hash_val


def get_machine_name():
    return platform.node()

def generate_hash(byte_string):
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    stream_str = ""
    size = len(byte_string)
    for i in range(size):
        ch_val = ~((byte_string[i] + byte_string[(i + 1) % size] + byte_string[(i + 2) % size] + byte_string[(i + 3) % size]) & 0xFF) * (i + 1)
        ch2_index = (ch_val >> 4) & 63 # Use 63 instead of 62 to stay within chars range
        if ch2_index >= len(chars):
            ch2_index = 5 # Fallback if index out of bounds, similar to C++'s if (ch2 == 0) ch2 = 5; which can happen due to modulo 62 in original
        ch2 = chars[ch2_index]
        ch_index = ch_val & 63 # Use 63 instead of 62
        if ch_index >= len(chars):
            ch_index = 5 # Fallback if index out of bounds
        stream_str += ch2 + chars[ch_index]
    return stream_str


def generate_system_fingerprint_legacy1(identifier=""):
    mac1, mac2 = get_mac_hash()
    cpu_hash_val = get_cpu_hash()
    volume_hash_val = get_volume_hash()

    combined_string = str(mac1) + str(mac2) + str(cpu_hash_val) + str(volume_hash_val) + identifier
    sha256_hash = hashlib.sha256(combined_string.encode()).digest()
    return generate_hash(sha256_hash)

def generate_computer_id(identifier=""):
    ram_size = psutil.virtual_memory().total
    processor_arch_info = ""
    system_platform = platform.system()
    if system_platform == "Windows":
        processor_arch_info = os.environ.get("NUMBER_OF_PROCESSORS", "") + " " + \
                              os.environ.get("PROCESSOR_ARCHITECTURE", "") + " " + \
                              os.environ.get("PROCESSOR_IDENTIFIER", "") + " " + \
                              os.environ.get("PROCESSOR_LEVEL", "") + " " + \
                              os.environ.get("PROCESSOR_REVISION", "")
    else: # Approximation for other platforms. Could be improved for specific OSes.
        processor_arch_info = platform.machine() + " " + platform.architecture()[0]

    cpu_hash_val = get_cpu_hash()
    volume_hash_val = get_volume_hash()

    combined_string = str(ram_size) + processor_arch_info + str(cpu_hash_val) + str(volume_hash_val) + identifier
    sha256_hash = hashlib.sha256(combined_string.encode()).digest()
    return generate_hash(sha256_hash)


# macOS specific function to get system serial number (requires PyObjC installation - pip install pyobjc)
def get_system_serial_number_mac():
    if platform.system() != "Darwin":
        return None
    try:
        import objc
        io_service = objc.io_service_get_matching_services
        master_port = objc.mach_port_name_t(objc.kIOMasterPortDefault)
        serial_number = None
        platform_expert_device = io_service(master_port, objc.IOServiceMatching(b"IOPlatformExpertDevice"))
        if platform_expert_device:
            platform_expert_device = objc.IORegistryEntryIDMatching(platform_expert_device, objc.kIOPlatformSerialNumberKey)
            if platform_expert_device:
                serial_number_cfstring = objc.IORegistryEntryCreateCFProperty(platform_expert_device, objc.CFSTR(objc.kIOPlatformSerialNumberKey), objc.kCFAllocatorDefault, 0)
                if serial_number_cfstring:
                    serial_number = str(serial_number_cfstring)
                    objc.CFRelease(serial_number_cfstring)
                objc.IOObjectRelease(platform_expert_device)
            objc.IOObjectRelease(platform_expert_device)
        return serial_number
    except ImportError:
        print("PyObjC is not installed. System serial number might not be available on macOS.")
        return None
    except Exception as e:
        print(f"Error getting system serial number on macOS: {e}")
        return None


