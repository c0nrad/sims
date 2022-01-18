import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  template: `
    <div>
      {{ time }}
      <br />
      <canvas id="canvas" width="500" height="500"> </canvas>
      <!-- {{ grid }} -->
      <!-- <table>
        <tr *ngFor="let row of grid">
          <td *ngFor="let v of row" style="width: 20px">{{ v | number: "1.0-0" }}</td>
        </tr>
      </table> -->
      <button (click)="step(); drawGrid()">Step</button>
    </div>
  `,
  styles: [],
})
export class AppComponent {
  cellWidth = 5;
  ctx!: CanvasRenderingContext2D;

  gridSize = 20;
  grid: number[][] = [];

  time: number = 0;

  constructor() {
    this.grid = this.makeGrid();
    this.grid[this.gridSize / 2][this.gridSize / 2] = 100;
    // this.grid[this.gridSize - 2][this.gridSize - 2] = 100;
  }

  makeGrid(): number[][] {
    let out: number[][] = [];
    for (let x = 0; x < this.gridSize; x++) {
      out.push(new Array<number>(this.gridSize).fill(0));
    }
    return out;
  }

  ngAfterViewInit() {
    var c = <HTMLCanvasElement>document.getElementById("canvas")!;
    this.ctx = c.getContext("2d")!;
    this.drawGrid();

    setInterval(() => {
      this.step();
      this.drawGrid();
    }, 200);
  }

  drawGrid() {
    for (let y = 0; y < this.gridSize; y++) {
      for (let x = 0; x < this.gridSize; x++) {
        this.ctx.beginPath();
        let value = (this.grid[y][x] / 100) * 255;

        value = 255 - value;
        this.ctx.fillStyle = `rgb(${value}, ${value}, ${value})`;
        this.ctx.rect((this.cellWidth + 1) * x, (1 + this.cellWidth) * y, this.cellWidth, this.cellWidth);
        this.ctx.fill();
      }
    }
  }

  addGrid(grid: number[][], x: number, y: number, value: number) {
    if (y < 0 || x < 0 || x >= this.gridSize || y >= this.gridSize) {
      return;
    }
    grid[y][x] += value;
  }

  step() {
    this.time += 1;
    let scale = 1;
    let newGrid = this.makeGrid();
    for (let y = 0; y < this.gridSize; y++) {
      for (let x = 0; x < this.gridSize; x++) {
        if (this.grid[y][x] < 0.000001) {
          continue;
        } else {
          // console.log(this.grid[y][x]);
        }
        if (this.grid[y][x] > 100) {
          // console.log(x, y);
        }

        for (let dy = -1; dy <= 1; dy++) {
          for (let dx = -1; dx <= 1; dx++) {
            if (dx == 0 && dy == 0) {
              continue;
            } else {
              if (Math.abs(dy) + Math.abs(dx) == 2) {
                console.log("2", dy, dx);
                this.addGrid(newGrid, x + dx, y + dy, (scale * (this.grid[y][x] * (Math.sqrt(2) / 2))) / (2 * Math.sqrt(2) + 4));
              } else {
                console.log("1", dx, dy);
                this.addGrid(newGrid, x + dx, y + dy, (scale * this.grid[y][x]) / (2 * Math.sqrt(2) + 4));
              }
            }
          }
        }
      }
    }
    this.grid = newGrid;
  }
}
