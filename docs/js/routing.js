function setHashLocation(location) {
  window.location.hash = location.reduce((acc, cur) => acc.concat('/', encodeURIComponent(cur)), '#')
}

function hashRouter (hash) {
  hash = decodeURIComponent(hash)
  let hash_arr = hash.split('/')
  if (hash_arr[0] === '#') {
    hash_arr = hash_arr.slice(1, hash_arr.length)
  }
  setHashLocation(hash_arr)
  if (hash_arr[0] === 'player-search') {
    pageButtonHandler(document.getElementById('show_app_button'))
    if (hash_arr.length > 1) {
      setInput(hash_arr[1])
      displayPlayers()
    }
  } else if (hash_arr[0] === 'about') {
    pageButtonHandler(document.getElementById('show_about_button'))
  }
}

function pageButtonHandler (el) {
  el.classList.remove('inactive')
  if(el.id == 'show_app_button') {
    document.getElementById('show_about_button').classList.add('inactive')
    document.getElementById('about').classList.add('hide-time')
    document.getElementById('about').classList.remove('show-time')
    document.getElementById('app').classList.remove('hide-time')
    document.getElementById('app').classList.add('show-time')
  }
  else {
    document.getElementById('show_app_button').classList.add('inactive')
    document.getElementById('app').classList.add('hide-time')
    document.getElementById('app').classList.remove('show-time')
    document.getElementById('about').classList.add('show-time')
    document.getElementById('about').classList.remove('hide-time')
  }
}
