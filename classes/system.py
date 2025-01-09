from classes.central_object import CentralObject
from classes.object import Object
import matplotlib.pyplot as plt
import numpy as np
import math
import json


class System:
    def __init__(self, config):
        self._central_object = CentralObject(
            mass=config["central_mass"],
            radius=config["central_radius"]
        )
        self._objects = []
        for data in config["objects"]:
            self._objects.append(
                Object(
                    pos_x=data["x"],
                    pos_y=data["y"],
                    mass=data["mass"],
                    velocity_x=data.get("vx", 0),
                    velocity_y=data.get("vy", 0)
                )
            )
        self._scale = config["scale"]
        self._dt = config["time_step"]
        self._image_size = config["image_size"]
        self._G = 6.67430e-11

    def central_object(self):
        return self._central_object

    def objects(self):
        return self._objects

    def scale(self):
        return self._scale

    def dt(self):
        return self._dt

    def image_size(self):
        return self._image_size

    def G(self):
        return self._G

    def create_image(self, trajectories):
        scale = self.scale()

        fig, ax = plt.subplots(figsize=(8, 8))
        if self.objects():
            max_range = max(max(abs(obj.pos_x()) for obj in self.objects()),
                            max(abs(obj.pos_y()) for obj in self.objects()))
        else:
            max_range = max(max(abs(x) for x in trajectory["x"]) for trajectory in trajectories.values())
        ax.set_xlim(-1.5 * max_range / scale, 1.5 * max_range / scale)
        ax.set_ylim(-1.5 * max_range / scale, 1.5 * max_range / scale)


        ax.scatter(0, 0, color="yellow", s=200, label="Obiekt centralny")


        for i, trajectory in trajectories.items():
            trajectory_x = np.array(trajectory["x"]) / scale
            trajectory_y = np.array(trajectory["y"]) / scale


            ax.plot(trajectory_x, trajectory_y, linestyle="--", alpha=0.7, label=f"Trajektoria {i + 1}")

        for i, obj in enumerate(self.objects()):
            current_x = obj.pos_x() / scale
            current_y = obj.pos_y() / scale
            ax.scatter(current_x, current_y, s=50, label=f"Obiekt {i + 1}")


        ax.set_title("Symulacja ruchu grawitacyjnego")
        ax.set_xlabel("Odległość (km) / skala")
        ax.set_ylabel("Odległość (km) / skala")
        ax.legend()

        plt.savefig("simulation_result.png")
        plt.show()

    def save_collision_report(self, collision_report, filename="collision_report.txt"):
        with open(filename, "w") as f:
            if collision_report:
                f.write("Raport kolizji:\n")
                for line in collision_report:
                    f.write(line + "\n")
            else:
                f.write("Brak kolizji w czasie symulacji.\n")

    def simulate(self, steps):

        objects = self.objects()
        trajectories = {i: {"x": [], "y": []} for i in range(len(objects))}
        collision_report = []

        for step in range(steps):

            for step in range(steps):
                print(f"Krok {step}: liczba obiektów: {len(objects)}")
                to_remove = []

                for i, obj in enumerate(objects):

                    r = self.calculate_distance(obj, self.central_object())

                    if r < self.central_object().radius():
                        print(f"Krok {step}: Obiekt {i} w kolizji z centralnym!")
                        collision_report.append(f"Krok {step}: Obiekt {i} w kolizji z centralnym!")
                        to_remove.append(i)
                        continue

                    dx = self.central_object().pos_x() - obj.pos_x()
                    dy = self.central_object().pos_y() - obj.pos_y()
                    distance = math.sqrt(dx**2 + dy**2)
                    force = self.G() * self.central_object().mass() * obj.mass() / distance**2

                    ax = force * dx / distance / obj.mass()
                    ay = force * dy / distance / obj.mass()

                    print(f"Krok {step}: Obiekt {i} - ax: {ax}, ay: {ay}")

                    new_vx = obj.velocity_x() + ax * self.dt()
                    new_vy = obj.velocity_y() + ay * self.dt()
                    obj.set_vel_x(new_vx)
                    obj.set_vel_y(new_vy)

                    print(f"Krok {step}: Obiekt {i} - vx: {new_vx}, vy: {new_vy}")

                    new_x = obj.pos_x() + new_vx * self.dt()
                    new_y = obj.pos_y() + new_vy * self.dt()
                    obj.set_pos_x(new_x)
                    obj.set_pos_y(new_y)

                    print(f"Krok {step}: Obiekt {i} - x: {new_x}, y: {new_y}")

                    trajectories[i]["x"].append(new_x)
                    trajectories[i]["y"].append(new_y)

                for index in sorted(to_remove, reverse=True):
                    objects.pop(index)

            collisions = self.check_collisions()
            if collisions:
                for (i, j) in collisions:
                    if j == -1:
                        self.central_object().set_mass(self.central_object().mass() + self._objects[i].mass())
                        self._objects.pop(i)
                    else:
                        self.merge_objects(i, j)
                collision_report.extend(collisions)

            return trajectories, collision_report

    def check_collisions(self):
        pixels = {}
        collisions = []

        for i, obj in enumerate(self.objects()):
            pixel_x = int(obj.pos_x() / self.scale())
            pixel_y = int(obj.pos_y() / self.scale())

            pixel_key = (pixel_x, pixel_y)
            if pixel_key in pixels:
                collisions.append((pixels[pixel_key], i))
            else:
                pixels[pixel_key] = i

            if self.calculate_distance(obj, self.central_object()) <= self.central_object().radius():
                collisions.append((i, -1))
        return collisions

    def merge_objects(self, i, j):
        obj1 = self._objects[i]
        obj2 = self._objects[j]

        new_mass = obj1.mass() + obj2.mass()

        new_x = (obj1.pos_x() * obj1.mass() + obj2.pos_x() * obj2.mass()) / new_mass
        new_y = (obj1.pos_y() * obj1.mass() + obj2.pos_y() * obj2.mass()) / new_mass

        new_vx = (obj1.velocity_x() * obj1.mass() + obj2.velocity_x() * obj2.mass()) / new_mass
        new_vy = (obj1.velocity_y() * obj1.mass() + obj2.velocity_y() * obj2.mass()) / new_mass

        new_obj = Object(new_x, new_y, new_mass, new_vx, new_vy)

        self._objects[i] = new_obj
        self._objects.pop(j)

    def calculate_distance(self, obj1, obj2):
        dx = obj1.pos_x() - obj2.pos_x()
        dy = obj1.pos_y() - obj2.pos_y()
        return (dx**2 + dy**2)**0.5

    def save_state(self, filename="simulation_state.json"):
        state = {
            "central_mass": float(self.central_object().mass()),
            "central_radius": float(self.central_object().radius()),
            "scale": float(self.scale()),
            "image_size": self.image_size(),
            "time_step": float(self.dt()),
            "objects": [
                {
                    "x": float(obj.pos_x()),
                    "y": float(obj.pos_y()),
                    "vx": float(obj.velocity_x()),
                    "vy": float(obj.velocity_y()),
                    "mass": float(obj.mass())
                }
                for obj in self.objects()
            ]
        }
        with open(filename, "w") as f:
            json.dump(state, f, indent=4)
