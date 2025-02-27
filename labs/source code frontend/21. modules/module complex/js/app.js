// app.js - Main module that initializes the app

import { setupEventListeners } from "./eventHandlers.js";

// Initialize event listeners when the script loads
document.addEventListener("DOMContentLoaded", () => {
    setupEventListeners();
});
