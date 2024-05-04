class Table {
  constructor(id, data, columns, columns_type) {
    let div = document.getElementById(id);
    let table = document.createElement('table');
    table.border = '1';
    div.appendChild(table);
    this.thead = table.createTHead();
    let tr = this.thead.insertRow();
    let th = document.createElement('th');
    tr.appendChild(th);
    th.textContent = '#';
    this.headers = []
    for(let i = 0; i < columns.length; i++) {
      let th = document.createElement('th');
      let h;
      if(columns_type[i] == 'filter') {
        let values = data.map(row => row[i]);
        values = [...new Set(values)].sort();
        h = new HeaderFilter(this, th, columns[i], values);
      }
      else if(columns_type[i] == 'sort')
        h = new HeaderSort(this, th, columns[i]);
      else
        h = new HeaderText(this, th, columns[i]);
      this.headers.push(h);
      tr.appendChild(th);
    }
    this.tbody = table.createTBody();
    this.data = data;
    this.update();
  }
  reset_sort() {
    for(let i = 0; i < this.headers.length; i++)
      this.headers[i].reset_sort();
  }
  update() {
    const range = [...Array(this.headers.length).keys()];
    let data = this.data.slice().sort(
        (row1, row2) => range.map(i => this.headers[i].compare(row1[i], row2[i])).reduce((acc, v) => acc+v, 0)
        ).filter(row => range.every(i => this.headers[i].filter(row[i])));
    this.tbody.innerHTML = '';
    for(let i = 0; i < data.length; i++) {
      let row = this.tbody.insertRow();
      row.insertCell().innerHTML = i+1;
      for(let j = 0; j < data[i].length; j++)
        row.insertCell().innerHTML = data[i][j];
    }
  }
}

class HeaderText {
  constructor(table, th, name) {
    th.textContent = name;
  }
  compare(value1, value2) { return 0; }
  filter(value) { return true; }
  reset_sort() {}
}

class HeaderFilter {
  constructor(table, th, name, categories) {
    let select = document.createElement('select');
    let option = document.createElement('option');
    option.text = name;
    select.add(option);
    for(let j = 0; j < categories.length; j++) {
      let option = document.createElement('option');
      option.text = categories[j];
      select.add(option);
    }
    select.onchange = () => this.table.update();
    th.appendChild(select);
    this.select = select;
    this.table = table;
  }
  compare(value1, value2) { return 0; }
  filter(value) {
    if(this.select.selectedIndex > 0)
        return value == this.select.options[this.select.selectedIndex].value;
    return true;
  }
  reset_sort() {}
}

class HeaderSort {
  constructor(table, th, name) {
    th.textContent = name;
    th.style.color = 'blue';
    th.style.textDecoration = 'underline';
    th.style.cursor = 'pointer';
    this.triangle = document.createElement('span');
    this.triangle.className = 'triangle';
    this.triangle.style.display = 'none';
    th.appendChild(this.triangle);
    th.onclick = function() {
      const old_sort = this.sort;
      this.table.reset_sort();
      this.sort = old_sort == null || old_sort == 'desc' ? 'asc' : 'desc';
      this.triangle.textContent = this.sort == 'asc' ? '▲' : '▼';
      this.triangle.style.display = 'inline';
      this.table.update();
    }.bind(this);
    this.sort = null;
    this.table = table;
  }
  compare(value1, value2) {
    if(this.sort == null)
        return 0;
    const order = this.sort == 'asc' ? 1 : -1;
    // convert to numbers if both values are numeric strings
    const num1 = parseFloat(value1);
    const num2 = parseFloat(value2);
    value1 = isNaN(num1) ? value1 : num1;
    value2 = isNaN(num2) ? value2 : num2;
    // whitespace always comes last
    if(value1 === '' || value2 === '')
      return value1 === '' ? 1 : -1;
    // check if both values are numbers or both are non-numeric strings
    if((!isNaN(num1) && !isNaN(num2)) || (isNaN(num1) && isNaN(num2)))
      // if both are numbers or both are non-numeric strings, use default comparison
      return order * (value1 < value2 ? -1 : (value1 > value2 ? 1 : 0));
    // if one is numeric and other is non-numeric, numeric always wins
    return isNaN(num1) ? 1 : -1;
  }
  filter(value) { return true; }
  reset_sort() {
    this.sort = null;
    this.triangle.style.display = 'none';
  }
}
