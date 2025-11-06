"""Main simulation executor."""

from typing import TYPE_CHECKING
import logging
import time

if TYPE_CHECKING:
    from core.instance import Instance

from .events import EventManager, EventType, SimulationEvent
from control.task_manager import TaskManager
from control.pod_selector import PodSelector
from control.path_planner import PathPlanner


class SimulationExecutor:
    """Executes the discrete event simulation."""

    def __init__(self, instance: 'Instance'):
        self.instance = instance
        self.event_manager = EventManager()
        
        # Controllers
        pathfinding_method = instance.controller_config.get('pathfinding', {}).get('method', 'WHCAvStar')
        task_method = instance.controller_config.get('task_assignment', {}).get('method', 'nearest')
        pod_method = instance.controller_config.get('pod_selection', {}).get('method', 'nearest')
        
        self.task_manager = TaskManager(instance, task_method)
        self.pod_selector = PodSelector(instance, pod_method)
        self.path_planner = PathPlanner(instance, pathfinding_method)
        
        # Simulation state
        self.is_running = False
        self.current_time = 0.0
        self.time_step = instance.setting_config.get('time_step', 0.1)
        self.max_time = instance.setting_config.get('simulation_duration', 3600.0)
        
        logging.info(f"SimulationExecutor initialized: {pathfinding_method}, timestep={self.time_step}")

    def execute(self):
        """Execute the simulation."""
        logging.info("Starting simulation...")
        self.is_running = True
        
        # Publish start event
        self.event_manager.publish(SimulationEvent(
            EventType.SIMULATION_START,
            self.current_time
        ))

        step_count = 0
        start_time = time.time()

        while self.is_running and self.current_time < self.max_time:
            self.step()
            step_count += 1
            
            # Log progress every 1000 steps
            if step_count % 1000 == 0:
                elapsed = time.time() - start_time
                logging.info(f"Step {step_count}, sim_time={self.current_time:.1f}s, "
                           f"real_time={elapsed:.1f}s")

        # Publish end event
        self.event_manager.publish(SimulationEvent(
            EventType.SIMULATION_END,
            self.current_time
        ))

        elapsed = time.time() - start_time
        logging.info(f"Simulation completed: {step_count} steps in {elapsed:.2f}s")
        logging.info(f"Simulation time: {self.current_time:.2f}s")

    def step(self):
        """Execute one simulation time step."""
        # Update all bots
        for bot in self.instance.bots:
            bot.update(self.time_step)

        # Update path planner
        self.path_planner.update(self.time_step)

        # Process orders (simplified)
        # In a full implementation, this would involve:
        # - Generating new orders
        # - Assigning tasks to bots
        # - Managing pod movements
        # - Handling item picking/storing

        # Advance time
        self.current_time += self.time_step
        self.instance.current_time = self.current_time

        # Publish time step event
        self.event_manager.publish(SimulationEvent(
            EventType.TIME_STEP,
            self.current_time
        ))

    def stop(self):
        """Stop the simulation."""
        self.is_running = False
        logging.info("Simulation stopped")

    def __repr__(self):
        status = "running" if self.is_running else "stopped"
        return f"SimulationExecutor(time={self.current_time:.2f}, status={status})"
