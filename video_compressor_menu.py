import os
import path_processor as ppr
from video_compressor import VideoCompressor


def compress_videos(vc, fast):
    work_dir = ppr.get_app_path()
    result_dir = ppr.get_result_paths()
    file_types = ('.mp4', '.webm', '.avi', '.mov')

    files = ppr.collect_file_paths(work_dir, file_types)
    if len(files) == 0:
        print('Файлы для сжатия не обнаружены. Поместите exe-файл в директорию с файлами для сжатия.')
        return

    # vc = VideoCompressor()
    for file in files:
        print(f'Начинаем обработку видео {file}')
        try:
            result_file = ppr.transfer_file_path(file, result_dir)
            if fast:
                vc.compress_fast(file, result_file)
            else:
                vc.compress_economic(file, result_file)
        except Exception as e:
            print(f"При сжатии видео {file} произошла ошибка: {e}")
            return

        print(f"Видео успешно сжато и сохранено как: {result_file}")


def fast_compression(vc):
    compress_videos(vc, True)


def economic_compression(vc):
    compress_videos(vc, False)
