const sum = require("./sum");

describe("sum", () => {
  test("dodaje dwie liczby", () => {
    expect(sum(2, 3)).toBe(5);
  });

  test("dodaje liczby ujemne", () => {
    expect(sum(-1, -4)).toBe(-5);
  });

  test("dodaje zero", () => {
    expect(sum(7, 0)).toBe(7);
  });
});
