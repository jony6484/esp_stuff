import math

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

def scale(v, s):
    return (v[0] * s, v[1] * s)

def norm(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def forward_kinematics(theta1_deg, theta2_deg, A, L1, L2, L3, L4, L5, K):
    theta1 = math.radians(theta1_deg)
    theta2 = math.radians(theta2_deg)
    B = [L5, 0]
    C = add(A, [L1 * math.cos(theta1),
                L1 * math.sin(theta1)])
    
    D = add(B, [L2 * math.cos(theta2),
                L2 * math.sin(theta2)])

    CD = sub(D, C)
    d_cd = norm(CD)
    alpha_cd = math.atan2(CD[1], CD[0])

    alpha_a = math.acos((d_cd**2 + L3**2 - L4**2) / (2 * L3 * d_cd))
    theta3 = alpha_cd + alpha_a

    E = add(C, [L3 * math.cos(theta3),
                L3 * math.sin(theta3)])
    DE = sub(E, D)

    k = (K + L4) / L4
    DP = scale(DE, k)
    P = add(DP, D)

    return A, B, C, D, E, P

def backward_kinematics(x, y, A, L1, L2, L3, L4, L5, K):
    B = [L5, 0]
    P = [x, y]
    
    BP = sub(P, B)
    alpha_bp = math.atan2(BP[1], BP[0])
    d_bp = norm(BP)

    alpha_2 = math.acos((L2**2 + d_bp**2 - (L4 + K)**2) / (2 * L2 * d_bp))
    theta2 = alpha_bp - alpha_2

    D = add(B, [L2 * math.cos(theta2),
                L2 * math.sin(theta2)])
    DP = sub(P, D)

    k = L4 / (L4 + K)
    DE = scale(DP, k)
    E = add(DE, D)

    AE = sub(E, A)
    d_ae = norm(AE)
    alpha_ae = math.atan2(AE[1], AE[0])

    alpha_1 = math.acos((L1**2 + d_ae**2 - L3**2) / (2 * L1 * d_ae))
    theta1 = alpha_ae + alpha_1

    return math.degrees(theta1), math.degrees(theta2)

def insert_points(points, N):
    """
    Inserts N equally spaced points between each pair of consecutive points.

    Args:
        points (list of [x, y]): List of points (at least 2).
        N (int): Number of points to insert between each pair.

    Returns:
        list of [x, y]: New list of points including the inserted ones.
    """
    new_points = []

    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        # Always include the starting point
        new_points.append([x1, y1])
        # Add N equally spaced points
        for j in range(1, N + 1):
            t = j / (N + 1)
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            new_points.append([x, y])

    # Add the final point
    new_points.append(points[-1])
    return new_points
