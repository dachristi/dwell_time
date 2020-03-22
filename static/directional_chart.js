//$(document).ready(function() {

  //$("#load_chart").click(function() {

  //$("#datepicker").change(function() {
  var chart_fn = function(){
    //alert($("#datepicker").val())
    var data_type = $('input[name=type_toggle]:checked').val()
    if (data_type == 1) {
      var chart_data_ajax = "/chart_data_directional"
      var dwell_text = ""
      var dwell_text_chart = ""
    } else {
      var chart_data_ajax = "/chart_data_non_directional"
      var dwell_text = "MOST LIKELY"
      var dwell_text_chart = ""
    }

    $.post(chart_data_ajax,
    {
      date_selected: $("#datepicker").val()
    },

    function(data,status){
      var date_selected = $("#datepicker").val()
    if (data_type == 1){
      var series_data = [
      {
          name: 'Actual',
          data: data.data_visitors_probable,
          step:'Right'
      }
    ]
    }
    else {
      var series_data = [
            {
                name: 'Mininum',
                data: data.data_visitors_min,
                step:'Right'
            },
            {
                name: 'Maximum',
                data: data.data_visitors_max,
                step:'Right'
            },
            {
                name: 'Expectation',
                data: data.data_visitors_expected,
                step:'Right'
            },
            {
                name: 'Most Likely',
                data: data.data_visitors_probable,
                step:'Right'
            }
          ]
    }

    Highcharts.chart('n_chart', {
      chart: {
          //type: 'spline'
          //type: 'column'
          //type: 'scatter'
          type: 'line'
          //type: 'area'
      },

      title: {
          text: 'Daily Occupancy Trend'
      },
      credits: {
          enabled: false
        },

      subtitle: {
          text: date_selected
      },

      xAxis: {
            //type: 'linear'
            type: 'datetime'
      },

      yAxis: {
          title: {
              text: dwell_text_chart + 'Occupancy'
          }
        },
      legend: {
          layout: 'horizontal',
          align: 'center',
          verticalAlign: 'bottom'
      },
      plotOptions: {
          series: {
              fillColor: {
                  linearGradient: [0, 0, 0, 300],
                  stops: [
                      [0, Highcharts.getOptions().colors[0]],
                      [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                  ]
              }
          }
      },
      // plotOptions: {
      //     series: {
      //         label: {
      //             connectorAllowed: false
      //         },
      //         // pointStart: 2010
      //     }
      // },


    series: series_data,

    //   series: [
    //   {
    //       name: 'Mininum',
    //       data: data.data_visitors_min,
    //       step:'Right'
    //   },
    //   {
    //       name: 'Maximum',
    //       data: data.data_visitors_max,
    //       step:'Right'
    //   },
    //   {
    //       name: 'Expectation',
    //       data: data.data_visitors_expected,
    //       step:'Right'
    //   },
    //   {
    //       name: 'Most Likely',
    //       data: data.data_visitors_probable,
    //       step:'Right'
    //   }
    // ],

      responsive: {
          rules: [{
              condition: {
                  maxWidth: 500
              },
              chartOptions: {
                  legend: {
                      layout: 'horizontal',
                      align: 'center',
                      verticalAlign: 'bottom'
                  }
              }
          }]
      }

  });
  $("#total_visitors").text(data.total_visitors)
  $("#average_dwell_probable").text(data.average_dwell_probable)
  $("#dwell_type").text(dwell_text)

  if (data_type == 1){
    $("#average_dwell_max").text("")
    $("#average_dwell_expected").text("")
    $("#average_dwell_min").text("")
    $("#dwell_type_max").text("")
    $("#dwell_type_expected").text("")
    $("#dwell_type_min").text("")
  }
  else {
    $("#average_dwell_min").text(data.average_dwell_min)
    $("#average_dwell_max").text(data.average_dwell_max)
    $("#average_dwell_expected").text(data.average_dwell_expected)

    $("#dwell_type_min").text(" MINUTES MINIMUM AVERAGE DWELL TIME")
    $("#dwell_type_max").text(" MINUTES MAXIMUM AVERAGE DWELL TIME")
    $("#dwell_type_expected").text(" MINUTES EXPECTED AVERAGE DWELL TIME")
  }
})
}//)
//})
