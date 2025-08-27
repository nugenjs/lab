const swap = (arr, x, y) => {
    [arr[x], arr[y]] = [arr[y], arr[x]];
};

const partition = (arr, left, right) => {
    const pivot = right--;
    //   process.stdout.write(` ${'  '.repeat(left)}${left}`);
    console.log(`PARTITION`);
    console.log(JSON.stringify(arr));
    console.log(` ${"  ".repeat(left)}${left}`);
    console.log(` ${"  ".repeat(right)}${right}`);
    console.log(` ${"  ".repeat(pivot)}${pivot}`);

    while (left <= right) {
        while (arr[left] < arr[pivot]) {
            left++;
            console.log(JSON.stringify(arr));
            console.log(`>${"  ".repeat(left)}${left}`);
            console.log(` ${"  ".repeat(right)}${right}`);
            console.log(` ${"  ".repeat(pivot)}${pivot}`);
        }
        while (arr[right] > arr[pivot]) {
            right--;
            console.log(JSON.stringify(arr));
            console.log(` ${"  ".repeat(left)}${left}`);
            console.log(`<${"  ".repeat(right)}${right}`);
            console.log(` ${"  ".repeat(pivot)}${pivot}`);
        }
        if (left <= right) {
            swap(arr, left, right);
            left++;
            right--;

            console.log(`SWAP`);
            console.log(JSON.stringify(arr));
            console.log(`>${"  ".repeat(left)}${left}`);
            console.log(`<${"  ".repeat(right)}${right}`);
            console.log(` ${"  ".repeat(pivot)}${pivot}`);
        }
    }
    swap(arr, left, pivot);
    console.log(`SWAP`);
    console.log(JSON.stringify(arr));
    return left;
};

const quickSort = (arr, left = 0, right = arr.length - 1) => {
    if (left < right) {
        const pivotIndex = partition(arr, left, right);
        quickSort(arr, left, pivotIndex - 1);
        quickSort(arr, pivotIndex + 1, right);
    }
    return arr;
};

// Example usage:
let nums = [7, 3, 1, 6, 0, 9, 2, 8];
console.log(quickSort(nums)); // [0, 1, 2, 3, 7, 8, 10]

console.log("HELO");
