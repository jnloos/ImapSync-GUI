import subprocess

class ImapSync:
    def __init__(self, config: dict[str, str]):
        self.config = config

    @staticmethod
    def check_credentials(host: str, port: str, user: str, password: str) -> bool:
        args = [
            "imapsync",
            "--host1", host,
            "--port1", port,
            "--user1", user,
            "--password1", password,
            "--justlogin",
            "--nolog"
        ]

        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=20)
            return result.returncode == 0
        except Exception:
            return False

    def sync_process(self) -> subprocess.Popen[str]:
        cfg = self.config

        args = [
            "imapsync",
            "--host1", cfg["host1"],
            "--port1", cfg["port1"],
            "--user1", cfg["user1"],
            "--password1", cfg["password1"],
            "--host2", cfg["host2"],
            "--port2", cfg["port2"],
            "--user2", cfg["user2"],
            "--password2", cfg["password2"],
            "--automap",
            "--syncinternaldates",
            "--nofoldersizes",
            "--nolog"
        ]

        return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

