'use strict';
const fs = require('fs');
const MILLISECONDS_IN_DAY = 86400000;

// Part One: What minute does that guard spend asleep the most?
function partOne(fileName) {
  let contents = fs.readFileSync(fileName, 'utf8');
  const lines = contents.split(/\r?\n/);
  let shiftMap = new Map();
  lines.forEach(line => {
    organizeByDate(line, shiftMap);
  });
  //console.log("shifts:", shiftMap);

  // find the guard who slept the most
  let guardMap = new Map();
  for (let shift of shiftMap.values()) {
    let guardEntry = guardMap.has(shift.id) ? guardMap.get(shift.id) : {
      minutesAsleep: 0
    };
    if (shift.sleeps !== undefined) {
      let sortedSleeps = shift.sleeps.sort((a, b) => a - b);
      let sortedWakes = shift.wakes.sort((a, b) => a - b);
      for (let i = 0; i < sortedSleeps.length; i++) {
        guardEntry.minutesAsleep += sortedWakes[i] - sortedSleeps[i];
      }
    }
    guardMap.set(shift.id, guardEntry);
  }
  //console.log(guardMap);

  let biggestSleeper = ['', {
    minutesAsleep: 0
  }];
  for (let guardEntry of guardMap.entries()) {
    if (guardEntry[1].minutesAsleep > biggestSleeper[1].minutesAsleep) {
      biggestSleeper = guardEntry;
    }
  }
  //console.log("Our biggest sleeper:", biggestSleeper);
  let biggestSleeperId = biggestSleeper[0];

  let minuteArray = [];
  for (let i = 0; i < 60; i++) {
    // prefill with zeros
    minuteArray[i] = 0;
  }
  for (let shift of shiftMap.values()) {
    if (shift.id === biggestSleeperId && shift.sleeps !== undefined) {
      let sortedSleeps = shift.sleeps.sort((a, b) => a - b);
      let sortedWakes = shift.wakes.sort((a, b) => a - b);
      for (let i = 0; i < sortedSleeps.length; i++) {
        for (let idx = sortedSleeps[i]; idx < sortedWakes[i]; idx++) {
          minuteArray[idx]++;
        }
      }
    }
  }
  let trackedMinute = 0;
  let largestNumberOfMinutes = 0;
  for (let i = 0; i < minuteArray.length; i++) {
    //console.log("Minute " + i, minuteArray[i]);
    if (minuteArray[i] > largestNumberOfMinutes) {
      trackedMinute = i;
      largestNumberOfMinutes = minuteArray[i];
    }
  }
  //console.log("The minute is:", trackedMinute);
  console.log("Part One:", biggestSleeperId * trackedMinute);
}

// Part Two: Of all guards, which guard is most frequently asleep on the same minute?
function partTwo(fileName) {
  let contents = fs.readFileSync(fileName, 'utf8');
  const lines = contents.split(/\r?\n/);
  let shiftMap = new Map();
  lines.forEach(line => {
    organizeByDate(line, shiftMap);
  });
  //console.log("shifts:", shiftMap);

  let minuteMap = new Map();
  // make a structure that looks like this for each minute
  // 0: { ids: ['11', '12', '13', '12'], winner: ['12', 2] }
  for (let i = 0; i < 60; i++) {
    minuteMap.set(i, {
      ids: []
    });
  }
  for (let shift of shiftMap.values()) {
    if (shift.sleeps !== undefined) {
      let sortedSleeps = shift.sleeps.sort((a, b) => a - b);
      let sortedWakes = shift.wakes.sort((a, b) => a - b);
      for (let i = 0; i < sortedSleeps.length; i++) {
        for (let idx = sortedSleeps[i]; idx < sortedWakes[i]; idx++) {
          minuteMap.get(idx).ids.push(shift.id);
        }
      }
    }
  }
  //console.log(minuteMap);

  let frequency = {
    id: '',
    times: 0
  };

  for (let minute of minuteMap.keys()) {
    let summary = minuteMap.get(minute).ids.reduce(function (acc, curr) {
      if (typeof acc[curr] == 'undefined') {
        acc[curr] = 1;
      } else {
        acc[curr] += 1;
      }
      return acc;
    }, {});
    //console.log("Minute " + minute, summary);
    for (let guardInMinute in summary) {
      if (summary.hasOwnProperty(guardInMinute) && summary[guardInMinute] > frequency.times) {
        frequency = {
          id: guardInMinute,
          minute: minute,
          times: summary[guardInMinute]
        };
      }
    }
  }
  //console.log("Frequency:", frequency);
  console.log("Part Two:", frequency.id * frequency.minute);

}

function organizeByDate(line, shiftMap) {
  const matchGroups = line.match(/\[(.*) (.*)\] (.*)/);
  let date = Date.parse(matchGroups[1]),
    time = matchGroups[2],
    hour = parseInt(time.split(':')[0]),
    minutes = parseInt(time.split(':')[1]),
    info = matchGroups[3];
  if (hour === 23) {
    // make it the next day because the only thing that happens at 11pm is a
    // guard shifts starting
    date += MILLISECONDS_IN_DAY;
  }
  // see if this is an ID
  let idMatches = info.match(/Guard #([0-9]+)/);
  let shift = shiftMap.has(date) ? shiftMap.get(date) : {};
  if (idMatches !== null) {
    shift.id = idMatches[1];
  } else if (info.match(/wakes/) !== null) {
    shift.wakes ? shift.wakes.push(minutes) : shift.wakes = [minutes];
  } else {
    // must be falls asleep
    shift.sleeps ? shift.sleeps.push(minutes) : shift.sleeps = [minutes];
  }
  shiftMap.set(date, shift);
}

partOne('day04.txt');
partTwo('day04.txt');