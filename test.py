import pandas as pd
import numpy as np
import pyvista as pv
# import pybullet as p

# Generate surface data using pandas (for demonstration)
x = np.linspace(-5, 5, 20)
y = np.linspace(-5, 5, 20)
X, Y = np.meshgrid(x, y)
Z = 0.5 * np.sin(X) * np.cos(Y)  # Wavy surface

# Create DataFrame for surface points
surface_df = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': Z.flatten()
})

# Create PyVista mesh for surface
surface = pv.StructuredGrid(X, Y, Z)

# Create sphere
sphere = pv.Sphere(radius=0.5, center=(0, 0, 1.0))

# Initialize PyBullet
# p.connect(p.DIRECT)
# p.setGravity(0, 0, -9.81)

# Create terrain
# terrainShape = p.createCollisionShape(p.GEOM_HEIGHTFIELD, meshScale=[0.5, 0.5, 1], heightfieldData=Z.flatten(), numHeightfieldRows=20, numHeightfieldColumns=20)
# terrainId = p.createMultiBody(0, terrainShape)
# p.resetBasePositionAndOrientation(terrainId, [0, 0, 0], [0, 0, 0, 1])

# Create sphere in PyBullet
# sphereId = p.createMultiBody(1, p.createCollisionShape(p.GEOM_SPHERE, radius=0.5), basePosition=[0, 0, 1])

# Create plotter
plotter = pv.Plotter()
plotter.add_mesh(surface, color='lightblue', opacity=0.8)
plotter.add_mesh(sphere, color='red')

print("Scene created. Opening window...")

# Function to update physics
def update_physics():
    p.stepSimulation()
    # pos, orn = p.getBasePositionAndOrientation(sphereId)
    sphere.center = pos
    # Update camera to follow the ball
    offset = np.array([0, -3, 2])  # behind and above
    plotter.camera.position = np.array(pos) + offset
    plotter.camera.focal_point = pos
    plotter.camera.up = [0, 0, 1]
    plotter.update()
    plotter.render()

# Add key press observer
def key_press(obj, event):
    key = obj.GetKeySym().lower()
    impulse = 5
    jump_force = 10
    # pos, orn = p.getBasePositionAndOrientation(sphereId)
    direction = np.array(plotter.camera.focal_point) - np.array(plotter.camera.position)
    direction[2] = 0  # ignore z for movement
    norm = np.linalg.norm(direction)
    if norm > 0:
        direction /= norm
    # Right vector: cross(direction, up)
    up = np.array([0, 0, 1])
    right = np.cross(direction, up)
    force = np.array([0.0, 0.0, 0.0])
    if key == 'w':
        force = direction * impulse
    elif key == 's':
        force = -direction * impulse
    elif key == 'a':
        force = -right * impulse
    elif key == 'd':
        force = right * impulse
    elif key == 'space':
        force[2] = jump_force
    # p.applyExternalForce(sphereId, -1, force, pos, p.WORLD_FRAME)

plotter.iren.add_observer('KeyPressEvent', key_press)

# Add timer for physics update
plotter.iren.add_timer_event(update_physics, 20, 1)

# Initial camera setup
offset = np.array([0, -3, 2])
plotter.camera.position = sphere.center + offset
plotter.camera.focal_point = sphere.center
plotter.camera.up = [0, 0, 1]

# Show the interactive window
plotter.show() 
