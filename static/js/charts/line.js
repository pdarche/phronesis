
var config = {
   chart: {
      renderTo: 'timeseries',
      zoomType: 'x',
      type: 'line'
    },
    subtitle: {
        text: document.ontouchstart === undefined ?
            'Click and drag in the plot area to zoom in' :
            'Drag your finger over the plot to zoom in'
     },
     legend: {
        layout: 'horizontal',
          borderRadius:0,
          borderWidth:0,
          symbolWidth: 15
     }, 
     tooltip: {
        pointFormat: '<span style="color:{series.color}; font-weight:bold">{series.name}</span>: <b>{point.y}</b><br/>',
        crosshairs: {
          width: 1,
          color: 'gray',
          dashStyle: 'shortdot'
        },
        shared: true,
        valueDecimals : 4
     },
     credits:{
        enabled: false
     },
     title: {
        text: 'Timeseries'
     },
     xAxis: {
          type: 'datetime',
          dateTimeLabelFormats: { // don't display the dummy year
              month: '%b %e',
              year: '%b'
          },
          labels: {
              // rotation: -90,
              // align: 'right'
           },
     },
     yAxis: {
        title: {
           text: ''
        }
     },
     plotOptions: {
        series: {
            marker: {
                states: {
                  hover: {
                    enabled: true
                  },
                },
                enabled: false
            },
            shadow: false
      },
      line: {
      }
    }
 }