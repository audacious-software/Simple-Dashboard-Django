/* global requirejs, alert */

requirejs.config({
  shim: {
    jquery: {
      exports: '$'
    },
    cookie: {
      exports: 'Cookies'
    },
    bootstrap: {
      deps: ['jquery']
    }
  },
  baseUrl: '/static/simple_dashboard/js/app',
  paths: {
    app: '/static/simple_dashboard/js/app',
    material: '/static/simple_dashboard/js/vendor/material-components-web-11.0.0',
    jquery: '/static/simple_dashboard/js/vendor/jquery-3.4.0.min',
    cookie: '/static/simple_dashboard/js/vendor/js.cookie'
  }
})

requirejs(['material', 'cookie', 'jquery', 'base'], function (mdc, Cookies) {
  console.log(mdc)

  mdc.textField.MDCTextField.attachTo(document.getElementById('username-field'))
  const emailField = mdc.textField.MDCTextField.attachTo(document.getElementById('email-field'))
  const currentPasswordField = mdc.textField.MDCTextField.attachTo(document.getElementById('current-password-field'))
  const newPasswordField = mdc.textField.MDCTextField.attachTo(document.getElementById('new-password-field'))
  const confirmPasswordField = mdc.textField.MDCTextField.attachTo(document.getElementById('confirm-password-field'))

  $('#update-form').submit(function (event) {
    const email = emailField.value
    const currentPassword = currentPasswordField.value
    const newPassword = newPasswordField.value
    const confirmPassword = confirmPasswordField.value

    console.log('e: ' + email + '; cp: ' + currentPassword + '; np: ' + newPassword + '; np2: ' + confirmPassword)

    if (newPassword !== '') {
      if (currentPassword === '') {
        alert('Enter current password to continue.')

        event.preventDefault()
      } else if (newPassword !== confirmPassword) {
        alert('Password confirmation does not match new password provided.')

        event.preventDefault()
      }
    }

    if (email === '') {
      alert('Please enter a valid e-mail address.')

      event.preventDefault()
    }
  })
})
