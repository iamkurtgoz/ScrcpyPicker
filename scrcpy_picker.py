#!/usr/bin/env python3

import os
import re
import shutil
import subprocess
import sys
from typing import List, Tuple


def run_command(cmd: List[str]) -> Tuple[int, str, str]:
	try:
		proc = subprocess.run(
			cmd,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			text=True,
			check=False,
		)
		return proc.returncode, proc.stdout, proc.stderr
	except FileNotFoundError as exc:
		return 127, "", str(exc)


def parse_adb_devices(output: str) -> List[dict]:
	devices: List[dict] = []
	lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
	# Skip header line like: "List of devices attached"
	if lines and lines[0].lower().startswith("list of devices"):  # defensive
		lines = lines[1:]

	for line in lines:
		# Expected formats (examples):
		# R58M123ABC\tdevice product:d1 model:SM_S911B device:d1 transport_id:1
		# emulator-5554\tdevice
		# XYZ\toffline
		# XYZ\tunauthorized
		parts = re.split(r"\s+", line)
		if not parts:
			continue

		serial = parts[0]
		# Identify state token (commonly second token)
		state = parts[1] if len(parts) > 1 else "unknown"

		# Only include healthy connected devices
		if state != "device":
			continue

		# Extract optional key:value tokens
		tokens = parts[2:] if len(parts) > 2 else []
		kv = {}
		for tok in tokens:
			if ":" in tok:
				k, v = tok.split(":", 1)
				kv[k] = v

		# Best-effort friendly name
		friendly = kv.get("model") or kv.get("device") or kv.get("product") or serial

		devices.append({
			"serial": serial,
			"state": state,
			"name": friendly,
			"meta": kv,
		})

	return devices


def find_scrcpy_path() -> List[str]:
	# Prefer explicit Homebrew path as requested
	explicit = "/opt/homebrew/bin/scrcpy"
	if os.path.exists(explicit) and os.access(explicit, os.X_OK):
		return [explicit]

	# Fallback to PATH lookup
	found = shutil.which("scrcpy")
	if found:
		return [found]

	return []


def main() -> int:
	# 1) List ADB devices
	code, out, err = run_command(["adb", "devices", "-l"])
	if code != 0:
		print("adb cihaz listesi alınamadı:")
		if err:
			print(err.strip())
		else:
			print("Bilinmeyen hata. adb kurulumunuzu ve PATH ayarlarınızı kontrol edin.")
		return code if code != 0 else 1

	devices = parse_adb_devices(out)
	if not devices:
		print("Bağlı ve yetkilendirilmiş (device) durumda hiçbir cihaz bulunamadı.")
		print("- Cihazı bağlı ve ekran kilidi açık olduğundan emin olun")
		print("- Geliştirici seçeneklerinde USB hata ayıklama açık olmalı")
		print("- Gerekirse 'adb kill-server && adb start-server' deneyin")
		return 1

	# 2) Print device list with indices
	print("Bulunan cihazlar:")
	for idx, d in enumerate(devices):
		print(f"[{idx}] {d['name']}  (serial: {d['serial']})")

	# 3) Ask for index
	while True:
		try:
			raw = input("Lütfen scrcpy çalıştırmak istediğiniz cihazın indexini girin: ").strip()
			if raw == "":
				print("Boş giriş. Lütfen bir index girin.")
				continue
			if not re.fullmatch(r"\d+", raw):
				print("Geçersiz giriş. Lütfen yalnızca sayı girin.")
				continue
			sel = int(raw)
			if sel < 0 or sel >= len(devices):
				print(f"Geçersiz index. 0 ile {len(devices)-1} arasında bir değer girin.")
				continue
			break
		except KeyboardInterrupt:
			print()  # newline
			return 130

	chosen = devices[sel]
	serial = chosen["serial"]

	# 4) Build scrcpy command
	scrcpy_bin = find_scrcpy_path()
	if not scrcpy_bin:
		print("scrcpy bulunamadı. Lütfen Homebrew ile kurun veya PATH'e ekleyin:")
		print("brew install scrcpy")
		return 127

	cmd = [
		scrcpy_bin[0],
		"--video-codec=h265",
		"--max-size=1920",
		"--max-fps=60",
		"--no-audio",
		"--keyboard=uhid",
		"-s",
		serial,
		"--turn-screen-off",
	]

	print(f"Çalıştırılıyor: {' '.join(cmd)}")
	try:
		# Forward all stdio to user so they can see scrcpy logs if any
		proc = subprocess.run(cmd)
		return proc.returncode
	except KeyboardInterrupt:
		print()
		return 130


if __name__ == "__main__":
	sys.exit(main())
