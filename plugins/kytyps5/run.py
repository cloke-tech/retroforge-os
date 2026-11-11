"""Starts a PS5 dump in KytyPS5. Runs as the game process (inside gamescope/cage).

Accepted layouts (roms/ps5/):

    <Spiel>.ps5/app0/eboot.bin     same layout as the AnyPS5 plugin
    <Spiel>.ps5/eboot.bin          dump directly in the folder
    <Spiel>.zar                    ZArchive dump, streamed read-only by KytyPS5

If the AnyPS5 plugin has converted the game before, its Linux modules sit in
app0/sce_module; KytyPS5 needs the original PS5 modules, so they are moved
back first (AnyPS5 converts again on its next start).

Stdlib only – it must not depend on the frontend being importable.
"""
import argparse
import importlib.util
import os
import sys
from pathlib import Path


class RunError(RuntimeError):
    pass


def game_root(game):
    """Returns the path KytyPS5 gets as --game."""
    game = Path(game)
    if game.is_file():
        if game.suffix.lower() != ".zar":
            raise RunError(f"{game.name}: KytyPS5 startet nur Spielordner oder ZArchive-Dumps (.zar).")
        return game
    for cand in (game / "app0", game):
        if (cand / "eboot.bin").is_file():
            return cand
    raise RunError(f"Keine eboot.bin in {game} – der entschlüsselte Dump gehört nach '<Spiel>.ps5/app0/'.")


def anyps5_converted(game):
    return Path(game, ".anyps5").is_dir()


def undo_anyps5(game, log=print):
    port_py = Path(__file__).resolve().parent.parent / "anyps5" / "port.py"
    if not port_py.is_file():
        raise RunError("Spiel wurde mit AnyPS5 konvertiert, das AnyPS5-Plugin fehlt aber – "
                       "Original-Module liegen in .anyps5/input/.")
    spec = importlib.util.spec_from_file_location("retroforge_anyps5_port_kyty", port_py)
    port = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(port)
    log("KytyPS5: AnyPS5-Port gefunden – lege die Original-Module zurück nach app0/.")
    port.restore(game, log=log)


def check_elf(root):
    if root.is_dir():
        with open(root / "eboot.bin", "rb") as f:
            if f.read(4) != b"\x7fELF":
                raise RunError("eboot.bin ist kein entschlüsseltes ELF (verschlüsselter SELF-Container?). "
                               "KytyPS5 braucht einen entschlüsselten Dump.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="KytyPS5: PS5-Dump starten")
    ap.add_argument("--emulator", required=True)
    ap.add_argument("--game", required=True)
    ap.add_argument("extra", nargs="*")
    args = ap.parse_args(argv)
    try:
        if Path(args.game).is_dir() and anyps5_converted(args.game):
            undo_anyps5(args.game)
        root = game_root(args.game)
        check_elf(root)
    except RunError as e:
        print(f"KytyPS5: {e}", file=sys.stderr)
        return 2
    cmd = [args.emulator, "--game", str(root)] + args.extra
    sys.stdout.flush()
    os.execv(cmd[0], cmd)


if __name__ == "__main__":
    sys.exit(main())
