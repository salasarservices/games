import streamlit as st
import random

# Grid size
WIDTH = 10
HEIGHT = 20

# Emojis/colors
PLANE = "✈️"
ENEMY = "💀"
BULLET = "🔴"
EMPTY = "⬛"

# Initialize game state
if 'plane_x' not in st.session_state:
    st.session_state.plane_x = WIDTH // 2
    st.session_state.bullets = []
    st.session_state.enemies = []
    st.session_state.score = 0
    st.session_state.running = True

def reset_game():
    st.session_state.plane_x = WIDTH // 2
    st.session_state.bullets = []
    st.session_state.enemies = []
    st.session_state.score = 0
    st.session_state.running = True

def move_plane(dx):
    x = st.session_state.plane_x + dx
    if 0 <= x < WIDTH:
        st.session_state.plane_x = x

def shoot():
    # Bullets start just above the plane
    st.session_state.bullets.append([st.session_state.plane_x, HEIGHT-2])

def next_frame():
    # Move bullets
    new_bullets = []
    for bx, by in st.session_state.bullets:
        by -= 1
        if by >= 0:
            new_bullets.append([bx, by])
    st.session_state.bullets = new_bullets

    # Move enemies
    new_enemies = []
    for ex, ey in st.session_state.enemies:
        ey += 1
        if ey < HEIGHT:
            new_enemies.append([ex, ey])
    st.session_state.enemies = new_enemies

    # Spawn new enemies
    if random.random() < 0.2:
        st.session_state.enemies.append([random.randint(0, WIDTH-1), 0])

    # Collision: bullets vs enemies
    bullets_to_remove = []
    enemies_to_remove = []
    for i, (bx, by) in enumerate(st.session_state.bullets):
        for j, (ex, ey) in enumerate(st.session_state.enemies):
            if bx == ex and by == ey:
                bullets_to_remove.append(i)
                enemies_to_remove.append(j)
                st.session_state.score += 1

    # Remove collided bullets and enemies
    st.session_state.bullets = [b for i, b in enumerate(st.session_state.bullets) if i not in bullets_to_remove]
    st.session_state.enemies = [e for j, e in enumerate(st.session_state.enemies) if j not in enemies_to_remove]

    # Collision: enemies reach plane
    for ex, ey in st.session_state.enemies:
        if ey == HEIGHT-1 and ex == st.session_state.plane_x:
            st.session_state.running = False

def render():
    grid = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for bx, by in st.session_state.bullets:
        if 0 <= by < HEIGHT:
            grid[by][bx] = BULLET
    for ex, ey in st.session_state.enemies:
        if 0 <= ey < HEIGHT:
            grid[ey][ex] = ENEMY
    # Place plane
    grid[HEIGHT-1][st.session_state.plane_x] = PLANE
    # Render grid
    for row in grid:
        st.markdown("".join(row))
    st.write(f"Score: {st.session_state.score}")

st.title("✈️ Retro Flight Shooter")
if not st.session_state.running:
    st.subheader("Game Over!")
    if st.button("Restart"):
        reset_game()
else:
    # Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⬅️"):
            move_plane(-1)
    with col2:
        if st.button("➡️"):
            move_plane(1)
    with col3:
        if st.button("🔫 Shoot"):
            shoot()
    with col4:
        if st.button("Next Frame"):
            next_frame()

    render()
