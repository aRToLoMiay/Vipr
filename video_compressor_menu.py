import msvcrt
import os
import path_processor as ppr
from video_compressor import VideoCompressor

from console_menu import Menu


class ViprVideoCompressor(object):
    _COMRESSOR_MENU_SPEC = {
        "size": (
            "Setup result video size:",
            VideoCompressor.get_sizes_dict
            ),
        "crf": (
            "Setup compression quality:",
            VideoCompressor.get_compression_quality_dict
            ),
        "audio_bitrate_preset": (
            "Setup audio bitrate:",
            VideoCompressor.get_audio_bitrate_preset_dict
            ),
        "preset": (
            "Setup ffmpeg preset options:",
            VideoCompressor.get_video_bitrate_preset_dict
            ),
        }

    def __init__(self):
        self.vc = VideoCompressor()


# --- Compressor methods ---
    def compress_videos(self, soft_compression=True):
        work_dir = ppr.get_app_path()
        result_dir = ppr.get_result_paths()
        file_types = (".mp4", ".webm", ".avi", ".mov")

        files = ppr.collect_file_paths(work_dir, file_types)
        if len(files) == 0:
            print("No files to compress found. Place the exe file in the directory with the files to compress.")
            return
        
        if soft_compression:
            print("Start soft compression (low process priority)")
        else:
            print("Start fast compression (high CPU load)")
        for file in files:
            print(f"Starting video processing {file}")
            try:
                result_file = ppr.transfer_file_path(file, result_dir)
                self.vc.compress(file, result_file, soft_compression)
            except Exception as e:
                print(f"An error occurred while compressing video {file}: {e}")
                return

            print(f"Video successfully compressed and saved as: {result_file}")


    def compress_to_720p(self, soft_compression=True):
        self.vc.set_size(VideoCompressor.Size.s720p)
        self.vc.set_audio_bitrate(VideoCompressor.AudioBitratePreset.base)
        self.vc.set_compression_quality(VideoCompressor.CompressionQuality.medium)
        self.vc.set_coding_speed(VideoCompressor.CodingSpeed.medium)
        self.compress_videos(soft_compression)
        msvcrt.getch()


    def _compress(self):
        self.compress_videos(soft_compression=False)


    def _compress_soft(self):
        self.compress_videos(soft_compression=True)


# --- Menu methods ---
    def generate_menu(self, parent, soft_compression=True):
        m = Menu(f"IN PROGRESS : Setup and launch video compressor:", parent_menu=parent)
        m.add_action_item(
            "Start compression", 
            self._compress_soft if soft_compression else self._compress)
        m.add_submenu_item(
            "Size options",
            self._get_setter_menu(m, "size"))
        m.add_submenu_item(
            "Compression quality options",
            self._get_setter_menu(m, "crf"))
        m.add_submenu_item(
            "Audio bitrate options", 
            self._get_setter_menu(m, "audio_bitrate_preset"))
        m.add_submenu_item(
            "ffmpeg preset options", 
            self._get_setter_menu(m, "preset"))
        return m
    

    def _get_setter_menu(self, parent, attr_name):
        title, options_getter = self._COMRESSOR_MENU_SPEC[attr_name]

        def set_value(value):
            setattr(self.vc, attr_name, value)
            self.vc.update_parameters()

        m = Menu(title=title, parent_menu=parent, close_mode=True)
        for label, value in options_getter().items():
            m.add_action_item(label, lambda v=value: set_value(v))
        return m
