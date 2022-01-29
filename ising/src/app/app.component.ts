import { Component, ViewChild } from "@angular/core";
import { EnergyPlotComponent } from "./components/energy-plot/energy-plot.component";
import { MagnetismPlotComponent } from "./components/magnetism-plot/magnetism-plot.component";

@Component({
  selector: "app-root",
  template: `
    <div>
      <h3>2D Ising</h3>
      <div style="display: flex; flex-direction: row">
        <div>
          <canvas id="canvas" width="500" height="500" style="border: 1px solid"> </canvas>
        </div>
        <div>
          <p>Step: {{ time }}</p>
          <!-- <p>Energy: {{ prevEnergy }}</p> -->
          <!-- <p>Magnetism: {{ prevMagnetism }}</p> -->

          <p>J = 1</p>
          <input type="range" min="0.01" max="10" step=".01" [(ngModel)]="T" />{{ T }}
          <p>Critical Is 2.269</p>

          <app-energy-plot #energyPlot style="border: 1px solid"></app-energy-plot>

          <app-magnetism-plot #magnetismPlot></app-magnetism-plot>
        </div>
      </div>
    </div>
  `,
  styles: [],
})
export class AppComponent {
  @ViewChild("energyPlot") energyPlot!: EnergyPlotComponent;
  @ViewChild("magnetismPlot") magnetismPlot!: MagnetismPlotComponent;

  cellWidth = 5;
  ctx!: CanvasRenderingContext2D;

  T = 2;

  gridSize = 100;
  grid: number[][] = [];

  time: number = 0;

  prevEnergy = 0;
  prevMagnetism = 0;

  constructor() {
    this.grid = this.makeGrid();
    this.prevEnergy = this.calculateEnergy();
    this.prevMagnetism = this.calculateMagnetism();
  }

  calculateEnergy(): number {
    let out = 0;
    for (let i = 0; i < this.gridSize - 1; i++) {
      for (let sweep = 0; sweep < this.gridSize; sweep++) {
        out += -this.grid[i][sweep] * this.grid[i + 1][sweep];
        out += -this.grid[sweep][i] * this.grid[sweep][i + 1];
      }
    }
    return out;
  }

  calculateMagnetism(): number {
    let out = 0;
    for (let y = 0; y < this.gridSize; y++) {
      for (let x = 0; x < this.gridSize; x++) {
        out += this.grid[x][y];
      }
    }
    return out;
  }

  makeGrid(): number[][] {
    let out: number[][] = [];
    for (let x = 0; x < this.gridSize; x++) {
      let row = [];
      for (let i = 0; i < this.gridSize; i++) {
        row.push(Math.random() < 0.5 ? -1 : 1);
      }
      out.push(row);
    }
    return out;
  }

  ngAfterViewInit() {
    var c = <HTMLCanvasElement>document.getElementById("canvas")!;
    this.ctx = c.getContext("2d")!;
    this.drawGrid();

    this.loop();
  }

  loop() {
    setTimeout(() => {
      for (let i = 0; i < 10000; i++) {
        this.step();
      }

      if (this.calculateEnergy() != this.prevEnergy) {
        alert("invalud energy");
      }

      if (this.calculateMagnetism() != this.prevMagnetism) {
        alert("invalid magnetism");
      }

      // this.prevEnergies.push(this.prevEnergy);
      // this.prevSteps.push(this.time);

      this.energyPlot.addPoint(this.time, this.prevEnergy);
      this.magnetismPlot.addPoint(this.time, this.prevMagnetism);

      // this.prevEnergies = this.prevEnergies.slice(-20);
      // this.prevSteps = this.prevSteps.slice(-20);

      // console.log(this.prevEnergies);

      this.loop();
    }, 0);
  }

  drawGrid() {
    for (let y = 0; y < this.gridSize; y++) {
      for (let x = 0; x < this.gridSize; x++) {
        let value = this.grid[y][x];
        this.drawSpot(x, y, value);
      }
    }
  }

  drawSpot(x: number, y: number, value: number) {
    this.ctx.beginPath();

    if (this.grid[y][x] == 1) {
      this.ctx.fillStyle = `black`;
    } else if (this.grid[y][x] == -1) {
      this.ctx.fillStyle = "white";
    } else {
      this.ctx.fillStyle = "red";
    }

    this.ctx.rect(this.cellWidth * x, this.cellWidth * y, this.cellWidth, this.cellWidth);
    this.ctx.fill();
  }

  step() {
    this.time += 1;

    let x = Math.floor(Math.random() * this.gridSize);
    let y = Math.floor(Math.random() * this.gridSize);

    this.set(x, y, this.at(x, y) * -1);

    let dE = this.calculateChangeInEnergy(x, y);
    let newEnergy = this.prevEnergy + this.calculateChangeInEnergy(x, y);

    if (newEnergy < this.prevEnergy || Math.random() < Math.exp(-dE / this.T)) {
      this.prevEnergy = newEnergy;
      this.prevMagnetism += 2 * this.at(x, y);
      this.drawSpot(x, y, this.at(x, y));
    } else {
      this.set(x, y, this.at(x, y) * -1);
    }
  }

  calculateChangeInEnergy(x: number, y: number): number {
    let out = 0;
    out -= this.at(x, y) * this.at(x - 1, y);
    out -= this.at(x, y) * this.at(x + 1, y);
    out -= this.at(x, y) * this.at(x, y - 1);
    out -= this.at(x, y) * this.at(x, y + 1);

    return 2 * out;
  }

  at(x: number, y: number): number {
    if (x < 0 || x >= this.gridSize) {
      return 0;
    }

    if (y < 0 || y >= this.gridSize) {
      return 0;
    }

    return this.grid[y][x];
  }

  set(x: number, y: number, v: number) {
    if (this.at(x, y) == 0) {
      alert("invalid coords" + y + ", " + x);
    }

    this.grid[y][x] = v;
  }
}
