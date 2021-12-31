import * as mocha from "mocha";
import * as chai from "chai";

const expect = chai.expect;

import { Complex } from "./complex";
import { identity, Matrix } from "./matrix";
import { L_minus, L_x, L_y, L_z } from "./operator";
import { find_orthogonal_subspace } from "./spin";

describe("spin", () => {
  it("orthogonal", () => {
    let a = new Matrix([
      [new Complex(0, 0)],
      [new Complex(0.6324555320336759, 0)],
      [new Complex(0, 0)],
      [new Complex(0.7745966692414833, 0)],
      [new Complex(0, 0)],
      [new Complex(0, 0)],
      [new Complex(0, 0)],
      [new Complex(0, 0)],
      [new Complex(0, 0)],
      [new Complex(0, 0)],
      [new Complex(0, 0)],
      [new Complex(0, 0)],
    ]);

    expect(
      find_orthogonal_subspace([a]).equals(
        new Matrix([
          [new Complex(0, 0)],
          [new Complex(0.7745966692414833, 0)],
          [new Complex(0, 0)],
          [new Complex(-0.6324555320336759, 0)],
          [new Complex(0, 0)],
          [new Complex(0, 0)],
          [new Complex(0, 0)],
          [new Complex(0, 0)],
          [new Complex(0, 0)],
          [new Complex(0, 0)],
          [new Complex(0, 0)],
          [new Complex(0, 0)],
        ])
      )
    ).to.be.true;

    // expect(L_z(1).equals(S3z)).to.be.true;
    // expect(L_z(1.5).equals(S4z)).to.be.true;
  });
});
