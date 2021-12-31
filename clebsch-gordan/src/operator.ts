import { Complex } from "./complex";
import { Matrix } from "./matrix";

export function L_z(l: number): Matrix {
  let out = Matrix.zero(2 * l + 1, 2 * l + 1);
  let i = 0;
  for (let m = l; m >= -l; m -= 1) {
    out.set(i, i, new Complex(m, 0));
    i++;
  }
  return out;
}

export function L_plus(l: number): Matrix {
  let out = Matrix.zero(2 * l + 1, 2 * l + 1);
  let i = 0;
  for (let m_old = -l; m_old <= l - 1; m_old++) {
    let coefficient = Math.sqrt(l * (l + 1) - m_old * (m_old + 1));
    out.set(2 * l - i, 2 * l - 1 - i, new Complex(coefficient, 0));
    i++;
  }
  return out;
}

export function L_minus(l: number): Matrix {
  return L_plus(l).transpose();
}

export function L_x(l: number): Matrix {
  return L_plus(l).add(L_minus(l)).mulScalar(new Complex(0.5, 0));
}

export function L_y(l: number): Matrix {
  return L_plus(l)
    .sub(L_minus(l))
    .mulScalar(new Complex(0, -1 / 2));
}
