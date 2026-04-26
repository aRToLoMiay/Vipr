import subprocess
from pathlib import Path
from typing import Optional, Tuple, Dict, Any


class VideoCompressor(object):
    class Size:
        s144p   = 0
        s240p   = 1
        s360p   = 2
        s480p   = 3
        s720p   = 4 # HD
        s1080p  = 5 # FHD
        s1440p  = 6 # 2K/QHD
        s2160p  = 7 # 4K UHD


    class BitratePreset:
        very_fast   = 0
        fast        = 1
        medium      = 2
        slow        = 3


    class AudioBitratePreset:
        very_low    = 0 # 64  - Mono lessons, podcasts, streams.
        low         = 1 # 96  - Stereo lessons, podcasts, streams.
        base        = 2 # 128 - Web and social platforms (YouTube, TikTok and other).
        medium      = 3 # 192 - Music and videogames sounds.
        high        = 4 # 256 - Music and videogames sounds.
        very_high   = 5 # 320 - Studio music.
        extra_high  = 6 # 640 - Music arhives and studio music.


    class CompressionQuality:
        extra_low   = 0 # 28 - Extra low flie size, can obtain visible video artifacts.
        low         = 1 # 25 - Low quality and file size.
        medium      = 2 # 23 - Best balance quality/file size.
        high        = 3 # 18 - High quality and file size.
    

    class CodingSpeed:
        very_slow   = 0
        slower      = 1
        slow        = 2
        medium      = 3
        fast        = 4
        faster      = 5
        very_fast   = 6
        super_fast  = 7
        ultra_fast  = 8
        

    def __init__(self):
        self.size = VideoCompressor.Size.s720p
        self.video_bitrate_preset = VideoCompressor.BitratePreset.medium
        self.audio_bitrate_preset = VideoCompressor.AudioBitratePreset.base
        self.compression_quality = VideoCompressor.CompressionQuality.medium
        self.coding_speed = VideoCompressor.CodingSpeed.fast
        self.overwrite = True

        self.max_height = self.get_height(self.size)
        self.max_width = self.get_width(self.size)
        self.video_bitrate = self.get_video_bitrate_by_preset(self.video_bitrate_preset, self.size)
        self.audio_bitrate = self.get_audio_bitrate_by_preset(self.audio_bitrate_preset)
        self.crf = self.get_crf_by_compression_quality(self.compression_quality)
        self.preset = self.get_preset_by_coding_speed(self.coding_speed)


    def update_parameters(self):
        self.max_height = self.get_height(self.size)
        self.max_width = self.get_width(self.size)
        self.video_bitrate = self.get_video_bitrate_by_preset(self.video_bitrate_preset, self.size)
        self.audio_bitrate = self.get_audio_bitrate_by_preset(self.audio_bitrate_preset)
        self.crf = self.get_crf_by_compression_quality(self.compression_quality)
        self.preset = self.get_preset_by_coding_speed(self.coding_speed)


    def get_height(self, size):
        """Return video width value for size options."""
        heights = {
            VideoCompressor.Size.s144p:     144,
            VideoCompressor.Size.s240p:     240,
            VideoCompressor.Size.s360p:     360,
            VideoCompressor.Size.s480p:     480,
            VideoCompressor.Size.s720p:     720,
            VideoCompressor.Size.s1080p:    1080,
            VideoCompressor.Size.s1440p:    1440,
            VideoCompressor.Size.s2160p:    2160,
        }
        return heights.get(size)


    def get_width(self, size):
        """Return video width value for size options. Used 9:16 screeen proportion."""
        widths = {
            VideoCompressor.Size.s144p:     256,
            VideoCompressor.Size.s240p:     426,
            VideoCompressor.Size.s360p:     640,
            VideoCompressor.Size.s480p:     854,
            VideoCompressor.Size.s720p:     1280,
            VideoCompressor.Size.s1080p:    1920,
            VideoCompressor.Size.s1440p:    2560,
            VideoCompressor.Size.s2160p:    3840,
        }
        return widths.get(size)


    def _get_preset_key(self, preset):
        preset_key = {
            VideoCompressor.BitratePreset.very_fast:    'veryfast',
            VideoCompressor.BitratePreset.fast:         'fast',
            VideoCompressor.BitratePreset.medium:       'medium',
            VideoCompressor.BitratePreset.slow:         'slow'
        }
        return preset_key[preset]


    def get_video_bitrate_by_preset(self, preset, size):
        """Return video bitrate value for bitrate preset options."""

        bitrate_map = {
            'veryfast': {
                144:    '100k',
                240:    '200k',
                360:    '350k',
                480:    '800k',
                720:    '1800k',
                1080:   '4000k',
                1440:   '7000k',
                2160:   '15000k'
            },
            'fast': {
                144:	'120k',
                240:	'250k',
                360:	'450k',
                480:	'1000k',
                720:	'2200k',
                1080:	'4500k',
                1440:	'8000k',
                2160:	'16000k'
            },
            'medium': {
                144:	'150k',
                240:	'300k',
                360:	'550k',
                480:	'1200k',
                720:	'2500k',
                1080:	'5000k',
                1440:	'9000k',
                2160:	'18000k'
            },
            'slow': {
                144:	'180k',
                240:	'350k',
                360:	'650k',
                480:	'1500k',
                720:	'3000k',
                1080:	'6000k',
                1440:	'10000k',
                2160:	'20000k'
            }
        }
        return bitrate_map[self._get_preset_key(preset)][self.get_height(size)]
    

    def get_audio_bitrate_by_preset(self, preset):
        """Return audio bitrate value for bitrate preset options."""
        bitrate = {
            VideoCompressor.AudioBitratePreset.very_low:    "64k",
            VideoCompressor.AudioBitratePreset.low:         "96k",
            VideoCompressor.AudioBitratePreset.base:        "128k",
            VideoCompressor.AudioBitratePreset.medium:      "192k",
            VideoCompressor.AudioBitratePreset.high:        "256k",
            VideoCompressor.AudioBitratePreset.very_high:   "320k",
            VideoCompressor.AudioBitratePreset.extra_high:  "640k",
        }
        return bitrate.get(preset)
    

    def get_crf_by_compression_quality(self, quality):
        """Return audio bitrate value for bitrate preset options."""
        crf = {
            VideoCompressor.CompressionQuality.extra_low:   28,
            VideoCompressor.CompressionQuality.low:         25,
            VideoCompressor.CompressionQuality.medium:      23,
            VideoCompressor.CompressionQuality.high:        18,
        }
        return crf.get(quality)


    def get_preset_by_coding_speed(self, speed):
        preset = {
            VideoCompressor.CodingSpeed.very_slow:  "veryslow",
            VideoCompressor.CodingSpeed.slower:     "slower",
            VideoCompressor.CodingSpeed.slow:       "slow",
            VideoCompressor.CodingSpeed.medium:     "medium",
            VideoCompressor.CodingSpeed.fast:       "fast",
            VideoCompressor.CodingSpeed.faster:     "faster",
            VideoCompressor.CodingSpeed.very_fast:  "varyfast",
            VideoCompressor.CodingSpeed.super_fast: "superfast",
            VideoCompressor.CodingSpeed.ultra_fast: "ultrafast"
        }
        return preset.get(speed)

    
    def get_current_options(self):
        options = {
            "video size":                   self.max_height,
            "video bitrate":                self.video_bitrate,
            "audio bitrate":                self.audio_bitrate,
            "compressing quality (crf)":    self.crf,
            "preset":                       self.preset,
        }
        return options


    def print_options(self):
        print(f"\nCompressing settings:")
        print(f"  Video size: {self.max_height}p")
        print(f"  Audio bitrate: {self.audio_bitrate}")
        print(f"  Compressing quality (CRF): {self.crf}")
        print(f"  Preset: {self.preset}")


    def compress_fast(self, input_path, output_path):
        self._compress(input_path, output_path, True)
        

    def compress_economic(self, input_path, output_path):
        self._compress(input_path, output_path, False)


    def _get_video_dimensions(self, file: str) -> Tuple[Optional[int], Optional[int]]:
        """Быстро получает размеры видео."""
        try:
            cmd = [
                'ffprobe', '-v', 'error',
                '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height',
                '-of', 'csv=p=0:s=x',
                file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
            width, height = map(int, result.stdout.strip().split('x'))
            return width, height
        except Exception as e:
            raise ValueError(f"Cannot get video size in {file} : {e}")
    
    
    def _is_compression_necessary(self, width, height):
        return height <= self.max_height and width <= self.max_width
    

    def _recalculate_size(self, width, height):
        """Рассчитывает новые размеры видео."""
        aspect_ratio = width / height
    
        if width / self.max_width > height / self.max_height:
            new_width = self.max_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = self.max_height
            new_width = int(new_height * aspect_ratio)
    
        # Even sizes for codecs.
        new_width = new_width & ~1
        new_height = new_height & ~1
    
        return max(2, new_width), max(2, new_height)


    def _print_compression_info(self, input_file, output_file):
        output_size = output_file.stat().st_size / (1024*1024)
        input_size = input_file.stat().st_size / (1024*1024)
        compression = ((input_size - output_size) / input_size * 100) if input_size > 0 else 0
                
        print(f"  Size of base file:       {input_size:.2f} MB")
        print(f"  Size of compressed file: {output_size:.2f} MB")
        print(f"  Compression:             {compression:.1f}%")


    def _duplicate_input_file(self, input_path, output_path):
        if input_path != output_path:
            import shutil
            shutil.copy2(input_path, output_path)
        return Path(output_path)


    def _compress(self, input_path, output_path, fast):
        input_file = Path(input_path)

        # Get actual video sizes.
        width, height = self._get_video_dimensions(input_path)
        if self._is_compression_necessary(width, height):
            print("Видео уже имеет требуемое разрешение или меньше")
            return
        new_width, new_height = self._recalculate_size(width, height)

        # Duplicate file.
        output_file = self._duplicate_input_file(input_path, output_path)

        # Get ffmpeg command.
        if fast:
            cmd = self._get_ffmpeg_command_fast(input_path, output_path, new_width, new_height)
        else:
            cmd = self._get_ffmpeg_command_economic(input_path, output_path, new_width, new_height)

        # Information output.
        self.print_options()
        print(f"  Original video sizes:   {width}x{height}")
        print(f"  Compressed video sizes: {new_width}x{new_height}")
        print(f"  ffmpeg command:")
        print('  '.join(cmd[:10]) + ' ... ' + ' '.join(cmd[-3:]))
        print()
    
        # Start of compressing.
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # Читаем вывод в реальном времени
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Выводим только важные строки
                if any(keyword in output.lower() for keyword in 
                        ['frame=', 'fps=', 'time=', 'bitrate=', 'speed=']):
                    print(output.strip())
        # Ждем завершения
        return_code = process.wait()
        
        # Errors check.
        if return_code != 0:
            raise Exception(f"ffmpeg finished work with error code {return_code}.")
        if not output_file.exists():
            raise FileNotFoundError(f"Ошибка: Выходной файл не создан")

        # Information output.
        print(f"\nCompression succesfuly finished!")
        self._print_compression_info(input_file, output_file)


    def _get_ffmpeg_command_fast(self, input_path, output_path, new_width, new_height):
        # Build ffmpeg command.
        cmd= [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={new_width}:{new_height}:flags=lanczos',  # lanczos для лучшего качества
            '-c:v', 'libx264',
            '-preset', self.preset,
            '-crf', str(self.crf),
            '-profile:v', 'high',
            '-level', '4.0',
            '-c:a', 'aac',
            '-b:a', self.audio_bitrate,
            '-movflags', '+faststart',  # Для веба
            '-max_muxing_queue_size', '1024',  # Для проблемных файлов
        ]
        # Добавляем дополнительные опции для качества
        if self.preset in ['slow', 'slower', 'veryslow']:
            cmd.extend(['-bf', '2'])  # B-кадры
            cmd.extend(['-refs', '4'])  # Референсные кадры
        # Опция перезаписи
        if self.overwrite:
            cmd.append('-y')
        else:
            cmd.append('-n')
        # Выходной файл
        cmd.append(output_path)

        return cmd

    
    def _get_ffmpeg_command_economic(self, input_path, output_path, new_width, new_height):
        # Build ffmpeg command.
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-vf', f'scale={new_width}:{new_height}:flags=lanczos',
            '-c:v', 'libx264',
            '-preset', self.preset,
            '-b:v', self.video_bitrate,
            '-maxrate', str(int(self.video_bitrate.replace('k', '')) * 2) + 'k',  # Ограничение пикового битрейта
            '-bufsize', str(int(self.video_bitrate.replace('k', '')) * 4) + 'k',  # Размер буфера
            '-profile:v', 'high',
            '-level', '4.0',
            '-c:a', 'aac',
            '-b:a', self.audio_bitrate,
            '-threads', '4',
            '-movflags', '+faststart',
            '-max_muxing_queue_size', '1024',
        ]
        # Опция перезаписи
        if self.overwrite:
            cmd.append('-y')
        else:
            cmd.append('-n')
        # Выходной файл
        cmd.append(output_path)
        return cmd


    def get_sizes_dict():
        sizes = {
            "144p": VideoCompressor.Size.s144p,
            "240p": VideoCompressor.Size.s240p,
            "360p": VideoCompressor.Size.s360p,
            "480p": VideoCompressor.Size.s480p,
            "720p (HD)": VideoCompressor.Size.s720p,
            "1080p (FHD)": VideoCompressor.Size.s1080p,
            "1440p (2K/QHD)": VideoCompressor.Size.s1440p,
            "2160p (4K UHD)": VideoCompressor.Size.s2160p,
        }
        return sizes


    def get_video_bitrate_preset_dict():
        preset = {
            "Very fast": VideoCompressor.BitratePreset.very_fast,
            "Fast": VideoCompressor.BitratePreset.fast,
            "Medium": VideoCompressor.BitratePreset.medium,
            "Slow": VideoCompressor.BitratePreset.slow,
        }
        return preset


    def get_audio_bitrate_preset_dict():
        preset = {
            "Very low (mono lessons, podcasts, streams)": VideoCompressor.AudioBitratePreset.very_low,
            "Low (steero lessons, podcasts, streams)": VideoCompressor.AudioBitratePreset.low,
            "Base (web and social platforms as YouTube, TikTok and other)": VideoCompressor.AudioBitratePreset.base,
            "Medium (music and videogames sounds)": VideoCompressor.AudioBitratePreset.medium,
            "High (music and videogames sounds)": VideoCompressor.AudioBitratePreset.high,
            "Very high (studio music)": VideoCompressor.AudioBitratePreset.very_high,
            "Extra high (musical arhives and studio music)": VideoCompressor.AudioBitratePreset.extra_high,
        }
        return preset


    def get_compression_quality_dict():
        quality = {
            "Extra low (extra low flie size, can obtain visible video artifacts)": VideoCompressor.CompressionQuality.extra_low,
            "Low (low quality and file size)": VideoCompressor.CompressionQuality.low,
            "Medium (best balance quality/file size)": VideoCompressor.CompressionQuality.medium, 
            "High (high quality and file size)": VideoCompressor.CompressionQuality.high,
        }
        return quality


    def get_coding_speed_dict():
        speed = {
            "Very slow": VideoCompressor.CodingSpeed.very_slow,
            "Slower": VideoCompressor.CodingSpeed.slower,
            "Slow": VideoCompressor.CodingSpeed.slow,
            "Medium": VideoCompressor.CodingSpeed.medium,
            "Fast": VideoCompressor.CodingSpeed.fast,
            "Faster": VideoCompressor.CodingSpeed.faster,
            "Very fast": VideoCompressor.CodingSpeed.very_fast,
            "Super fast": VideoCompressor.CodingSpeed.super_fast,
            "Ultra fast": VideoCompressor.CodingSpeed.ultra_fast,
        }
        return speed
