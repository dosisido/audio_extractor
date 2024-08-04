

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

        
