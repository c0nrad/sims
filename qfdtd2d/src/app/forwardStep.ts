// asc fib.ts --out fib.wasm --optimize

export function forwardEulerStep(
  psi_present_r: Float32Array[],
  psi_present_i: Float32Array[],
  psi_past_r: Float32Array[],
  psi_past_i: Float32Array[],
  c2V: Float32Array[],
  c1: f32,
  width: number,
  height: number,
  psi_future_r: Float32Array[],
  psi_future_i: Float32Array[]
): void {
  // console.log("Do I even start?");
  // console.log("");
  for (let y = 1; y < height - 1; y++) {
    for (let x = 1; x < width - 1; x++) {
      console.log(x.toString());
      psi_future_i[x][y] =
        c1 * (psi_present_r[x + 1][y] + psi_present_r[x][y + 1] - 4 * psi_present_r[x][y] + psi_present_r[x - 1][y] + psi_present_r[x][y - 1]) - c2V[x][y] * psi_present_r[x][y] + psi_past_i[x][y];
      psi_future_r[x][y] =
        -c1 * (psi_present_i[x + 1][y] + psi_present_i[x][y + 1] - 4 * psi_present_i[x][y] + psi_present_i[x - 1][y] + psi_present_i[x][y - 1]) + c2V[x][y] * psi_present_i[x][y] + psi_past_r[x][y];
    }
  }
}
