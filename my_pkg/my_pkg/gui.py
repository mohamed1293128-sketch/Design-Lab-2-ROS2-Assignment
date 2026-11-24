import tkinter as tk

BG = "#111827"
PANEL = "#1F2937"
TEXT = "#F9FAFB"
MUTED = "#9CA3AF"

CYAN = "#06B6D4"
BLUE = "#3B82F6"
ORANGE = "#F59E0B"
PURPLE = "#A855F7"
GREEN = "#22C55E"

class GUI:
    def __init__(self, on_change):
        self.on_change = on_change
        self.sliders = {}

        # Gripper default state = OPEN
        self.gripper_angle = 90

        self.root = tk.Tk()
        self.root.title("Robotic Arm Control")
        self.root.geometry("560x750")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.build_gui()

    #GUI
    def build_gui(self):
        tk.Label(
            self.root,
            text="ROBOTIC ARM CONTROL",
            font=("Arial", 20, "bold"),
            bg=BG,
            fg=TEXT
        ).pack(pady=(25, 5))

        tk.Label(
            self.root,
            text="ROS 2 • Joint Trajectory Controller",
            font=("Arial", 10),
            bg=BG,
            fg=MUTED
        ).pack(pady=(0, 20))

        self.status = tk.Label(
            self.root,
            text="● SYSTEM READY",
            font=("Arial", 10, "bold"),
            bg=BG,
            fg=GREEN
        )
        self.status.pack(pady=(0, 15))

        # Arm panel
        self.arm_panel = tk.Frame(self.root, bg=PANEL)
        self.arm_panel.pack(fill="x", padx=25, pady=5)

        self.create_slider("BASE", "joint1", -60, 60, CYAN)
        self.create_slider("SHOULDER", "joint2", -60, 60, BLUE)
        self.create_slider("ELBOW", "joint3", -45, 45, ORANGE)
        self.create_slider("WRIST", "joint4", -45, 45, PURPLE)

        # Gripper buttons
        self.create_gripper()

        # Initial position button
        tk.Button(
            self.root,
            text="INITIAL POSITION",
            font=("Arial", 10, "bold"),
            width=20,
            bg=BLUE,
            fg="white",
            activebackground="#2563EB",
            relief="flat",
            command=self.initial
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="/arm_controller/joint_trajectory",
            font=("Arial", 9),
            bg=BG,
            fg=MUTED
        ).pack(pady=10)

    #ARM SLIDERS
    def create_slider(self, title, joint_name, minimum, maximum, color):
        panel = tk.Frame(self.arm_panel, bg=PANEL)
        panel.pack(fill="x", padx=20, pady=12)

        tk.Label(
            panel,
            text=title,
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=color
        ).pack(anchor="w")

        angle_label = tk.Label(
            panel,
            text="0°",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=TEXT
        )
        angle_label.pack(anchor="e")

        slider = tk.Scale(
            panel,
            from_=minimum,
            to=maximum,
            orient="horizontal",
            resolution=1,
            showvalue=False,
            length=450,
            bg=PANEL,
            fg=TEXT,
            troughcolor="#374151",
            activebackground=color,
            highlightthickness=0,
            bd=0,
            command=lambda value: self.slider_changed(
                joint_name, angle_label, value
            )
        )

        slider.set(0)
        slider.pack(fill="x")

        self.sliders[joint_name] = slider

    #GRIPPER
    def create_gripper(self):
        panel = tk.Frame(self.root, bg=PANEL)
        panel.pack(fill="x", padx=25, pady=15)

        tk.Label(
            panel,
            text="GRIPPER",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=GREEN
        ).pack(pady=(15, 10))

        buttons = tk.Frame(panel, bg=PANEL)
        buttons.pack(pady=10)

        # CLOSE = 0 degrees
        self.close_button = tk.Button(
            buttons,
            text="CLOSE  •  0°",
            font=("Arial", 11, "bold"),
            width=16,
            bg="#374151",
            fg=TEXT,
            relief="flat",
            activebackground="#4B5563",
            command=self.close_gripper
        )
        self.close_button.pack(side="left", padx=10)

        # OPEN = 90 degrees
        self.open_button = tk.Button(
            buttons,
            text="OPEN  •  90°",
            font=("Arial", 11, "bold"),
            width=16,
            bg=GREEN,
            fg="white",
            relief="flat",
            activebackground="#16A34A",
            command=self.open_gripper
        )
        self.open_button.pack(side="left", padx=10)

        self.gripper_status = tk.Label(
            panel,
            text="GRIPPER: OPEN",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=GREEN
        )
        self.gripper_status.pack(pady=(5, 15))

    def close_gripper(self):
        self.gripper_angle = 0

        self.gripper_status.config(
            text="GRIPPER: CLOSED",
            fg=ORANGE
        )

        self.close_button.config(bg=ORANGE, fg="white")
        self.open_button.config(bg="#374151", fg=TEXT)

        self.send_command()

    def open_gripper(self):
        self.gripper_angle = 90

        self.gripper_status.config(
            text="GRIPPER: OPEN",
            fg=GREEN
        )

        self.open_button.config(bg=GREEN, fg="white")
        self.close_button.config(bg="#374151", fg=TEXT)

        self.send_command()

    #CALLBACK
    def slider_changed(self, joint_name, label, value):
        value = int(float(value))
        label.config(text=f"{value}°")

        self.send_command()

    #COMMAND
    def get_angles(self):
        return {
            "joint1": self.sliders["joint1"].get(),
            "joint2": self.sliders["joint2"].get(),
            "joint3": self.sliders["joint3"].get(),
            "joint4": self.sliders["joint4"].get(),
            "joint5": self.gripper_angle
        }

    def send_command(self):
        self.on_change(self.get_angles())

        self.status.config(
            text="COMMAND TRANSMITTED",
            fg=GREEN
        )

    #INITIAL
    def initial(self):
        self.sliders["joint1"].set(0)
        self.sliders["joint2"].set(0)
        self.sliders["joint3"].set(0)
        self.sliders["joint4"].set(0)

        # Initial gripper = CLOSED
        self.gripper_angle = 0

        self.gripper_status.config(
            text="GRIPPER: CLOSED",
            fg=ORANGE
        )

        self.close_button.config(bg=ORANGE, fg="white")
        self.open_button.config(bg="#374151", fg=TEXT)

        self.send_command()

    #RUN
    def run(self):
        self.root.mainloop()