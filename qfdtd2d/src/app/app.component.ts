import { ChangeDetectorRef, Component, NgZone, ViewChild } from "@angular/core";
import { GPU, IKernelRunShortcut, input, Input } from "gpu.js";

@Component({
  selector: "app-root",
  template: `<div class="container-fluid">
    <div class="row">
      <div class="col-md-6">
        <canvas width="{{ constants.width }}" height="{{ constants.height }}" id="canvas" style="border: 1px solid"> </canvas>
      </div>
      <div class="col-md-6">
        <p>FPS: {{ fps | number: "1.1-1" }}</p>
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
    width: 600,
    height: 250,

    steps_per_update: 20,

    //simulation
    dx: 1.0,
    mass: 1.0,
    hbar: 1.0,

    //initial pulse
    sigma: 40,
    k0: Math.PI / 3,

    //potential
    v0: 10,

    // calculated
    c1: 0,
    c2: 0,
    dt: 0,
  };

  time = 0;

  psi_present_r = this.new_grid(this.constants.width, this.constants.height);
  psi_present_i = this.new_grid(this.constants.width, this.constants.height);

  psi_future_r = this.new_grid(this.constants.width, this.constants.height);
  psi_future_i = this.new_grid(this.constants.width, this.constants.height);

  psi_past_r = this.new_grid(this.constants.width, this.constants.height);
  psi_past_i = this.new_grid(this.constants.width, this.constants.height);

  potential = this.new_grid(this.constants.width, this.constants.height);
  psi_p = this.new_grid(this.constants.width, this.constants.height);
  max_p = 0;

  // optimization
  c2V = this.new_grid(this.constants.width, this.constants.height);

  gpu!: GPU;
  leapStepKernel!: IKernelRunShortcut;

  start!: DOMHighResTimeStamp;
  fps!: number;

  forwardEulerStepWASM: any;

  constructor() {
    this.initializeConstants();
    this.initializePotential();
    this.initializePsi();
    this.initializeGPU();
    this.normalize();
  }

  async ngOnInit() {
    this.gpuStep();
    this.drawPotential();
    this.drawPsi();

    this.start = performance.now();
    requestAnimationFrame(() => this.animateStep());
  }

  initializeGPU() {
    this.gpu = new GPU();
    this.leapStepKernel = this.gpu.createKernel(
      function (psi_present_r: number[][], psi_present_i: number[][], psi_past_r: number[][], psi_past_i: number[][], c2V: number[][]): number {
        //@ts-ignore
        let c1 = this.constants.c1 as number;

        let x = this.thread.y;
        let y = this.thread.x;

        if (this.thread.z == 1) {
          return (
            c1 * (psi_present_r[x + 1][y] + psi_present_r[x][y + 1] - 4 * psi_present_r[x][y] + psi_present_r[x - 1][y] + psi_present_r[x][y - 1]) - c2V[x][y] * psi_present_r[x][y] + psi_past_i[x][y]
          );
        }

        if (this.thread.z == 0) {
          return (
            -c1 * (psi_present_i[x + 1][y] + psi_present_i[x][y + 1] - 4 * psi_present_i[x][y] + psi_present_i[x - 1][y] + psi_present_i[x][y - 1]) + c2V[x][y] * psi_present_i[x][y] + psi_past_r[x][y]
          );
        }
        return 0;
      },
      {
        output: [this.constants.height, this.constants.width, 2],
        constants: { c1: this.constants.c1 },
        optimizeFloatMemory: true,
        tactic: "speed",
        // argumentTypes: { psi_present_r: "Array", b: "Array(2)" },
      }
    );
  }

  initializeConstants() {
    this.constants.dt = this.constants.hbar / ((2 * this.constants.hbar ** 2) / (this.constants.mass * this.constants.dx ** 2) + this.constants.v0);
    this.constants.c1 = (this.constants.dt * this.constants.hbar) / 2 / this.constants.mass;
    this.constants.c2 = this.constants.dt / this.constants.hbar;
  }

  new_grid(width: number, height: number): Float32Array[] {
    let out = new Array(width).fill(0).map(() => new Float32Array(height).fill(0));
    return out;
  }

  gaussian(x: number, y: number, a: number, b: number, sigma: number): number {
    return Math.exp(-((x - a) ** 2 + (y - b) ** 2) / (2 * sigma ** 2));
  }

  initializePotential() {
    for (let x = Math.round((1 * this.constants.width) / 2); x < Math.round((1 * this.constants.width) / 2) + 5; x++) {
      for (let y = 0; y < (3 * this.constants.height) / 10; y++) {
        this.potential[x][y] = this.constants.v0;
      }

      for (let y = (4 * this.constants.height) / 10; y < (6 * this.constants.height) / 10; y++) {
        this.potential[x][y] = this.constants.v0;
      }

      for (let y = (7 * this.constants.height) / 10; y < this.constants.height; y++) {
        (this.potential[x][y] = this.constants.v0), 0;
      }
    }

    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.c2V[x][y] = this.constants.c2 * this.potential[x][y];
      }
    }
  }

  initializePsi() {
    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.psi_present_r[x][y] = Math.cos(this.constants.k0 * x) * this.gaussian(x, y, this.constants.width / 4, this.constants.height / 2, this.constants.sigma);
        this.psi_present_i[x][y] = Math.sin(this.constants.k0 * x) * this.gaussian(x, y, this.constants.width / 4, this.constants.height / 2, this.constants.sigma);

        this.psi_past_r[x][y] = Math.cos(this.constants.k0 * x) * this.gaussian(x, y, this.constants.width / 4, this.constants.height / 2, this.constants.sigma);
        this.psi_past_i[x][y] = Math.sin(this.constants.k0 * x) * this.gaussian(x, y, this.constants.width / 4, this.constants.height / 2, this.constants.sigma);
      }
    }
  }

  normalize() {
    let norm = 0;
    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.psi_p[x][y] = this.psi_present_r[x][y] ** 2 + this.psi_present_i[x][y] ** 2;
        norm += this.psi_p[x][y];
      }
    }
    norm = Math.sqrt(norm);

    console.log("Norm", norm);

    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        this.psi_present_r[x][y] /= norm;
        this.psi_present_i[x][y] /= norm;

        this.psi_past_r[x][y] /= norm;
        this.psi_past_i[x][y] /= norm;
      }
    }
  }

  drawPotential() {
    var canvas = document.getElementById("canvas") as HTMLCanvasElement;
    var ctx = canvas!.getContext("2d")!;

    ctx.fillStyle = "black";
    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        if (this.potential[x][y] == 0) {
          continue;
        }
        ctx.fillRect(x, y, 1, 1); // fill in the pixel at (10,10)
      }
    }
  }

  drawPsi() {
    var canvas = document.getElementById("canvas") as HTMLCanvasElement;
    var ctx = canvas!.getContext("2d")!;

    var imgData = ctx.createImageData(this.constants.width, this.constants.height);

    for (let y = 0; y < this.constants.height; y++) {
      for (let x = 0; x < this.constants.width; x++) {
        let fill = Math.floor(255 - Math.round(255 * (this.psi_p[x][y] / this.max_p)));

        let index = 4 * (this.constants.width * y + x);

        imgData.data[index + 0] = fill;
        imgData.data[index + 1] = fill;
        imgData.data[index + 2] = fill;
        imgData.data[index + 3] = 255;
      }
    }
    // console.log(imgData);
    ctx.putImageData(imgData, 0, 0);
  }

  animateStep() {
    for (let i = 0; i < this.constants.steps_per_update; i++) {
      this.gpuStep();
      // this.stepWASM(false);
    }
    // this.stepWASM(true);
    this.gpuStep(true);

    this.drawPsi();
    this.drawPotential();

    requestAnimationFrame(() => {
      this.animateStep();
    });
  }

  // flatten(a: Float32Array[]): number[] {
  //   return a.map();
  // }

  // get2D(x: number, y: number) {

  gpuStep(update_p = false) {
    let out = this.leapStepKernel(this.psi_present_r, this.psi_present_i, this.psi_past_r, this.psi_past_i, this.c2V) as Float32Array[][];
    [this.psi_future_r, this.psi_future_i] = out;

    this.stepCleanup(update_p);
  }

  step(update_p = false) {
    this.forwardEulerStep(
      this.psi_present_r,
      this.psi_present_i,
      this.psi_past_r,
      this.psi_past_i,
      this.c2V,
      this.constants.c1,
      this.constants.width,
      this.constants.height,

      //Return
      this.psi_future_r,
      this.psi_future_i
    );

    this.stepCleanup(update_p);
  }

  stepCleanup(update_p: boolean) {
    this.max_p = 0;

    this.psi_past_r = this.psi_present_r;
    this.psi_present_r = this.psi_future_r;

    this.psi_past_i = this.psi_present_i;
    this.psi_present_i = this.psi_future_i;

    if (update_p) {
      for (let y = 0; y < this.constants.height; y++) {
        for (let x = 0; x < this.constants.width; x++) {
          this.psi_p[x][y] = this.psi_present_r[x][y] ** 2 + this.psi_present_i[x][y] ** 2;

          if (this.psi_p[x][y] > this.max_p) {
            this.max_p = this.psi_p[x][y];
          }
        }
      }
      this.fps = (this.time / (performance.now() - this.start)) * 1000;
    }

    this.time += 1;
  }

  forwardEulerStep(
    psi_present_r: Float32Array[],
    psi_present_i: Float32Array[],
    psi_past_r: Float32Array[],
    psi_past_i: Float32Array[],
    c2V: Float32Array[],
    c1: number,
    width: number,
    height: number,
    //
    psi_future_r: Float32Array[],
    psi_future_i: Float32Array[]
  ) {
    for (let y = 1; y < height - 1; y++) {
      for (let x = 1; x < width - 1; x++) {
        psi_future_i[x][y] =
          c1 * (psi_present_r[x + 1][y] + psi_present_r[x][y + 1] - 4 * psi_present_r[x][y] + psi_present_r[x - 1][y] + psi_present_r[x][y - 1]) - c2V[x][y] * psi_present_r[x][y] + psi_past_i[x][y];
        psi_future_r[x][y] =
          -c1 * (psi_present_i[x + 1][y] + psi_present_i[x][y + 1] - 4 * psi_present_i[x][y] + psi_present_i[x - 1][y] + psi_present_i[x][y - 1]) + c2V[x][y] * psi_present_i[x][y] + psi_past_r[x][y];
      }
    }
  }
}
