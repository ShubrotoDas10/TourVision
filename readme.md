# 🎬 TourVision - AI-Powered Property Tour Video Generator

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-AI-orange?style=for-the-badge)
![Veo](https://img.shields.io/badge/Veo-3.1-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**TourVision** automatically transforms static property images into professional video tours using Google's Gemini AI for image classification and Veo 3.1 for cinematic video generation. No manual editing required - just provide images and get a polished property tour video!

## ✨ Features

🤖 **AI-Powered Classification** - Automatically categorizes images by room type using Gemini Vision

🎥 **Cinematic Video Generation** - Creates smooth transitions with Veo 3.1

🔄 **Smart Scene Selection** - Intelligently picks the best image pairs for transitions

⚡ **Automated Stitching** - Combines all clips with crossfades and professional effects

📊 **Token Tracking** - Logs all API usage and costs in CSV format

🎯 **Dynamic Pacing** - Automatically adjusts clip duration to hit target length

🎨 **Professional Effects** - Fade-in, fade-out, and crossfade transitions

## 🚀 How It Works

```
Images → AI Classification → Video Generation → Automated Stitching → Final Tour
```

1. **Image Analysis** - Gemini 2.0 Flash identifies room types (bedroom, kitchen, living_room, etc.)
2. **Grouping** - Images are automatically grouped by detected labels
3. **Smart Selection** - For multi-image rooms, AI selects the best pair for transitions
4. **Video Generation** - Veo 3.1 creates smooth cinematic clips with panoramas or frame bridging
5. **Final Assembly** - MoviePy stitches everything with crossfade transitions

## 📁 Project Structure

```
TourVision/
├── pipeline_new.py           # Main pipeline script
├── .env                      # API keys (not committed)
├── token_counter.csv         # API usage tracking
├── images/
│   └── {PROPERTY_CODE}/      # Input images folder
│       ├── image1.webp
│       ├── image2.jpg
│       └── ...
└── output/
    └── {PROPERTY_CODE}/      # Generated videos
        ├── 005_bedroom.mp4
        ├── 005_kitchen.mp4
        └── final_property_tour_005.mp4
```

## 🎯 Quick Start

### Prerequisites

- Python 3.8+
- Google Gemini API Key ([Get one here](https://ai.google.dev/))
- Veo API Access (requires Google Cloud account)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YourUsername/TourVision.git
cd TourVision
```

2. **Install dependencies**
```bash
pip install google-genai moviepy python-dotenv
```

3. **Set up environment variables**
```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

4. **Prepare your images**
```bash
# Create folder structure
mkdir -p images/005
# Add your property images to images/005/
```

5. **Run the pipeline**
```bash
python pipeline_new.py
```

## ⚙️ Configuration

Edit these settings in `pipeline_new.py`:

```python
# Property Settings
PROPERTY_CODE = "005"  # Change for each property

# Paths
IMAGE_FOLDER = f"D:\\rentremote\\images\\{PROPERTY_CODE}"
OUTPUT_FOLDER = f"output/{PROPERTY_CODE}"

# AI Models
MODEL_VISION = "gemini-2.0-flash"        # Image classification
MODEL_VIDEO = "veo-3.1-fast-generate-preview"  # Video generation

# Video Settings
TRANSITION_DUR = 1.2          # Crossfade duration in seconds
TOTAL_TARGET_DURATION = 45.0  # Final video target length
```

## 📊 Output

### Generated Files

1. **Individual Scene Clips**
   - `005_bedroom.mp4`
   - `005_kitchen.mp4`
   - `005_living_room.mp4`
   - etc.

2. **Final Tour Video**
   - `final_property_tour_005.mp4` (45 seconds, 16:9, 24fps)

3. **Usage Report**
   - `token_counter.csv` - Detailed API usage tracking

### CSV Tracking Format

| Timestamp | Property ID | Process Name | Model | Execution Time | Prompt Tokens | Candidate Tokens | Total Tokens |
|-----------|-------------|--------------|-------|----------------|---------------|------------------|--------------|
| 2024-01-28 10:30:45 | 005 | Image Classification | gemini-2.0-flash | 1.234 | 256 | 12 | 268 |
| 2024-01-28 10:31:02 | 005 | Video Generation | veo-3.1 | 45.678 | 128 | 0 | 128 |

## 🎨 Scene Types Detected

The AI automatically identifies and groups:
- 🛏️ Bedroom
- 🍳 Kitchen
- 🛋️ Living Room
- 🚿 Bathroom
- 🏢 Lobby / Entrance
- 🏗️ Exterior
- 🅿️ Parking
- 🏊 Pool / Amenities
- And more...

## 💡 How Video Generation Works

### Single Image Rooms
```python
# Creates smooth panorama pan
"A smooth horizontal panorama pan of this {room_type}."
```

### Multiple Image Rooms
```python
# AI selects best 2 images, creates transition
"Accurate bridge between frames for {room_type}."
```

## 🔧 Advanced Usage

### Process Multiple Properties

```python
properties = ["001", "002", "003"]
for code in properties:
    PROPERTY_CODE = code
    run_full_pipeline()
```

### Custom Video Duration

```python
TOTAL_TARGET_DURATION = 60.0  # 1-minute tour
```

### Adjust Transition Speed

```python
TRANSITION_DUR = 2.0  # Slower, smoother transitions
```

## 📈 Performance

- **Image Classification:** ~1-2 seconds per image
- **Video Generation:** ~30-60 seconds per clip
- **Stitching:** ~5-10 seconds
- **Total Time:** ~5-10 minutes for 10-image property

## 🐛 Troubleshooting

### "No scenes found"
- Ensure images are in correct folder: `images/{PROPERTY_CODE}/`
- Check image formats (supports .webp, .jpg, .jpeg)

### API Key Errors
```bash
# Verify .env file exists and contains:
GEMINI_API_KEY=your_actual_key
```

### Video Generation Timeout
```python
# Increase wait time in the code
while not operation.done:
    time.sleep(30)  # Increase from 15 to 30 seconds
```

### MoviePy Errors
```bash
# Reinstall with specific version
pip uninstall moviepy
pip install moviepy==2.0.0
```

## 📊 Cost Estimation

Based on Google AI pricing (approximate):

- **Gemini 2.0 Flash:** ~$0.01 per 1000 images
- **Veo 3.1 Fast:** ~$0.05 per generated video clip
- **Example:** 10-image property ≈ $0.50 - $1.00

## 🎯 Use Cases

- 🏠 **Real Estate** - Automated property listings
- 🏨 **Hotels** - Virtual room tours
- 🏢 **Commercial** - Office space showcases
- 🏘️ **Rentals** - Apartment walk-throughs
- 🏗️ **Construction** - Progress documentation

## 🔐 Security Best Practices

- Never commit `.env` files to Git
- Add `.env` to `.gitignore`
- Use environment variables for API keys
- Rotate API keys periodically

## 📝 Sample .gitignore

```gitignore
# Environment
.env
*.env

# Output
output/
*.mp4

# API Tracking
token_counter.csv

# Python
__pycache__/
*.pyc
.venv/
venv/

# OS
.DS_Store
Thumbs.db
```

## 🚀 Future Enhancements

- [ ] Audio narration using text-to-speech
- [ ] Custom branding/watermarks
- [ ] Batch processing UI
- [ ] Cloud deployment (AWS/GCP)
- [ ] Real-time progress dashboard
- [ ] Custom music integration
- [ ] Multi-language support
- [ ] 360° virtual tour support

## 📖 API Documentation

### Main Function

```python
run_full_pipeline()
```
Executes the complete pipeline:
1. Classify images
2. Group by room type
3. Generate video clips
4. Stitch final tour
5. Log API usage

### Helper Functions

```python
log_api_hit(process_name, model_name, start_time, usage_metadata)
# Tracks API usage to CSV

load_image_for_veo(path)
# Prepares image for Veo model

get_image_part(path)
# Prepares image for Gemini Vision

clean_json_response(text)
# Parses JSON from AI response
```

## 🤝 Contributing

Contributions welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) - Image classification
- [Google Veo](https://deepmind.google/technologies/veo/) - Video generation
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing
- Real estate photography community

## 👨‍💻 Author

**Shubroto Das**
- GitHub: [@ShubrotoDas10](https://github.com/ShubrotoDas10)

## 📞 Support

Issues or questions?
- Open an [Issue](https://github.com/YourUsername/TourVision/issues)
- Check [Documentation](#)
- Review [Examples](#)

## 🌟 Star History

If this project helped you, please consider giving it a ⭐!

---

<div align="center">

**Transform Property Images into Professional Tours with AI** ✨

[Report Bug](https://github.com/YourUsername/TourVision/issues) · [Request Feature](https://github.com/YourUsername/TourVision/issues)

</div>
