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
  $('#deselect_all_sources').hide()
  $('#deselect_all_types').hide()

  $('#select_all_sources').click(function () {
    $('.source_checkbox').prop('checked', true)
    $('#select_all_sources').hide()
    $('#deselect_all_sources').show()
  })

  $('#deselect_all_sources').click(function () {
    $('.source_checkbox').prop('checked', false)
    $('#deselect_all_sources').hide()
    $('#select_all_sources').show()
  })

  $('#select_all_types').click(function () {
    $('.data_type_checkbox').prop('checked', true)
    $('#select_all_types').hide()
    $('#deselect_all_types').show()
  })

  $('#deselect_all_types').click(function () {
    $('.data_type_checkbox').prop('checked', false)
    $('#deselect_all_types').hide()
    $('#select_all_types').show()
  })

  $('.export_list').height(400)
})
