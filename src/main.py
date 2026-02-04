"""
AceTrack AI
Author: Öner Efe Güngör
UI: Professional Casino Aesthetics (Gold, Green & Deep Charcoal)
Logic: Temporal Majority Voting & Shoe Inventory Management
"""

import cv2
import customtkinter as ctk
from PIL import Image
from ultralytics import YOLO
import time
from datetime import datetime
from collections import Counter

# --- Global Professional Styling ---
ctk.set_appearance_mode("dark")

class AceTrackAI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Logical Core States ---
        self.is_running = False
        self.running_count = 0
        self.inventory = {}
        self.cooldown_registry = {}
        self.inference_buffer = []
        self.cap = None

        # --- Precision Parameters ---
        self.ANALYSIS_WINDOW = 1.2
        self.RECOGNITION_QUOTA = 7   # Slightly faster recognition
        self.CONFIDENCE_THRESHOLD = 0.58
        self.RE_SCAN_COOLDOWN = 3.5

        # --- UI Colors ---
        self.CLR_GOLD = "#D4AF37"    # Premium Casino Gold
        self.CLR_GREEN = "#1E5631"   # Classic Table Felt Green
        self.CLR_BG = "#0B0E11"      # Deep Charcoal
        self.CLR_ACCENT = "#3498DB"  # Electric Blue

        # Model Init
        try:
            self.model = YOLO("best.pt")
        except Exception as error:
            print(f"[!] Critical Error: {error}")

        self.initialize_interface()

    def initialize_interface(self):
        """Builds the high-end Casino UI dashboard."""
        self.title("AceTrack AI")
        self.geometry("1300x850")
        self.configure(fg_color=self.CLR_BG)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Control Panel) ---
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color="#121619")
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.brand_title = ctk.CTkLabel(
            self.sidebar, text="ACETRACK AI",
            font=ctk.CTkFont(family="Impact", size=32),
            text_color=self.CLR_GOLD
        )
        self.brand_title.pack(pady=(40, 5))

        ctk.CTkLabel(self.sidebar, text="PROFESSIONAL DEALER TOOL", font=("Inter", 10), text_color="gray").pack()

        # Premium Display Card
        self.stats_card = ctk.CTkFrame(self.sidebar, fg_color=self.CLR_GREEN, corner_radius=15, border_width=2, border_color=self.CLR_GOLD)
        self.stats_card.pack(padx=20, pady=30, fill="x")

        ctk.CTkLabel(self.stats_card, text="RUNNING COUNT", font=("Inter", 12, "bold"), text_color="white").pack(pady=(15, 0))
        self.count_display = ctk.CTkLabel(
            self.stats_card, text="0",
            font=ctk.CTkFont(size=90, weight="bold"),
            text_color="white"
        )
        self.count_display.pack(pady=(0, 15))

        # Deck Config Section
        self.setup_config_ui()

        # Event History
        self.event_log = ctk.CTkTextbox(self.sidebar, width=280, height=300, font=("Consolas", 12), fg_color="#080A0C", text_color="#2ECC71", border_width=1, border_color="#222")
        self.event_log.pack(padx=20, pady=10)
        self.event_log.configure(state="disabled")

        self.btn_reset = ctk.CTkButton(
            self.sidebar, text="RESET TABLE SESSION",
            command=self.perform_reset,
            fg_color="#A93226", hover_color="#7B241C",
            font=("Inter", 13, "bold"), height=40
        )
        self.btn_reset.pack(pady=20)

        # --- Main Workspace (Vision Area) ---
        self.setup_main_workspace()

    def setup_config_ui(self):
        config_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        config_frame.pack(fill="x", padx=40)

        ctk.CTkLabel(config_frame, text="SHOE SIZE:", font=("Inter", 11)).grid(row=0, column=0, padx=5)
        self.deck_selector = ctk.CTkEntry(config_frame, placeholder_text="1", width=60, justify="center", fg_color="#1A1F24", border_color=self.CLR_GOLD)
        self.deck_selector.insert(0, "1")
        self.deck_selector.grid(row=0, column=1, padx=5)

    def setup_main_workspace(self):
        # Stream View
        self.stream_view = ctk.CTkLabel(self, text="VISION ENGINE OFFLINE", fg_color="#000", corner_radius=25, font=("Inter", 14))
        self.stream_view.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

        # Control Button
        self.btn_toggle = ctk.CTkButton(
            self, text="START SCANNER ENGINE",
            command=self.toggle_engine,
            height=65, font=("Inter", 18, "bold"),
            fg_color=self.CLR_GOLD, text_color="black",
            hover_color="#B8860B"
        )
        self.btn_toggle.grid(row=1, column=1, pady=(0, 30), padx=60, sticky="ew")

    def post_log(self, message):
        timestamp = datetime.now().strftime("%H:%M")
        self.event_log.configure(state="normal")
        self.event_log.insert("1.0", f"[{timestamp}] > {message}\n")
        self.event_log.configure(state="disabled")

    def perform_reset(self):
        self.running_count = 0
        self.inventory.clear()
        self.cooldown_registry.clear()
        self.inference_buffer.clear()
        self.count_display.configure(text="0")
        self.post_log("SESSION_CLEARED: Ready for new shoe.")

    def evaluate_hilo(self, label):
        if any(v in label for v in ['10', 'J', 'Q', 'K', 'A']): return -1
        if any(v in label for v in ['2', '3', '4', '5', '6']): return 1
        return 0

    def process_frame_logic(self, results):
        now = time.time()
        self.inference_buffer = [inf for inf in self.inference_buffer if (now - inf[1]) < self.ANALYSIS_WINDOW]

        if results[0].boxes:
            for i in range(len(results[0].boxes)):
                if float(results[0].boxes.conf[i]) >= self.CONFIDENCE_THRESHOLD:
                    label = self.model.names[int(results[0].boxes.cls[i])].upper()
                    self.inference_buffer.append((label, now))

        if not self.inference_buffer: return

        consensus = Counter([inf[0] for inf in self.inference_buffer])
        dominant_label, frequency = consensus.most_common(1)[0]

        if frequency >= self.RECOGNITION_QUOTA:
            if dominant_label in self.cooldown_registry:
                if now < self.cooldown_registry[dominant_label]: return
                else: del self.cooldown_registry[dominant_label]

            try: max_decks = int(self.deck_selector.get())
            except: max_decks = 1

            if self.inventory.get(dominant_label, 0) < max_decks:
                self.running_count += self.evaluate_hilo(dominant_label)
                self.inventory[dominant_label] = self.inventory.get(dominant_label, 0) + 1
                self.cooldown_registry[dominant_label] = now + self.RE_SCAN_COOLDOWN
                self.inference_buffer = [inf for inf in self.inference_buffer if inf[0] != dominant_label]

                self.count_display.configure(text=str(self.running_count))
                self.post_log(f"RECOGNIZED: {dominant_label}")

    def run_engine_loop(self):
        if self.is_running:
            success, frame = self.cap.read()
            if success:
                results = self.model.predict(frame, conf=0.35, verbose=False)
                self.process_frame_logic(results)

                rendered = results[0].plot()
                img = Image.fromarray(cv2.cvtColor(rendered, cv2.COLOR_BGR2RGB))
                ctk_img = ctk.CTkImage(img, size=(880, 500))
                self.stream_view.configure(image=ctk_img)
                self.stream_view.image = ctk_img

            self.after(10, self.run_engine_loop)

    def toggle_engine(self):
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)
            self.is_running = True
            self.btn_toggle.configure(text="STOP ENGINE", fg_color="#A93226", text_color="white")
            self.run_engine_loop()
        else:
            self.is_running = False
            if self.cap: self.cap.release()
            self.btn_toggle.configure(text="START SCANNER ENGINE", fg_color=self.CLR_GOLD, text_color="black")

if __name__ == "__main__":
    app = AceTrackAI()
    app.mainloop()