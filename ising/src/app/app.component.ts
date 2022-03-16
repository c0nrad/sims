import { Component, ViewChild } from "@angular/core";
import { EnergyPlotComponent } from "./components/energy-plot/energy-plot.component";
import { MagnetismPlotComponent } from "./components/magnetism-plot/magnetism-plot.component";
import { SimplePlotComponent } from "./components/simple-plot/simple-plot.component";

@Component({
  selector: "app-root",
  template: `
    <div class="container-fluid">
      <h3>2D Ising</h3>
      <div>
        <div class="float-start">
          <canvas id="canvas" width="512" height="512" style="border: 1px solid"> </canvas>

          <div>
            <button (click)="reset()">Reset Grid</button>

            <p>Step: {{ time | number }}</p>
            <p>Energy: {{ prevEnergy }}</p>
            <p>Magnetism: {{ prevMagnetism }}</p>
            <p>Correlation: {{ prevCorrelation }}</p>
            <p>J = 1</p>

            <select [(ngModel)]="gridSize" (change)="setupGrid()">
              <option *ngFor="let i of [32, 64, 128, 256, 512, 1024]" [ngValue]="i">{{ i }}</option>
            </select>

            <input type="range" min="0.01" max="10" step=".01" [(ngModel)]="T" />{{ T }}
            <button (click)="T = 2.269">Go Critical</button>
            <p>Critical Is 2.269</p>
          </div>
        </div>

        <div>
          <app-simple-plot [title]="'Energy'" #energyPlot></app-simple-plot>

          <!-- <app-magnetism-plot #magnetismPlot></app-magnetism-plot> -->

          <app-simple-plot [title]="'Magnetism'" #magnetismPlot></app-simple-plot>

          <app-simple-plot [title]="'Neighbor Correlation'" #correlationPlot></app-simple-plot>
          <button (click)="clear()">Clear Charts</button>
        </div>
      </div>
    </div>
  `,
  styles: [],
})
export class AppComponent {
  @ViewChild("energyPlot") energyPlot!: EnergyPlotComponent;
  @ViewChild("magnetismPlot") magnetismPlot!: MagnetismPlotComponent;
  @ViewChild("correlationPlot") correlationPlot!: SimplePlotComponent;

  cellWidth = 4;
  ctx!: CanvasRenderingContext2D;

  T = 2;

  gridSize = 128;
  grid: number[][] = [];

  time: number = 0;

  prevEnergy = 0;
  prevMagnetism = 0;
  prevCorrelation = 0;

  constructor() {
    this.T = 2;
    this.time = 0;
    this.setupGrid();
  }

  reset() {
    this.time = 0;
    this.setupGrid();
    this.clear();
  }

  setupGrid() {
    console.log(this.gridSize);
    this.cellWidth = 512 / this.gridSize;
    this.grid = this.makeGrid();

    this.prevEnergy = this.calculateEnergy();
    this.prevMagnetism = this.calculateMagnetism();
  }

  calculateEnergy(): number {
    let out = 0;
    for (let i = 0; i < this.gridSize; i++) {
      for (let sweep = 0; sweep < this.gridSize; sweep++) {
        out += -this.at(i, sweep) * this.at(i + 1, sweep);
        out += -this.at(sweep, i) * this.at(sweep, i + 1);
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
    return out / (this.gridSize * this.gridSize);
  }

  calculateCorrelation(): number {
    let out = 0;
    for (let y = 0; y < this.gridSize; y++) {
      for (let x = 0; x < this.gridSize; x++) {
        let spotCount = 0;
        if (this.at(x, y) * this.at(x + 1, y) == 1) {
          spotCount += 1;
        }

        if (this.at(x, y) * this.at(x - 1, y) == 1) {
          spotCount += 1;
        }
        if (this.at(x, y) * this.at(x, y + 1) == 1) {
          spotCount += 1;
        }
        if (this.at(x, y) * this.at(x, y - 1) == 1) {
          spotCount += 1;
        }
        // spotSum between -4 and 4. map to -1, 1
        out += spotCount / 4.0;
      }
    }
    return out / this.gridSize ** 2;
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
    // this.loopCorrelationPlot();
  }

  async loops(count: number) {
    for (let i = 0; i < count; i++) {
      this.stepWithoutDraw();
    }
  }

  loop() {
    setTimeout(() => {
      for (let i = 0; i < 100000; i++) {
        this.step();
      }

      if (this.calculateEnergy() != this.prevEnergy) {
        alert("invalud energy");
      }

      if (Math.abs(this.calculateMagnetism() - this.prevMagnetism) > 0.0001) {
        // console.log(this.calculateMagnetism(), this.prevMagnetism);
        alert("invalid magnetism");
      }

      // this.prevEnergies.push(this.prevEnergy);
      // this.prevSteps.push(this.time);

      this.prevCorrelation = this.calculateCorrelation();

      this.energyPlot.addPoint(this.time, this.prevEnergy);
      this.magnetismPlot.addPoint(this.time, this.prevMagnetism);
      this.correlationPlot.addPoint(this.time, this.prevCorrelation);

      // this.prevEnergies = this.prevEnergies.slice(-20);
      // this.prevSteps = this.prevSteps.slice(-20);

      // console.log(this.prevEnergies);

      this.loop();
    }, 10);
  }

  clear() {
    this.magnetismPlot.clear();
    this.energyPlot.clear();
    this.correlationPlot.clear();
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

  stepWithoutDraw() {
    this.time += 1;

    let x = Math.floor(Math.random() * this.gridSize);
    let y = Math.floor(Math.random() * this.gridSize);

    this.set(x, y, this.at(x, y) * -1);

    let dE = this.calculateChangeInEnergy(x, y);
    let newEnergy = this.prevEnergy + this.calculateChangeInEnergy(x, y);

    if (newEnergy < this.prevEnergy || Math.random() < Math.exp(-dE / this.T)) {
      this.prevEnergy = newEnergy;
      this.prevMagnetism += (2 * this.at(x, y)) / (this.gridSize * this.gridSize);
    } else {
      this.set(x, y, this.at(x, y) * -1);
    }
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
      this.prevMagnetism += (2 * this.at(x, y)) / (this.gridSize * this.gridSize);
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
    x = (x + this.gridSize) % this.gridSize;
    y = (y + this.gridSize) % this.gridSize;

    // console.log(x, y, x % this.gridSize, y % this.gridSize);

    if (!this.grid || this.grid == undefined) {
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
