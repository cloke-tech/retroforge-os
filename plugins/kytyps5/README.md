# KytyPS5-Plugin (PS5, experimentell)

[KytyPS5](https://github.com/KytyPS5/KytyPS5) ist eine freie PS5-Übersetzungsschicht (GPL-2.0) für Linux, Windows
und macOS. Seit Herbst 2026 starten damit deutlich mehr Spiele als mit dem [AnyPS5-Relinker](../anyps5/README.md),
deshalb steht KytyPS5 bei der PS5 an erster Stelle. Wie weit ein Spiel kommt, zeigt die
[Kompatibilitätsliste](https://kytyps5.github.io/). Vieles startet, durchspielbar ist bisher nur wenig.

## Voraussetzungen

- x86-64-Prozessor mit AVX2, FMA, F16C und BMI1/2 (Intel ab Haswell, AMD ab Zen)
- Vulkan 1.3, mindestens GPU-Klasse 4, 16 GB RAM (empfohlen 32 GB)
- RetroForge OS (Linux); das Spiel läuft in gamescope bzw. cage

Installation: *Emulatoren › KytyPS5* lädt den offiziellen Linux-Build aus den
[GitHub-Releases](https://github.com/KytyPS5/KytyPS5/releases) nach `/userdata/emulators/kytyps5/`.

## Spiel ablegen

```
roms/ps5/<Spielname>.ps5/app0/eboot.bin   ← gleiches Layout wie beim AnyPS5-Plugin
roms/ps5/<Spielname>.ps5/eboot.bin        ← Dump direkt im Ordner geht auch
roms/ps5/<Spielname>.zar                  ← ZArchive-Dump, wird ohne Entpacken gelesen
```

`eboot.bin` muss ein **entschlüsseltes ELF** sein. Wurde das Spiel vorher mit AnyPS5 konvertiert, legt das Plugin vor
dem Start die Original-Module zurück; AnyPS5 konvertiert beim nächsten AnyPS5-Start einfach neu.

Welcher PS5-Weg genutzt wird, lässt sich pro System oder pro Spiel unter *Einstellungen › Emulator* wählen.

## Rechtliches

RetroForge und KytyPS5 enthalten keine Spiele, Firmware oder Schlüssel. Ein entschlüsselter Dump stammt von einer
eigenen, gejailbreakten Konsole. Das Umgehen eines Kopierschutzes kann je nach Land verboten sein, in Deutschland
z. B. nach § 95a UrhG, auch für private Kopien.
