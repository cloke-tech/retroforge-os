"""KytyPS5 for RetroForge: experimental PS5 support through a translation layer.

KytyPS5 (https://github.com/KytyPS5/KytyPS5, GPL-2.0) runs decrypted PS5
dumps on x86-64 Linux with Vulkan 1.3. As of November 2026 it starts far more
titles than the AnyPS5 relinker, so it is put first for the PS5; both stay
flagged experimental and never move the "highest console" of the ladder.
"""
import importlib.util
import sys
from pathlib import Path

from retroforge.model import Emulator, Req

REPO = "KytyPS5/KytyPS5"


def register(api):
    plugin_dir = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("retroforge_kytyps5_run", plugin_dir / "run.py")
    run = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(run)

    api.add_emulator(Emulator(
        id="kytyps5", name="KytyPS5", kind="standalone", binary="kyty_emulator", args=("--game", "{rom}"),
        # PS5 code runs on the host CPU, so the Zen 2 extensions are required as for AnyPS5
        min=Req(archs=("x86_64",), isa=("avx2", "fma", "f16c", "bmi1", "bmi2"), cpu=4.5, threads=8, gpu=4,
                ram=16, vulkan="1.3"),
        rec=Req(cpu=5.5, threads=12, gpu=5, ram=32),
        features=(), experimental=True,
        note="KytyPS5: Übersetzungsschicht, viele Spiele starten, spielbar sind nur einzelne – Stand November 2026",
        source={"type": "github", "repo": REPO, "assets": {"x86_64": r"Linux-x86_64\.tar\.gz$"}}))
    api.add_emulator_to_system("ps5", "kytyps5", first=True)

    def before_launch(plan, core, **_):
        if plan.emulator.id != "kytyps5":
            return plan
        game = plan.game
        exe = plan.cmd[0] if plan.cmd else "kyty_emulator"
        plan.cmd = [sys.executable, str(plugin_dir / "run.py"), "--emulator", exe, "--game", game.path]
        try:
            run.game_root(game.path)
        except run.RunError as e:
            plan.notes.append(str(e))
        if Path(game.path).is_dir() and run.anyps5_converted(game.path):
            plan.notes.append("Mit AnyPS5 konvertiert: vor dem Start werden die Original-Module "
                              "zurückgelegt, AnyPS5 konvertiert später neu.")
        if not plan.windowed:
            plan.notes.append("KytyPS5 braucht X11/Wayland (gamescope oder cage) – "
                              "'Standalone in gamescope starten' bitte anlassen.")
        return plan

    api.on("game.before_launch", before_launch)
