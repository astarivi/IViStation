# Apparently unused?
import glob, os, shutil, sqlite3, sys, xbmc, xbmcgui
pDialog				= xbmcgui.DialogProgress()
dialog				= xbmcgui.Dialog()
pDialog.update(0)
try:
	Updaye_Emulators = sys.argv[1:][0]
	Update_CUT_Games = sys.argv[2:][0]
	Update_XBE_Games = sys.argv[3:][0]
except:
	Updaye_Emulators = "0"
	Update_CUT_Games = "0"
	Update_XBE_Games = "1"
#####	Sets paths.
Root_Directory 	= xbmc.translatePath("Special://root/")
if str(xbmc.getCondVisibility('Skin.String(Custom_Emulator_Path)')) == "1":
	Emulator_Folder_Path		= xbmc.getInfoLabel('Skin.String(Custom_Emulator_Path)')
else:
	Emulator_Folder_Path		= Root_Directory + '_emulators\\'
Game_Directories		= [ "E:\\Games\\","E:\\Games1\\","E:\\Games2\\","F:\\Games\\","F:\\Games1\\","F:\\Games2\\","G:\\Games\\","G:\\Games1\\","G:\\Games2\\" ]
Homebrew_Directories	= [ "E:\\Homebrew\\","F:\\Homebrew\\","G:\\Homebrew\\" ]
MyPrograms6_db			= xbmc.translatePath("special://profile/database/MyPrograms6.db")
ThumbDirectory			= xbmc.translatePath("special://profile/thumbnails/programs/")
Temp_Profile_Directory	= xbmc.translatePath("special://profile/thumbnails/temp/")
Sub_Directories			= [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f" ]
###########
## Cleanup
if os.path.isdir(Temp_Profile_Directory): shutil.rmtree(Temp_Profile_Directory)
## Xbox Games
if os.path.isfile(MyPrograms6_db):
	for Sub_Directories in Sub_Directories:
		if not os.path.isdir(Temp_Profile_Directory): os.mkdir(Temp_Profile_Directory)
		if not os.path.isdir(os.path.join(Temp_Profile_Directory, Sub_Directories)): os.mkdir(os.path.join(Temp_Profile_Directory, Sub_Directories))
	try:
		rows = sqlite3.connect(xbmc.translatePath(MyPrograms6_db)).cursor().execute("SELECT * FROM files").fetchall()
		CountList = 1
		for row in rows:
			Game_Title = row[3]
			DefaultTBN = row[1][:-3] + "tbn"
			ThumbCache = xbmc.getCacheThumbName(row[1])
			if os.path.isdir(row[1][:9]):
				if os.path.isfile(row[1]):
					if CountList == 1: pDialog.create("Generating Thumbnails","Initializing")
					pDialog.update(((CountList-1) * 100) / len(os.listdir(row[1][:9])),"Scanning [B][UPPERCASE]Xbox Games[/B][/UPPERCASE] for .tbn files",Game_Title)
					if os.path.isfile(DefaultTBN):
						shutil.copy2(DefaultTBN, Temp_Profile_Directory + ThumbCache[0] + "\\" + ThumbCache)
					CountList = CountList + 1
	except:
		dialog.ok("Error","","Database is empty.","Enter the games menu so XBMC can scan in your games.")
if not os.path.isdir(Temp_Profile_Directory):
	for Sub_Directories in Sub_Directories:
		if not os.path.isdir(Temp_Profile_Directory): os.mkdir(Temp_Profile_Directory)
		if not os.path.isdir(os.path.join(Temp_Profile_Directory, Sub_Directories)): os.mkdir(os.path.join(Temp_Profile_Directory, Sub_Directories))
## Homebrew
CountList = 1
pDialog.update(0)
for Homebrew_Directories in Homebrew_Directories:
	if os.path.isdir(Homebrew_Directories):
		if CountList == 1:	pDialog.create("Generating Thumbnails","Initializing")
		for Folders in sorted(os.listdir(Homebrew_Directories)):
			HomebrewFolder = os.path.join(Homebrew_Directories, Folders) + "\\"
			if os.path.isdir(HomebrewFolder):
				for XBE_Files in sorted(glob.glob(HomebrewFolder + "default.xbe")):
					print XBE_Files
					XBE_Files = XBE_Files.replace("\\","\\").lower()
					DefaultTBN = XBE_Files[:-3] + "tbn"
					ThumbCache = xbmc.getCacheThumbName(XBE_Files)
					pDialog.update(((CountList-1) * 100) / len(XBE_Files),"Scanning [B][UPPERCASE]Xbox Homebrew[/B][/UPPERCASE] for .tbn files",XBE_Files)
					if os.path.isfile(DefaultTBN):
						shutil.copy2(DefaultTBN, Temp_Profile_Directory + ThumbCache[0] + "\\" + ThumbCache)
					CountList = CountList + 1
## Remove old programs folder and rename temp folder	
if os.path.isdir(ThumbDirectory): shutil.rmtree(ThumbDirectory)
os.rename(Temp_Profile_Directory[:-1], Temp_Profile_Directory[:-5] + "Programs")
pDialog.update(0)
pDialog.close()
dialog.ok("Thumbnail Generator","","Process Complete")