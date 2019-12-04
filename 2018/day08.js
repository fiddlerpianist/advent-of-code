'use strict';
const fs = require('fs');

function partOne(fileName) {
  let contents = fs.readFileSync(fileName, 'utf8');
  let array = contents.split(' ');
  console.log(array);
  deriveMetadata(array, 0, array.length, 0);
}

function deriveMetadata(array, startIdx, endIdx, cumulativeSum) {
  if (startIdx === endIdx) {
    return;
  }
  let numChildren = parseInt(array[startIdx]);
  let numMetadata = parseInt(array[startIdx + 1]);
  let sum = 0;
  for (let i = endIdx - 1; endIdx - i < numMetadata; i--) {
    sum += array[i];
  }
}

function peek(array) {
  // return last element in array
  return array[array.length - 1];
}

partOne('day08-test.txt');
//partTwo('day05.txt');