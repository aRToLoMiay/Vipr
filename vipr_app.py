import subprocess
import sys
from console_menu import Menu

from video_compressor import VideoCompressor
from video_compressor_menu import fast_compression, economic_compression


class ViprApp(object):
    def __init__(self):
        self.vc = VideoCompressor()


    def start(self):
        self._setup()
        main_menu = self._get_menu()
        main_menu.run()


    def _get_menu(self):
        def fast_options(): print("Fast options")
        def economic_compression(): print("Economic compression")
        def convert_to_gif(): print("Conversion to gif")

        m = Menu("Choose an option:")
        m.add_action_item(
            "Fast options", 
            fast_options)
        m.add_submenu_item(
            "Fast video compression (heavy computation load)", 
            self._get_fast_compression_menu())
        m.add_action_item(
            "Economic video compression", 
            economic_compression)
        m.add_action_item(
            "Conversion to gif", 
            convert_to_gif)
        return m


    def _get_fast_compression_menu(self):
        m = Menu(f"Setup and launch video compressor:")
        m.add_action_item("Start compression", fast_compression)
        m.add_submenu_item("Size options", self._get_compressor_size_menu())
        m.add_submenu_item("Compression quality options", self._get_compressor_crf_menu())
        m.add_submenu_item("Audio bitrate options", self._get_compressor_audio_bitrate_menu())
        m.add_submenu_item("ffmpeg preset options", self._get_compressor_preset_menu())
        return m


    def _get_compressor_size_menu(self):
        def set_size(menu, size):
            self.vc.size = size
            self.vc.update_parameters()
            menu.stop()

        m = Menu("Setup result video size:")
        for label, size in VideoCompressor.get_sizes_dict().items():
            m.add_action_item(label, lambda: set_size(m, size))
        return m


    def _get_compressor_preset_menu(self):
        def set_preset(menu, preset):
            self.vc.preset = preset
            self.vc.update_parameters()
            menu.stop()

        m = Menu("Setup ffmpeg preset options:")
        for label, size in VideoCompressor.get_video_bitrate_preset_dict().items():
            m.add_action_item(label, lambda: set_preset(m, size))
        return m


    def _get_compressor_crf_menu(self):
        def set_quality(menu, vc, crf):
            vc.crf = crf
            vc.update_parameters()
            menu.stop()

        m = Menu("Setup compression quality:")
        for label, size in VideoCompressor.get_compression_quality_dict().items():
            m.add_action_item(label, lambda: set_quality(m, size))
        return m
    
    
    def _get_compressor_audio_bitrate_menu(self):
        def set_audio_bitrate(menu, vc, bitrate):
            vc.audio_bitrate_preset = bitrate
            vc.update_parameters()
            menu.stop()

        m = Menu("Setup audio bitrate:")
        for label, size in VideoCompressor.get_audio_bitrate_preset_dict().items():
            m.add_action_item(label, lambda: set_audio_bitrate(m, size))
        return m


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
