import math

# Simple 2D water rocket trajectory simulator
# Units: SI (m, s, kg, Pa)

def simulate(
    total_time=10.0,
    dt=0.01,
    bottle_volume=2e-3,     # m^3 (2L)
    water_mass=1.0,         # kg initial water mass
    bottle_mass=0.2,        # kg empty bottle mass
    air_pressure=5e5,       # Pa (absolute pressure inside bottle)
    nozzle_diameter=0.022,  # m
    angle_deg=45,
):
    g = 9.81
    rho_w = 1000.0
    gamma = 1.4
    Cd = 0.8
    P_atm = 1e5

    angle = math.radians(angle_deg)
    A_nozzle = math.pi * (nozzle_diameter / 2) ** 2

    # initial air volume
    V_air = bottle_volume - water_mass / rho_w
    if V_air <= 0:
        raise ValueError("Not enough volume for water")
    # pressure-volume constant (assuming adiabatic expansion)
    PV_const = air_pressure * (V_air ** gamma)

    mass = bottle_mass + water_mass
    x = y = 0.0
    vx = vy = 0.0

    t = 0.0
    data = []
    while t < total_time and y >= 0:
        if water_mass > 0:
            P = PV_const / (V_air ** gamma)
            if P <= P_atm:
                thrust = 0.0
                m_dot = 0.0
            else:
                v_e = math.sqrt(2 * (P - P_atm) / rho_w)
                m_dot = Cd * A_nozzle * rho_w * v_e
                thrust = m_dot * v_e
                dm = m_dot * dt
                if dm > water_mass:
                    dm = water_mass
                water_mass -= dm
                mass -= dm
                V_air = bottle_volume - water_mass / rho_w
        else:
            thrust = 0.0
            m_dot = 0.0

        ax = (thrust * math.cos(angle)) / mass
        ay = (thrust * math.sin(angle)) / mass - g

        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        data.append((t, x, y, vx, vy, mass))

        t += dt
        if y < 0:
            break
    return data


def main():
    data = simulate()
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; printing final state only")
        print("Final position: x={:.2f} m, y={:.2f} m".format(data[-1][1], data[-1][2]))
        return

    xs = [d[1] for d in data]
    ys = [d[2] for d in data]
    plt.plot(xs, ys)
    plt.xlabel('x (m)')
    plt.ylabel('y (m)')
    plt.title('Water Rocket Trajectory')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
