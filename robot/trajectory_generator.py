import os
import pickle
import pathfinder as pf
import wpilib

WHEELBASE_WIDTH = 2.0 #feet
TRAJECTORY_DIRECTORY = 'trajectories'
PICKLE_FILE = os.path.join(os.path.dirname(__file__), TRAJECTORY_DIRECTORY, 'trajectories.pickle')
MAX_GENERATION_VELOCITY = 3.4
MAX_GENERATION_ACCEL = 1.2
MAX_GENERATION_JERK = 3

trajectories = {
    "charge": [
        pf.Waypoint(0,0,0),
        pf.Waypoint(1.5, 0, 0)
    ]
}
def load_trajectories():
    if wpilib.RobotBase.isSimulation():
        generated_trajectories = _generate_trajectories()
        _write_trajectories(generated_trajectories)
    else:
        with open(PICKLE_FILE, 'rb') as f:
            generated_trajectories = pickle.load(f)
    
    return generated_trajectories

def _write_trajectories(trajectories):
    with open(PICKLE_FILE, 'wb') as f:
        pickle.dump(trajectories, f)

def _generate_trajectories():
    generated_trajectories = {}

    for trajectory_name, trajectory in trajectories.items():
        generated_trajectory = pf.generate(
            trajectory,
            pf.FIT_HERMITE_CUBIC,
            pf.SAMPLES_HIGH,
            dt=0.02,
            max_velocity=MAX_GENERATION_VELOCITY,
            max_acceleration=MAX_GENERATION_ACCEL,
            max_jerk=MAX_GENERATION_JERK
        )[1]

        modifier = pf.modifiers.TankModifier(generated_trajectories).modify(WHEELBASE_WIDTH)

        generated_trajectories[trajectory_name] = (
            modifier.getLeftTrajectory(),
            modifier.getRightTrajectory()
        )

    if wpilib.RobotBase.isSimulation():
        from pyfrc.sim import get_user_renderer

        renderer = get_user_renderer()
        if renderer:
            renderer.draw_pathfinder_trajectory(modifier.getLeftTrajectory(), '#0000ff', offset=(-0.9, 0))
            renderer.draw_pathfinder_trajectory(modifier.source, '#00ff00', show_dt=True)
            renderer.draw_pathfinder_trajectory(modifier.getRightTrajectory(), '#0000ff', offset=(0.9, 0))

    return generated_trajectories