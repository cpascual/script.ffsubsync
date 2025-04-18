from pathlib import Path
import subprocess
import xbmc
import xbmcaddon
import xbmcgui

addon = xbmcaddon.Addon()
player = xbmc.Player()
current_video = Path(player.getPlayingFile())
current_dir= current_video.parent
sub_files=list(current_dir.glob(current_video.stem+"*.srt"))
sub = None
if not sub_files:
    sub_files=list(current_dir.glob("*.srt"))
if len(sub_files)>1:
    idx=xbmcgui.Dialog().select("Choose the subtitle to synchronize", [f.stem for f in sub_files])
    sub = str(sub_files[idx])
elif len(sub_files) == 1:
    sub = str(sub_files[0])
    confirm=xbmcgui.Dialog().yesno("Synchronize", f"Synchronize '{sub}'?", defaultbutton=xbmcgui.DLG_YESNO_YES_BTN)
    if not confirm:
        sub = None
else:
    xbmcgui.Dialog().notification("Cannot find subtitle file", "", xbmcgui.NOTIFICATION_ERROR)
if sub is not None:
    sync= str(Path(sub).with_suffix(".sync.srt"))
    ffs = subprocess.run(["ffs", str(current_video), "-i", sub, "-o", sync])
    if ffs.returncode ==0:
        xbmcgui.Dialog().notification("Sub Sync succeeded", sync, xbmcgui.NOTIFICATION_INFO)
        player.setSubtitles(sync)   
    else:
        xbmcgui.Dialog().notification("Sub Sync failed", sub, xbmcgui.NOTIFICATION_ERROR)