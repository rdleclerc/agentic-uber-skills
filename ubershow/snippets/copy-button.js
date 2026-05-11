// Ubershow authoring snippet. Inline this pattern into final generated HTML.
async function copyTextFromElement(elementId, button) {
  const el = document.getElementById(elementId);
  const text = el ? el.innerText || el.textContent || '' : '';
  try {
    await navigator.clipboard.writeText(text);
    if (button) {
      const old = button.textContent;
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = old; }, 1200);
    }
  } catch (_) {
    window.prompt('Copy this text:', text);
  }
}
