import { Component, ElementRef, ViewChild } from "@angular/core";
import { Project, Path } from "paper";
import * as paper from "paper";
import { Point } from "paper/dist/paper-core";

@Component({
  selector: "app-root",
  template: ` <div class="container-fluid">
    <h1>Two Body Central Force</h1>
    <div class="row">
      <div class="col-md-8">
        <canvas id="cv1" style="border: 1px solid; width: 100%"></canvas>
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
          />
        </div>
        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="r_1"></ng-katex> = ({{ circle1.position }})
          </label>
          <input type="text" class="form-control" [(ngModel)]="r1Str" />
        </div>
        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="r_2"></ng-katex> = ({{ circle2.position }})
          </label>
          <input type="text" class="form-control" [(ngModel)]="r2Str" />
        </div>
        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="v_1"></ng-katex> = ({{ v1 }})
          </label>
          <input type="text" class="form-control" [(ngModel)]="v1Str" />
        </div>
        <div class="mb-2">
          <label for="m2" class="form-label"
            ><ng-katex equation="v_2"></ng-katex> = ({{ v2 }})
          </label>
          <input type="text" class="form-control" [(ngModel)]="v2Str" />
        </div>
      </div>
    </div>
  </div>`,
  styles: [],
})
export class AppComponent {
  project!: paper.Project;
  m1: number = 1000;
  m2: number = 2000;

  gamma: number = 0.1;
  dt: number = 10;

  r1Str: string = "100, 100";
  r2Str: string = "500, 500";
  v1Str: string = "1, 0";
  v2Str: string = "-1, 0";

  circle1!: paper.Path.Circle;
  circle2!: paper.Path.Circle;

  v1: paper.Point = new Point(5, 0);
  v2: paper.Point = new Point(5, 0);

  intervalID: any = 0;

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

    // this.r2.x = parseInt(this.r2Str.split(",")[0]);
    // this.r2.y = parseInt(this.r2Str.split(",")[1]);
  }

  ngOnInit() {
    this.project = new paper.Project("cv1");
    this.circle1 = new Path.Circle({
      center: [80, 50],
      radius: 20,
      strokeColor: "black",
    });

    this.circle2 = new Path.Circle({
      center: [80, 50],
      radius: 30,
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
    this.start();
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

    let a1 = this.circle2.position
      .subtract(this.circle1.position)
      .normalize()
      .multiply(
        (this.m2 * this.gamma) /
          Math.pow(this.circle1.position.getDistance(this.circle2.position), 2)
      );

    let a2 = this.circle1.position
      .subtract(this.circle2.position)
      .normalize()
      .multiply(
        (this.m1 * this.gamma) /
          Math.pow(this.circle1.position.getDistance(this.circle2.position), 2)
      );

    this.v1 = this.v1.add(a1.multiply(this.dt));
    this.v2 = this.v2.add(a2.multiply(this.dt));
    // semi-implicit euler
    this.circle1.position.x += this.v1.x;
    this.circle1.position.y += this.v1.y;

    this.circle2.position.x += this.v2.x;
    this.circle2.position.y += this.v2.y;

    // var circle1Radius = this.circle1.bounds.width / 2;
    // this.circle1.scale(this.m1 / circle1Radius);

    // var circle2Radius = this.circle2.bounds.width / 2;
    // this.circle2.scale(this.m2 / circle2Radius);

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

    this.v1Str = "" + Math.round(this.v1.x) + ", " + Math.round(this.v1.y);
    this.v2Str = "" + Math.round(this.v2.x) + ", " + Math.round(this.v2.y);
  }
}
