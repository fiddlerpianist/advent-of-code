'use strict';

const fs = require('fs');

// Part One: What is the checksum for your list of box IDs?
function partOne(fileName) {
  var contents = fs.readFileSync(fileName, 'utf8');
  const lines = contents.split(/\r?\n/);
  var twos = 0;
  var threes = 0;
  lines.forEach(line => {
    //console.log(result);
    var result = twosAndThrees(line);
    twos += result.twos ? 1 : 0;
    threes += result.threes ? 1 : 0;
  });
  console.log("Part One:", twos * threes);
}

function twosAndThrees(id) {
  //console.log("ID:", id);
  var map = new Map();
  Array.from(id).forEach(element => {
    if (map.has(element)) {
      map.set(element, map.get(element) + 1);
    } else {
      map.set(element, 1);
    }
  });
  //console.log(map);
  var counts = Array.from(map.values()).filter(number => (number == 2 || number == 3));
  return {
    twos: counts.includes(2),
    threes: counts.includes(3)
  }
}

// Part Two: What letters are common between the two correct box IDs?
function partTwo(fileName) {
  var contents = fs.readFileSync(fileName, 'utf8');
  const lines = contents.split(/\r?\n/);
  var i, j;
  for (i = 0; i < lines.length; i++) {
    for (j = i+1; j < lines.length; j++) {
      var indexCompare = compareLines(i, j, lines);
      if (indexCompare > -1) {
        console.log("Part Two:", removeIndex(lines[i], indexCompare));
        return;
      }
    }
  }
}

function compareLines(first, second, lines) {
  var indexWhereDifferent = -1;
  var line1 = lines[first], line2 = lines[second];
  // all lines have the same number of letters
  for (var i=0; i < line1.length; i++) {
    if (!(line1[i] === line2[i])) {
      if (indexWhereDifferent > -1) {
        // it's not this one, as there is more than one letter different
        return -1;
      }
      indexWhereDifferent = i;
    }
  }
  // we made it! We found the two
  return indexWhereDifferent;
}

function removeIndex(string, indexToRemove) {
  var arr = Array.from(string);
  arr.splice(indexToRemove, 1);
  return arr.join('');
}

partOne('day02.txt');
partTwo('day02.txt');
