// 3749: MMMDCCXLIX
// 58: LVIII
// 1994: MCMXCIV
// 1 <= 3999

// const intToRomanMap = [
//   { int: 1000, romanChar: "M" },
//   { int: 500, romanChar: "D" },
//   { int: 100, romanChar: "C" },
//   { int: 50, romanChar: "L" },
//   { int: 10, romanChar: "X" },
//   { int: 5, romanChar: "V" },
//   { int: 1, romanChar: "I" },
// ];

const romanToIntMap = new Map([
    ["M", 1000],
    ["D", 500],
    ["C", 100],
    ["L", 50],
    ["X", 10],
    ["V", 5],
    ["I", 1],
]);

const romanToInt = (roman: string) => {
    let intRes = 0;
    let i;

    for (i = 0; i < roman.length - 1; i++) {
        const currChar = roman[i]!;
        const nextChar = roman[i + 1]!;

        const currInt = romanToIntMap.get(currChar)!;
        const nextInt = romanToIntMap.get(nextChar)!;
        if (currInt < nextInt) {
            intRes += (nextInt - currInt);
            i++;
        } else {
            intRes += romanToIntMap.get(currChar) ?? 0;
        }
    }
    if (i < roman.length) {
        const currInt = romanToIntMap.get(roman[i]!)!;
        intRes += currInt;
    }

    return intRes;
};

console.log(romanToInt('MMMDCCXLIX'));
console.log(romanToInt('LVIII'));
console.log(romanToInt('MCMXCIV'));
