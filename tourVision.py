import os
import time
import json
import re
import csv
from google import genai
from google.genai import types
from dotenv import load_dotenv
from moviepy import VideoFileClip, concatenate_videoclips, vfx

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Configuration
PROPERTY_CODE = "005"  # This will be logged in the CSV
IMAGE_FOLDER = f"D:\\rentremote\\images\\{PROPERTY_CODE}"
OUTPUT_FOLDER = f"output/{PROPERTY_CODE}"
FINAL_OUTPUT = f"output/{PROPERTY_CODE}/final_property_tour_{PROPERTY_CODE}.mp4"
MODEL_VISION = "gemini-2.0-flash" 
MODEL_VIDEO = "veo-3.1-fast-generate-preview" 
TRANSITION_DUR = 1.2 
TOTAL_TARGET_DURATION = 45.0
CSV_FILE = "token_counter.csv"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- CONTINUOUS TRACKER (APPEND MODE) ---
def log_api_hit(process_name, model_name, start_time, usage_metadata):
    """Appends API hit details to CSV. Does not overwrite."""
    end_time = time.time()
    execution_time = round(end_time - start_time, 3)
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.isfile(CSV_FILE)
    
    try:
        # Extract token data
        p_tokens = getattr(usage_metadata, 'prompt_token_count', 0) or 0
        c_tokens = getattr(usage_metadata, 'candidates_token_count', 0) or 0
        t_tokens = getattr(usage_metadata, 'total_token_count', 0) or 0
        
        # 'a' mode ensures continuous addition (Append)
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            
            # Add headers ONLY if the file is being created for the first time
            if not file_exists:
                writer.writerow([
                    "Timestamp", "Property ID", "Process Name", "Model", 
                    "Execution Time (s)", "Prompt Tokens", "Candidate Tokens", "Total Tokens"
                ])
            
            writer.writerow([
                time.strftime("%Y-%m-%d %H:%M:%S"), 
                PROPERTY_CODE, 
                process_name, 
                model_name, 
                execution_time, 
                p_tokens, 
                c_tokens, 
                t_tokens
            ])
    except Exception as e:
        print(f"Logging Error: {e}")

def load_image_for_veo(path):
    with open(path, "rb") as f:
        data = f.read()
    mime = "image/png" if data.startswith(b'\x89PNG') else "image/jpeg"
    return types.Image(image_bytes=data, mime_type=mime)

def get_image_part(path):
    with open(path, "rb") as f:
        return types.Part.from_bytes(data=f.read(), mime_type="image/webp")

def clean_json_response(text):
    text = re.sub(r'```json\s*|\s*```', '', text).strip()
    return json.loads(text)

def run_full_pipeline():
    # --- STEP 1: Open-World Identification ---
    dynamic_groups = {}
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.webp', '.jpg', '.jpeg'))]
    
    print(f"🔍 Analyzing {len(image_files)} images for Property {PROPERTY_CODE}...")
    
    for filename in image_files:
        try:
            path = os.path.join(IMAGE_FOLDER, filename)
            prompt_classify = (
                "Identify the primary subject or location. Task: Provide a single-word label "
                "(use underscores for multiple words). No adjectives. Return ONLY the word."
            )
            
            start_api = time.time()
            resp = client.models.generate_content(
                model=MODEL_VISION,
                contents=[get_image_part(path), prompt_classify]
            )
            # Log classification hit
            log_api_hit(f"Image Classification ({filename})", MODEL_VISION, start_api, resp.usage_metadata)
            
            label = resp.text.strip().lower().replace('"', '').replace("'", "").replace(".", "")
            if label not in dynamic_groups:
                dynamic_groups[label] = []
            dynamic_groups[label].append(filename)
        except Exception as e:
            print(f"Error classifying {filename}: {e}")
        time.sleep(1)

    # --- TIME CALCULATION ---
    num_scenes = len(dynamic_groups)
    if num_scenes == 0: 
        print("No scenes found.")
        return
        
    target_clip_duration = (TOTAL_TARGET_DURATION + (num_scenes - 1) * TRANSITION_DUR) / num_scenes

    # --- STEP 2 & 3: Selection & Generation ---
    generated_files = []
    for label, files in dynamic_groups.items():
        output_path = os.path.join(OUTPUT_FOLDER, f"{PROPERTY_CODE}_{label}.mp4")
        try:
            print(f"🎬 Processing: {label}")
            if len(files) == 1:
                img_path = os.path.join(IMAGE_FOLDER, files[0])
                first_frame = load_image_for_veo(img_path)
                
                start_api = time.time()
                operation = client.models.generate_videos(
                    model=MODEL_VIDEO,
                    prompt=f"A smooth horizontal panorama pan of this {label}.",
                    image=first_frame,
                    config=types.GenerateVideosConfig(aspect_ratio="16:9")
                )
            else:
                room_parts = [get_image_part(os.path.join(IMAGE_FOLDER, f)) for f in files]
                prompt_select = f"From {files}, select two images for '{label}'. Return ONLY JSON list."
                
                start_api_sel = time.time()
                sel_resp = client.models.generate_content(
                    model=MODEL_VISION, 
                    contents=room_parts + [prompt_select],
                    config=types.GenerateContentConfig(response_mime_type="application/json")
                )
                log_api_hit(f"Image Selection ({label})", MODEL_VISION, start_api_sel, sel_resp.usage_metadata)
                
                pair = clean_json_response(sel_resp.text)
                if not all(p in files for p in pair): pair = [files[0], files[1]]
                
                start_api = time.time()
                operation = client.models.generate_videos(
                    model=MODEL_VIDEO,
                    prompt=f"Accurate bridge between frames for {label}.",
                    image=load_image_for_veo(os.path.join(IMAGE_FOLDER, pair[0])),
                    config=types.GenerateVideosConfig(last_frame=load_image_for_veo(os.path.join(IMAGE_FOLDER, pair[1])), aspect_ratio="16:9")
                )

            # Wait for Generation
            while not operation.done:
                time.sleep(15)
                operation = client.operations.get(operation)

            if operation.response:
                usage = getattr(operation.response, 'usage_metadata', None)
                log_api_hit(f"Video Generation ({label})", MODEL_VIDEO, start_api, usage)
                
                video_clip_data = (getattr(operation.response, 'generated_videos', None) or 
                                  getattr(operation.response, 'generated_clips', None))[0]
                resource = getattr(video_clip_data, 'video_resource', None) or getattr(video_clip_data, 'video', None)
                video_bytes = client.files.download(file=resource)
                with open(output_path, "wb") as f:
                    f.write(video_bytes)
                generated_files.append(output_path)

        except Exception as e:
            print(f"❌ Error in {label}: {e}")

    # --- STEP 4: Automated Stitching ---
    if len(generated_files) > 0:
        print(f"📽️ Stitching {len(generated_files)} clips...")
        generated_files.sort(key=lambda x: (0 if "exterior" in x or "lobby" in x else 1))
        clips = []
        try:
            for i, file_path in enumerate(generated_files):
                clip = VideoFileClip(file_path).without_audio().with_duration(target_clip_duration)
                effects = []
                if i > 0: effects.append(vfx.CrossFadeIn(TRANSITION_DUR))
                if i == 0: effects.append(vfx.FadeIn(TRANSITION_DUR))
                if i == len(generated_files) - 1: effects.append(vfx.FadeOut(TRANSITION_DUR))
                clips.append(clip.with_effects(effects))

            final_video = concatenate_videoclips(clips, method="compose", padding=-TRANSITION_DUR)
            final_video.write_videofile(FINAL_OUTPUT, codec="libx264", audio=False, fps=24, threads=8)
            print(f"✨ DONE: {FINAL_OUTPUT}")
        except Exception as e:
            print(f"❌ Stitching Error: {e}")
        finally:
            for clip in clips: clip.close()

if __name__ == "__main__":
    run_full_pipeline()