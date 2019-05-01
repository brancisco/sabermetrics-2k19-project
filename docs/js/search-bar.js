function searchValues (pattern, obj) {
  if (pattern.length <= 2) {
    return []
  }
  let matches = []
  let re = new RegExp(pattern, 'i')
  for (let k in obj) {
    if (re.test(obj[k])) {
      matches.push([k, obj[k]])
    }
  }
  return matches
}

function displayPlayers () {
  let input = document.getElementById('search_input').value
  let result = searchValues(input, playerMap)
  let list = document.getElementById('player_list')
  if (result.length > 0) {
    document.getElementById('search_component').classList.remove('empty')
    while (list.firstChild) {
      list.removeChild(list.firstChild);
    }
    for (let i in result) {
      let li = document.createElement('li')
      li.classList.add('list-result-wrap')
      li.onclick = () => { setInput(result[i][1]); drawChart(result[i][0]) }
      let div = document.createElement('div')
      div.classList.add('list-result')
      let t = document.createTextNode(`${result[i][1]}: ${result[i][0]}`)
      div.appendChild(t)
      li.appendChild(div)
      list.appendChild(li)
      if (i == result.length - 1) {
        li.classList.add('last-result')
      }
    }
  }
  else if (list.firstChild) {
    while (list.firstChild) {
      list.removeChild(list.firstChild);
      document.getElementById('search_component').classList.add('empty')
    }
  }
  else {
    document.getElementById('search_component').classList.add('empty')
  }
}

function setInput (value) {
  document.getElementById('search_input').value = value
}
function searchFocusIn () {
  document.getElementById('search_component').classList.add('active')
}
function searchFocusOut () {
  document.getElementById('search_component').classList.remove('active')
}