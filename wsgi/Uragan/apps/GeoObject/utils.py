# coding: utf-8


def convert_color_hex_to_kml(color):
    color.strip(' #')
    color = color if color else '#0000ff'
    r, g, b = color[1:3], color[3:5], color[5:7]
    line_color = 'ff' + b + g + r
    polygon_color = '7f' + b + g + r
    return line_color, polygon_color