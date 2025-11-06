"""Pygame-based 2D visualization."""

import pygame
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.instance import Instance

from simulation.executor import SimulationExecutor
from statistics.tracker import StatisticsTracker


class PygameRenderer:
    """2D visualization using Pygame."""

    def __init__(self, instance: 'Instance', width: int = 1200, height: int = 800):
        self.instance = instance
        self.width = width
        self.height = height
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(f"RAWSim-O: {instance.name}")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Colors
        self.colors = {
            'background': (240, 240, 240),
            'waypoint': (200, 200, 200),
            'waypoint_storage': (220, 220, 220),
            'bot_idle': (50, 120, 200),
            'bot_carrying': (50, 200, 50),
            'pod': (255, 140, 0),
            'input_station': (0, 200, 200),
            'output_station': (200, 0, 200),
            'path': (150, 150, 150),
            'text': (0, 0, 0),
        }
        
        # Simulation
        self.executor = SimulationExecutor(instance)
        self.statistics = StatisticsTracker(instance)
        self.paused = False
        self.speed = 1.0
        
        # Calculate scale
        if instance.compound and instance.compound.tiers:
            tier = instance.compound.tiers[0]
            self.scale_x = (width - 400) / tier.length  # Leave space for stats
            self.scale_y = (height - 100) / tier.width
            self.scale = min(self.scale_x, self.scale_y) * 0.9
            self.offset_x = 50
            self.offset_y = 50
        else:
            self.scale = 10
            self.offset_x = 50
            self.offset_y = 50

    def world_to_screen(self, x: float, y: float) -> tuple:
        """Convert world coordinates to screen coordinates."""
        screen_x = int(self.offset_x + x * self.scale)
        screen_y = int(self.offset_y + y * self.scale)
        return screen_x, screen_y

    def run(self):
        """Run the visualization loop."""
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_r:
                        # Reset simulation
                        self.executor.current_time = 0.0
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        self.speed = min(self.speed * 2, 16.0)
                    elif event.key == pygame.K_MINUS:
                        self.speed = max(self.speed / 2, 0.25)

            # Update simulation
            if not self.paused:
                for _ in range(int(self.speed)):
                    self.executor.step()
                    if self.executor.current_time >= self.executor.max_time:
                        running = False
                        break
                
                # Record statistics every second
                if int(self.executor.current_time) % 10 == 0:
                    self.statistics.record_snapshot(self.executor.current_time)

            # Render
            self.render()
            
            # Control frame rate
            self.clock.tick(60)

        # Show final statistics
        print("\n=== Simulation Complete ===")
        summary = self.statistics.get_summary()
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        pygame.quit()

    def render(self):
        """Render the current state."""
        self.screen.fill(self.colors['background'])
        
        # Draw waypoints
        for waypoint in self.instance.waypoints:
            x, y = self.world_to_screen(waypoint.x, waypoint.y)
            color = self.colors['waypoint_storage'] if waypoint.pod_storage_location else self.colors['waypoint']
            pygame.draw.circle(self.screen, color, (x, y), int(waypoint.radius * self.scale))
        
        # Draw paths (simplified - just show grid)
        # for waypoint in self.instance.waypoints:
        #     x1, y1 = self.world_to_screen(waypoint.x, waypoint.y)
        #     for neighbor in waypoint.paths:
        #         x2, y2 = self.world_to_screen(neighbor.x, neighbor.y)
        #         pygame.draw.line(self.screen, self.colors['path'], (x1, y1), (x2, y2), 1)
        
        # Draw stations
        for station in self.instance.input_stations:
            x, y = self.world_to_screen(station.x, station.y)
            pygame.draw.circle(self.screen, self.colors['input_station'], (x, y), 
                             int(station.radius * self.scale * 2))
            label = self.small_font.render('IN', True, (255, 255, 255))
            self.screen.blit(label, (x - 10, y - 5))
        
        for station in self.instance.output_stations:
            x, y = self.world_to_screen(station.x, station.y)
            pygame.draw.circle(self.screen, self.colors['output_station'], (x, y), 
                             int(station.radius * self.scale * 2))
            label = self.small_font.render('OUT', True, (255, 255, 255))
            self.screen.blit(label, (x - 12, y - 5))
        
        # Draw pods
        for pod in self.instance.pods:
            if not pod.is_carried():
                x, y = self.world_to_screen(pod.x, pod.y)
                pygame.draw.circle(self.screen, self.colors['pod'], (x, y), 
                                 int(pod.radius * self.scale * 1.5))
        
        # Draw bots
        for bot in self.instance.bots:
            x, y = self.world_to_screen(bot.x, bot.y)
            color = self.colors['bot_carrying'] if bot.has_pod() else self.colors['bot_idle']
            pygame.draw.circle(self.screen, color, (x, y), int(bot.radius * self.scale * 2))
            
            # Draw pod on bot if carrying
            if bot.has_pod():
                pygame.draw.circle(self.screen, self.colors['pod'], (x, y), 
                                 int(bot.radius * self.scale * 1.2), 2)
        
        # Draw statistics panel
        self.draw_stats_panel()
        
        pygame.display.flip()

    def draw_stats_panel(self):
        """Draw statistics panel on the right side."""
        panel_x = self.width - 350
        panel_y = 20
        
        stats = [
            f"Time: {self.executor.current_time:.1f}s",
            f"Speed: {self.speed}x",
            f"Status: {'PAUSED' if self.paused else 'RUNNING'}",
            f"",
            f"Bots: {len(self.instance.bots)}",
            f"Pods: {len(self.instance.pods)}",
            f"Waypoints: {len(self.instance.waypoints)}",
            f"Input Stations: {len(self.instance.input_stations)}",
            f"Output Stations: {len(self.instance.output_stations)}",
            f"",
            f"Controls:",
            f"SPACE - Pause/Resume",
            f"+/- - Speed Up/Down",
            f"R - Reset",
            f"ESC - Exit",
        ]
        
        y = panel_y
        for stat in stats:
            text = self.small_font.render(stat, True, self.colors['text'])
            self.screen.blit(text, (panel_x, y))
            y += 25
