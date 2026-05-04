import subprocess


class AppLauncher:
    """Abre aplicaciones en macOS usando el comando 'open -a'."""

    @staticmethod
    def open(app_name: str) -> None:
        """Lanza la aplicación indicada. app_name debe coincidir con el nombre en /Applications."""
        subprocess.run(["open", "-a", app_name], check=False)