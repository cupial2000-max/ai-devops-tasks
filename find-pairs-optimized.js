function findPairs(arr, targetSum) {
  const seen = new Map();
  const pairs = [];

  for (let j = 0; j < arr.length; j++) {
    const need = targetSum - arr[j];
    const count = seen.get(need) || 0;

    for (let k = 0; k < count; k++) {
      pairs.push([need, arr[j]]);
    }

    seen.set(arr[j], (seen.get(arr[j]) || 0) + 1);
  }

  return pairs;
}
