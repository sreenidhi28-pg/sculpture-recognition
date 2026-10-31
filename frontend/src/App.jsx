
import { useState, useRef, useEffect } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [cameraOpen, setCameraOpen] = useState(false);

  const videoRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  function stopCamera() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    setCameraOpen(false);
  }

  function handleImageChange(event) {
    const file = event.target.files[0];

    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResults([]);
      setError("");
      stopCamera();
    }
  }

  async function startCamera() {
    try {
      setError("");

      const stream = await navigator.mediaDevices.getUserMedia({
        video: true
      });

      streamRef.current = stream;
      setCameraOpen(true);

      // Wait for the video element to render
      setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      }, 100);

    } catch (err) {
      setError("Unable to access camera. Please allow camera permission.");
    }
  }

  function captureImage() {
    const video = videoRef.current;

    if (!video || !video.videoWidth) {
      setError("Camera is not ready. Please try again.");
      return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0);

    canvas.toBlob(blob => {
      if (!blob) {
        setError("Unable to capture image.");
        return;
      }

      const file = new File([blob], "captured-sculpture.jpg", {
        type: "image/jpeg"
      });

      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResults([]);
      setError("");
      stopCamera();
    }, "image/jpeg");
  }

  function clearImage() {
    if (preview) {
      URL.revokeObjectURL(preview);
    }

    setImage(null);
    setPreview(null);
    setResults([]);
    setError("");

    const fileInput = document.getElementById("sculpture-upload");
    if (fileInput) fileInput.value = "";
  }

  async function searchSculptures() {
    if (!image) {
      setError("Please upload or capture a sculpture image first.");
      return;
    }

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const formData = new FormData();
      formData.append("image", image);

      const response = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        throw new Error("Unable to search sculptures. Please try again.");
      }

      const data = await response.json();
      setResults(data.results || []);

    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">

      <header className="header">
        <div className="brand">SCULPTURE<span>AI</span></div>
        <p>AI-Powered Sculpture Recognition</p>
      </header>

      <main className="container">

        <section className="hero">
          <p className="eyebrow">✦ DISCOVER ART THROUGH AI</p>
          <h1>Every sculpture has a story.</h1>
          <p className="subtitle">
            Upload an image or capture one with your camera
            to discover visually similar artworks from
            The Metropolitan Museum of Art collection.
          </p>
        </section>

        <section className="search-panel">

          <h2>Find Similar Sculptures</h2>
          <p className="section-description">
            Upload an image or use your webcam to get started.
          </p>

          <label className="upload-box">

            {preview ? (
              <img
                className="preview-image"
                src={preview}
                alt="Selected sculpture"
              />
            ) : (
              <div className="upload-placeholder">
                <div className="upload-icon">↑</div>
                <h3>Upload your sculpture image</h3>
                <p>Click here to browse your computer</p>
                <span>JPG, PNG or other supported image formats</span>
              </div>
            )}

            <input
              id="sculpture-upload"
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              hidden
            />

          </label>

          <div className="camera-controls">

            {!cameraOpen ? (
              <button className="camera-button" onClick={startCamera}>
                📷 Open Camera
              </button>
            ) : (
              <>
                <video
                  ref={videoRef}
                  autoPlay
                  playsInline
                  className="camera-preview"
                />

                <button className="camera-button" onClick={captureImage}>
                  Capture Image
                </button>

                <button className="stop-button" onClick={stopCamera}>
                  Close Camera
                </button>
              </>
            )}

          </div>

          <div className="action-buttons">

            <button
              className="search-button"
              onClick={searchSculptures}
              disabled={loading || !image}
            >
              {loading ? "Analyzing Image..." : "Find Similar Sculptures →"}
            </button>

            {preview && (
              <button className="clear-button" onClick={clearImage}>
                Clear Image
              </button>
            )}

          </div>

          {loading && (
            <div className="loading-area">
              <div className="loader"></div>
              <p>AI is analyzing your sculpture...</p>
            </div>
          )}

          {error && <p className="error-message">{error}</p>}

        </section>

        {results.length > 0 && (
          <section className="results-section">

            <div className="results-heading">
              <div>
                <p className="eyebrow">✦ YOUR DISCOVERIES</p>
                <h2>Similar Sculptures</h2>
                <p>Here are the closest visual matches from our collection.</p>
              </div>

              <span>{results.length} matches</span>
            </div>

            <div className="results-grid">

              {results.map((item, index) => {
                const score = Math.max(
                  0,
                  Math.min(100, item.similarity_score * 100)
                );

                return (
                  <article className="sculpture-card" key={item.object_id}>

                    <div className="image-wrapper">
                      <img
                        src={item.image_url}
                        alt={item.title || "Sculpture"}
                        className="sculpture-image"
                        loading="lazy"
                      />

                      <span className="match-number">
                        MATCH #{index + 1}
                      </span>
                    </div>

                    <div className="card-content">

                      <p className="object-id">
                        OBJECT #{item.object_id}
                      </p>

                      <h3>{item.title || "Untitled sculpture"}</h3>

                      <p className="artist">
                        {item.artist || "Artist unknown"}
                      </p>

                      <div className="metadata">
                        <span>Medium</span>
                        <strong>{item.medium || "Not available"}</strong>
                      </div>

                      <div className="metadata">
                        <span>Date</span>
                        <strong>{item.date || "Not available"}</strong>
                      </div>

                      <div className="similarity">
                        <div className="similarity-label">
                          <span>Visual similarity</span>
                          <strong>{score.toFixed(1)}%</strong>
                        </div>

                        <div className="progress-track">
                          <div
                            className="progress-fill"
                            style={{ width: `${score}%` }}
                          ></div>
                        </div>
                      </div>

                    </div>
                  </article>
                );
              })}

            </div>
          </section>
        )}

      </main>

      <footer className="footer">
        <p>SCULPTURE AI · Powered by OpenCLIP and Qdrant</p>
        <p>Artwork references from The Metropolitan Museum of Art</p>
      </footer>

    </div>
  );
}

export default App;

