google.charts.load('current', {'packages':['timeline']});
google.charts.setOnLoadCallback(drawChartGlobal);

const data = [{"date": "1995-6", "topics": [[{"keyword": "test", "weight": -0.9664996487646695}, {"keyword": "di", "weight": -0.25666793515702446}, {"keyword": "hall", "weight": 1.4747241957538237e-15}, {"keyword": "d", "weight": -1.234929840970158e-15}, {"keyword": "beet", "weight": -1.1638816061725995e-15}, {"keyword": "hallo", "weight": -6.99301637053672e-16}, {"keyword": "hoi", "weight": -2.5758432482904033e-16}, {"keyword": "goedenmidd", "weight": 2.4142209231160626e-16}, {"keyword": "mn", "weight": -2.3728712929814974e-16}, {"keyword": "br", "weight": -2.041844619514774e-16}], [{"keyword": "dag", "weight": 0.828078671210825}, {"keyword": "corne", "weight": 0.34503277967117746}, {"keyword": "allema", "weight": 0.3450327796711771}, {"keyword": "ma", "weight": 0.2760262237369416}, {"keyword": "hoi", "weight": 1.4077473557204264e-15}, {"keyword": "person", "weight": 5.516592634028206e-16}, {"keyword": "1t", "weight": 5.049113472753162e-16}, {"keyword": "hello", "weight": -3.6881751538466924e-16}, {"keyword": "test", "weight": 2.343825307246053e-16}, {"keyword": "mieg", "weight": -2.2371656600671593e-16}]]}, {"date": "1995-12", "topics": [[{"keyword": "hallo", "weight": -0.9471231692754316}, {"keyword": "h", "weight": -0.18525451161547313}, {"keyword": "pigg", "weight": -0.18525451161547307}, {"keyword": "iede", "weight": -0.1852545116154729}, {"keyword": "willemgt", "weight": 1.566703285715597e-16}, {"keyword": "isser", "weight": 1.4303094853922894e-16}, {"keyword": "tjoe", "weight": 1.3627281431639134e-16}, {"keyword": "weini", "weight": 1.176151320127208e-16}, {"keyword": "d", "weight": -1.1388922095536714e-16}, {"keyword": "iem", "weight": 1.0160822710472084e-16}], [{"keyword": "willemgt", "weight": 0.7071067811865478}, {"keyword": "d", "weight": 0.7071067811865474}, {"keyword": "goedemidda", "weight": -3.1977967241512434e-16}, {"keyword": "helem", "weight": 3.1194257247079413e-16}, {"keyword": "rogier", "weight": -1.4543807580719273e-16}, {"keyword": "binne", "weight": -1.3616999439884419e-16}, {"keyword": "wauw", "weight": 1.3487117947886734e-16}, {"keyword": "vanmiddag", "weight": 1.291060120160746e-16}, {"keyword": "komt", "weight": -1.2280838860711546e-16}, {"keyword": "duur", "weight": -1.0628180440990894e-16}]]}, {"date": "1995-11", "topics": [[{"keyword": "hiiiiiiiii", "weight": 0.8457594721337865}, {"keyword": "hi", "weight": 0.2733907465136304}, {"keyword": "jongens", "weight": 0.2733907465136304}, {"keyword": "dag", "weight": -0.26000568718531775}, {"keyword": "allema", "weight": -0.2600056871853176}, {"keyword": "hallo", "weight": 1.8800146801227242e-14}, {"keyword": "hall", "weight": 6.957520458758835e-15}, {"keyword": "anyb", "weight": 6.925344240219743e-15}, {"keyword": "nie", "weight": 7.085152963332948e-16}, {"keyword": "goeieavond", "weight": 6.450756161919024e-16}], [{"keyword": "allema", "weight": -0.6575690402013243}, {"keyword": "dag", "weight": -0.6575690402013242}, {"keyword": "hiiiiiiiii", "weight": -0.33441701068881124}, {"keyword": "jongens", "weight": -0.10809990217243048}, {"keyword": "hi", "weight": -0.10809990217243035}, {"keyword": "hallo", "weight": 1.4558186007553453e-15}, {"keyword": "mestgtz", "weight": 6.084875329466612e-16}, {"keyword": "hall", "weight": 5.497804003911809e-16}, {"keyword": "anyb", "weight": 5.442337498841607e-16}, {"keyword": "nie", "weight": 4.3693877942594043e-16}]]}, {"date": "1995-10", "topics": [[{"keyword": "e", "weight": -0.6318533929080979}, {"keyword": "hallo", "weight": -0.5959575581167328}, {"keyword": "hall", "weight": -0.3214854401060039}, {"keyword": "ff", "weight": -0.2413154906815639}, {"keyword": "zien", "weight": -0.2413154906815639}, {"keyword": "h", "weight": -0.09269422583265712}, {"keyword": "anyb", "weight": -0.0926942258326571}, {"keyword": "k", "weight": -0.09269422583265698}, {"keyword": "coen", "weight": 6.735900016764824e-16}, {"keyword": "i", "weight": 3.7752838402265975e-16}], [{"keyword": "hall", "weight": -0.5841426789228809}, {"keyword": "ff", "weight": 0.4154895348885616}, {"keyword": "zien", "weight": 0.4154895348885616}, {"keyword": "e", "weight": 0.37709855747527815}, {"keyword": "hallo", "weight": -0.3726646291288039}, {"keyword": "k", "weight": -0.10397431670582434}, {"keyword": "h", "weight": -0.10397431670582415}, {"keyword": "anyb", "weight": -0.1039743167058241}, {"keyword": "ger", "weight": 3.9196808844011126e-16}, {"keyword": "coen", "weight": -2.25186880132166e-16}]]}, {"date": "1995-8", "topics": [[{"keyword": "hallo", "weight": 0.8732247100880635}, {"keyword": "hall", "weight": 0.47181415958020906}, {"keyword": "robb", "weight": 0.0704036090723543}, {"keyword": "h", "weight": 0.07040360907235423}, {"keyword": "iede", "weight": 0.07040360907235417}, {"keyword": "boeh", "weight": -9.289569913715285e-16}, {"keyword": "goeie", "weight": -6.620948940634636e-16}, {"keyword": "hoi", "weight": 1.8843217193338484e-16}, {"keyword": "wou", "weight": 1.1071563935191753e-16}, {"keyword": "hmmmm", "weight": 9.559344637116489e-17}], [{"keyword": "hoi", "weight": -0.872825360891053}, {"keyword": "b", "weight": -0.35557229388448636}, {"keyword": "e", "weight": -0.23637283389502248}, {"keyword": "gaat", "weight": -0.23637283389502242}, {"keyword": "hall", "weight": 6.26413334283848e-14}, {"keyword": "hallo", "weight": -3.1233824881075037e-14}, {"keyword": "iede", "weight": -1.0377820672114146e-14}, {"keyword": "robb", "weight": -1.0255760515332887e-14}, {"keyword": "h", "weight": -1.018539802608919e-14}, {"keyword": "hee", "weight": -3.065398435394519e-16}]]}, {"date": "1995-9", "topics": [[{"keyword": "goedenavon", "weight": -0.8567627507899479}, {"keyword": "harrie", "weight": -0.2970303955362005}, {"keyword": "zeg", "weight": -0.29703039553620036}, {"keyword": "hoi", "weight": -0.21154606722184557}, {"keyword": "ee", "weight": -0.21154606722184352}, {"keyword": "hallo", "weight": 1.3880737453293662e-15}, {"keyword": "zitt", "weight": 8.290452983056669e-16}, {"keyword": "stille", "weight": 7.306452693958042e-16}, {"keyword": "boe", "weight": 7.282468730533728e-16}, {"keyword": "dag", "weight": 6.929299511119427e-16}], [{"keyword": "harrie", "weight": 0.6383913335726289}, {"keyword": "zeg", "weight": 0.6383913335726289}, {"keyword": "goedenavon", "weight": -0.36112867281594413}, {"keyword": "hoi", "weight": -0.16507436522506397}, {"keyword": "ee", "weight": -0.1650743652250637}, {"keyword": "hallo", "weight": 7.626153446399579e-16}, {"keyword": "dag", "weight": 6.09532580501656e-16}, {"keyword": "zitt", "weight": 5.335544391107792e-16}, {"keyword": "ma", "weight": -3.78431124622239e-16}, {"keyword": "hall", "weight": 2.6683643637687996e-16}]]}, {"date": "1996-1", "topics": [[{"keyword": "allemaal", "weight": 0.7071067811865476}, {"keyword": "e", "weight": 0.7071067811865476}, {"keyword": "hoi", "weight": 6.118627767130263e-16}, {"keyword": "ehhhhallo", "weight": -4.0237623242815926e-16}, {"keyword": "c", "weight": 3.0361643797714286e-16}, {"keyword": "eindel", "weight": 2.8848058922657754e-16}, {"keyword": "welkom", "weight": 2.621960377618899e-16}, {"keyword": "hie", "weight": -2.2252033071124306e-16}, {"keyword": "gelukkig", "weight": 2.1293376654669828e-16}, {"keyword": "goeie", "weight": 1.7138067434807124e-16}], [{"keyword": "hoi", "weight": -0.864652628755109}, {"keyword": "eindel", "weight": -0.4205997307104137}, {"keyword": "gelukkig", "weight": 0.24704360821574534}, {"keyword": "n", "weight": 0.12017135163154628}, {"keyword": "he", "weight": 6.414430951705137e-15}, {"keyword": "hall", "weight": 4.67491082093667e-15}, {"keyword": "hallo", "weight": 2.7899996072731946e-15}, {"keyword": "goeie", "weight": -2.575342208667538e-15}, {"keyword": "morg", "weight": -2.084353844787789e-15}, {"keyword": "ehhhhallo", "weight": -1.2972971109904884e-15}]]}, {"date": "1995-7", "topics": [[{"keyword": "hallo", "weight": 0.7931987358826154}, {"keyword": "guys", "weight": 0.515720317375695}, {"keyword": "doei", "weight": 0.18164841810754492}, {"keyword": "dag", "weight": 0.13272341463706797}, {"keyword": "herm", "weight": 0.1327234146370679}, {"keyword": "d", "weight": 0.1327234146370678}, {"keyword": "anto", "weight": 0.13272341463706774}, {"keyword": "da", "weight": 0.02655327350316475}, {"keyword": "he", "weight": 0.02655327350316475}, {"keyword": "hal", "weight": 2.1544490060216138e-16}], [{"keyword": "hal", "weight": -0.7071067811865476}, {"keyword": "triest", "weight": -0.7071067811865474}, {"keyword": "hallo", "weight": 4.712664991453978e-16}, {"keyword": "doei", "weight": 4.6670768255994965e-16}, {"keyword": "guys", "weight": -3.3235438203937876e-16}, {"keyword": "dag", "weight": -2.824324672637138e-16}, {"keyword": "morni", "weight": -2.482325083008307e-16}, {"keyword": "herm", "weight": 2.1057253334481612e-16}, {"keyword": "hoi", "weight": 2.0299023118015793e-16}, {"keyword": "pieter", "weight": -1.9495506581329426e-16}]]}];

let timeline = true;

let dataParsed = []
for(let i of data){
  let keywords = [];
  for(let j of i["topics"][0]){
    keywords.push(j["keyword"]);
  }
  keywords = keywords.join(" ");

  let date1 = new Date(i["date"]);
  let splittedDate = i["date"].split("-");
  let monthNumber = Number(splittedDate[1]) + 1;
  let year = Number(splittedDate[0]);
  if(monthNumber == 13){
    year += 1;
    let date2 = new Date(year+"-"+1);
    dataParsed.push(['Café', keywords, date1, date2]);
  } else {
    let date2 = new Date(year + "-" + monthNumber);
    dataParsed.push(['Café', keywords, date1, date2]);
  }
}

function drawChartGlobal() {
  var container = document.getElementById('timeline');
  var chart = new google.visualization.Timeline(container);
  var dataTable = new google.visualization.DataTable();

  dataTable.addColumn({ type: 'string', id: 'Cafe' });
  dataTable.addColumn({ type: 'string', id: 'Keyword' });
  dataTable.addColumn({ type: 'date', id: 'Start' });
  dataTable.addColumn({ type: 'date', id: 'End' });

  dataTable.addRows(dataParsed);
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

  dataTable.addRows(dataParsed);
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
