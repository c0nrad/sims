import { ChangeDetectorRef, Component, NgZone, ViewChild } from "@angular/core";
import { BaseChartDirective } from "ng2-charts";

@Component({
  selector: "app-root",
  template: `<div class="container-fluid">
    <div class="row">
      <div class="col-md-6">
        <canvas
          baseChart
          width="400"
          height="400"
          [data]="chartData"
          [type]="'line'"
          [options]="{
            animation: false,
            datasets: {
              line: {
                pointRadius: 0
              }
            },
            elements: {
              point: {
                radius: 0
              }
            },
            scales: {
              y: {
                type: 'linear',
                min: -0.05,
                max: 0.05
              }
            }
          }"
        >
        </canvas>
      </div>
      <div class="col-md-6"></div>
    </div>
  </div> `,
  styles: [],
})
export class AppComponent {
  @ViewChild(BaseChartDirective) chart!: BaseChartDirective;

  title = "qfdtd1d";

  GridSize = 1200;

  chartData: any = {
    datasets: [],
    labels: [],
  };

  PlotSkip = 20;
  time = 0;
  dx = 1.0;
  mass = 1.0;
  hbar = 1;

  X = new Array<number>(this.GridSize).fill(0);
  V = new Array<number>(this.GridSize).fill(0);
  indexes = Array.from(Array(this.GridSize).keys());

  sigma = 40;
  x0 = this.GridSize / 2 - 5 * this.sigma;
  k0 = Math.PI / 20;
  v0 = 0.01;

  E = (this.hbar ** 2 / 2.0 / this.mass) * (this.k0 ** 2 + 0.5 / this.sigma ** 2);

  dt = this.hbar / ((2 * this.hbar ** 2) / (this.mass * this.dx ** 2) + this.v0);
  c1 = (this.hbar * this.dt) / (this.mass * this.dx ** 2);
  c2 = (2 * this.dt) / this.hbar;

  c2V = new Array<number>(this.GridSize).fill(0);

  psi_r_past = new Array<number>(this.GridSize).fill(0);
  psi_r_present = new Array<number>(this.GridSize).fill(0);
  psi_r_future = new Array<number>(this.GridSize).fill(0);

  psi_i_past = new Array<number>(this.GridSize).fill(0);
  psi_i_present = new Array<number>(this.GridSize).fill(0);
  psi_i_future = new Array<number>(this.GridSize).fill(0);

  psi_p = new Array<number>(this.GridSize).fill(0);

  constructor() {
    this.initializePotential();
    this.initializePsi();
    this.normalize();

    this.chartData = {
      datasets: [
        { data: this.psi_p, label: "psi^2" },
        { data: this.V, label: "Potential" },
      ],
      labels: this.indexes,
    };

    requestAnimationFrame(() => this.animateStep());

    // setInterval(() => {
    //   this.step();
    // }, 1);
  }

  gaussian(x: number, t: number, sigma: number): number {
    return Math.exp(-((x - t) ** 2) / (2 * sigma ** 2));
  }

  initializePotential() {
    for (let i = this.GridSize / 2; i < (3 * this.GridSize) / 4 - 275; i++) {
      this.V[i] = this.v0;
      this.c2V[i] = this.v0 * this.c2;
    }
  }

  initializePsi() {
    for (let x = 0; x < this.GridSize; x++) {
      this.psi_r_present[x] = Math.cos(this.k0 * x) * this.gaussian(x, this.x0, this.sigma);
      this.psi_i_present[x] = Math.sin(this.k0 * x) * this.gaussian(x, this.x0, this.sigma);
      this.psi_r_past[x] = Math.cos(this.k0 * x) * this.gaussian(x, this.x0, this.sigma);
      this.psi_i_past[x] = Math.sin(this.k0 * x) * this.gaussian(x, this.x0, this.sigma);
    }
  }

  normalize() {
    for (let x = 0; x < this.GridSize; x++) {
      this.psi_p[x] = this.psi_r_present[x] ** 2 + this.psi_i_present[x] ** 2;
    }

    let P = this.psi_p.reduce((sum: number, a: number) => sum + a, 0);

    for (let x = 0; x < this.GridSize; x++) {
      this.psi_r_present[x] /= Math.sqrt(P);
      this.psi_i_present[x] /= Math.sqrt(P);
      this.psi_r_past[x] /= Math.sqrt(P);
      this.psi_i_past[x] /= Math.sqrt(P);
    }
  }

  animateStep() {
    for (let i = 0; i < this.PlotSkip; i++) {
      this.step();
    }

    this.chartData.datasets[0].data = this.psi_p;
    this.chart.chart!.update();

    requestAnimationFrame(() => {
      this.animateStep();
    });
  }

  step() {
    for (let x = 1; x < this.GridSize - 1; x++) {
      this.psi_i_future[x] = this.c1 * (this.psi_r_present[x + 1] - 2 * this.psi_r_present[x] + this.psi_r_present[x - 1]) - this.c2V[x] * this.psi_r_present[x] + this.psi_i_past[x];
      this.psi_r_future[x] = -this.c1 * (this.psi_i_present[x + 1] - 2 * this.psi_i_present[x] + this.psi_i_present[x - 1]) + this.c2V[x] * this.psi_i_present[x] + this.psi_r_past[x];

      this.psi_p[x] = 1 * (this.psi_r_future[x] ** 2 + this.psi_i_future[x] ** 2);
    }

    for (let x = 0; x < this.GridSize; x++) {
      this.psi_r_past[x] = this.psi_r_present[x];
      this.psi_r_present[x] = this.psi_r_future[x];

      this.psi_i_past[x] = this.psi_i_present[x];
      this.psi_i_present[x] = this.psi_i_future[x];
    }

    this.time += 1;
  }
}
