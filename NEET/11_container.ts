import * as fs from 'fs';


const bucket = ( pillars: number[] = [], n = 0 ) => {
    if (pillars.length < 2) {
        return;
    }

    let lastIndex = n - 1;
    let verstappen = 0;

    for (let leftPtr = 0;leftPtr < lastIndex; leftPtr++) {

        for (let ritePtr = leftPtr + 1; ritePtr <= lastIndex; ritePtr++) {
            let leftVal = pillars[leftPtr]!;
            let riteVal = pillars[ritePtr]!;
            let max = smallerValue(leftVal, riteVal) * (ritePtr - leftPtr);
            verstappen = largerValue(max, verstappen);
        }
    }
    return verstappen;
}

const smallerValue = (a: number,b: number) => a < b ? a : b;
const largerValue = (a: number,b: number) => a > b ? a : b;

// 5         #
// 4  #   # ##
// 3  # # ####
// 2  # # ####
// 1 ###############
//  0123456789012345
const pillars = [0,1,4,1,3,1,4,3,4,5,1,1,1,1,1,1];
const n = pillars.length; // 10 in this example
console.log(`1: bucket = ${bucket(pillars, n)}`)

// 6  #   #
// 5  #   #   
// 4  #   # 
// 3  # # #
// 2  # # ###      #
// 1 ###############
//  0123456789012345
const pillars2 = [0,1,4,1,3,1,4,3,4,5,1,1,1,1,1,1];
const n2 = pillars2.length; // 10 in this example
console.log(`2: bucket = ${bucket(pillars2, n2)}`)



// 6  #  #
// 5  #  #   
// 4  #  #  
// 3  # ## 
// 2  # ## ##      #
// 1 ###############
//  0123456789012345
const pillars3 = [0,1,4,1,3,4,1,3,5,4,1,1,1,1,1,1];
const n3 = pillars3.length; // 10 in this example
console.log(`3: bucket = ${bucket(pillars3, n3)}`)
