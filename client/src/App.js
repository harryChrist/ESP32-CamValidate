import React, { useState } from "react";
import axios from "axios";

function App() {
  const [imageSrc, setImageSrc] = useState(null);
  const [username, setUsername] = useState('Harry')

  const handleCaptureClick = async () => {
    try {
      const response = await axios.get("http://192.168.15.134/capture?_cb=", {
        responseType: "blob",  // Alterando o responseType para "blob"
      });
      const imageUrl = URL.createObjectURL(response.data);  // Convertendo blob para URL de objeto
      setImageSrc(imageUrl);
      console.log(imageUrl)
    } catch (error) {
      console.error("Error fetching image: ", error);
    }
  };

  const handleConfirmClick = async () => {
    if (!imageSrc) {
      console.error("No image to send");
      return;
    }
  
    try {
      const response = await fetch(imageSrc);
      const blob = await response.blob();
      const formData = new FormData();
      formData.append("image", blob);
      formData.append("name", username);
      await axios.post("http://127.0.0.1:5000/register", formData, {  // Alterado {formData} para formData
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      alert("Image sent successfully");
    } catch (error) {
      console.error("Error sending image: ", error);
    }
  };

  const handleVerifyClick = async () => {
    if (!imageSrc) {
      console.error("No image to verify");
      return;
    }

    try {
      const response = await fetch(imageSrc);
      const blob = await response.blob();
      const formData = new FormData();
      formData.append("image", blob);

      const result = await axios.post("http://127.0.0.1:5000/verify", formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (result.data.message === "MATCH!") {
        alert("Match found!");
      } else {
        alert("No match found");
      }

    } catch (error) {
      console.error("Error verifying image: ", error);
    }
  };

  

  return (
    <div>
      <button onClick={handleCaptureClick}>Capture</button>
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      {imageSrc && (
        <div>
          <img src={imageSrc} alt="Captured" />
          <button onClick={handleConfirmClick}>Confirmar</button>
          <button onClick={handleVerifyClick}>Verificar</button>
        </div>
      )}
    </div>
  );
}

export default App;
