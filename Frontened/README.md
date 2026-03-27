# Potato Disease Predictor - Frontend

Beautiful web interface for the Potato Disease Predictor backend API.

## 📋 Features

- 🎨 Modern, responsive UI with gradient design
- 📤 Drag-and-drop image upload
- 🖼️ Real-time image preview
- 🤖 AI-powered disease prediction
- 📊 Confidence level visualization
- ⚡ Fast prediction results
- 📱 Mobile-friendly design

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Backend API running on `http://localhost:8000`

### Option 1: Using Python Server (Recommended)

```bash
# Navigate to the Frontened folder
cd Frontened

# Run the server
python server.py
```

Then open **`http://localhost:3000`** in your browser.

### Option 2: Using VS Code Live Server Extension

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 3: Direct File Access

Simply open `index.html` directly in your browser:
```
file:///C:/Users/Bhwan/Desktop/Programming language/Deep Learning/Untitled Folder/Frontened/index.html
```

## 🔧 Configuration

To change the API URL, edit `server.py` or `index.html`:

**In `index.html` (line ~170):**
```javascript
const API_URL = 'http://localhost:8001';  // Change this URL
```

**In `server.py`:**
```python
PORT = 3000  # Change frontend port
```

## 📡 Backend Requirements

Make sure your backend API is running:

```bash
cd api
python main.py
```

Backend should be accessible at `http://localhost:8000` with these endpoints:
- `GET /ping` - Health check
- `POST /predict` - Predict disease from image

## 📸 How to Use

1. **Upload Image**: Click or drag-drop a potato leaf image
2. **Predict**: Click the "Predict" button
3. **View Results**: See the predicted disease and confidence level
4. **Clear**: Click "Clear" to reset and try another image

## 📁 Project Structure

```
Frontened/
├── index.html      # Main web interface
├── server.py       # Python HTTP server with CORS
└── README.md       # This file
```

## ⚠️ CORS Note

If you encounter CORS errors:
- Make sure backend runs with CORS enabled
- Frontend server (`server.py`) automatically adds CORS headers
- Direct file access (`file://`) may have CORS restrictions

## 🐛 Troubleshooting

### "Backend not accessible" error
- Ensure `python main.py` is running in the `api` folder
- Check that backend is on `http://localhost:8000`
- Verify no firewall is blocking the connection

### Port already in use
```powershell
# Find process using port 3000
netstat -ano | findstr :3000

# Kill the process (replace PID)
taskkill /PID <PID> /F
```

### CORS errors when accessing from direct file
- Use `python server.py` instead of opening directly
- Or use a browser extension like CORS Unblock

## 🎯 Supported Image Formats

- PNG
- JPG / JPEG
- GIF
- Up to 10MB file size

## 💡 Tips

- Use high-quality, clear images of potato leaves
- Ensure the leaf is well-lit for better predictions
- Try multiple angles for better accuracy

## 📝 API Response Format

```json
{
  "predicted_class": "Potato___healthy",
  "confidence": 95.67
}
```

## 🔗 Disease Classes

- `Potato___Early_blight`
- `Potato___Late_blight`
- `Potato___healthy`

---

**Built with ❤️ for potato farmers**
