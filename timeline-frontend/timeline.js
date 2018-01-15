google.charts.load('current', {'packages':['timeline']});
google.charts.setOnLoadCallback(drawChartGlobal);

const fragmentsPerCafe = [
  [ 'Gay', 'aa', new Date(1995, 1, 2), new Date(1995, 1, 3)],
  [ 'Sport', 'EK',  new Date(1995, 1, 2), new Date(1995, 1, 6) ],
  [ 'Politiek', 'Lubbers', new Date(1995, 1, 4), new Date(1995, 1, 10)]
];

const fragmentsGlobal = [
  [ 'Café', 'aa', new Date(1995, 1, 2), new Date(1995, 1, 3)],
  [ 'Café', 'EK',  new Date(1995, 1, 3), new Date(1995, 1, 6) ],
  [ 'Café', 'Lubbers', new Date(1995, 1, 6), new Date(1995, 1, 10)]
];

let timeline = true;

function drawChartGlobal() {
  var container = document.getElementById('timeline');
  var chart = new google.visualization.Timeline(container);
  var dataTable = new google.visualization.DataTable();

  dataTable.addColumn({ type: 'string', id: 'Cafe' });
  dataTable.addColumn({ type: 'string', id: 'Keyword' });
  dataTable.addColumn({ type: 'date', id: 'Start' });
  dataTable.addColumn({ type: 'date', id: 'End' });

  dataTable.addRows(fragmentsGlobal);
  chart.draw(dataTable);
}

function drawChartPerCafe() {
  var container = document.getElementById('timeline');
  var chart = new google.visualization.Timeline(container);
  var dataTable = new google.visualization.DataTable();

  dataTable.addColumn({ type: 'string', id: 'Cafe' });
  dataTable.addColumn({ type: 'string', id: 'Keyword' });
  dataTable.addColumn({ type: 'date', id: 'Start' });
  dataTable.addColumn({ type: 'date', id: 'End' });

  dataTable.addRows(fragmentsPerCafe);
  chart.draw(dataTable);
}

function switchTimeline(){
  timeline = !timeline;
  if(timeline){
    drawChartGlobal();
  } else {
    drawChartPerCafe()
  }
}
