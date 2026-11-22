import msvcrt
import subprocess
import sys
from console_menu import Menu

from video_compressor_menu import ViprVideoCompressor


class ViprApp(object):
    def __init__(self):
        self.vc = ViprVideoCompressor()


    def _setup(self):
        if not self._check_ffmpeg_installed():
            print("FFmpeg is not installed in system!")
            sys.exit(1)


    def _check_ffmpeg_installed(self) -> bool:
        """Check ffmpeg installation in system."""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                          capture_output=True, 
                          check=True,
                          timeout=5)
            subprocess.run(['ffprobe', '-version'], 
                          capture_output=True, 
                          check=True,
                          timeout=5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError, TimeoutError):
            return False


    def start(self):
        self._setup()
        main_menu = self._get_menu()
        main_menu.run()


# --- Menu functions ---
    def _get_menu(self):
        m = Menu("Choose an option:", close_mode=False)
        m.add_submenu_item(
            "Fast options", 
            self._get_fast_options_menu(m))
        m.add_submenu_item(
            "Fast video compression (heavy computation load)", 
            self.vc.generate_menu(m, soft_compression=False))
        m.add_submenu_item(
            "Soft video compression (low process priority)",
            self.vc.generate_menu(m, soft_compression=True))
        m.add_action_item(
            "Conversion to gif", 
            self.convert_to_gif)
        return m


    def _get_fast_options_menu(self, parent):
        m = Menu(f"Choose fast option:", parent_menu=parent)
        m.add_action_item("Fast compression to 720p", self._fo_compress_to_720)
        m.add_action_item("Soft compression to 720p", self._fo_soft_compress_to_720)
        m.add_action_item("Cut video in 1h sections", self._fo_cut_to_1h_sections)
        return m


# --- Fast options ---
    def _fo_compress_to_720(self):
        self.vc.compress_to_720p(soft_compression=False)


    def _fo_soft_compress_to_720(self):
        self.vc.compress_to_720p(soft_compression=True)


    def _fo_cut_to_1h_sections(self):
        print("IN PROGRESS : _fo_to_1h_sections")
        msvcrt.getch()


# --- Gif convertation ---
    def convert_to_gif(self):
        print("Conversion to gif")
        msvcrt.getch()
