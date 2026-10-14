import cv2
import numpy as np

img = cv2.imread('frontend/preview/assets/tribal_spider/tribal_full_transparent.png', cv2.IMREAD_UNCHANGED)
alpha = img[:, :, 3]
h, w = alpha.shape

left_mask = np.zeros_like(alpha)
left_mask[:, :479] = (alpha[:, :479] > 50).astype(np.uint8) * 255
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(left_mask)

l1_raw = np.isin(labels, [4, 48])
l2_raw = (labels == 25)
l3_raw = np.isin(labels, [134, 135])
l4_raw = np.isin(labels, [154, 209])

pivots = {
    'L1': [(440, 380), (418, 320), (405, 245)],
    'L2': [(440, 425), (390, 415), (320, 345)],
    'L3': [(440, 465), (360, 470), (285, 520)],
    'L4': [(440, 525), (395, 560), (360, 640)],
}

def add_joint_cap(mask, center, radius=8):
    cv2.circle(mask, center, radius, 255, -1)

# L1:
l1_s1 = (l1_raw & (np.indices(alpha.shape)[0] >= 322)).astype(np.uint8) * 255
add_joint_cap(l1_s1, pivots['L1'][0], 8)
add_joint_cap(l1_s1, pivots['L1'][1], 8)

l1_s2 = (l1_raw & (np.indices(alpha.shape)[0] >= 242) & (np.indices(alpha.shape)[0] <= 328)).astype(np.uint8) * 255
add_joint_cap(l1_s2, pivots['L1'][1], 8)
add_joint_cap(l1_s2, pivots['L1'][2], 8)

l1_s3 = (l1_raw & (np.indices(alpha.shape)[0] <= 248)).astype(np.uint8) * 255
add_joint_cap(l1_s3, pivots['L1'][2], 8)

# L2:
l2_s1 = (l2_raw & (np.indices(alpha.shape)[1] >= 388)).astype(np.uint8) * 255
add_joint_cap(l2_s1, pivots['L2'][0], 8)
add_joint_cap(l2_s1, pivots['L2'][1], 8)

l2_s2 = (l2_raw & (np.indices(alpha.shape)[1] >= 315) & (np.indices(alpha.shape)[1] <= 394)).astype(np.uint8) * 255
add_joint_cap(l2_s2, pivots['L2'][1], 8)
add_joint_cap(l2_s2, pivots['L2'][2], 8)

l2_s3 = (l2_raw & (np.indices(alpha.shape)[1] <= 322)).astype(np.uint8) * 255
add_joint_cap(l2_s3, pivots['L2'][2], 8)

# L3:
l3_s1 = (l3_raw & (np.indices(alpha.shape)[1] >= 358)).astype(np.uint8) * 255
add_joint_cap(l3_s1, pivots['L3'][0], 8)
add_joint_cap(l3_s1, pivots['L3'][1], 8)

l3_s2 = (l3_raw & (np.indices(alpha.shape)[1] >= 280) & (np.indices(alpha.shape)[1] <= 366)).astype(np.uint8) * 255
add_joint_cap(l3_s2, pivots['L3'][1], 8)
add_joint_cap(l3_s2, pivots['L3'][2], 8)

l3_s3 = (l3_raw & (np.indices(alpha.shape)[1] <= 288)).astype(np.uint8) * 255
add_joint_cap(l3_s3, pivots['L3'][2], 8)

# L4:
l4_s1 = (l4_raw & (np.indices(alpha.shape)[0] <= 564)).astype(np.uint8) * 255
add_joint_cap(l4_s1, pivots['L4'][0], 8)
add_joint_cap(l4_s1, pivots['L4'][1], 8)

l4_s2 = (l4_raw & (np.indices(alpha.shape)[0] >= 556) & (np.indices(alpha.shape)[0] <= 645)).astype(np.uint8) * 255
add_joint_cap(l4_s2, pivots['L4'][1], 8)
add_joint_cap(l4_s2, pivots['L4'][2], 8)

l4_s3 = (l4_raw & (np.indices(alpha.shape)[0] >= 638)).astype(np.uint8) * 255
add_joint_cap(l4_s3, pivots['L4'][2], 8)

def mask_to_svg_path(mask, approx_eps=0.6):
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    if not contours:
        return ""
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    d_list = []
    for c in contours:
        if cv2.contourArea(c) < 25:
            continue
        approx = cv2.approxPolyDP(c, approx_eps, True)
        pts = approx.reshape(-1, 2)
        if len(pts) < 3:
            continue
        sub_d = f"M {pts[0][0]} {pts[0][1]} " + " ".join([f"L {p[0]} {p[1]}" for p in pts[1:]]) + " Z"
        d_list.append(sub_d)
    return " ".join(d_list)

paths = {
    'L1_s1': mask_to_svg_path(l1_s1),
    'L1_s2': mask_to_svg_path(l1_s2),
    'L1_s3': mask_to_svg_path(l1_s3),
    'L2_s1': mask_to_svg_path(l2_s1),
    'L2_s2': mask_to_svg_path(l2_s2),
    'L2_s3': mask_to_svg_path(l2_s3),
    'L3_s1': mask_to_svg_path(l3_s1),
    'L3_s2': mask_to_svg_path(l3_s2),
    'L3_s3': mask_to_svg_path(l3_s3),
    'L4_s1': mask_to_svg_path(l4_s1),
    'L4_s2': mask_to_svg_path(l4_s2),
    'L4_s3': mask_to_svg_path(l4_s3),
}

# Mirror a path across midline X=479
# For an SVG path string "M x y L x y ... Z", mirrored x' = 958 - x
import re
def mirror_path(path_str):
    def repl(match):
        x = float(match.group(1))
        y = float(match.group(2))
        return f"{958 - x:.1f} {y:.1f}"
    # Match pairs of numbers: command (M|L) x y
    # Actually split by tokens:
    tokens = path_str.split()
    out = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ['M', 'L']:
            x = float(tokens[i+1])
            y = float(tokens[i+2])
            out.append(f"{t} {958 - x:.1f} {y:.1f}")
            i += 3
        elif t == 'Z':
            out.append('Z')
            i += 1
        else:
            i += 1
    return " ".join(out)

for leg in ['L1', 'L2', 'L3', 'L4']:
    r_leg = 'R' + leg[1]
    for seg in ['s1', 's2', 's3']:
        paths[f'{r_leg}_{seg}'] = mirror_path(paths[f'{leg}_{seg}'])

print("Generated all paths for L1..L4 and R1..R4 successfully!")
for k in paths:
    print(f"{k}: {len(paths[k])} chars")
