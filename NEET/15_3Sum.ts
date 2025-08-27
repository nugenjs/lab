// int array nums, return all triplets `[nums[i], nums[j], nums[k]]`
// such that i != j. i != k, j != k, and [nums[i], nums[j], nums[k]] == 0
// 3 <= len <= 3000
// 10^5
// can be unordered

// [-2. -1, -1, 1, 2, 3]
// [-1,-1, 2], [-2, -1, 3]

// [-2. -1, -1, 0, 0, 0, 0, 1, 2, 3]
// [-2, 0, 2], [-2, 0, 2], [-2, 0, 2], [-2, 0, 2] [-1,-1, 2], [-2, -1, 3]

// return tuple [a, b, c]
// hypothesis, brute force first two numbers (a, b), 
// third number is gotten by `-(a + b)`, and check dictionary if value exist
// -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5
//              1   2     1  1  1




const threeSum = (nums: number[]) => {
  console.log(nums)
  // Key = number, value = frequency of occurance
  const numsDict = new Map();
  for (let i = 0; i < nums.length; i++) {
    const key = nums[i];
    const value = numsDict.get(key);
    console.log(`key = ${key}`)
    if (value === undefined) {
      numsDict.set(nums[i], 1);
    } else {
      numsDict.set(nums[i], value + 1);
    }
  }

  console.log(numsDict);

  for (let a of numsDict) {
    console.log(`a = ${a}`);
  }

  

  return;
}


threeSum([-2, -1, -1, 1, 2, 3]);