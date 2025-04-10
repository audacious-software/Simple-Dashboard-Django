/* global requirejs */

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
    cookie: '/static/simple_dashboard/js/vendor/js.cookie',
    chart: '/static/simple_dashboard/js/vendor/chart-3.4.0.min',
    moment: '/static/simple_dashboard/js/vendor/moment-with-locales'
  }
})

requirejs(['material', 'cookie', 'chart', 'jquery', 'base', 'moment'], function (mdc, Cookies) {
  require(['chart'], function (Chart) {
    console.log('Chart: ')
    console.log(Chart)
  })
})
