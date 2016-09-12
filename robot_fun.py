
def map_angle(angle):
    angle_in_circle = angle % 360
    angle_symmetry = angle_in_circle - (360/2)
    angle_normal = angle_symmetry / (360/2)
    return angle_normal