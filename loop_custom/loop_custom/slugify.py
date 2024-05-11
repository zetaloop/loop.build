def wrapper(default):
    def _uslugify(value, sep, **kwargs):
        if sep == "__LOOP__HASH12":
            import hashlib

            hash = hashlib.sha256(value.encode()).hexdigest()
            hash = str(int(hash, 16))[:12]
            return f"{hash}"
        else:
            return default(value, sep, **kwargs)

    return _uslugify


import pymdownx.slugs

pymdownx.slugs._uslugify = wrapper(pymdownx.slugs._uslugify)

print("\033[32mINFO    -  Slugify patched (pymdownx.slugs._uslugify)\033[0m")
