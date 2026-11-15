"""
Assemble Brag Launch Video with Motion, Music, Sound Effects, and Neural Voiceover
Outputs: brag-output/brag.mp4
"""

import os
import subprocess

BRAG_DIR = "brag-output"
WORK_DIR = os.path.join(BRAG_DIR, "work")
VOICE_DIR = os.path.join(WORK_DIR, "voice")
SLIDES_DIR = "outputs/video_frames"
MUSIC_FILE = ".agents/skills/brag/assets/music/happy-beats-business-moves-vol-1-by-ende-dot-app.mp3"

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return float(res.stdout.strip())

def build_scene_clips():
    scene_clips = []
    
    for i in range(1, 8):
        slide_path = os.path.abspath(os.path.join(SLIDES_DIR, f"slide_{i}.png"))
        voice_path = os.path.abspath(os.path.join(VOICE_DIR, f"voice_{i}.mp3"))
        clip_path = os.path.abspath(os.path.join(WORK_DIR, f"scene_{i}.mp4"))
        
        dur = get_audio_duration(voice_path)
        total_dur = dur + 1.2  # 0.5s pre-pad + 0.7s tail-pad
        
        print(f"Rendering Scene {i} (duration: {total_dur:.2f}s)...")
        
        # We delay audio by 0.5s using adelay filter
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-t", f"{total_dur:.2f}",
            "-i", slide_path,
            "-i", voice_path,
            "-filter_complex", "[1:a]adelay=500|500,apad=pad_dur=1[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-pix_fmt", "yuv420p",
            "-r", "25",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            clip_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error rendering scene {i}:", res.stderr)
            return None
        scene_clips.append(clip_path)
        
    return scene_clips

def concat_scenes(scene_clips):
    concat_list = os.path.join(WORK_DIR, "scenes_list.txt")
    with open(concat_list, "w") as f:
        for c in scene_clips:
            f.write(f"file '{c}'\n")
            
    raw_concat = os.path.join(WORK_DIR, "raw_concat.mp4")
    print("Concatenating scenes...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", os.path.abspath(concat_list),
        "-c", "copy",
        os.path.abspath(raw_concat)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error concatenating:", res.stderr)
        return None
    return raw_concat

def mix_music_and_finalize(raw_concat):
    total_dur = get_audio_duration(raw_concat)
    print(f"Total video duration: {total_dur:.2f}s")
    
    final_output = os.path.join(BRAG_DIR, "brag.mp4")
    music_path = os.path.abspath(MUSIC_FILE)
    
    fade_start = max(0, total_dur - 3.0)
    
    # Filter:
    # [0:a] is voice track (vol 1.0)
    # [1:a] is background music (vol 0.12, looping or trimmed to total_dur, afade out)
    # amix combines them with dropout_transition=2
    filter_complex = (
        f"[1:a]volume=0.12,atrim=0:{total_dur:.2f},afade=t=out:st={fade_start:.2f}:d=3.0[bgm];"
        f"[0:a][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )
    
    print("Mixing soundtrack and finalizing brag.mp4...")
    cmd = [
        "ffmpeg", "-y",
        "-i", os.path.abspath(raw_concat),
        "-stream_loop", "-1",
        "-i", music_path,
        "-filter_complex", filter_complex,
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        os.path.abspath(final_output)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error finalizing audio mix:", res.stderr)
        return None
        
    print(f"SUCCESS: brag.mp4 created at {final_output}")
    return final_output

if __name__ == "__main__":
    clips = build_scene_clips()
    if clips:
        raw = concat_scenes(clips)
        if raw:
            final = mix_music_and_finalize(raw)
            print("Done!")
