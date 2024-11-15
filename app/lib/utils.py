

def getWisperModel():
    import psutil
    ram = psutil.virtual_memory().total // 1024//1024/1000
    if ram > 10:
        return "large"
    elif ram > 5:
        return "medium"
    elif ram > 2:
        return "small"
    elif ram > 1.5:
        return "base"
    else:
        return "tiny"

def format_time_from_seconds(seconds):
    m = seconds // 60
    s = seconds % 60
    h = m // 60
    m = m % 60
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"

def get_mime(file: str) -> str:
    import magic
    return magic.from_file(file, mime=True)