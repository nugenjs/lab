// strs = ['helly', 'hellione', 'helicopter'];
// output is 'he'
// 1 < len < 200, 0 < strs[i].len < 200
// will be only lowercase

const longestCommonPrefix = (strs: string[]) => {
  let prefix = '';

  if (strs.length === 1) {
    return strs[0];
  }

  let i = 0;
  while(true) {
    const currChar = strs[0]![i];
    for ( const str of strs) {
      if ( str[i] === undefined ) {
        return prefix;
      }
      if ( str[i] !== currChar ) {
        return prefix;
      }
    }
    prefix += currChar;
    i++;
  }
}


console.log(longestCommonPrefix(['helly', 'hellyione', 'helicopter']));

