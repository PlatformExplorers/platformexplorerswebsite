/* Keep the supplied Kit form and its listeners, presenting it inline on this page. */
(() => {
  const slot = document.querySelector('.newsletter-signup');
  const status = document.querySelector('.newsletter-status');
  if (!slot) return;

  function mountForm() {
    const form = document.querySelector('form[data-uid="dbb0c59509"]');
    if (!form) return false;
    if (form.parentElement !== slot) slot.append(form);
    const fields = [
      ['fields[first_name]', 'newsletter-first-name', 'First name', 'Your first name', 'given-name'],
      ['email_address', 'newsletter-email', 'Email address', 'Your email address', 'email']
    ];
    for (const [name, id, text, placeholder, autocomplete] of fields) {
      const input = form.elements.namedItem(name);
      if (!input) continue;
      if (!input.id) input.id = id;
      input.placeholder = placeholder;
      input.autocomplete = autocomplete;
      input.setAttribute('aria-label', text);
      const field = input.closest('.formkit-field');
      if (field && !field.querySelector('label')) {
        const label = document.createElement('label');
        label.htmlFor = input.id;
        label.className = 'newsletter-field-label';
        label.textContent = text;
        field.prepend(label);
      }
    }
    const firstNameField = form.querySelector('input[name="fields[first_name]"]')?.closest('.formkit-field');
    const emailField = form.querySelector('input[name="email_address"]')?.closest('.formkit-field');
    if (firstNameField && emailField && firstNameField.parentElement === emailField.parentElement && firstNameField.nextElementSibling !== emailField) {
      emailField.parentElement.insertBefore(firstNameField, emailField);
    }
    const submitText = form.querySelector('[data-element="submit"] > span');
    if (submitText && submitText.textContent !== 'Subscribe for free') submitText.textContent = 'Subscribe for free';
    if (status) status.hidden = true;
    return true;
  }

  // Kit may move a modal form after inserting it. Keep the same form inline
  // through that initialization and any subsequent validation updates.
  function updateSuccessMessage() {
    // Kit creates this alert after accepting the signup. Never treat a click,
    // an attempted submission or an error alert as a successful subscription.
    const success = slot.querySelector('.formkit-alert-success');
    if (!success || !success.textContent.trim() || success.dataset.newsletterMessage === 'true') return;
    success.dataset.newsletterMessage = 'true';
    success.setAttribute('role', 'status');
    success.setAttribute('aria-live', 'polite');
    const heading = document.createElement('strong');
    heading.textContent = 'Check your inbox! 🎉';
    const message = document.createElement('p');
    message.textContent = 'Confirm your email to join the Platform Explorers newsletter.';
    const help = document.createElement('p');
    help.textContent = 'Don’t see it? Check your spam or promotions folder.';
    success.replaceChildren(heading, message, help);
  }

  const refresh = () => {
    mountForm();
    updateSuccessMessage();
  };
  const observer = new MutationObserver(refresh);
  observer.observe(document.body, {childList: true, subtree: true});
  refresh();

  window.setTimeout(() => {
    if (!slot.querySelector('form') && status) {
      status.replaceChildren('The signup form could not load. ', Object.assign(document.createElement('a'), {
        href: 'https://platform-explorers.kit.com/dbb0c59509',
        textContent: 'Open the signup form',
        target: '_blank',
        rel: 'noopener noreferrer'
      }));
    }
  }, 12000);
})();
