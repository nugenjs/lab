// I 1, V 5, X 10, L 50, C 100, D 500, M 1000
// not start with 4 or 9, 
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
            if (firstDigit === '4' || firstDigit === '9') {
                console.log('HEREG OT');
            }

            let div = ~~(num / romanMapInt);
            let remainder = num % romanMapInt;


            console.log(`romanMapInt: ${romanMapInt}, romanMapChar: ${romanMapChar},       div ${div}, remainder ${remainder}`)
            num = remainder;
            romanRes += `${romanMapChar.repeat(div)}`;
        }
    }

    return romanRes;
}


console.log(intToRoman(3749))
