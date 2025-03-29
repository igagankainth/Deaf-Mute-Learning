// Toggle Dark Mode
const toggle = document.getElementById('toggle-mode');
toggle.addEventListener('click', () => {
    document.body.classList.toggle('dark');
    toggle.innerText = document.body.classList.contains('dark') ? 'Light Mode' : 'Dark Mode';
});

// ---- Voice to Text + Translate ----
const voiceBtn = document.querySelector("#voice .btn");
voiceBtn.addEventListener('click', () => {
    const targetLang = document.getElementById("language-select").value;

    if (!targetLang) {
        alert("Please select a target language.");
        return;
    }

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            const mediaRecorder = new MediaRecorder(stream);
            let audioChunks = [];

            // Disable button during recording
            voiceBtn.disabled = true;
            voiceBtn.innerText = "Recording... Click to Stop";

            mediaRecorder.start();

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            // Allow user to click again to stop manually
            voiceBtn.onclick = () => {
                if (mediaRecorder.state !== "inactive") {
                    mediaRecorder.stop();
                }
            };

            mediaRecorder.onstop = () => {
                // Re-enable button
                voiceBtn.disabled = false;
                voiceBtn.innerText = "Start Listening";

                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                const formData = new FormData();
                formData.append('audio', audioBlob, "audio.webm");
                formData.append('target_lang', targetLang);

                const outputDiv = document.getElementById("voice-output");
                outputDiv.innerText = "Processing audio... Please wait.";

                fetch("http://127.0.0.1:8000/api/voice_to_text/", {
                    method: "POST",
                    mode: "cors",
                    body: formData
                })
                .then(response => {
                    if (!response.ok) throw new Error("Network response was not ok");
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        outputDiv.innerText = data.error;
                    } else {
                        outputDiv.innerHTML = `<strong>Captured Voice:</strong> ${data.original_text} <br> <strong>Translated Text:</strong> ${data.translated_text}`;
                    }
                })
                .catch(error => {
                    outputDiv.innerText = "Error occurred while processing the audio.";
                    console.error("Error:", error);
                });
            };
        })
        .catch(err => alert("Microphone access denied or not available."));
});

// ---- Text Translator ----
function translateText() {
    const text = document.getElementById("text-input").value;
    const target = document.getElementById("language-select").value;

    fetch("http://127.0.0.1:8000/api/translate/", {
        method: "POST",
        mode: "cors",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `text=${encodeURIComponent(text)}&target_lang=${target}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = data.translated_text || data.error || "Translation failed!";
    })
    .catch(() => {
        document.getElementById("output").innerText = "Error occurred!";
    });
}