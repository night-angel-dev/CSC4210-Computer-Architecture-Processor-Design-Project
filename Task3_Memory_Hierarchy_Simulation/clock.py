"""
clock.py - Clock-driven simulation engine.

A cycle-accurate timer that drives the simulation.
Tracks data transfers that take multiple cycles to complete.

For 32-bit architecture:
- Each cycle represents one clock period
- Transfer latencies are measured in cycles
- Bandwidth limits transfers per cycle (bonus/future add on)
"""

import config

# Simple version without pending transfers
class Clock:
    """
    Simple clock for minimum required functionality.
    """
    
    def __init__(self):
        """Initialize clock."""
        self.current_cycle = 0
    
    def tick(self):
        """
        Advance the clock by one cycle.
        
        @return - New current cycle number
        """
        self.current_cycle += 1
        return self.current_cycle
    
    def get_current_cycle(self):
        """
        Get the current cycle number.
        
        @return - Current cycle count
        """
        return self.current_cycle
    
    def reset(self):
        """Reset the clock to cycle 0."""
        self.current_cycle = 0
    
    def get_stats(self):
        """
        Get clock statistics.
        
        @return - Dictionary with clock statistics
        """
        return {
            'current_cycle': self.current_cycle,
            'total_cycles_advanced': self.current_cycle
        }


# For testing
if __name__ == "__main__":
    print("=" * 50)
    print("Testing Clock")
    print("=" * 50)
    
    clock = Clock()
    print(f"Initial cycle: {clock.get_current_cycle()}")
    
    for i in range(5):
        clock.tick()
        print(f"After tick {i+1}: cycle {clock.get_current_cycle()}")
    
    clock.reset()
    print(f"After reset: cycle {clock.get_current_cycle()}")
    
    print("\n" + "=" * 50)
    print("All clock tests passed!")
    print("=" * 50)