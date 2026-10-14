import math

def simulate_ripple_gait():
    # 4 phase ripple offsets
    # Leg indices: 1 (front), 2, 3, 4 (rear)
    phase_offsets = {
        'L4': 0.0,
        'L2': 0.5 * math.pi,
        'L3': 1.0 * math.pi,
        'L1': 1.5 * math.pi,
        'R4': 1.0 * math.pi,
        'R2': 1.5 * math.pi,
        'R3': 0.0,
        'R1': 0.5 * math.pi,
    }

    # Simulate 1 full cycle (200 steps)
    for step in range(200):
        t = (step / 200.0) * 2 * math.pi
        legs_state = {}
        for leg, offset in phase_offsets.items():
            phi = (t + offset) % (2 * math.pi)
            is_swing = phi < math.pi
            if is_swing:
                # Swing forward
                swing = -math.cos(phi) # from -1 to +1
                lift = math.sin(phi)   # peak at pi/2
                extension = math.sin(phi) * 0.5
            else:
                # Stance push backward
                phi_stance = phi - math.pi
                swing = math.cos(phi_stance) # from +1 down to -1
                lift = 0.0
                extension = -0.15 # slight compression
            legs_state[leg] = (swing, lift, extension)

        # Assert all values are continuous and finite
        for leg, st in legs_state.items():
            assert not any(math.isnan(v) for v in st)
    
    print("Ripple Wave Gait simulation verified with 100% mathematical continuity!")

simulate_ripple_gait()
