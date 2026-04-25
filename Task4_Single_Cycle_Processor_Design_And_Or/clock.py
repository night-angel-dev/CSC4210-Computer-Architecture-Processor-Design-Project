"""
clock.py - Reuses Clock from Task3_Memory_Hierarchy_Simulation.
Inputs PCNext 32 bits, outputs PC 32 bits, contains a CLK.

Task3's Clock is loaded by absolute file path to avoid a naming conflict:
both files are named 'clock.py', so a normal sys.path import would find
this file again and loop. importlib loads Task3's file as a separate module.
"""

import importlib.util
import os
import sys

_task3_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "Task3_Memory_Hierarchy_Simulation"
)
_task3_clock_path = os.path.join(_task3_dir, "clock.py")

# Add task 3 path
if _task3_dir not in sys.path:
    sys.path.insert(0, _task3_dir)

_spec = importlib.util.spec_from_file_location("task3_clock", _task3_clock_path)
_mod  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

# Re-export Task3's Clock so we can just do from clock import Clock for each file that needs Clock
Clock = _mod.Clock


if __name__ == "__main__":
    print("=" * 50)
    print("Testing Clock (re-exported from Task 3)")
    print("=" * 50)

    clk = Clock()
    print(f"Initial cycle: {clk.get_current_cycle()}")

    for i in range(4):
        clk.tick()
        print(f"After tick {i + 1}: cycle {clk.get_current_cycle()}")

    clk.reset()
    print(f"After reset: cycle {clk.get_current_cycle()}")

    stats = clk.get_stats()
    print(f"Stats: {stats}")

    print("\n" + "=" * 50)
    print("Clock tests passed!")
    print("=" * 50)
