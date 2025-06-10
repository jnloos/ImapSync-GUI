import tkinter as tk
from threading import Thread
from app.ImapSync import ImapSync
from app.Localization import __
from app.modules.CredentialForm import CredentialForm
from app.modules.OutputBox import OutputBox
from app.modules.StatusIndicator import StatusIndicator

class ImapSyncWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("IMAPSync")
        self.root.geometry("900x600")
        self.root.configure(bg="white")

        # Main container
        self.container = tk.Frame(self.root, bg="white", padx=20, pady=20)
        self.container.pack(fill="both", expand=True)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

        # Credential block
        forms_frame = tk.Frame(self.container, bg="white")
        forms_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        forms_frame.grid_columnconfigure(0, weight=1)
        forms_frame.grid_columnconfigure(1, weight=1)

        # Source credential form
        source = tk.Frame(forms_frame, bg="white")
        source.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        source.grid_columnconfigure(0, weight=1)
        source.grid_columnconfigure(1, weight=0)

        tk.Label(source, text=__("sections.source"), font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        self.source_status = StatusIndicator(source, row=0, column=1, sticky="e", padx=(5, 0))
        self.source_form = CredentialForm(source, ["host", "port", "user", "password"])
        self.source_form.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(5, 0))

        # Target credential form
        target = tk.Frame(forms_frame, bg="white")
        target.grid(row=0, column=1, sticky="nsew")
        target.grid_columnconfigure(0, weight=1)
        target.grid_columnconfigure(1, weight=0)

        tk.Label(target, text=__("sections.target"), font=("Arial", 11, "bold"), bg="white").grid(row=0, column=0, sticky="w")
        self.target_status = StatusIndicator(target, row=0, column=1, sticky="e", padx=(5, 0))
        self.target_form = CredentialForm(target, ["host", "port", "user", "password"])
        self.target_form.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(5, 0))

        # Buttons
        button_frame = tk.Frame(self.container, bg="white")
        button_frame.grid(row=1, column=0, columnspan=2, pady=(15, 15), sticky="e")

        self.start_button = tk.Button(
            button_frame,
            text=__("button_start"),
            bg="#0A9B31",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.__start_sync,
            state="normal"
        )
        self.start_button.pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text=__("button_clear"),
            bg="#777777",
            fg="white",
            font=("Arial", 11),
            command=self.__clear_output
        ).pack(side="left", padx=10)

        # Output container
        self.container.grid_rowconfigure(3, weight=1)
        tk.Label(self.container, text=__("sections.output"), font=("Arial", 11, "bold"), bg="white").grid(row=2, column=0, sticky="w")
        self.output_box = OutputBox(self.container)
        self.output_box.widget().grid(row=3, column=0, columnspan=2, sticky="nsew")

    def __clear_output(self):
        self.output_box.clear()

    def __start_sync(self):
        cfg = self.__build_config()

        # Check credentials
        cred1 = ImapSync.check_credentials(cfg['host1'], cfg['port1'], cfg['user1'], cfg['password1'])
        self.source_status.set_status('success' if cred1 else 'failure')
        cred2 = ImapSync.check_credentials(cfg['host2'], cfg['port2'], cfg['user2'], cfg['password2'])
        self.target_status.set_status('success' if cred2 else 'failure')
        if not (cred1 and cred2):
            self.output_box.append(__("check_failed"))
            return

        # Start migration if valid
        self.output_box.append(__("migration_starting"))
        self.start_button.config(state="disabled")
        Thread(target=self.__run_sync, daemon=True).start()

    def __run_sync(self):
        # Run process and display logs
        cfg = self.__build_config()
        process = ImapSync(cfg).sync_process()
        for line in process.stdout:
            self.output_box.append(line.strip())
        process.wait()

        # Feedback and reset
        if process.returncode == 0:
            self.output_box.append(__("migration_success"))
        else:
            self.output_box.append(f"{__('migration_failed')} (Code {process.returncode})")
        self.start_button.config(state="normal")

    def __build_config(self) -> dict[str, str]:
        src = self.source_form.get_config()
        tgt = self.target_form.get_config()

        return {
            'host1': src['host'], 'port1': src['port'], 'user1': src['user'], 'password1': src['password'],
            'host2': tgt['host'],  'port2': tgt['port'], 'user2': tgt['user'], 'password2': tgt['password'],
        }
