import os
import zlib
import xbmc
import base64
import xbmcgui
import datetime
import traceback
import xml.sax.saxutils
import simplejson as json

from utils.layout_helper import *
from ivistation.downloader import memory_download, turbo_download

LISTING_URL = "https://raw.githubusercontent.com/astarivi/IVistation/master/remote/library.json"


class DownloadListingManager(object):
    def __init__(self, progress_dialog):
        self.progress_dialog = progress_dialog

        self.progress_dialog.update(
            0,
            "Retrieving latest downloads listing.",
            "Snapshot: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "This can take some time, please be patient."
        )

        self.library = json.loads(
            memory_download(LISTING_URL, timeout=10)
        )

        self.progress_dialog.update(
            25,
            "Downloads listing retrieved.",
            "Snapshot: {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            "Advancing to next step."
        )

        self.thumbnails_path = xbmc.translatePath(
            "special://root/ivistation/media/downloader"
        )

        if not os.path.isdir(self.thumbnails_path):
            os.makedirs(self.thumbnails_path)

        self.label_sections = []
        self.visibility_toggles = 0
        self.item_id = 100

    def _handle_sections(self, layout_target):
        for section, content in self.library.items():

            thumbnails_section = os.path.join(self.thumbnails_path, section)
            if not os.path.isdir(thumbnails_section):
                os.makedirs(thumbnails_section)

            # Handle section
            self.visibility_toggles += 1
            self.label_sections.append(
                (self.visibility_toggles, content["title"],)
            )

            # Write the section header
            layout_target.write(
                DOWNLOAD_SECTION_HEADER.format(
                    focus_id=self.visibility_toggles
                )
            )

            # Write the section items
            for item in content["items"]:
                self.item_id += 1

                img_extension = item["thumbnail"].split(".")[-1]
                description = xml.sax.saxutils.escape(item["description"])
                # So the encoding takes less space
                del item["description"]

                layout_target.write(
                    DOWNLOAD_ITEM.format(
                        self.item_id,
                        description,
                        item["download_size"],
                        item["install_size"],
                        item["id"],
                        item["url"],
                        type=section,
                        title=xml.sax.saxutils.escape(item["title"]),
                        # Compress the data, then encode it
                        entry=base64.b64encode(zlib.compress(json.dumps(item), 9)),
                        img_extension=img_extension,
                    )
                )

                thumbnail_file = os.path.join(thumbnails_section,  "{}.{}".format(item["id"], img_extension))

                # Download the thumbnail if we don't have it
                if not os.path.isfile(thumbnail_file):
                    turbo_download(item["thumbnail"], thumbnail_file)

            # Write the section footer
            layout_target.write(DOWNLOAD_SECTION_FOOTER)

    def _handle_labels(self, layout_target):
        visibility_toggles = []

        for x in range(1, self.visibility_toggles + 1):
            visibility_toggles.append(
                DOWNLOAD_VISIBILITY_TOGGLE.format(
                    x
                )
            )

        layout_target.write(
            DOWNLOAD_LABEL_GROUP_LIST_HEADER.format(
                visibility_toggles=" | ".join(visibility_toggles)
            )
        )

        for label in self.label_sections:
            layout_target.write(
                DOWNLOAD_LABEL_SECTION.format(
                    id=label[0],
                    label=label[1]
                )
            )

        layout_target.write(
            DOWNLOAD_LABEL_GROUP_LIST_FOOTER
        )

    def create_layout(self):
        # Remove existing layout
        if os.path.isfile(URL_DOWNLOADER_TARGET):
            os.remove(URL_DOWNLOADER_TARGET)

        # Let's create it
        with open(URL_DOWNLOADER_TEMPLATE, "r") as layout_template, open(URL_DOWNLOADER_TARGET, "w") as layout_target:
            for line in layout_template:
                # Transfer the line
                layout_target.write(line)

                self.progress_dialog.update(
                    50,
                    "Creating download items listings.",
                    "",
                    "This can take some time, please be patient."
                )
                # Items
                if "<!-- DOWNLOAD SECTIONS -->" in line:
                    self._handle_sections(layout_target)
                    continue

                self.progress_dialog.update(
                    75,
                    "Grouping items and writing section titles.",
                    "",
                    "Almost there!."
                )

                # Labels
                if "<!-- DOWNLOAD LABEL GROUP LIST -->" in line:
                    self._handle_labels(layout_target)

        self.progress_dialog.update(
            100,
            "All done!.",
            "",
            "Sending you there..."
        )


def retrieve_from_library(dwn_type, item_id):
    """
    For usage with intents
    """

    library = json.loads(
        memory_download(LISTING_URL, timeout=10)
    )

    if dwn_type not in library:
        raise ValueError("This dwn_type wasn't found in the library", dwn_type)

    for item in library[dwn_type]["items"]:
        if not item["id"] == item_id:
            continue

        if "description" in item:
            del item["description"]
        return dwn_type, item

    raise KeyError("item_id wasn't found in the library", item_id)


def main():
    progress_dialog = xbmcgui.DialogProgress()

    progress_dialog.create("LIBRARY DOWNLOADER", "Initializing...")

    try:
        listing_manager = DownloadListingManager(
            progress_dialog
        )

        listing_manager.create_layout()
        progress_dialog.close()
        xbmc.executebuiltin("ActivateWindow(1901)")
    except Exception as e:
        print("download_loader: Failed to create listing due to: ", e)
        traceback.print_exc()
        xbmcgui.Dialog().ok(
            "LIBRARY DOWNLOADER",
            "Failed to create listing."
        )
    finally:
        xbmc.executebuiltin('Dialog.Close(1101,true)')


if __name__ == '__main__':
    print("Preparing downloads listing...")
    main()
