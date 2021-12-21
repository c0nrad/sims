// @ts-nocheck
import { Component, ElementRef, ViewChild } from "@angular/core";
import { Project, Path } from "paper";
import * as paper from "paper";
import { Point } from "paper/dist/paper-core";
import { BaseChartDirective } from "ng2-charts";
import { ChartConfiguration, ChartType } from "chart.js";

@Component({
  selector: "app-root",
  template: ` <div class="container-fluid">
    <h1>Two Body Central Force</h1>
    <div class="row">
      <div class="col-md-8">
        <canvas id="cv1" style="border: 1px solid; width: 100%"></canvas>
        <div class="row">
          <div class="col-md-4">
            <button
              class="btn btn-primary"
              (click)="start()"
              [disabled]="intervalID != 0"
            >
              Start
            </button>
            <button
              class="btn btn-danger"
              (click)="stop()"
              [disabled]="intervalID == 0"
            >
              Stop
            </button>

            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                value=""
                id="flexCheckDefault"
                [(ngModel)]="isCenter"
              />
              <label class="form-check-label" for="flexCheckDefault">
                Track Center of Mass
              </label>
            </div>

            <ng-katex equation="\\gamma"></ng-katex> = {{ gamma }} <br />

            <ng-katex equation="\\bm{M}"></ng-katex> = {{ M }} <br />
            <ng-katex equation="\\bm{r}"></ng-katex> = {{ r }} <br />
            <ng-katex equation="|\\bm{r}|"></ng-katex> = {{ r.length }} <br />

            <ng-katex equation="\\mu"></ng-katex> = {{ mu }} <br />
            <ng-katex equation="l"></ng-katex> = {{ l }} <br />
            <ng-katex equation="T_1"></ng-katex> = {{ T1 }} <br />
            <ng-katex equation="T_2"></ng-katex> = {{ T2 }} <br />
            <ng-katex equation="U(r)"></ng-katex> = {{ U }} <br />
            <ng-katex equation="E_{total}"></ng-katex> = {{ T1 + T2 + U }}
            <br />
          </div>
          <div class="col-md-8">
            <div style="display: block">
              <canvas
                baseChart
                [data]="barChartData"
                [options]="barChartOptions"
                type="line"
              >
              </canvas>
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <ng-katex
          equation="F = \\frac{\\gamma m_1 m_2} {|r_1 - r_2|^2}"
        ></ng-katex>
        <div class="mb-2">
          <label for="m1" class="form-label"
            ><ng-katex equation="m_1"></ng-katex> = {{ m1 }}
          </label>
          <input
            type="range"
            class="form-range"
            min="10"
            max="100"
            step="10"
            [(ngModel)]="m1"
            (change)="updatePositions()"
          />
        </div>

        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="m_2"></ng-katex> = {{ m2 }}
          </label>
          <input
            type="range"
            class="form-range"
            min="10"
            max="100"
            step="10"
            [(ngModel)]="m2"
            (change)="updatePositions()"
          />
        </div>
        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="r_1"></ng-katex> = ({{ circle1.position }})
          </label>
          <input
            type="text"
            class="form-control"
            [(ngModel)]="r1Str"
            (change)="updatePositions()"
          />
        </div>
        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="r_2"></ng-katex> = ({{ circle2.position }})
          </label>
          <input
            type="text"
            class="form-control"
            [(ngModel)]="r2Str"
            (change)="updatePositions()"
          />
        </div>
        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="v_1"></ng-katex> = ({{ v1 }})
          </label>
          <input
            type="text"
            class="form-control"
            [(ngModel)]="v1Str"
            (change)="updatePositions()"
          />
        </div>
        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="v_2"></ng-katex> = ({{ v2 }})
          </label>
          <input
            type="text"
            class="form-control"
            [(ngModel)]="v2Str"
            (change)="updatePositions()"
          />
        </div>
      </div>
    </div>
  </div>`,
  styles: [],
})
export class AppComponent {
  project!: paper.Project;
  m1: number = 10;
  m2: number = 20;

  M: paper.Point = new Point(5, 0);
  mu: number = 5;
  r: paper.Point = new Point(5, 0);

  l: number = 5;
  u: number = 5;
  u_cf: number = 5;

  gamma: number = 1000000;
  dt: number = 10;

  T1: number = 0;
  T2: number = 0;
  U: number = 0;

  r1Str: string = "250, 100";
  r2Str: string = "250, 300";
  v1Str: string = "200, 0";
  v2Str: string = "-100, 0";

  circle1!: paper.Path.Circle;
  circle2!: paper.Path.Circle;

  v1: paper.Point = new Point(5, 0);
  v2: paper.Point = new Point(5, 0);

  intervalID: any = 0;

  isCenter: boolean = false;

  @ViewChild(BaseChartDirective) chart: BaseChartDirective | undefined;

  public barChartOptions: ChartConfiguration["options"] = {
    responsive: true,
    // We use these empty structures as placeholders for dynamic theming.
    scales: {
      x: {},
      y: {
        max: 2000000,
        min: -2000000,
      },
    },
  };
  public barChartType: any = "bar";

  public barChartData: any = {
    labels: ["2006", "2007", "2008", "2009", "2010", "2011", "2012"],
    datasets: [
      { data: [65, 59, 80, 81, 56, 55, 40], label: "Series A" },
      { data: [28, 48, 40, 19, 86, 27, 90], label: "Series B" },
    ],
  };

  constructor() {}

  updatePositions() {
    this.circle1.position = new paper.Point(
      parseInt(this.r1Str.split(",")[0]),
      parseInt(this.r1Str.split(",")[1])
    );

    this.circle2.position = new paper.Point(
      parseInt(this.r2Str.split(",")[0]),
      parseInt(this.r2Str.split(",")[1])
    );

    this.v1 = new paper.Point(
      parseInt(this.v1Str.split(",")[0]),
      parseInt(this.v1Str.split(",")[1])
    );

    this.v2 = new paper.Point(
      parseInt(this.v2Str.split(",")[0]),
      parseInt(this.v2Str.split(",")[1])
    );

    this.M = this.circle1.position
      .multiply(this.m1)
      .add(this.circle2.position.multiply(this.m2))
      .divide(this.m1 + this.m2);

    // console.log(this.M, this.r);

    let c1 = this.circle1.position.subtract(this.M);
    let c2 = this.circle2.position.subtract(this.M);

    this.l =
      this.circle1.position.subtract(this.M).cross(this.v1.multiply(this.m1)) +
      this.circle2.position.subtract(this.M).cross(this.v2.multiply(this.m2));
    // this.l /= 10;

    this.mu = (this.m1 * this.m2) / (this.m1 + this.m2);

    let ranges = [];
    let us = [];
    let ucfs = [];
    let ueffs = [];
    for (let r = 1; r < 1000; r += 10) {
      ranges.push(r);
      us.push((-this.gamma * this.m1 * this.m2) / r);
      ucfs.push((this.l * this.l) / (2 * this.mu * r * r));
      ueffs.push(us.slice(-1)[0] + ucfs.slice(-1)[0]);
    }

    this.barChartData = {
      labels: ranges,
      datasets: [
        { data: us, label: "U" },
        { data: ucfs, label: "U_cf" },
        { data: ueffs, label: "U_eff" },
      ],
    };

    // this.r2.x = parseInt(this.r2Str.split(",")[0]);
    // this.r2.y = parseInt(this.r2Str.split(",")[1]);
  }

  ngOnInit() {
    this.project = new paper.Project("cv1");
    this.circle1 = new Path.Circle({
      center: [80, 50],
      radius: this.m1,
      strokeColor: "black",
    });

    this.circle2 = new Path.Circle({
      center: [80, 50],
      radius: this.m2,
      strokeColor: "black",
    });

    var toolPan = new paper.Tool();
    toolPan.activate();

    // On drag, scroll the View by the difference between mousedown
    // and mouseup
    toolPan.onMouseDrag = function (event: any) {
      var delta = event.downPoint.subtract(event.point);
      //@ts-ignore
      paper.view.scrollBy(delta);
    };

    this.updatePositions();
    this.step();
    this.start();
    this.updatePositions();
  }

  start() {
    this.intervalID = setInterval(() => {
      this.step();
    }, this.dt);
  }

  stop() {
    clearInterval(this.intervalID);
    this.intervalID = 0;
  }

  step() {
    // func (s *Spring) Step(dt float64) {
    //   a := -(s.K / s.M) * (s.X)
    //   s.V += a * dt
    //   s.X += s.V * dt
    // }

    this.r = this.circle1.position.subtract(this.circle2.position);

    let a1 = this.circle2.position
      .subtract(this.circle1.position)
      .normalize()
      .multiply((this.m2 * this.gamma) / (this.r.length * this.r.length));

    let a2 = this.circle1.position
      .subtract(this.circle2.position)
      .normalize()
      .multiply((this.m1 * this.gamma) / (this.r.length * this.r.length));

    this.v1 = this.v1.add(a1.multiply(this.dt / 1000));
    this.v2 = this.v2.add(a2.multiply(this.dt / 1000));
    // semi-implicit euler
    this.circle1.position.x += this.v1.x * (this.dt / 1000);
    this.circle1.position.y += this.v1.y * (this.dt / 1000);

    this.circle2.position.x += this.v2.x * (this.dt / 1000);
    this.circle2.position.y += this.v2.y * (this.dt / 1000);

    var circle1Radius = this.circle1.bounds.width / 2;
    this.circle1.scale(this.m1 / circle1Radius);

    var circle2Radius = this.circle2.bounds.width / 2;
    this.circle2.scale(this.m2 / circle2Radius);

    this.mu = (this.m1 * this.m2) / (this.m1 + this.m2);

    this.v1Str = "" + Math.round(this.v1.x) + ", " + Math.round(this.v1.y);
    this.v2Str = "" + Math.round(this.v2.x) + ", " + Math.round(this.v2.y);

    this.M = this.circle1.position
      .multiply(this.m1)
      .add(this.circle2.position.multiply(this.m2))
      .divide(this.m1 + this.m2);

    this.r = this.circle1.position.subtract(this.circle2.position);

    this.l =
      this.circle1.position.subtract(this.M).cross(this.v1) * this.m1 +
      this.circle2.position.subtract(this.M).cross(this.v2) * this.m2;

    this.T1 = 0.5 * this.m1 * this.v1.length * this.v1.length;
    this.T2 = 0.5 * this.m2 * this.v2.length * this.v2.length;
    this.U = (-this.gamma * this.m1 * this.m2) / this.r.length;

    if (this.isCenter) {
      // this.circle1.position = this.circle1.position.subtract(this.M);
      // this.circle2.position = this.circle2.position.subtract(this.M);
      //@ts-ignore
      paper.view.scrollBy(this.M.subtract(paper.view.center));
    }

    this.r1Str =
      "" +
      Math.round(this.circle1.position.x) +
      ", " +
      Math.round(this.circle1.position.y);
    this.r2Str =
      "" +
      Math.round(this.circle2.position.x) +
      ", " +
      Math.round(this.circle2.position.y);
  }
}
