## ScrcpyPicker

Basit bir terminal aracı ve çift tıklanabilir macOS uygulaması ile `adb` üzerinden bağlı Android cihazlarını listeler, seçtiğiniz cihazı `scrcpy` ile başlatır.

- Python betiği: `scrcpy_picker.py`
- macOS uygulaması: `ScrcpyPicker.app`

---

### Türkçe (TR)

#### Gereksinimler
- **ADB** (Android Platform Tools)
  - Kurulum (Homebrew):
```bash
brew install --cask android-platform-tools
```
- **scrcpy**
  - Kurulum (Homebrew):
```bash
brew install scrcpy
```
- **Python 3** (macOS’te genellikle `/usr/bin/python3` mevcut)

Not: Uygulama öncelikle `/opt/homebrew/bin/scrcpy` yolunu dener, yoksa `PATH` içinden `scrcpy` arar.

#### Hızlı Başlangıç
- Terminal’den Python betiği:
```bash
python3 /Users/iamkurtgoz/Software/ScrpyApp/scrcpy_picker.py
```
- Finder’dan macOS uygulaması:
  - `ScrcpyPicker.app` üzerine çift tıklayın.
  - İlk açılışta “Bilinmeyen geliştirici” uyarısı görürseniz Sistem Ayarları → Güvenlik ve Gizlilik → “Yine de Aç”.

#### Nasıl Çalışır
1. `adb devices -l` çıktısı okunur ve yalnızca `device` durumundaki cihazlar listelenir.
2. Ekranda `[index] İsim (serial: XYZ)` formatında cihazlar gösterilir.
3. Sizden çalıştırmak istediğiniz cihazın index’i istenir.
4. Seçim yapıldığında aşağıdaki parametrelerle `scrcpy` başlatılır:
```bash
/opt/homebrew/bin/scrcpy --video-codec=h265 --max-size=1920 --max-fps=60 --no-audio --keyboard=uhid -s ADB_DEVICE_CODE --turn-screen-off
```
  - Eğer `/opt/homebrew/bin/scrcpy` yoksa `which scrcpy` sonucundaki ikili kullanılır.

#### macOS Uygulaması (Çift Tıklama)
- Uygulama yapısı:
  - `ScrcpyPicker.app/Contents/Info.plist`
  - `ScrcpyPicker.app/Contents/MacOS/ScrcpyPicker` (başlatıcı)
  - `ScrcpyPicker.app/Contents/Resources/run.command` (Terminal uyumlu başlatma)
- Çalışma mantığı:
  - `ScrcpyPicker` başlatıcı, `Resources/run.command` dosyasını Terminal ile açar.
  - `run.command` Python betiğini çalıştırır, hata varsa pencerenin kapanmasını engellemek için Enter bekletmesi yapar.

#### İzinler ve Güvenlik
- İlk çalıştırmada macOS Gatekeeper uyarı verebilir. Sistem Ayarları → Güvenlik ve Gizlilik’ten “Yine de Aç” deyin.
- `adb` ile cihaz bağlantısı için:
  - Geliştirici seçeneklerinden USB hata ayıklama aktif olmalı.
  - Cihazda yetkilendirme penceresi kabul edilmeli (ilk bağlantıda).
- Terminal izinleri: Bazı macOS sürümlerinde Terminal için erişim izinleri (Erişilebilirlik/Automation) gerekebilir.

#### Sorun Giderme
- Uygulama açılıp kapanıyor, aksiyon yok:
  - `adb` kurulu mu? `adb devices -l` çıktısını kontrol edin.
  - `scrcpy` kurulu mu? `which scrcpy` bir yol döndürmeli.
  - Cihaz `device` durumunda mı? `unauthorized/offline` cihazlar listelenmez.
  - `run.command` açıldığında hata kodu mesajı görürseniz bağımlılıkları kontrol edin.
- `scrcpy` performansı düşük:
  - USB 3.0 kablo kullanın, `--max-size` ve `--max-fps` parametrelerini düşürmeyi deneyin.
- `scrcpy` sesi yok:
  - Parametreler `--no-audio` içerir. Ses gerekiyorsa bu parametreyi betikte/komutta kaldırın.

#### Özelleştirme
- `scrcpy` argümanlarını güncellemek için `scrcpy_picker.py` içindeki `cmd` listesinde değişiklik yapın.
- `python3` yolunu sabitlemek için `ScrcpyPicker.app/Contents/Resources/run.command` dosyasında `PY_BIN` değişkenini `/usr/bin/python3` olarak bırakabilirsiniz.
- Uygulama ikonunu eklemek için `ScrcpyPicker.app/Contents/Resources/AppIcon.icns` yerleştirin ve `Info.plist` içine ekleyin:
```xml
<key>CFBundleIconFile</key>
<string>AppIcon</string>
```

#### Bilinen Kısıtlar
- Yalnızca `device` durumundaki cihazlar listelenir.
- `adb` ve `scrcpy` yoksa uygulama çalışmaz.
- Komut, varsayılan olarak ekranı kapatma (`--turn-screen-off`) parametresiyle başlar.

---

### English (EN)

#### Requirements
- **ADB** (Android Platform Tools)
  - Install (Homebrew):
```bash
brew install --cask android-platform-tools
```
- **scrcpy**
  - Install (Homebrew):
```bash
brew install scrcpy
```
- **Python 3** (macOS usually has `/usr/bin/python3`)

Note: The app first tries `/opt/homebrew/bin/scrcpy`; if missing, it falls back to the `scrcpy` found in `PATH`.

#### Quick Start
- From Terminal (Python script):
```bash
python3 /Users/iamkurtgoz/Software/ScrpyApp/scrcpy_picker.py
```
- From Finder (macOS app):
  - Double-click `ScrcpyPicker.app`.
  - If you see an “Unidentified developer” warning, go to System Settings → Security & Privacy → “Open Anyway”.

#### How It Works
1. Reads `adb devices -l` and lists only devices in `device` state.
2. Prints devices as `[index] Name (serial: XYZ)`.
3. Prompts you for the selected index.
4. Launches `scrcpy` with the following parameters:
```bash
/opt/homebrew/bin/scrcpy --video-codec=h265 --max-size=1920 --max-fps=60 --no-audio --keyboard=uhid -s ADB_DEVICE_CODE --turn-screen-off
```
  - If `/opt/homebrew/bin/scrcpy` is unavailable, uses the binary from `which scrcpy`.

#### macOS App (Double-Click)
- App layout:
  - `ScrcpyPicker.app/Contents/Info.plist`
  - `ScrcpyPicker.app/Contents/MacOS/ScrcpyPicker` (launcher)
  - `ScrcpyPicker.app/Contents/Resources/run.command` (Terminal-friendly launcher)
- Behavior:
  - The launcher opens `run.command` in Terminal.
  - `run.command` runs the Python script; on failure it waits for Enter so the window does not close immediately.

#### Permissions & Security
- macOS Gatekeeper may block the first run. Use System Settings → Security & Privacy → “Open Anyway”.
- For `adb` device access:
  - USB debugging must be enabled in Developer Options.
  - Accept the authorization prompt on the device (first connection).
- Terminal permissions: some macOS versions may require Accessibility/Automation permissions for Terminal.

#### Troubleshooting
- App opens then closes with no action:
  - Is `adb` installed? Check `adb devices -l` output.
  - Is `scrcpy` installed? `which scrcpy` should return a path.
  - Is the device in `device` state? `unauthorized/offline` devices are ignored.
  - If `run.command` shows a non-zero exit code, verify dependencies.
- Low `scrcpy` performance:
  - Use a USB 3.0 cable; try lowering `--max-size` and `--max-fps`.
- No audio in `scrcpy`:
  - Parameters include `--no-audio`. Remove it if you need audio.

#### Customization
- Change `scrcpy` arguments inside `scrcpy_picker.py` in the `cmd` list.
- To pin the Python binary, set `PY_BIN` to `/usr/bin/python3` in `ScrcpyPicker.app/Contents/Resources/run.command`.
- To add an app icon, place `AppIcon.icns` at `ScrcpyPicker.app/Contents/Resources/` and add to `Info.plist`:
```xml
<key>CFBundleIconFile</key>
<string>AppIcon</string>
```

#### Known Limitations
- Only lists devices in `device` state.
- The app will not work without `adb` and `scrcpy` installed.
- By default, it launches with `--turn-screen-off` parameter.

## Find this repository useful? :heart:
Support it by joining __[stargazers](https://github.com/iamkurtgoz/ScrcpyPicker)__ for this repository. :star: <br>
Also, __[follow me](https://github.com/iamkurtgoz)__ on GitHub for my next creations! 🤩

# License
```xml
    Copyright 2024 Mehmet KURTGOZ

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
```