// domUtils.js - Handles updates to the DOM

export function updateGreetingMessage(name) {
    const messageElement = document.getElementById("greetingMessage");
    if (name.trim() === "") {
        messageElement.textContent = "Please enter your name!";
        messageElement.style.color = "red";
    } else {
        messageElement.textContent = `Hello, ${name}!`;
        messageElement.style.color = "green";
    }
}
