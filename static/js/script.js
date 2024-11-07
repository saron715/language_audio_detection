document.addEventListener("DOMContentLoaded", function() {
    let mediaRecorder;
    let recordedChunks = [];
    
    function startRecording() {
        // Add 'recording' class to change button color and text
        document.getElementById('record').classList.add('recording');
        document.getElementById('record').innerText = 'Recording...';
    
        // Your recording logic here
    }
    document.getElementById('record').addEventListener('click', function() {
        startRecording();
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                mediaRecorder = new MediaRecorder(stream);
                mediaRecorder.start();
    
                document.getElementById('stop').disabled = false;
                document.getElementById('record').disabled = true;
    
                mediaRecorder.addEventListener('dataavailable', function(e) {
                    recordedChunks.push(e.data);
                });
            });
    });
    
    document.getElementById('stop').addEventListener('click', function() {
        mediaRecorder.stop();
        document.getElementById('record').classList.remove('recording');
        document.getElementById('record').innerText = 'Record';
    
        document.getElementById('play').disabled = false;
        document.getElementById('submit').disabled = false;
        document.getElementById('stop').disabled = true;
        // Informative text
        
    });
    
    document.getElementById('play').addEventListener('click', function() {
        let audioBlob = new Blob(recordedChunks);
        let audioUrl = URL.createObjectURL(audioBlob);
        let audio = document.createElement('audio');
        audio.setAttribute('src', audioUrl);
        audio.setAttribute('controls', true);
    
        // Clear any existing media player in the container
        let mediaPlayerContainer = document.querySelector('.media-player-container');
        mediaPlayerContainer.innerHTML = '';
    
        // Append the newly created audio element to the container
        mediaPlayerContainer.appendChild(audio);
    });

    function updatePrediction(language, text) {
        const predictionDiv = document.getElementById('prediction');
        predictionDiv.innerHTML = ''; // Clear previous content
    
        const languageParagraph = document.createElement('p');
        languageParagraph.textContent = `Language: ${language}`;
        predictionDiv.appendChild(languageParagraph);
    
        if (text) {
            const textParagraph = document.createElement('p');
            predictionDiv.appendChild(textParagraph);
    
            let i = 0;
            let intervalId = setInterval(function() {
                if (i < text.length) {
                    textParagraph.textContent += text[i];
                    i++;
                } else {
                    clearInterval(intervalId);
                }
            }, 50);  // Adjust this value to change the speed of the text display
        }
    }
        
        
        

    // Function to handle the response from the form submission
    function handleFormResponse(data) {
        // Extract language and text from the response
        const language = data.language;
        const text = data.text;
        const melPath = data.mel_path;
        var startIndex = text.indexOf("text='") + 6;
        var endIndex =  text.lastIndexOf("'");

        // Extract the text between single quotes
        var languageText = text.substring(startIndex, endIndex);
        console.log(melPath)
        if (melPath) {
            const melSpectrogramImg = document.getElementById('mel-spectrogram');
            melSpectrogramImg.src = melPath;
        }
        
        // Update the prediction result on the HTML page
        document.getElementById('prediction').textContent = '';
        document.querySelector('.prediction-container').classList.remove('loading');
        updatePrediction(language, languageText);
        

    }
    function handleFormResponse1(data) {
        // Extract language and text from the response
        const language = data.language;
        const text = data.text;
        
        var startIndex = text.indexOf("text='") + 6;
        var endIndex =  text.lastIndexOf("'");

        // Extract the text between single quotes
        var languageText = text.substring(startIndex, endIndex);
       
        
        // Update the prediction result on the HTML page
        document.getElementById('prediction').textContent = '';
        document.querySelector('.prediction-container').classList.remove('loading');
        updatePrediction(language, languageText);
        

  

    }
    
    document.getElementById('submit').addEventListener('click', function() {
 
        let audioBlob = new Blob(recordedChunks);
        let formData = new FormData();

        formData.append('audio', audioBlob);
        document.getElementById('prediction').textContent = 'Processing...';
        document.querySelector('.prediction-container').classList.add('loading');
        fetch('/create_mel_spectrogram/', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
          .then(spectrogramUrl => {
                // Display the Mel Spectrogram
                document.getElementById('mel-spectrogram').src = spectrogramUrl;
            })
          .catch(error => console.error(error));

        fetch('/predict_response/', {
            method: 'POST',
            body: formData
        }).then(response => response.json())
          .then(data => {
                // Handle the response
                handleFormResponse1(data);
                console.log(data);
            })
          .catch(error => console.error(error));
    });

    document.getElementById('upload-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission
   // Show animation 
        let formData = new FormData(this);
        document.getElementById('prediction').textContent = 'Processing...';
        document.querySelector('.prediction-container').classList.add('loading');
        fetch('/predict_language/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response
            handleFormResponse(data);
        })
        .catch(error => console.error(error));
    });
});