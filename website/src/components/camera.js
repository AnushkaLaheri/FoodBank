import React, { useRef, useState, useEffect } from 'react';
import ListFood from './ListFood'; // Assuming ListFood handles displaying model prediction
import '../index.css';
import '../Pages/Profile';
import './camera.css';

const WebCam = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [photo, setPhoto] = useState(null);
  const [buttonClicked, setButtonClicked] = useState(false);
  const [mlJson, setMlJson] = useState("");
  const [loading, setLoading] = useState(false); // Loading state for API calls
  const [error, setError] = useState(""); // Error state for any failures

  useEffect(() => {
    const startWebcam = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error('Error accessing webcam: ', err);
      }
    };

    startWebcam();

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const stream = videoRef.current.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, []);

  const takePhoto = async () => {
    const width = videoRef.current.videoWidth;
    const height = videoRef.current.videoHeight;
    const canvas = canvasRef.current;

    setButtonClicked(true);
    setLoading(true); // Start loading

    canvas.width = width;
    canvas.height = height;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoRef.current, 0, 0, width, height);

    const imageData = canvas.toDataURL('image/png');
    setPhoto(imageData);

    try {
      const response = await fetch('http://localhost:5001/save-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageData }),
      });

      const result = await response.json();
      if (response.ok) {
        setMlJson(result);
      } else {
        setError("Failed to process the image.");
      }
    } catch (err) {
      setError('Error saving the image');
    } finally {
      setLoading(false); // Stop loading
    }
  };

  const donateItem = async () => {
    console.log("Donated!");
    setLoading(true); // Start loading for donation

    try {
      const response = await fetch('http://localhost:5001/insert-food', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mlJson }),
      });

      const result = await response.json();
      if (response.ok) {
        alert('You have successfully donated the item!');
        setButtonClicked(false);
      } else {
        setError('Failed to donate the item.');
      }
    } catch (err) {
      setError('Error donating the item');
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div>
      <h1 className="skibidi fst-italic font-weight-bold text-primary">
        <a href="ranks">LeaderBoard 3</a>
      </h1>
      <div className="top-right-button">
        <button className="btn" onClick={() => window.location.href = 'profile'}>
          <a href="profile"></a>
        </button>
      </div>

      <video ref={videoRef} autoPlay width="600" height="400" className="camera-screen" />
      <div>
        <button className="button" onClick={takePhoto} disabled={loading}>
          {loading ? 'Capturing...' : 'Take a Photo'}
        </button>
      </div>

      <canvas ref={canvasRef} style={{ display: 'none' }} />
      {photo && (
        <div>
          <h2>Captured Photo:</h2>
          <img src={photo} alt="Captured" className="taken_picture" />
          <ListFood data={mlJson} />
          <button className="donate-button" onClick={donateItem} disabled={loading}>
            {loading ? 'Processing Donation...' : 'Donate!'}
          </button>
        </div>
      )}
      {error && <p className="error-message">{error}</p>} {/* Display error messages */}
    </div>
  );
};

export default WebCam;
