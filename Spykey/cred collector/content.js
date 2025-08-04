(function () {
  console.log('[EXT-DEBUG] 🚀 Extension script injected.');

  const url = window.location.href.toLowerCase();

  // Check if URL indicates a login or signup page
  const isLoginLikePage = /login|signin|signup|register|auth/.test(url);
  if (!isLoginLikePage) {
    console.log('[EXT-DEBUG] ⛔ Page URL does not suggest a login/signup page. Skipping...');
    return;
  }

  console.log('[EXT-DEBUG] ✅ URL suggests a login/signup page:', url);

  // Function to identify login input fields and log them
  function logLoginInputFields() {
    const inputs = document.querySelectorAll('input');
    const collectedData = [];

    inputs.forEach((input, index) => {
      const type = input.type?.toLowerCase() || 'text';
      const name = input.name?.toLowerCase() || '';
      const value = input.value || '';

      const isUsernameField = /user|email|login|id/.test(name) && type !== 'hidden';
      const isPasswordField = type === 'password';

      if ((isUsernameField || isPasswordField) && value.trim() !== '') {
        collectedData.push({
          index: index + 1,
          type,
          name,
          value,
        });
      }
    });

    if (collectedData.length > 0) {
      console.log('[EXT-DEBUG] 🔐 Non-empty login-related fields detected:');
      collectedData.forEach(field => {
        console.log(`[EXT-DEBUG] #${field.index} → Type: ${field.type}, Name: ${field.name}, Value: ${field.value}`);
      });
    } else {
      console.log('[EXT-DEBUG] ⚠️ No non-empty login input fields found.');
    }
  }

  // Run once on load
  window.addEventListener('load', () => {
    console.log('[EXT-DEBUG] 🧭 Page fully loaded. Checking for login fields...');
    logLoginInputFields();
  });

  // Run again after a delay for dynamically populated fields
  setTimeout(() => {
    console.log('[EXT-DEBUG] ⏱️ Re-checking login fields after delay...');
    logLoginInputFields();
  }, 3000);
})();
