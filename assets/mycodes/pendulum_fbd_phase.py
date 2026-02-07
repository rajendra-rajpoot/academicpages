import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp

# ----------------------------------------------------
# Physical parameters
# ----------------------------------------------------
g = 9.81
l = 0.9

# Initial conditions
theta0 = np.deg2rad(39.64)
omega0 = -1.17

tmax = 3.85
dt = 0.02
t_eval = np.arange(0.0, tmax, dt)

# ----------------------------------------------------
# Pendulum equations
# ----------------------------------------------------
def pendulum(t, y):
    theta, omega = y
    return [omega, -(g/l)*np.sin(theta)]

sol = solve_ivp(
    pendulum,
    [0, tmax],
    [theta0, omega0],
    t_eval=t_eval,
    rtol=1e-9
)

theta = sol.y[0]
omega = sol.y[1]
t = sol.t

# ----------------------------------------------------
# Geometry
# ----------------------------------------------------
x = l*np.sin(theta)
y = -l*np.cos(theta)

# ----------------------------------------------------
# Figure
# ----------------------------------------------------
fig = plt.figure(figsize=(12, 5.8))

ax_phase = plt.subplot2grid((1, 2), (0, 0))
ax_pend  = plt.subplot2grid((1, 2), (0, 1))

# ----------------------------------------------------
# Phase space panel
# ----------------------------------------------------
ax_phase.set_title('Phase space')
ax_phase.set_xlabel(r'$\theta$ (rad)')
ax_phase.set_ylabel(r'$\omega$ (rad s$^{-1}$)')

ax_phase.set_xlim(1.2*np.min(theta), 1.2*np.max(theta))
ax_phase.set_ylim(1.2*np.min(omega), 1.2*np.max(omega))

phase_traj, = ax_phase.plot([], [], lw=2)
state_vec,  = ax_phase.plot([], [], lw=3, color='orange')

# ----------------------------------------------------
# Pendulum panel
# ----------------------------------------------------
ax_pend.set_aspect('equal')
ax_pend.set_xlim(-1.2*l, 1.2*l)
ax_pend.set_ylim(-1.2*l, 0.3*l)
ax_pend.axis('off')

rod, = ax_pend.plot([], [], lw=3)
bob, = ax_pend.plot([], [], 'o', ms=10)

# theta visual arc
theta_arc, = ax_pend.plot([], [], color='green', lw=2)
theta_label = ax_pend.text(0, 0, r'$\theta$', fontsize=12, color='green')

# ----------------------------------------------------
# Boxed equations
# ----------------------------------------------------
eq_text = ax_pend.text(
    -1.1*l, 0.45*l,
    r'$\frac{d^2\theta}{dt^2}=-\frac{g}{\ell}\sin\theta$'
    '\n'
    r'$\omega=\frac{d\theta}{dt}$',
    fontsize=14,
    bbox=dict(boxstyle='round', fc='white', ec='black')
)

# live values
info_text = ax_pend.text(
    -0.0, 0.95, '',
    transform=ax_pend.transAxes,
    va='top',
    fontsize=11
)

# ----------------------------------------------------
# Free-body diagram artists
# ----------------------------------------------------
fbd_g, = ax_pend.plot([], [], lw=2, color='tab:blue')
fbd_T, = ax_pend.plot([], [], lw=2, color='tab:red')

fbd_g_text = ax_pend.text(0, 0, r'$mg$', fontsize=11)
fbd_T_text = ax_pend.text(0, 0, r'$T$',  fontsize=11)

# ----------------------------------------------------
# Init
# ----------------------------------------------------
def init():
    phase_traj.set_data([], [])
    state_vec.set_data([], [])

    rod.set_data([], [])
    bob.set_data([], [])

    theta_arc.set_data([], [])
    theta_label.set_position((0, 0))

    fbd_g.set_data([], [])
    fbd_T.set_data([], [])

    fbd_g_text.set_position((0, 0))
    fbd_T_text.set_position((0, 0))

    info_text.set_text('')

    return (phase_traj, state_vec,
            rod, bob,
            theta_arc, theta_label,
            fbd_g, fbd_T,
            fbd_g_text, fbd_T_text,
            info_text)

# ----------------------------------------------------
# Update
# ----------------------------------------------------
def update(i):

    if i >= len(t):
        i = len(t) - 1

    # -------------------------
    # phase space
    # -------------------------
    phase_traj.set_data(theta[:i+1], omega[:i+1])
    state_vec.set_data([0, theta[i]], [0, omega[i]])

    # -------------------------
    # pendulum
    # -------------------------
    xb = x[i]
    yb = y[i]

    rod.set_data([0, xb], [0, yb])
    bob.set_data([xb], [yb])

    # -------------------------
    # theta arc (visual)
    # -------------------------
    r_arc = 0.25*l
    ang = theta[i]

    a = np.linspace(0.0, ang, 60)

    xarc = r_arc*np.sin(a)
    yarc = -r_arc*np.cos(a)

    theta_arc.set_data(xarc, yarc)

    am = 0.5*ang
    theta_label.set_position(
        (r_arc*np.sin(am), -r_arc*np.cos(am))
    )

    # -------------------------
    # info
    # -------------------------
    info_text.set_text(
        r'$\theta = %.3f\ \mathrm{rad}\ (\ %.2f^\circ)$' % (theta[i], np.rad2deg(theta[i])) + ', ' +
        r'$\omega = %.2f\ \mathrm{rad/s}$' % omega[i]
    )

    # -------------------------
    # free-body diagram
    # -------------------------
    s = 0.18*l

    ex = np.sin(theta[i])
    ey = -np.cos(theta[i])

    # gravity
    fbd_g.set_data([xb, xb], [yb, yb - s])

    # tension
    fbd_T.set_data([xb, xb - s*ex], [yb, yb - s*ey])

    fbd_g_text.set_position((xb + 0.02, yb - s - 0.02))
    fbd_T_text.set_position((xb - s*ex - 0.05, yb - s*ey))

    return (phase_traj, state_vec,
            rod, bob,
            theta_arc, theta_label,
            fbd_g, fbd_T,
            fbd_g_text, fbd_T_text,
            info_text)

# ----------------------------------------------------
# Animation
# ----------------------------------------------------
ani = FuncAnimation(
    fig, update,
    frames=range(len(t)),
    init_func=init,
    blit=True
)

# ----------------------------------------------------
# Save GIF
# ----------------------------------------------------
writer = PillowWriter(fps=20)
ani.save("pendulum_phase_fbd_theta.gif", writer=writer)

# plt.show()
















exit()




import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from scipy.integrate import solve_ivp

# ----------------------------------------------------
# Physical parameters
# ----------------------------------------------------
g = 9.81
l = 0.9

# Initial conditions (as in your figure)
theta0 = np.deg2rad(39.64)
omega0 = -1.17

tmax = 0.85
dt = 0.02
t_eval = np.arange(0.0, tmax, dt)

# ----------------------------------------------------
# Pendulum equations
# ----------------------------------------------------
def pendulum(t, y):
    theta, omega = y
    return [omega, -(g/l)*np.sin(theta)]

sol = solve_ivp(
    pendulum,
    [0, tmax],
    [theta0, omega0],
    t_eval=t_eval,
    rtol=1e-9
)

theta = sol.y[0]
omega = sol.y[1]
t = sol.t

# ----------------------------------------------------
# Geometry
# ----------------------------------------------------
x = l*np.sin(theta)
y = -l*np.cos(theta)

# ----------------------------------------------------
# Figure
# ----------------------------------------------------
fig = plt.figure(figsize=(12, 5.8))

ax_phase = plt.subplot2grid((1, 2), (0, 0))
ax_pend  = plt.subplot2grid((1, 2), (0, 1))

# ----------------------------------------------------
# Phase space panel
# ----------------------------------------------------
ax_phase.set_title('Phase space')
ax_phase.set_xlabel(r'$\theta$ (rad)')
ax_phase.set_ylabel(r'$\omega$ (rad s$^{-1}$)')

ax_phase.set_xlim(1.2*np.min(theta), 1.2*np.max(theta))
ax_phase.set_ylim(1.2*np.min(omega), 1.2*np.max(omega))

phase_traj, = ax_phase.plot([], [], lw=2)
state_vec,  = ax_phase.plot([], [], lw=3, color='orange')

# ----------------------------------------------------
# Pendulum panel
# ----------------------------------------------------
ax_pend.set_aspect('equal')
ax_pend.set_xlim(-1.2*l, 1.2*l)
ax_pend.set_ylim(-1.2*l, 0.3*l)
ax_pend.axis('off')

rod, = ax_pend.plot([], [], lw=3)
bob, = ax_pend.plot([], [], 'o', ms=10)

# ----------------------------------------------------
# Boxed equations
# ----------------------------------------------------
eq_text = ax_pend.text(
    -1.1*l, 0.45*l,
    r'$\frac{d^2\theta}{dt^2}=-\frac{g}{\ell}\sin\theta$'
    '\n'
    r'$\omega=\frac{d\theta}{dt}$',
    fontsize=14,
    bbox=dict(boxstyle='round', fc='white', ec='black')
)


# live values
info_text = ax_pend.text(
    -0.0, 0.95, '',
    transform=ax_pend.transAxes,
    va='top',
    fontsize=11
)

# ----------------------------------------------------
# Free-body diagram artists
# ----------------------------------------------------
fbd_g, = ax_pend.plot([], [], lw=2, color='tab:blue')
fbd_T, = ax_pend.plot([], [], lw=2, color='tab:red')

fbd_g_text = ax_pend.text(0, 0, r'$mg$', fontsize=11)
fbd_T_text = ax_pend.text(0, 0, r'$T$',  fontsize=11)

# ----------------------------------------------------
# Init
# ----------------------------------------------------
def init():
    phase_traj.set_data([], [])
    state_vec.set_data([], [])

    rod.set_data([], [])
    bob.set_data([], [])

    fbd_g.set_data([], [])
    fbd_T.set_data([], [])

    fbd_g_text.set_position((0, 0))
    fbd_T_text.set_position((0, 0))

    info_text.set_text('')

    return (phase_traj, state_vec,
            rod, bob,
            fbd_g, fbd_T,
            fbd_g_text, fbd_T_text,
            info_text)

# ----------------------------------------------------
# Update
# ----------------------------------------------------
def update(i):

    if i >= len(t):
        i = len(t) - 1

    # -------------------------
    # phase space
    # -------------------------
    phase_traj.set_data(theta[:i+1], omega[:i+1])
    state_vec.set_data([0, theta[i]], [0, omega[i]])

    # -------------------------
    # pendulum
    # -------------------------
    xb = x[i]
    yb = y[i]

    rod.set_data([0, xb], [0, yb])
    bob.set_data([xb], [yb])

    # -------------------------
    # info
    # -------------------------
    info_text.set_text(
        r'$\theta = %.3f\ \mathrm{rad}\ (\ %.2f^\circ)$' % (theta[i], np.rad2deg(theta[i])) + ',' + ' ' +
        r'$\omega = %.2f\ \mathrm{rad/s}$' % omega[i]
    )

    # -------------------------
    # free-body diagram
    # -------------------------
    s = 0.18*l

    ex = np.sin(theta[i])
    ey = -np.cos(theta[i])

    # gravity
    fbd_g.set_data([xb, xb], [yb, yb - s])

    # tension (toward pivot)
    fbd_T.set_data([xb, xb - s*ex], [yb, yb - s*ey])

    fbd_g_text.set_position((xb + 0.02, yb - s - 0.02))
    fbd_T_text.set_position((xb - s*ex - 0.05, yb - s*ey))

    return (phase_traj, state_vec,
            rod, bob,
            fbd_g, fbd_T,
            fbd_g_text, fbd_T_text,
            info_text)

# ----------------------------------------------------
# Animation
# ----------------------------------------------------
ani = FuncAnimation(
    fig, update,
    frames=range(len(t)),
    init_func=init,
    blit=True
)


# ----------------------------------------------------
# Save GIF
# ----------------------------------------------------
writer = PillowWriter(fps=20)
ani.save("pendulum_phase_fbd.gif", writer=writer)

plt.show()



# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation, PillowWriter
# from scipy.integrate import solve_ivp

# # ---------------------------------------------------
# # Parameters
# # ---------------------------------------------------
# g = 9.81
# l = 0.9

# # initial conditions
# theta0 = np.deg2rad(39.64)   # rad
# omega0 = -1.17              # rad/s

# tmax = 2.0
# dt   = 0.02
# t_eval = np.arange(0, tmax, dt)

# # ---------------------------------------------------
# # Pendulum ODE
# # ---------------------------------------------------
# def pendulum(t, y):
#     theta, omega = y
#     dtheta = omega
#     domega = -(g/l)*np.sin(theta)
#     return [dtheta, domega]

# sol = solve_ivp(pendulum, [0, tmax],
#                 [theta0, omega0],
#                 t_eval=t_eval, rtol=1e-9)

# theta = sol.y[0]
# omega = sol.y[1]
# t     = sol.t

# # ---------------------------------------------------
# # Geometry of pendulum
# # ---------------------------------------------------
# x = l*np.sin(theta)
# y = -l*np.cos(theta)

# # ---------------------------------------------------
# # Figure layout
# # ---------------------------------------------------
# fig = plt.figure(figsize=(10,5))

# # phase space
# ax_phase = plt.subplot2grid((1,2),(0,0))

# # pendulum
# ax_pend  = plt.subplot2grid((1,2),(0,1))

# # ---------------------------------------------------
# # Phase space (theta, omega)
# # ---------------------------------------------------
# ax_phase.set_xlim(np.min(theta)*1.2, np.max(theta)*1.2)
# ax_phase.set_ylim(np.min(omega)*1.2, np.max(omega)*1.2)

# ax_phase.set_xlabel(r'$\theta$ (rad)')
# ax_phase.set_ylabel(r'$\omega$ (rad s$^{-1}$)')
# ax_phase.set_title('Phase space')

# phase_traj, = ax_phase.plot([], [], lw=2)
# state_vec,  = ax_phase.plot([], [], lw=3, color='orange')

# # ---------------------------------------------------
# # Pendulum axis
# # ---------------------------------------------------
# ax_pend.set_aspect('equal')
# ax_pend.set_xlim(-1.1*l, 1.1*l)
# ax_pend.set_ylim(-1.1*l, 0.2*l)
# ax_pend.axis('off')

# rod, = ax_pend.plot([], [], lw=3)
# bob, = ax_pend.plot([], [], 'o', markersize=12)

# # ---------------------------------------------------
# # Governing equation text
# # ---------------------------------------------------
# eq_text = ax_pend.text(-1.0*l, 0.6*l,
#         r'$\dfrac{d^2\theta}{dt^2}=-\dfrac{g}{\ell}\sin\theta$',
#         fontsize=14)

# info_text = ax_pend.text(0.05, 0.92, '',
#                           transform=ax_pend.transAxes,
#                           fontsize=12,
#                           va='top')

# # ---------------------------------------------------
# # Animation functions
# # ---------------------------------------------------
# def init():
#     phase_traj.set_data([], [])
#     state_vec.set_data([], [])
#     rod.set_data([], [])
#     bob.set_data([], [])
#     info_text.set_text('')
#     return phase_traj, state_vec, rod, bob, info_text

# def update(i):

#     if i >= len(t):
#         i = len(t) - 1

#     phase_traj.set_data(theta[:i+1], omega[:i+1])

#     state_vec.set_data([0, theta[i]], [0, omega[i]])

#     rod.set_data([0, x[i]], [0, y[i]])

#     bob.set_data([x[i]], [y[i]])

#     info_text.set_text(
#         r'$\theta = %.2f^\circ$' % (np.rad2deg(theta[i])) +
#         '\n' +
#         r'$\omega = %.2f$ rad/s' % (omega[i])
#     )

#     return phase_traj, state_vec, rod, bob, info_text


# # ---------------------------------------------------
# # Create animation
# # ---------------------------------------------------
# ani = FuncAnimation(fig, update, frames=len(t),
#                     init_func=init, blit=True)

# # ---------------------------------------------------
# # Save GIF
# # ---------------------------------------------------
# writer = PillowWriter(fps=30)
# ani.save("pendulum_phase_and_motion.gif", writer=writer)

# plt.show()
