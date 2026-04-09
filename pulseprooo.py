import tkinter as tk
from tkinter import ttk
import time
import threading

class CircuitPulsePro:
    def __init__(self, root):
        self.root = root
        self.root.title("CircuitPulse Pro | AI Hardware Diagnostics")
        
        # Set Full Screen and ensure it stays on top for visibility
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#020617")

        # Core Data
        self.devices = {
            "Air Conditioner": {
                "watts": 2500, "ideal": 10, 
                "logic": "Main Inrush → Capacitor Bank → Compressor Hub → Evaporator", 
                "danger": "Voltage Fluctuation < 180V + Clogged Condenser Coils", 
                "why": "Low voltage increases current draw, causing motor winding insulation to burn.", 
                "parts": ["Rotary Compressor", "Condenser Coils", "Expansion Valve", "Fan Motor", "Capacitor Bank"], 
                "chain": [
                    "PHASE 1: Blocked filters restrict volumetric airflow.", 
                    "PHASE 2: Compressor operates at higher discharge pressure.", 
                    "PHASE 3: Start/Run capacitors undergo dielectric breakdown.", 
                    "PHASE 4: Motor winding insulation degrades.", 
                    "PHASE 5: Mechanical seizure of the compressor pump."
                ]
            },
            "Gaming Laptop": {"watts": 230, "ideal": 6, "logic": "DC Jack → Buck Converter → VRM → CPU", "danger": "Dust Clogged Vents + Max TDP Load", "why": "Solder fatigue (BGA) due to thermal cycling.", "parts": ["Heat Sink", "Cooling Fan", "VRM MOSFETs"], "chain": ["TIM Pump-out", "Throttling", "Solder cracking"]},
            "Washing Machine": {"watts": 2200, "ideal": 12, "logic": "Main Power → Control Board → Motor Inverter → Drum", "danger": "Unbalanced Load + Motor Overheat", "why": "Excessive vibration damages drum bearings.", "parts": ["Inverter Motor", "Drum Bearings", "Water Pump"], "chain": ["Vibration spike", "Bearing wear", "Motor seizure"]},
            "Fridge": {"watts": 400, "ideal": 24, "logic": "Thermostat → Relay → Compressor Hub", "danger": "Unstable Voltage + Restricted Backflow", "why": "Compressor motor stalls and overheats.", "parts": ["Compressor", "Evaporator", "Start Relay"], "chain": ["Gas leak", "Motor stall", "Overheat"]},
            "Server Blade": {"watts": 1200, "ideal": 168, "logic": "PSU → PDU → CPU/RAM Arrays", "danger": "Humidity > 60% + Fan Failure", "why": "Corrosion on contact pins and short circuits.", "parts": ["Xeon Scalable CPU", "DDR5 ECC RAM", "Dual PSU"], "chain": ["Humidity spike", "Pin oxidation", "Short circuit"]}
        }

        self.selected_device = tk.StringVar(value="Select Hardware")
        self.usage_hrs = tk.DoubleVar(value=2.0)
        self.wattage_var = tk.StringVar(value="-- WATTS")

        # Main Layout Container with Scrollable Canvas for small screens
        self.outer_container = tk.Frame(self.root, bg="#020617")
        self.outer_container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.outer_container, bg="#020617", highlightthickness=0)
        self.main_container = tk.Frame(self.canvas, bg="#020617")
        
        # Configure canvas to resize with window
        self.canvas_window = self.canvas.create_window((0, 0), window=self.main_container, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.root.bind("<Configure>", self._on_resize)
        
        self.setup_styles()
        self.show_loading_screen()

    def _on_resize(self, event):
        # Update canvas window width to match actual screen width
        self.canvas.itemconfig(self.canvas_window, width=self.root.winfo_width())
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground="#cbd5e1", background="#38BDF8", foreground="black", font=("Segoe UI", 16, "bold"))

    def show_loading_screen(self):
        """ The 'Front Loading' page with Logo and Progress """
        for w in self.main_container.winfo_children(): w.destroy()
        
        loading_f = tk.Frame(self.main_container, bg="#020617")
        loading_f.pack(expand=True, pady=150)

        # Vector-like Logo using Text/Shapes
        logo_frame = tk.Frame(loading_f, bg="#020617")
        logo_frame.pack()
        
        tk.Label(logo_frame, text="⚡", font=("Arial", 80), fg="#38BDF8", bg="#020617").pack()
        tk.Label(logo_frame, text="CIRCUIT PULSE PRO", font=("Impact", 70), fg="white", bg="#020617").pack()
        tk.Label(logo_frame, text="HARDWARE DIAGNOSTIC AI v2.5", font=("Consolas", 14), fg="#38BDF8", bg="#020617").pack()
        
        progress = ttk.Progressbar(loading_f, orient="horizontal", length=500, mode="determinate")
        progress.pack(pady=50)

        status_lbl = tk.Label(loading_f, text="BOOTING SYSTEM...", font=("Consolas", 12), fg="#94A3B8", bg="#020617")
        status_lbl.pack()

        def run_boot():
            tasks = ["SYNCING DATABASE...", "CALIBRATING SENSORS...", "LOADING DEVICE PROFILES...", "READY"]
            for i, task in enumerate(tasks):
                status_lbl.config(text=task)
                for p in range(25):
                    time.sleep(0.015)
                    progress['value'] += 1
                    self.root.update_idletasks()
            self.show_dashboard()

        threading.Thread(target=run_boot).start()

    def update_wattage(self, event=None):
        dev = self.selected_device.get()
        if dev in self.devices:
            self.wattage_var.set(f"CURRENT LOAD: {self.devices[dev]['watts']} WATTS")

    def show_dashboard(self):
        for w in self.main_container.winfo_children(): w.destroy()
        
        # Header - Scaled for visibility
        tk.Label(self.main_container, text="DIAGNOSTIC COMMAND CENTER", 
                 font=("Impact", 60), fg="white", bg="#020617").pack(pady=(60, 20))
        
        # Central Control Panel
        card = tk.Frame(self.main_container, bg="#0F172A", padx=40, pady=40, 
                        highlightbackground="#1E293B", highlightthickness=2)
        card.pack(pady=20, padx=80, fill="x")

        tk.Label(card, text="SEARCH & SELECT DEVICE", font=("Arial", 14, "bold"), fg="#94A3B8", bg="#0F172A").pack()
        
        cb = ttk.Combobox(card, textvariable=self.selected_device, 
                          values=list(self.devices.keys()), state="readonly", width=80)
        cb.pack(pady=15, ipady=10)
        cb.bind("<<ComboboxSelected>>", self.update_wattage)

        tk.Label(card, textvariable=self.wattage_var, font=("Consolas", 36, "bold"), 
                 fg="#38BDF8", bg="#0F172A").pack(pady=10)

        # Operational Hours Slider
        tk.Label(card, text="OPERATIONAL DURATION (HOURS)", font=("Arial", 12, "bold"), fg="#94A3B8", bg="#0F172A").pack(pady=(15, 0))
        
        slider_frame = tk.Frame(card, bg="#1E293B", pady=15, padx=20)
        slider_frame.pack(pady=15, fill="x")
        
        val_lbl = tk.Label(slider_frame, text="2.0", font=("Arial", 16, "bold"), fg="white", bg="#1E293B")
        val_lbl.pack()
        
        def update_lbl(v):
            val_lbl.config(text=f"{float(v):.1f}")
            self.usage_hrs.set(float(v))

        s = tk.Scale(slider_frame, from_=0, to=24, orient="horizontal", bg="#1E293B", fg="white",
                     highlightthickness=0, troughcolor="#020617", showvalue=0, 
                     resolution=0.5, command=update_lbl)
        s.set(2.0)
        s.pack(fill="x")
        
        # Visible Action Buttons - Using a grid to ensure they aren't pushed off screen
        btn_grid = tk.Frame(self.main_container, bg="#020617")
        btn_grid.pack(pady=30, fill="x", padx=80)

        # Grid column configuration for equal width
        btn_grid.columnconfigure((0,1,2), weight=1)

        tk.Button(btn_grid, text="HEALTH SCAN", bg="#38BDF8", font=("Arial", 18, "bold"), 
                  height=3, relief="flat", command=self.view_health).grid(row=0, column=0, padx=10, sticky="ew")
        
        tk.Button(btn_grid, text="HAZARD MAP", bg="#F43F5E", font=("Arial", 18, "bold"), 
                  height=3, relief="flat", command=self.view_hazard).grid(row=0, column=1, padx=10, sticky="ew")
        
        tk.Button(btn_grid, text="SAFETY CODE", bg="#4ADE80", font=("Arial", 18, "bold"), 
                  height=3, relief="flat", command=self.view_safety).grid(row=0, column=2, padx=10, sticky="ew")

        # System Footer
        tk.Button(self.main_container, text="TERMINATE SESSION [ESC]", command=self.root.destroy, 
                  bg="#020617", fg="#475569", relief="flat", font=("Arial", 10)).pack(pady=20)

    def view_hazard(self):
        """ Deep Scan Hazard Map layout matching Screenshot (303) """
        for w in self.main_container.winfo_children(): w.destroy()
        dev = self.selected_device.get()
        if dev not in self.devices: self.show_dashboard(); return
        data = self.devices[dev]
        
        h_f = tk.Frame(self.main_container, bg="#020617", padx=50, pady=40)
        h_f.pack(fill="both", expand=True)

        tk.Label(h_f, text=f"DEEP-SCAN HAZARD MAP: {dev.upper()}", 
                 font=("Arial", 40, "bold"), fg="#F43F5E", bg="#020617").pack(anchor="w", pady=(0, 30))

        # Structural Logic Box
        l_box = tk.Frame(h_f, bg="#020617", highlightbackground="#38BDF8", highlightthickness=2)
        l_box.pack(fill="x", pady=10)
        tk.Label(l_box, text="STRUCTURAL LOGIC & CONNECTIVITY", font=("Arial", 12, "bold"), fg="#38BDF8", bg="#020617").pack(anchor="w", padx=20, pady=(10, 0))
        tk.Label(l_box, text=data["logic"], font=("Consolas", 28, "bold"), fg="white", bg="#020617").pack(anchor="w", padx=20, pady=(0, 15))

        # Danger Box
        d_box = tk.Frame(h_f, bg="#020617", highlightbackground="#F43F5E", highlightthickness=2)
        d_box.pack(fill="x", pady=20)
        tk.Label(d_box, text=f"DANGER WHEN: {data['danger']}", font=("Arial", 18, "bold"), fg="white", bg="#991B1B", padx=20, pady=5).pack(fill="x")
        tk.Label(d_box, text=f"WHY: {data['why']}", font=("Arial", 14), fg="#FDA4AF", bg="#020617", wraplength=1200, justify="left").pack(anchor="w", padx=20, pady=15)

        # Content Split
        split = tk.Frame(h_f, bg="#020617")
        split.pack(fill="both", expand=True)

        # Parts Section
        p_f = tk.Frame(split, bg="#0F172A", highlightbackground="#1E293B", highlightthickness=1, padx=25, pady=25)
        p_f.pack(side="left", fill="both", expand=True, padx=(0, 20))
        tk.Label(p_f, text="INTERNAL PARTS", font=("Arial", 16, "bold"), fg="#38BDF8", bg="#0F172A").pack(anchor="w")
        for p in data["parts"]:
            tk.Label(p_f, text=f"• {p}", font=("Arial", 14), fg="white", bg="#0F172A").pack(anchor="w", pady=5)

        # Failure Chain Section
        c_f = tk.Frame(split, bg="#020617", highlightbackground="#F43F5E", highlightthickness=1, padx=25, pady=25)
        c_f.pack(side="left", fill="both", expand=True)
        tk.Label(c_f, text="FAILURE CHAIN", font=("Arial", 16, "bold"), fg="#F43F5E", bg="#020617").pack(anchor="w")
        for step in data["chain"]:
            tk.Label(c_f, text=step, font=("Consolas", 12), fg="#FDA4AF", bg="#020617", wraplength=500, justify="left").pack(anchor="w", pady=8)

        # Navigation back - Centered at bottom
        tk.Button(h_f, text="BACK TO CENTER", command=self.show_dashboard, bg="#1E293B", fg="white",
                  font=("Arial", 18, "bold"), padx=60, pady=20, relief="flat").pack(pady=30)

    def view_health(self):
        for w in self.main_container.winfo_children(): w.destroy()
        dev = self.selected_device.get()
        if dev not in self.devices: self.show_dashboard(); return
        hrs = self.usage_hrs.get()
        score = max(5, int(100 - (hrs * 3.5)))
        clr = "#4ADE80" if score > 75 else "#FACC15" if score > 45 else "#F43F5E"
        
        f = tk.Frame(self.main_container, bg="#020617")
        f.pack(expand=True, pady=100)
        tk.Label(f, text="HEALTH ANALYTICS", font=("Impact", 50), fg="white", bg="#020617").pack()
        tk.Label(f, text=f"{score}%", font=("Arial", 150, "bold"), fg=clr, bg="#020617").pack()
        tk.Button(f, text="BACK TO CENTER", command=self.show_dashboard, bg="#1E293B", fg="white", font=("Arial", 18), padx=60, pady=20).pack(pady=40)

    def view_safety(self):
        for w in self.main_container.winfo_children(): w.destroy()
        f = tk.Frame(self.main_container, bg="#020617")
        f.pack(expand=True, pady=80)
        tk.Label(f, text="SAFETY PROTOCOLS", font=("Impact", 50), fg="#4ADE80", bg="#020617").pack(pady=30)
        protocols = ["EMERGENCY SHUTDOWN ARMED", "THERMAL LIMITS SET", "VOLTAGE MONITOR ACTIVE", "FIRE SUPPRESSION READY"]
        for s in protocols:
            tk.Label(f, text=f"STATUS: {s}", font=("Consolas", 22), fg="white", bg="#0F172A", pady=15, width=45).pack(pady=8)
        tk.Button(f, text="BACK TO CENTER", command=self.show_dashboard, bg="#1E293B", fg="white", font=("Arial", 18), padx=60, pady=20).pack(pady=40)

if __name__ == "__main__":
    root = tk.Tk()
    # High DPI fix for clear text on laptop screens
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except: pass
    
    app = CircuitPulsePro(root)
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()