import { Complex } from "./complex";
import { identity, Matrix } from "./matrix";
import { L_minus } from "./operator";

function print_decomposed(state: Matrix, s1: number, s2: number) {
  let i = 0;
  for (let m1 = s1; m1 >= -s1; m1 -= 1) {
    for (let m2 = s2; m2 >= -s2; m2 -= 1) {
      if (!state.at(0, i).equals(new Complex(0, 0))) {
        let sign = state.at(0, i).real > 0 ? 1 : -1;
        process.stdout.write(`${(sign * state.at(0, i).real * state.at(0, i).real).toPrecision(2)} |${m1} ${m2}>   `);
      }
      i++;
    }
  }
  console.log("");
}

// Gram-Schmidt
export function find_orthogonal_subspace(vectors: Matrix[]): Matrix {
  let out = Matrix.zero(1, vectors[0].height());
  for (let a of vectors) {
    for (let i = 0; i < a.height(); i++) {
      if (!a.at(0, i).equals(new Complex(0, 0))) {
        out.set(0, i, new Complex(1, 0));
      }
    }
  }

  for (let a of vectors) {
    let proj = a.mulScalar(out.adjoint().mulMatrix(a).at(0, 0));
    out = out.sub(proj).normalize();
  }
  return out;
}

let l1 = 1.5;
let particleOne = new Matrix([[new Complex(1, 0), new Complex(0, 0), new Complex(0, 0), new Complex(0, 0)]]).transpose();

let l2 = 1;
let particleTwo = new Matrix([[new Complex(1, 0), new Complex(0, 0), new Complex(0, 0)]]).transpose();

let lminus = L_minus(l1)
  .tensor(identity(2 * l2 + 1))
  .add(identity(2 * l1 + 1).tensor(L_minus(l2)));

let previous_subspace = [particleOne.tensor(particleTwo)];

// console.log(`l1=${l1} l2=${l2}`);
console.log(l1 + l2);
process.stdout.write(`|${l1 + l2} ${l1 + l2}> = `);
print_decomposed(previous_subspace[0], l1, l2);

for (let M = l1 + l2 - 1; M >= -l1 + -l2; M -= 1) {
  console.log(M);
  let current_subspace = [];
  for (let prev of previous_subspace) {
    current_subspace.push(lminus.mulMatrix(prev).normalize());
  }

  if (M > 0 && l1 + l2 != M) {
    current_subspace.push(find_orthogonal_subspace(current_subspace));
  }

  previous_subspace = current_subspace;
  if (M + 1 < 0) {
    previous_subspace.pop();
  }

  let i = 0;
  for (let prev of previous_subspace) {
    process.stdout.write(`|${l1 + l2 - i} ${M}> = `);
    print_decomposed(prev, l1, l2);
    i++;
  }
  // state = lminus.mulMatrix(state).normalize();

  // if (Math.abs(M) != math.abs(l1 + l2)) {
  // }
  // previous_subspace = [state];
  // state.print();
}
