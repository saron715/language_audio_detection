let recorder;

function recordAudio() {
  navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
      recorder = new Recorder(stream);
      recorder.record();
      console.log('Recording started'); // Log for verification
    })
    .catch(error => {
      console.error('Error accessing microphone:', error);
    });
}

function stopRecording() {
  recorder.stop();
  recorder.ondataavailable = (blob) => {
    // Send recorded audio to the Django view using AJAX or Fetch API
    sendAudioToServer(blob);
  };
  console.log('Recording stopped'); // Log for verification
}

function sendAudioToServer(blob) {
  const formData = new FormData();
  formData.append('audio_data', blob);

  // Assuming you're dynamically fetching the URL from a separate Django view
  fetch('/get-predict-language-url/', {
    method: 'POST',
    body: formData,
  })
    .then(response => {
      if (response.ok) {
        return response.json(); // Parse the JSON response containing the prediction URL
      } else {
        console.error('Error fetching prediction URL:', response.statusText);
        return Promise.reject(new Error('Failed to fetch prediction URL')); // Handle the error
      }
    })
    .then(data => {
      const predictLanguageUrl = data.url; // Extract the URL from the response data
      // Send the audio data to the predict language view using the fetched URL
      fetch(predictLanguageUrl, {
        method: 'POST',
        body: formData,
      })
        .then(response => {
          if (response.ok) {
            return response.json(); // Parse the JSON response from the prediction view
          } else {
            console.error('Error sending audio to prediction view:', response.statusText);
            return Promise.reject(new Error('Failed to send audio')); // Handle the error
          }
        })
        .then(data => {
          // Handle successful prediction response (display results, etc.)
          console.log('Prediction:', data.predicted_language);
          // Update UI elements with the predicted language, transcribed text (if available), etc.
        })
        .catch(error => {
          console.error('Error processing audio:', error);
          // Handle errors gracefully (display error messages, etc.)
        });
    })
    .catch(error => {
      console.error('Error fetching or sending audio:', error);
      // Handle errors gracefully (display error messages, etc.)
    });
}

document.getElementById('record-btn').addEventListener('click', recordAudio);
document.getElementById('stop-btn').addEventListener('click', stopRecording);
