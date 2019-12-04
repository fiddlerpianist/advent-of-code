'use strict';
const fs = require('fs');

// Part One: How many units remain after fully reacting the polymer you scanned?
function partOne(fileName) {
  let contents = fs.readFileSync(fileName, 'utf8');
  depolarize([], Array.from(contents), 0, function (result) {
    console.log("Part One:", result.length);
  });
}

function partTwo(fileName) {
  let contents = fs.readFileSync(fileName, 'utf8');
  let contentsArray = Array.from(contents);
  let firstCharCode = "A".charCodeAt(0);
  let charMap = new Map();
  for (let currentPolymerCode = firstCharCode; currentPolymerCode < firstCharCode + 26; currentPolymerCode++) {
    let filteredPolymer = filterOutChar(currentPolymerCode, contentsArray);
    depolarize([], filteredPolymer, 0, function (result) {
      console.log(String.fromCharCode(currentPolymerCode) + ":", result.length);
    });
  }
  console.log("Part Two: visually scan through the following numbers and find the lowest.");
}

function filterOutChar(charCode, array) {
  return array.filter(char => char.toUpperCase() !== String.fromCharCode(charCode));
}

function depolarize(left, right, rightIndex, callback) {
  if (rightIndex % 100 === 0) {
    setImmediate(function () {
      _depolarize(left, right, rightIndex, callback);
    });
  } else {
    _depolarize(left, right, rightIndex, callback);
  }
}

function _depolarize(left, right, rightIndex, callback) {
  if (rightIndex === right.length) {
    callback(left);
  } else if (left.length === 0 || Math.abs(peek(left).charCodeAt(0) - right[rightIndex].charCodeAt(0)) !== 32) {
    left.push(right[rightIndex]);
    depolarize(left, right, ++rightIndex, callback);
  } else {
    left.pop();
    depolarize(left, right, ++rightIndex, callback);
  }
}

function peek(array) {
  // return last element in array
  return array[array.length - 1];
}

partOne('day05.txt');
partTwo('day05.txt');