var chart;

function drawChart(mlbid) {
  let pdata;
  let rows = []
  let player = playerMap[mlbid]

  if (pitchers[mlbid]) {
    pdata = pitchers[mlbid]
  }
  else if (batters[mlbid]) {
    pdata = batters[mlbid]
  }

  if (pdata) {
    let avgData = simpleMovingAvg(pdata, 1, 15)

    let data = new google.visualization.DataTable()
    data.addColumn('number', 'Event #')
    data.addColumn('number', 'Event')
    data.addColumn({'type': 'string', 'role': 'tooltip'})
    data.addColumn({'type': 'string', 'role': 'style'})
    data.addColumn('number', 'Avg Ranking')
    data.addRows(pdata.length)
    
    for (let i = 0; i < pdata.length; i ++) {
      for (let j = 0; j < 4; j ++) {
        data.setCell(i, j, pdata[i][j])
      }
      data.setCell(i, 4, avgData[i])
    }
    
    let options = {
      title: `${player} Points Season 2018`,
      legend: { position: 'bottom' },
      seriesType: 'scatter',
      vAxis: {title: 'Points'},
      hAxis: {title: 'Event #'},
      series: {
        0: { label: 'Redfkj' },
        1: {
          type: 'line',
          color: '#a537fd',
          lineWidth: 3
        }
      }
    }

    chart = new google.visualization.ComboChart(document.getElementById('curve_chart'))
    chart.draw(data, options)
  }
}