#!/usr/bin/env python3
"""Local secret store for API keys (voice and publishing providers). Never prints a secret.

  python secrets_store.py set fish_api_key       # reads the secret from stdin (never pass it as an argument)
  python secrets_store.py check fish_api_key     # says whether it exists, without showing it
  python secrets_store.py delete fish_api_key
  python secrets_store.py backend                # which backend is in use
  from secrets_store import read; read("fish_api_key")

Lookup order when reading:
  1. environment variable TRAVUS_<NAME> (e.g. TRAVUS_FISH_API_KEY) - handy for CI
  2. OS keychain through the `keyring` package (macOS Keychain, Windows Credential Manager, Secret Service)
  3. Windows only, when `keyring` is missing: DPAPI-encrypted file in %APPDATA%\\travus-reels\\secrets\\<name>.dpapi
Secrets are never written in plain text. Known names: fish_api_key, elevenlabs_api_key, ghl_token, gemini_api_key.
"""
import os
import sys

SERVICE = "travus-reels-maker"


def _env_name(name):
    return "TRAVUS_" + name.upper()


def _keyring():
    try:
        import keyring  # type: ignore
        from keyring.backends import fail  # type: ignore

        if isinstance(keyring.get_keyring(), fail.Keyring):
            return None
        return keyring
    except Exception:
        return None


# ---------------------------------------------------------------- Windows DPAPI fallback
def _dpapi_dir():
    return os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "travus-reels", "secrets")


def _dpapi(data, protect):
    import ctypes
    import ctypes.wintypes as wt

    class BLOB(ctypes.Structure):
        _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    def blob(b):
        buf = ctypes.create_string_buffer(b, len(b))
        return BLOB(len(b), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char))), buf

    inp, _k1 = blob(data)
    ent, _k2 = blob(SERVICE.encode())
    out = BLOB()
    fn = ctypes.windll.crypt32.CryptProtectData if protect else ctypes.windll.crypt32.CryptUnprotectData
    args = (ctypes.byref(inp), SERVICE if protect else None, ctypes.byref(ent), None, None, 0x1, ctypes.byref(out))
    if not fn(*args):
        raise OSError("DPAPI failed (different Windows user or machine?)")
    res = ctypes.string_at(out.pbData, out.cbData)
    ctypes.windll.kernel32.LocalFree(out.pbData)
    return res


def backend():
    if _keyring():
        return "keyring (%s)" % type(_keyring().get_keyring()).__name__
    if os.name == "nt":
        return "windows-dpapi"
    return "none (install it: python -m pip install keyring)"


def read(name, required=True):
    v = os.environ.get(_env_name(name))
    if v:
        return v
    kr = _keyring()
    if kr:
        v = kr.get_password(SERVICE, name)
        if v:
            return v
    if os.name == "nt":
        p = os.path.join(_dpapi_dir(), name + ".dpapi")
        if os.path.exists(p):
            return _dpapi(open(p, "rb").read(), False).decode("utf-8")
    if required:
        raise SystemExit("secret '%s' not found. Run:  python %s set %s   (and paste it on stdin)"
                         % (name, os.path.abspath(__file__), name))
    return None


def write(name, value):
    kr = _keyring()
    if kr:
        kr.set_password(SERVICE, name, value)
        return "keyring"
    if os.name == "nt":
        os.makedirs(_dpapi_dir(), exist_ok=True)
        open(os.path.join(_dpapi_dir(), name + ".dpapi"), "wb").write(_dpapi(value.encode("utf-8"), True))
        return "windows-dpapi"
    raise SystemExit("no secure backend available. Install one:  python -m pip install keyring\n"
                     "or export %s in your shell profile." % _env_name(name))


def delete(name):
    kr = _keyring()
    if kr:
        try:
            kr.delete_password(SERVICE, name)
        except Exception:
            pass
    p = os.path.join(_dpapi_dir(), name + ".dpapi")
    if os.path.exists(p):
        os.remove(p)


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "backend":
        print(backend())
    elif len(sys.argv) == 3 and sys.argv[1] in ("set", "check", "delete"):
        cmd, name = sys.argv[1], sys.argv[2]
        if cmd == "set":
            if sys.stdin.isatty():  # typed or pasted in a terminal: hidden input
                import getpass
                value = getpass.getpass("paste the value for %s (hidden) and press Enter: " % name).strip()
            else:
                value = sys.stdin.readline().strip()
            if not value:
                raise SystemExit("nothing received on stdin")
            where = write(name, value)
            print("stored:", name, "(%d characters, %s)" % (len(value), where))
        elif cmd == "check":
            v = read(name, required=False)
            print(("ok: %s exists (%d characters)" % (name, len(v))) if v else ("missing: " + name))
            sys.exit(0 if v else 1)
        else:
            delete(name)
            print("deleted:", name)
    else:
        raise SystemExit(__doc__)
