import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.uix.label import Label

# Constants
WIDTH, HEIGHT = 400, 700
Window.size = (WIDTH, HEIGHT)
PLANE_SIZE = (40, 40)
ENEMY_SIZE = (40, 40)
BULLET_SIZE = (6, 20)

class Plane(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = PLANE_SIZE
        self.center_x = WIDTH // 2
        self.y = 30

class Enemy(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = ENEMY_SIZE
        self.x = random.randint(0, WIDTH - ENEMY_SIZE[0])
        self.y = HEIGHT
        with self.canvas:
            Color(random.random(), random.random(), random.random())
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def move(self):
        self.y -= 5
        self.rect.pos = self.pos

class Bullet(Widget):
    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.size = BULLET_SIZE
        self.x = x + PLANE_SIZE[0] // 2 - BULLET_SIZE[0] // 2
        self.y = y + PLANE_SIZE[1]
        with self.canvas:
            Color(1, 0, 0)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def move(self):
        self.y += 15
        self.rect.pos = self.pos

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plane = Plane()
        self.add_widget(self.plane)
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.label = Label(text=f"Score: {self.score}", pos=(10, HEIGHT - 40), size_hint=(None, None), color=(1,1,0,1))
        self.add_widget(self.label)
        Clock.schedule_interval(self.update, 1/30)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        if self._keyboard.widget:
            pass
        self._keyboard.bind(on_key_down=self.on_key_down)
        self.spawn_enemy()

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self.on_key_down)
        self._keyboard = None

    def on_touch_move(self, touch):
        self.plane.center_x = touch.x

    def on_touch_down(self, touch):
        self.shoot()

    def on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.plane.x = max(0, self.plane.x - 20)
        elif keycode[1] == 'right':
            self.plane.x = min(WIDTH - PLANE_SIZE[0], self.plane.x + 20)
        elif keycode[1] == 'spacebar':
            self.shoot()
        return True

    def spawn_enemy(self):
        enemy = Enemy()
        self.enemies.append(enemy)
        self.add_widget(enemy)
        Clock.schedule_once(lambda dt: self.spawn_enemy(), random.uniform(0.7, 1.5))

    def shoot(self):
        bullet = Bullet(self.plane.x, self.plane.y)
        self.bullets.append(bullet)
        self.add_widget(bullet)

    def update(self, dt):
        # Move bullets
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y > HEIGHT:
                self.remove_widget(bullet)
                self.bullets.remove(bullet)

        # Move enemies
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.y < 0:
                self.remove_widget(enemy)
                self.enemies.remove(enemy)
                continue
            # Collision
            for bullet in self.bullets[:]:
                if enemy.collide_widget(bullet):
                    self.remove_widget(enemy)
                    self.remove_widget(bullet)
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.score += 1
                    self.label.text = f"Score: {self.score}"
                    break
            if enemy.collide_widget(self.plane):
                self.end_game()

    def end_game(self):
        Clock.unschedule(self.update)
        self.label.text = f"Game Over! Final Score: {self.score}"

class FlightShooterApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    FlightShooterApp().run()
