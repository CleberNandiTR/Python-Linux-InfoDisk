import os
import contextlib
from textwrap import dedent

def clean():
    os.system('cls' if os.name == 'nt' else 'clear')

def convertBytes(intVal):
    result = intVal
    # Recebe valor em bytes
    if len(str(result)) >= 4:
        kbytes = str(result / 1024)
        kbytes = kbytes.split(".")[0]

        # Recebe valor em kbytes
        if len(kbytes) >=4:
            megabytes =  str(int(kbytes) / 1024)
            megabytes = megabytes.split(".")[0]

            # Recebe valor em megabytes
            if int(megabytes) >= 1024:
                gigabytes =  str(int(megabytes) / 1024)
                return "{:.4s} gigabytes.".format(gigabytes)
            else:
                return "{:.4s} megabytes".format(megabytes)
        else:
            return "{:.4s} kbytes".format(kbytes)
    else:
        return "{:.4s} bytes".format(result)

def diskUsageLinux(path):
    import collections
    _ntuple_diskusage = collections.namedtuple('usage', 'total used free')
    st = os.statvfs(path)
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize    

    result = dedent("""\
                ************************************************************************************************
                {}{}{}
                ************************************************************************************************
                {}{}{}{}{}{}{}
                ************************************************************************************************
                {}{}{}{}{}{}{}
                ************************************************************************************************
                """.format("*", path.center(94), "*".center(2),
                                "*", "Espaço total".center(30), "*".center(2),"Espaço usado".center(30), "*".center(2), "Espaço livre".center(30), "*".center(2), 
                                "*", str(convertBytes(total)).center(30), "*".center(2), str(convertBytes(used)).center(30), "*".center(2), 
                                str(convertBytes(free)).center(30), "*".center(2)))
    
    # return _ntuple_diskusage(total, used, free)
    return result

if __name__ == "__main__":
    clean()
    with contextlib.closing(open("/etc/mtab")) as fp:
        for m in fp:
            fs_spec, fs_file, fs_vf, fs_mn, fs_preq, fs_passno = m.split()
            if fs_spec.startswith("/"):
                r = os.statvfs(fs_file)
                print(diskUsageLinux(fs_file))