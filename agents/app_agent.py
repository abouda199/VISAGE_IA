
import os
import subprocess
import shutil


class AppAgent:

    def __init__(self):

        self.applications = {
            "calculatrice": "calc.exe",
            "calculator": "calc.exe",
            "bloc-notes": "notepad.exe",
            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "explorateur": "explorer.exe",
            "explorateur de fichiers": "explorer.exe",
            "powershell": "powershell.exe",
            "terminal": "powershell.exe",
            "vscode": "code",
            "vs code": "code",
            "visual studio code": "code"
        }

    def execute(self, application):

        application = application.strip().lower()

        command = self.applications.get(application)

        if not command:
            return {
                "handled": False
            }

        if os.name != "nt":
            return {
                "handled": True,
                "agent": "AppAgent",
                "response": (
                    "Cet agent est configuré pour Windows."
                ),
                "emotion": "sad"
            }

        executable = shutil.which(command)

        if executable is None:
            return {
                "handled": True,
                "agent": "AppAgent",
                "response": (
                    f"Je ne trouve pas l'application "
                    f"{application} sur ton ordinateur."
                ),
                "emotion": "sad"
            }

        subprocess.Popen(
            [executable],
            shell=False
        )

        return {
            "handled": True,
            "agent": "AppAgent",
            "response": (
                f"Je lance {application}."
            ),
            "emotion": "happy"
        }
