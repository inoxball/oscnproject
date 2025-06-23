import os
import subprocess


def encode_video(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    FFMPEG_PATH = "C:/ffmpeg/bin/ffmpeg.exe"

    resolutions = [
        {"name": "360p", "width": 640, "height": 360, "bitrate": "800k"},
        {"name": "720p", "width": 1280, "height": 720, "bitrate": "2500k"},
        {"name": "1080p", "width": 1920, "height": 1080, "bitrate": "5000k"}
    ]

    for res in resolutions:
        print(f"Encoding {res['name']} version...")
        output_file = os.path.join(output_dir, f"output_{res['name']}.mp4")

        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-c:v", "libx264",
            "-crf", "23",
            "-preset", "fast",
            "-vf", f"scale={res['width']}:{res['height']}",
            "-b:v", res["bitrate"],
            "-maxrate", res["bitrate"],
            "-bufsize", "1000k",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            output_file
        ]

        subprocess.run([FFMPEG_PATH] + cmd[1:], check=True)


def package_hls(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    FFMPEG_PATH = "C:/ffmpeg/bin/ffmpeg.exe"
    variants = ["output_360p.mp4", "output_720p.mp4", "output_1080p.mp4"]

    for variant in variants:
        input_path = os.path.join(input_dir, variant)
        variant_name = os.path.splitext(variant)[0]

        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "copy",
            "-c:a", "copy",
            "-f", "hls",
            "-hls_time", "2",
            "-hls_playlist_type", "vod",
            "-hls_segment_filename", os.path.join(output_dir, f"{variant_name}_%03d.ts"),
            os.path.join(output_dir, f"{variant_name}.m3u8")
        ]

        subprocess.run([FFMPEG_PATH] + cmd[1:], check=True)


if __name__ == "__main__":
    encode_video("input.mp4", "encoded_videos")
    package_hls("encoded_videos", "hls_videos")