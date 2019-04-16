from ctypes import *
from ctypes.wintypes import BOOL, DWORD, HANDLE, LPCWSTR, LPCVOID, LPVOID

jpeg_dll = cdll.LoadLibrary("utils/xy2res.dll")

jpeg_dll.jpeg_to_rgb.argtype = [c_char_p, c_int]
jpeg_dll.jpeg_to_rgb.restype = POINTER(c_char * 230400)

jpeg_dll.mapx_to_rgb.argtype = [c_void_p, c_int]
jpeg_dll.mapx_to_rgb.restype = POINTER(c_char * 230400)

jpeg_dll.read_color_palette.argtype = c_void_p
jpeg_dll.read_color_palette.restype = POINTER(c_char * 1024)


def read_pic(data, pic, color_board_origin, color_board):
    jpeg_dll.read_pic.argtype = [c_void_p, c_void_p, c_void_p]
    _size = pic.width * pic.height * 4
    jpeg_dll.read_pic.restype = POINTER(c_char * _size)
    return jpeg_dll.read_pic(data, color_board_origin, color_board)
    # _bytes = res.contents.raw
    # return _bytes


def delete_me(data):
    jpeg_dll.delete_me.argtype = c_void_p
    jpeg_dll.delete_me(data)


def read_new_map_to_rgb(data):
    res = jpeg_dll.jpeg_to_rgb(data, len(data))
    _bytes = res.contents.raw
    jpeg_dll.free_rgb_data()
    return _bytes


def read_old_map_to_rgb(data):
    res = jpeg_dll.mapx_to_rgb(data, len(data))
    _bytes = res.contents.raw
    jpeg_dll.free_rgb_data()
    return _bytes


def decompress_mask(data, out_size):
    jpeg_dll.decompress_mask.argtype = [c_void_p, c_int]
    jpeg_dll.decompress_mask.restype = POINTER(c_char*(out_size*4))
    res = jpeg_dll.decompress_mask(data, out_size)
    _bytes = res.contents.raw
    jpeg_dll.free_temp_data()
    return _bytes


def read_color_palette(data):
    res = jpeg_dll.read_color_palette(data)
    _bytes = res.contents.raw
    return _bytes
