// The entry file of your WebAssembly module.

class SparseMatrix {
  data: number[][3];

  get(a: number, b: number) {}
}

export function add(a: i32, b: i32): i32 {
  return a + b;
}

export function forwardEulerStep(
  psi_present_r: number[][],
  psi_present_i: number[][],
  psi_past_r: number[][],
  psi_past_i: number[][],
  c2V: number[][],
  c1: number,
  width: number,
  height: number
): Float32Array[][] {
  let psi_future_r = new Array(width).fill(0).map(() => new Float32Array(height).fill(0));
  let psi_future_i = new Array(width).fill(0).map(() => new Float32Array(height).fill(0));

  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      psi_future_r[x][y] =
        c1 * (psi_present_r[x + 1][y] + psi_present_r[x][y + 1] - 4 * psi_present_r[x][y] + psi_present_r[x - 1][y] + psi_present_r[x][y - 1]) - c2V[x][y] * psi_present_r[x][y] + psi_past_i[x][y];
      psi_future_i[x][y] =
        -c1 * (psi_present_i[x + 1][y] + psi_present_i[x][y + 1] - 4 * psi_present_i[x][y] + psi_present_i[x - 1][y] + psi_present_i[x][y - 1]) + c2V[x][y] * psi_present_i[x][y] + psi_past_r[x][y];
    }
  }

  return [psi_future_r, psi_future_i];
}
