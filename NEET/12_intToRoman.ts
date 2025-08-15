// I 1, V 5, X 10, L 50, C 100, D 500, M 1000
// not start with 4 or 9, normal
// start with 4 or 9, use subtractive (e.g. 40 = XL, 900 = CM)
// only powers of 10 can be consecutive, maximum of 3 times.
//  
// 3749: MMMDCCXLIX
// 58: LVIII
// 1994: MCMXCIV
// 1 <= 3999

const intToRomanMap = [
    {int: 1000, romanChar: 'M'},
    {int: 500 , romanChar: 'D'},
    {int: 100 , romanChar: 'C'},
    {int: 50, romanChar: 'L'},
    {int: 10, romanChar: 'X'},
    {int: 5, romanChar: 'V'},
    {int: 1, romanChar: 'I'},
];


const intToRoman = (num: number) => {
    let romanRes = '';
    for (let i = 0; i < intToRomanMap.length && num > 0; i++) {
        const romanMapInt = intToRomanMap[i]?.int!;
        const romanMapChar = intToRomanMap[i]?.romanChar!;
        if (num > romanMapInt) {
            const firstDigit = num.toString()[0];
            let remainder = 0;
            if (firstDigit === '9') {
                // Use 10xxx - 1xxx to get 9xxx
                let {int: tensMapInt, romanChar: tensMapChar} = intToRomanMap[i-1]!;
                let {int: onesMapInt, romanChar: onesMapChar} = intToRomanMap[i+1]!;
                remainder = num - (tensMapInt - onesMapInt);
                romanRes += `${onesMapChar}${tensMapChar}`
            }
            else if (firstDigit === '4') {
                // Use 5xxx - 1xxx to get 4xxx
                let {int: fivesMapInt, romanChar: fivesMapChar} = intToRomanMap[i-1]!;
                remainder = num - (fivesMapInt - romanMapInt);
                romanRes += `${romanMapChar}${fivesMapChar}`
            } else {
                let div = ~~(num / romanMapInt);
                remainder = num % romanMapInt;
            
                romanRes += `${romanMapChar.repeat(div)}`;
            }
            num = remainder;
        }
    }

    return romanRes;
}


console.log(intToRoman(3749))
