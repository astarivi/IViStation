import sys
import xbmc
import xbmcgui

print "| dialog_ok.py loaded."
show_dialog = 0
try:
    setting = sys.argv[1:][0]
except:
    setting = ""
try:
    title = sys.argv[2:][0]
except:
    title = ""
try:
    line1 = sys.argv[3:][0]
except:
    line1 = ""
try:
    line2 = sys.argv[4:][0]
except:
    line2 = ""
try:
    line3 = sys.argv[5:][0]
except:
    line3 = ""
try:
    runscript = sys.argv[6:][0]
except:
    runscript = ""
try:
    extra = sys.argv[7:][0]
except:
    extra = ""
try:
    show_dialog = setting.split('-')[1]
except:
    pass
if setting == "run_script":
    xbmc.executebuiltin('RunScript("' + runscript + '")')
    xbmcgui.Dialog().ok(title, line1, line2, line3)
elif extra == "reboot":
    xbmcgui.Dialog().ok(title, line1, line2, line3)
    xbmc.executebuiltin('RestartApp')
elif setting.startswith("show_enabled"):
    if xbmc.getCondVisibility('Skin.HasSetting(' + show_dialog + ')'):
        xbmcgui.Dialog().ok(title, line1, line2, line3)
elif setting.startswith("show_disabled"):
    if not xbmc.getCondVisibility('Skin.HasSetting(' + show_dialog + ')'):
        xbmcgui.Dialog().ok(title, line1, line2, line3)
elif setting.startswith("show_both"):
    xbmcgui.Dialog().ok(title, line1, line2, line3)
