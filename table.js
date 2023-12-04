var table;
var listing;
var topics_description;
var sort_field;
var cur_topic, cur_filter;

function createTable(table_id, _listing, _topics_description) {
  table = document.getElementById(table_id).getElementsByTagName('tbody')[0];
  listing = _listing;
  topics_description = _topics_description;
  fillTable();
}

function toggleFilter(key, value) {
  if(cur_filter && cur_filter[1] == value) {
    document.getElementById(value).classList.remove("active");
    cur_filter = null;
  }
  else {
    if(cur_filter)
      document.getElementById(cur_filter[1]).classList.remove("active");
    document.getElementById(value).classList.add("active");
    cur_filter = [key, value];
  }
  fillTable();
}

function toggleTopic(value) {
  if(cur_topic && cur_topic == value) {
    document.getElementById(value).classList.remove("active");
    cur_topic = null;
  }
  else {
    if(cur_topic)
      document.getElementById(cur_topic).classList.remove("active");
    document.getElementById(value).classList.add("active");
    cur_topic = value;
  }
  let description = document.getElementById('topic_description');
  description.innerHTML = cur_topic ? '<i>Topic description:</i> ' + topics_description[cur_topic] : '';
  description.style.display = cur_topic ? 'block' : 'none';
  // hide filters that do not correspond to this topic
  if(cur_filter) {
    document.getElementById(cur_filter[1]).classList.remove("active");
    cur_filter = null;
  }
  let filters = document.querySelectorAll('a.filter.other');
  for(let j = 0; j < filters.length; j++) {
    if(cur_topic == null) {
        filters[j].style.display = 'inline-block';
        continue;
    }
    let value = filters[j].id;
    let found = false;
    for(let i = 0; i < listing.length; i++) {
      if(cur_topic && listing[i]['topic'] != cur_topic)
        continue;
      if(listing[i]['type'] == value ||
         listing[i]['sjr-rank'] == value ||
         listing[i]['core-rank'] == value) {
        found = true;
        break;
      }
    }
    filters[j].style.display = found ? 'inline-block' : 'none';
  }
  sort_field = null;
  fillTable();
}

function sort(field, order, type) {
    sort_field = [field, order, type];
    fillTable();
}

function fillTable() {
  this.table.innerHTML = '';
  let j = 0;

  let _listing = listing;
  if(sort_field)
    _listing = listing.slice().sort(function(a, b) {
      a = a[sort_field[0]];
      a = sort_field[2] == 'int' ? parseInt(a) : a;
      b = b[sort_field[0]];
      b = sort_field[2] == 'int' ? parseInt(b) : b;
      if(a === '' && b != '')
        return sort_field[1] == 'asc' ? 1 : -1;
      if(a != '' && b === '')
        return sort_field[1] == 'asc' ? -1 : 1;
      if(a < b)
        return sort_field[1] == 'asc' ? -1 : 1;
      if(a > b)
        return sort_field[1] == 'asc' ? 1 : -1;
      return 0;
    });

  for(let i = 0; i < _listing.length; i++) {
    if(cur_topic && _listing[i]['topic'] != cur_topic)
      continue
    if(cur_filter && _listing[i][cur_filter[0]] != cur_filter[1])
      continue;
    var row = table.insertRow(j);
    row.insertCell(0).innerHTML = _listing[i]['year'];
    row.insertCell(1).innerHTML = '<a href="' + _listing[i]['url'] + '">' + _listing[i]['title'] + '</a><br>' + _listing[i]['where'];
    row.insertCell(2).innerHTML = _listing[i]['type'];
    row.insertCell(3).innerHTML = _listing[i]['citations'];
    row.insertCell(4).innerHTML = _listing[i]['topic'];
    row.insertCell(5).innerHTML = _listing[i]['sjr-rank'];
    row.insertCell(6).innerHTML = _listing[i]['core-rank'];
    j++;
  }
}
