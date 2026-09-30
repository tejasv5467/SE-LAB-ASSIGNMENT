# Anvil Dodge Repair Lab

This project is a modular survival dodger game using **Pygame**. It introduces students to falling hazard mechanics, boundary management, collision detection, and survival time tracking within a clean, object-oriented codebase.

---

## What's Provided

A working Anvil Dodge game with:

- A player character that can move left and right across the ground line using keyboard inputs
- Heavy anvils spawned continuously from random horizontal positions falling toward the ground
- Collision detection when an anvil hits the player, triggering game over
- Real-time survival time tracking and a Game Over overlay with restart functionality

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left / A to move left, Right / D to move right, R to reset after Game Over.   


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the player off-screen boundary bug

The player is supposed to stay inside the visible left and right boundaries of the screen. In the current build, player.update() has no boundary checks, allowing the player to walk indefinitely off the left or right edges of the screen where anvils cannot hit them, achieving infinite survival time. Implement horizontal bounds in player.update() so the player cannot step past 0 or self.screen_width - self.width.

### Task 2: Implement dynamic difficulty scaling

Right now, anvils spawn at a constant interval of 700ms throughout the entire run. Implement logic in game_engine.update() to decrease spawn_delay as survival_time increases (for example, reducing the delay gradually down to a minimum cap of 200ms), making the game progressively more challenging over time.

### Task 3: Implement speed-based anvil tinting

All falling anvils currently share identical shades of grey. In anvil.render(), introduce dynamic color tinting based on each anvil's randomized falling speed (self.speed). Fast-falling anvils should render with an orange or red accent, warning the player of rapid hazards.

### Task 4: Implement ground impact effects

When an anvil leaves the bottom of the screen, it is silently removed from the game. Add a brief visual effect—such as a small dust puff, ground particles, or screen-shake vibration—whenever an anvil strikes the ground before being removed.

---

## Expected Behavior

- The player cannot move beyond the visible left and right edges of the screen
- Anvils fall continuously from randomized X coordinates and clean up after passing below the screen
- Touching any falling anvil immediately triggers the Game Over screen and stops time tracking
- Pressing R after losing resets the player, clears all falling anvils, and restarts the survival timer

---

## Folder Structure

```
anvil_dodge/
├── game/
│   ├── anvil.py
│   ├── game_engine.py
│   └── player.py
├── main.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
