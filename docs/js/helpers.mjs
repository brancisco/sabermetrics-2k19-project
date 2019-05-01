export const simpleMovingAvg = (arr, i, windowSize = 5) => {
  return arr.map((c, j, arr2) => {
    let windowAvg = 0
    if (j > windowSize) {
      for (let k = j - windowSize; k < j; k++) {
        windowAvg += arr2[k][i]
      }
      windowAvg /= windowSize
    }
    else {
      let k
      for (k = 0; k <= j; k++) {
        windowAvg += arr2[k][i]
      }
      windowAvg /= k
    }
    return windowAvg
  })
}

// let foo = [['hi', 2], ['hey', 10], ['hi', 3], ['hello', 40], ['okay', 20]]
// console.log(foo)
// console.log(mapWindowAvg(foo, 1))

// foo = [['hi', 2], ['hey', 10], ['hi', 3], ['hello', 40]]
// console.log(foo)
// console.log(mapWindowAvg(foo, 1))