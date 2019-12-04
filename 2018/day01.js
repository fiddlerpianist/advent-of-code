'use strict';

const fs = require('fs');

// Part One: What is the resulting frequency after all of the changes in frequency have been applied?
function partOne(fileName, callback) {
  fs.readFile(fileName, 'utf8', function (error, contents) {
    const lines = contents.split(/\r?\n/);
    var freq = 0;
    lines.forEach(line => {
      freq += eval(line);
      //console.log(line, "Frequency:", freq);
    });
    callback(freq);
  });
}

// Part Two: What is the first frequency your device reaches twice?
function partTwo(fileName, callback) {
  fs.readFile(fileName, 'utf8', function (error, contents) {
    const lines = contents.split(/\r?\n/);
    var freq = 0, encountered = new Set([0]);
    var result = iterateLines(lines, freq, encountered, callback);
    var i = 1;
    while (!result.finished) {
      //console.log("Iteration " + i++);
      result = iterateLines(lines, result.frequency, encountered, callback);
    }
  });
}

function iterateLines(lines, freq, encountered, callback) {
  for (var i = 0; i < lines.length; i++) {
    var line = lines[i];
    freq += eval(line);
    if (encountered.has(freq)) {
      callback(freq);
      return {
        frequency: freq,
        finished: true
      }
    }
    encountered.add(freq);
  }
  return {
    frequency: freq,
    finished: false
  }
}

partOne('day01.txt',
  function (value) {
    console.log("Part One:", value);
  }
);

partTwo('day01.txt',
  function (value) {
    console.log("Part Two:", value);
  }
);