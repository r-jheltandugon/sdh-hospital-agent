let state = { step: 0 };

async function sendMessage() {
    const userInput = document.getElementById("user-input").value;
    const responseDiv = document.getElementById("messages");

    if (userInput) {
        // Display the user's message
        responseDiv.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;
        document.getElementById("user-input").value = "";  // Clear input field

        // Send the message to the backend API and get the next message
        const response = await fetch("http://127.0.0.1:8000/conversation", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ ...state, ...{ [getKeyForStep(state.step)]: userInput } }),
        });

        const data = await response.json();
        // Display AI's response
        responseDiv.innerHTML += `<div><strong>AI:</strong> ${data.message}</div>`;
        
        // Update state and proceed to the next step
        state = { ...state, ...{ step: state.step + 1 } };
    }
}

function getKeyForStep(step) {
    switch (step) {
        case 0: return "symptoms";
        case 1: return "temperature";
        case 2: return "heart_rate";
        case 3: return "blood_pressure";
        case 4: return "respiratory_rate";
        default: return "";
    }
}
