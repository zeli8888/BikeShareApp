// eventHandlers.js - Handles events

import { updateGreetingMessage } from "./domUtils.js";

export function setupEventListeners() {
    const button = document.getElementById("greetButton");
    const input = document.getElementById("nameInput");

    // Button click event
    button.addEventListener("click", () => {
        updateGreetingMessage(input.value);
    });

    // Enter key event on input field
    input.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            updateGreetingMessage(input.value);
        }
    });
}
