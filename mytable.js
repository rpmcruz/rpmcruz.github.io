class Table {
  constructor(id, columns, columns_type, columns_sort_order, data) {
    let div = document.getElementById(id);
    let table = document.createElement('table');
    table.border = '1';
    div.appendChild(table);
    this.thead = table.createTHead();
    let tr = this.thead.insertRow();
    let th = document.createElement('th');
    tr.appendChild(th);
    th.textContent = '#';
    for(let i = 0; i < columns.length; i++) {
      let th = document.createElement('th');
      tr.appendChild(th);
      th.textContent = columns[i];
      if(columns_sort_order[i]) {
        const triangle = document.createElement('span');
        triangle.className = 'triangle';
        triangle.style.display = 'none';
        triangle.textContent = columns_sort_order[i] == 'asc' ? '▲' : '▼';
        th.appendChild(triangle);
        th.style.textDecoration = 'underline';
        th.style.cursor = 'pointer';
        th.onclick = function() {
          const triangles = this.thead.querySelectorAll('.triangle');
          for(let j = 0; j < triangles.length; j++)
            triangles[j].style.display = 'none';
          triangle.style.display = 'inline';
          this.sort_field = columns[i];
          this.sort_type = columns_type[i];
          this.sort_order = columns_sort_order[i];
          this.update();
        }.bind(this);
      }
    }
    this.tbody = table.createTBody();
    this.data = data;
    this.reset();
    this.update();
  }
  reset() {
    const triangles = this.thead.querySelectorAll('.triangle');
    for(let j = 0; j < triangles.length; j++)
      triangles[j].style.display = 'none';
    this.sort_field = null;
    this.filters = {};
  }
  set_filters(filters) {
    this.filters = filters;
  }
  update() {
    this.tbody.innerHTML = '';
    let rows = this.data;
    if(this.sort_field)
      rows = this.data.slice().sort(function(row1, row2) {
        if(row1[this.sort_field] == '') return 1;
        if(row2[this.sort_field] == '') return -1;
        if(row1[this.sort_field] == 'n/a') return 1;
        if(row2[this.sort_field] == 'n/a') return -1;
        let a = this.sort_type == 'numeric' ? parseFloat(row1[this.sort_field]) : row1[this.sort_field];
        let b = this.sort_type == 'numeric' ? parseFloat(row2[this.sort_field]) : row2[this.sort_field];
        if(a < b)
          return this.sort_order == 'asc' ? -1 : 1;
        if(a > b)
          return this.sort_order == 'asc' ? 1 : -1;
        return 0;
      }.bind(this));
    let id = 1;
    for(let i = 0; i < rows.length; i++) {
      let filter_out = false;
      for(let key in this.filters)
        if(rows[i][key] != this.filters[key])
          filter_out = true;
      if(filter_out)
        continue;
      let row = this.tbody.insertRow();
      row.insertCell().innerHTML = id;
      for(let key in rows[i])
        row.insertCell().innerHTML = rows[i][key];
      id++;
    }
  }
}

class Filters {
  constructor(table, id, filters) {
    this.table = table;
    this.filters = {};
    let div = document.getElementById(id);
    for(let key in filters) {
      let select = document.createElement('select');
      div.appendChild(select);
      div.appendChild(document.createTextNode(' '));
      select.onchange = () => this.changed();
      let option = document.createElement('option');
      option.text = key;
      select.add(option);
      for(let j = 0; j < filters[key].length; j++) {
        let option = document.createElement('option');
        option.text = filters[key][j];
        select.add(option);
      }
      this.filters[key] = select;
    }
    var reset = document.createElement('button');
    div.appendChild(reset);
    reset.textContent = 'Reset';
    reset.onclick = () => this.reset();
  }
  reset() {
    for(let key in this.filters)
      this.filters[key].selectedIndex = 0;
    this.table.reset();
    this.table.update();
  }
  changed() {
    let d = {};
    for(let key in this.filters)
      if(this.filters[key].selectedIndex > 0)
        d[key] = this.filters[key].value;
    this.table.set_filters(d);
    this.table.update();
  }
}
