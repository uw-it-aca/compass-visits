// utility functions are simple functions that don't utilize Vue specific
// functionality (i.e. reative state, or lifecycle hooks).
// these should be limited to simple helper functions

// format.js

function formatPhoneNumber(phoneNumber) {
  var phoneNumberString = Math.floor(parseFloat(phoneNumber)).toString();
  var cleaned = ("" + phoneNumberString).replace(/\D/g, "");
  var match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
  if (match) {
    return "(" + match[1] + ") " + match[2] + "-" + match[3];
  }
  return null;
}

// expose the callable method as return value
export { formatPhoneNumber };
