import { Component, ElementRef, ViewChild } from "@angular/core";
import { Project, Path } from "paper";
import * as paper from "paper";

@Component({
  selector: "app-root",
  template: ` <canvas id="cv1"></canvas>
    <p>Sup</p>`,
  styles: [],
})
export class AppComponent {
  project!: paper.Project;

  constructor() {}

  ngOnInit() {
    this.project = new paper.Project("cv1");
    const path = new Path.Circle({
      center: [80, 50],
      radius: 30,
      strokeColor: "black",
    });
  }
}
