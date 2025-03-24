import React, {useRef, useEffect, useState} from "react";
// import {useNavigate} from "react-router-dom"
import ListFood from "./ListFood";
import '../index.css';
import '../Pages/Profile';
import './camera.css';


const WebCam = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [photo, setPhoto] = useState(null);
  const [buttonClicked, setButtonClicked] = useState(false)
  const [mlJson, setMlJson] = useState("")

  // const navigate = useNavigate()

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

  // Capture the current frame from the video stream
  const takePhoto = async () => {
    const width = videoRef.current.videoWidth;
    const height = videoRef.current.videoHeight;
    const canvas = canvasRef.current;

    setButtonClicked(true)

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
        console.log('result: ', result)
        setMlJson(result)
      } else {
        console.error('Failed to save image:', result.error);
      }
    } catch (err) {
      console.error('Error saving the image:', err);
    }
  };

  const donateItem = async () => {
    console.log("Donated!")
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
        console.log('result: ', result)
        alert("You have succesfully donated the item!")
        setButtonClicked(false)
      } else {
        console.error('Failed to save image:', result.error);
      }
    } catch (err) {
      console.error('Error saving the image:', err);
    }
  }

  return (
    // <div className="background">
    <div>
      <h1 className= "skibidi fst-italic font-weight-bold text-primary"><a href="ranks">LeaderBoard 3</a></h1>  
      <div className="top-right-button">
        <button className="btn"  onClick={() => window.location.href='profile'}><a href='profile'></a></button>
      </div>
      
      <video ref={videoRef} autoPlay width="600" height="400" children className="camera-screen" />
        <div>
        <button class="button" onClick={takePhoto}>
          <svg xmlns="http://www.w3.org/2000/svg" width="24" viewBox="0 0 24 24" height="24" fill="none" class="svg-icon"><g stroke-width="2" stroke-linecap="round" stroke="#fff" fill-rule="evenodd" clip-rule="evenodd"><path d="m4 9c0-1.10457.89543-2 2-2h2l.44721-.89443c.33879-.67757 1.03131-1.10557 1.78889-1.10557h3.5278c.7576 0 1.4501.428 1.7889 1.10557l.4472.89443h2c1.1046 0 2 .89543 2 2v8c0 1.1046-.8954 2-2 2h-12c-1.10457 0-2-.8954-2-2z"></path><path d="m15 13c0 1.6569-1.3431 3-3 3s-3-1.3431-3-3 1.3431-3 3-3 3 1.3431 3 3z"></path></g></svg>
          <span class="lable">Take a Photo</span>
        </button>
        </div>
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      {photo && (
        <div>
          <h2>Captured Photo:</h2>
          <img src={photo} alt="Captured" className="taken_picture" />
          <ListFood data={mlJson}></ListFood>
          <button className="donate-button" onClick={donateItem}>
            Donate!
          </button>
          <br></br>
        </div>
      )}
    </div>
    // </div>
  );
};

export default WebCam;
