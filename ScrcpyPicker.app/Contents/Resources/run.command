#!/bin/zsh

PY_SCRIPT="/Users/iamkurtgoz/Software/ScrpyApp/scrcpy_picker.py"

PY_BIN="$(command -v python3 || true)"
if [ -z "$PY_BIN" ]; then
	PY_BIN="/usr/bin/python3"
fi

# Run the Python picker
"$PY_BIN" "$PY_SCRIPT"
STATUS=$?

# Keep the window if something failed to show the message
if [ $STATUS -ne 0 ]; then
	echo "\nÇıkış kodu: $STATUS"
	echo "Pencereyi kapatmak için Enter'a basın..."
	read _
fi

exit $STATUS
