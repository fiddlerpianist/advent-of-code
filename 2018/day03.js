'use strict';

const fs = require('fs');

// Part One: How many square inches of fabric are within two or more claims?
function partOne(fileName) {
  var contents = fs.readFileSync(fileName, 'utf8');
  const lines = contents.split(/\r?\n/);
  var grid = [], conflictCounter = 0;
  lines.forEach(line => {
    var data = parse(line);
    //console.log(data);
    var x, y;
    for (var i = 0; i < data.width; i++) {
      for (var j = 0; j < data.height; j++) {
        x = data.x + i;
        y = data.y + j;
        if (grid[x] === undefined) {
          grid[x] = [];
        }
        if (grid[x][y] === undefined) {
          grid[x][y] = 0;
        } else if (grid[x][y] === 0) {
          // first and n conflicts
          conflictCounter++;
          grid[x][y] = 1;
        }
      }
    }
  });
  console.log("Part One:", conflictCounter);
}

// Part Two: What is the ID of the only claim that doesn't overlap?
function partTwo(fileName) {
  var contents = fs.readFileSync(fileName, 'utf8');
  const lines = contents.split(/\r?\n/);
  var grid = [], noConflicts = new Set();
  lines.forEach(line => {
    var data = parse(line);
    // it doesn't conflict yet
    noConflicts.add(data.id);
    //console.log(data);
    var x, y;
    for (var i = 0; i < data.width; i++) {
      for (var j = 0; j < data.height; j++) {
        x = data.x + i;
        y = data.y + j;
        if (grid[x] === undefined) {
          grid[x] = [];
        }
        if (grid[x][y] === undefined) {
          grid[x][y] = new Set([data.id]);
        } else {
          // found a conflict, so remove it and remove this id from noConflicts
          grid[x][y].add(data.id);
          grid[x][y].forEach(id => {
            noConflicts.delete(id);
          })
        }
      }
    }
  });
  console.log("Part Two:", noConflicts.values().next().value);
}

//format of #1 @ 1,3: 4x4
function parse(line) {
  var lineArray = line.split(' ');
  // id is at index 0
  var id = lineArray[0].slice(1); // remove the #
  // '@' is at index 1
  // coordinates are at index 2
  var coordinates = lineArray[2].split(',');
  var xCoordinate = eval(coordinates[0]);
  var yCoordinate = eval(coordinates[1].slice(0, coordinates[1].length - 1));
  // size is at index 3
  var size = lineArray[3].split('x');
  var width = eval(size[0]);
  var height = eval(size[1]);
  return {
    id: id,
    x: xCoordinate,
    y: yCoordinate,
    width: width,
    height: height
  }
}

partOne('day03.txt');
partTwo('day03.txt');
