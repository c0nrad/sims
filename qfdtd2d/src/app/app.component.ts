import { ChangeDetectorRef, Component, NgZone, ViewChild } from "@angular/core";
import { Complex } from "./complex";

@Component({
  selector: "app-root",
  template: `<div class="container-fluid">
    <div class="row">
      <div class="col-md-6">
        <canvas width="400" height="200" id="canvas" style="border: 1px solid"> </canvas>
      </div>
      <div class="col-md-6">
        <pre>{{ constants | json }}</pre>
        <!-- {{ psi_p }} -->
      </div>
    </div>
  </div> `,
  styles: [],
})
export class AppComponent {
  constants = {
    //display
    width: 400,
    height: 200,

    steps_per_update: 20,

    //simulation
    dx: 1.0,
    mass: 1.0,
    hbar: 1.0,

    //initial pulse
    sigma: 40,
    k0: Math.PI / 5,

    //potential
    v0: 5,

    // calculated
    c1: new Complex(0, 0),
    c2: new Complex(0, 0),
    dt: 0,
  };

  time = 0;

  psi_present = this.new_grid(this.constants.width, this.constants.height);
  psi_future = this.new_grid(this.constants.width, this.constants.height);
  psi_past = this.new_grid(this.constants.width, this.constants.height);
  potential = this.new_grid(this.constants.width, this.constants.height);
  psi_p = this.new_grid(this.constants.width, this.constants.height);
  max_p = 0;

  // optimization
  c2V = this.new_grid(this.constants.width, this.constants.height);

  constructor() {
    this.initializeConstants();
    this.initializePotential();
    this.initializePsi();
    this.normalize();
  }

  ngOnInit() {
    requestAnimationFrame(() => this.animateStep());
  }

  initializeConstants() {
    this.constants.dt = this.constants.hbar / ((2 * this.constants.hbar ** 2) / (this.constants.mass * this.constants.dx ** 2) + this.constants.v0);
    this.constants.c1 = new Complex(0, (this.constants.dt * this.constants.hbar) / 2 / this.constants.mass);
    this.constants.c2 = new Complex(0, -this.constants.dt / this.constants.hbar);
  }

  new_grid(width: number, height: number): Complex[][] {
    let out = new Array(width).fill(false).map(() => new Array(height).fill(new Complex(0, 0)));

    // delete me?
    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        out[x][y] = new Complex(0, 0);
      }
    }
    return out;
  }

  gaussian(x: number, y: number, a: number, b: number, sigma: number): number {
    return Math.exp(-((x - a) ** 2 + (y - b) ** 2) / (2 * sigma ** 2));
  }

  initializePotential() {
    for (let x = Math.round((2 * this.constants.width) / 3); x < Math.round((2 * this.constants.width) / 3) + 10; x++) {
      for (let y = 0; y < (3 * this.constants.height) / 10; y++) {
        this.potential[x][y] = new Complex(this.constants.v0, 0);
      }

      for (let y = (4 * this.constants.height) / 10; y < (6 * this.constants.height) / 10; y++) {
        this.potential[x][y] = new Complex(this.constants.v0, 0);
      }

      for (let y = (7 * this.constants.height) / 10; y < this.constants.height; y++) {
        this.potential[x][y] = new Complex(this.constants.v0, 0);
      }
    }

    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.c2V[x][y] = this.constants.c2.mul(this.potential[x][y]);
      }
    }
  }

  initializePsi() {
    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.psi_present[x][y] = new Complex(
          Math.cos(this.constants.k0 * x) * this.gaussian(x, y, this.constants.width / 4, this.constants.height / 2, this.constants.sigma),
          Math.sin(this.constants.k0 * x) * this.gaussian(x, y, this.constants.width / 4, this.constants.height / 2, this.constants.sigma)
        );

        this.psi_past[x][y] = new Complex(
          Math.cos(this.constants.k0 * x) * this.gaussian(x, y, this.constants.width / 4, this.constants.height / 2, this.constants.sigma),
          Math.sin(this.constants.k0 * x) * this.gaussian(x, y, this.constants.width / 4, this.constants.height / 2, this.constants.sigma)
        );
      }
    }
  }

  normalize() {
    let norm = 0;
    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.psi_p[x][y] = new Complex(this.psi_present[x][y].real ** 2 + this.psi_present[x][y].imag ** 2, 0);
        norm += this.psi_p[x][y].real;
      }
    }
    norm = Math.sqrt(norm);

    console.log("Norm", norm);

    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.psi_present[x][y] = this.psi_present[x][y].div(new Complex(norm, 0));
        this.psi_past[x][y] = this.psi_past[x][y].div(new Complex(norm, 0));
      }
    }
  }

  drawPotential() {
    var canvas = document.getElementById("canvas") as HTMLCanvasElement;
    var ctx = canvas!.getContext("2d")!;

    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        if (this.potential[x][y].real == 0) {
          continue;
        }
        let fill = Math.floor(255 - 255 * this.potential[x][y].real);
        ctx.fillStyle = `rgb(
          ${fill}, ${fill}, ${fill})`;
        ctx.fillRect(x, y, 1, 1); // fill in the pixel at (10,10)
      }
    }
  }

  drawPsi() {
    var canvas = document.getElementById("canvas") as HTMLCanvasElement;
    var ctx = canvas!.getContext("2d")!;

    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        // if (this.psi_p[x][y].real / this.max_p < 0.01) {
        //   continue;
        // }
        let fill = Math.floor(255 - 255 * (this.psi_p[x][y].real / this.max_p));
        ctx.fillStyle = `rgb(
          ${fill}, ${fill}, ${fill}, .5)`;
        ctx.fillRect(x, y, 1, 1); // fill in the pixel at (10,10)
      }
    }
  }

  animateStep() {
    for (let i = 0; i < this.constants.steps_per_update - 1; i++) {
      this.step(false);
    }
    this.step(true);

    this.drawPotential();
    this.drawPsi();

    requestAnimationFrame(() => {
      this.animateStep();
    });
  }

  gpuStep() {}

  step(updateP = true) {
    if (this.time % 100 == 0) {
      console.log(this.time);
    }

    let leapTemp = new Complex(0, 0);

    this.max_p = 0;
    for (let y = 1; y < this.constants.height - 1; y++) {
      for (let x = 1; x < this.constants.width - 1; x++) {
        let leapReal = this.psi_present[x + 1][y].real + this.psi_present[x][y + 1].real + this.psi_present[x - 1][y].real + this.psi_present[x][y - 1].real - this.psi_present[x][y].real * 4;
        let leapImag = this.psi_present[x + 1][y].imag + this.psi_present[x][y + 1].imag + this.psi_present[x - 1][y].imag + this.psi_present[x][y - 1].imag - this.psi_present[x][y].imag * 4;
        leapTemp.set(leapReal, leapImag);

        this.psi_future[x][y].set(
          leapTemp.mul(this.constants.c1).real - this.c2V[x][y].mul(this.psi_present[x][y]).real + this.psi_past[x][y].real,
          leapTemp.mul(this.constants.c1).imag - this.c2V[x][y].mul(this.psi_present[x][y]).imag + this.psi_past[x][y].imag
        );

        if (updateP) {
          this.psi_p[x][y].set(this.psi_future[x][y].real ** 2 + this.psi_future[x][y].imag ** 2, 0);
          if (this.max_p < this.psi_p[x][y].real) {
            this.max_p = this.psi_p[x][y].real;
          }
        }
      }
    }

    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.psi_past[x][y].set(this.psi_present[x][y].real, this.psi_present[x][y].imag);
        this.psi_present[x][y].set(this.psi_future[x][y].real, this.psi_future[x][y].imag);
      }
    }

    this.time += 1;
  }
}
