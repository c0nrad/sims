import * as mocha from "mocha";
import * as chai from "chai";

const expect = chai.expect;

import { Complex } from "./complex";
import { identity, Matrix } from "./matrix";
import { L_minus, L_x, L_y, L_z } from "./operator";

describe("operators", () => {
  it("LZ", () => {
    let S3z = new Matrix([
      [new Complex(1, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(0, 0), new Complex(-1, 0)],
    ]);

    let S4z = new Matrix([
      [new Complex(1.5, 0), new Complex(0, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(0.5, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(0, 0), new Complex(-0.5, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(0, 0), new Complex(0, 0), new Complex(-3 / 2, 0)],
    ]);

    expect(L_z(1).equals(S3z)).to.be.true;
    expect(L_z(1.5).equals(S4z)).to.be.true;
  });

  it("L_minus", () => {
    let S3Minus = new Matrix([
      [new Complex(0, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(1, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(1, 0), new Complex(0, 0)],
    ]).mulScalar(new Complex(Math.sqrt(2), 0));

    expect(L_minus(1).equals(S3Minus)).to.be.true;

    let S4Minus = new Matrix([
      [new Complex(0, 0), new Complex(0, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(Math.sqrt(3), 0), new Complex(0, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(2, 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(0, 0), new Complex(Math.sqrt(3), 0), new Complex(0, 0)],
    ]);

    expect(L_minus(1.5).equals(S4Minus)).to.be.true;
  });

  it("L_x", () => {
    let S3x = new Matrix([
      [new Complex(0, 0), new Complex(1, 0), new Complex(0, 0)],
      [new Complex(1, 0), new Complex(0, 0), new Complex(1, 0)],
      [new Complex(0, 0), new Complex(1, 0), new Complex(0, 0)],
    ]).mulScalar(new Complex(1 / Math.sqrt(2), 0));

    let S4x = new Matrix([
      [new Complex(0, 0), new Complex(Math.sqrt(3), 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(Math.sqrt(3), 0), new Complex(0, 0), new Complex(2, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(2, 0), new Complex(0, 0), new Complex(Math.sqrt(3), 0)],
      [new Complex(0, 0), new Complex(0, 0), new Complex(Math.sqrt(3), 0), new Complex(0, 0)],
    ]).mulScalar(new Complex(0.5, 0));

    expect(L_x(1).equals(S3x)).to.be.true;
    expect(L_x(1.5).equals(S4x)).to.be.true;
  });

  it("L_y", () => {
    let S3y = new Matrix([
      [new Complex(0, 0), new Complex(1, 0), new Complex(0, 0)],
      [new Complex(-1, 0), new Complex(0, 0), new Complex(1, 0)],
      [new Complex(0, 0), new Complex(-1, 0), new Complex(0, 0)],
    ]).mulScalar(new Complex(0, -1 / Math.sqrt(2)));

    let S4y = new Matrix([
      [new Complex(0, 0), new Complex(Math.sqrt(3), 0), new Complex(0, 0), new Complex(0, 0)],
      [new Complex(-Math.sqrt(3), 0), new Complex(0, 0), new Complex(2, 0), new Complex(0, 0)],
      [new Complex(0, 0), new Complex(-2, 0), new Complex(0, 0), new Complex(Math.sqrt(3), 0)],
      [new Complex(0, 0), new Complex(0, 0), new Complex(-Math.sqrt(3), 0), new Complex(0, 0)],
    ]).mulScalar(new Complex(0, -1 / 2));

    expect(L_y(1).equals(S3y)).to.be.true;
    expect(L_y(1.5).equals(S4y)).to.be.true;
  });
});
