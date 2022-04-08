let constants = {
  eps0: 8.8541e-12,
  mu0: 1.25663e-6,
  c0: 299792458,

  width: 1000,
};

let Ex = new Array(constants.width);
let Hz = new Array(constants.width);

let Ex_prev = new Array(constants.width);
let Hz_prev = new Array(constants.width);

let dx = 200e-9 / 20;
let dt = dx / constants.c0;

function source(t: number) {
  let lambda_0 = 550e-9;
  let w0 = (2 * Math.PI * constants.c0) / lambda_0;
  let tau = 300;
  let t0 = tau * 3;

  return Math.exp((-1 * (t - t0) ** 2) / tau ** 2) * Math.sin(w0 * t * dt);
}
