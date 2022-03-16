import { Component, ElementRef, Input, OnInit, Output, SimpleChanges, ViewChild } from "@angular/core";
import { Chart, Point } from "chart.js";

@Component({
  selector: "app-simple-plot",
  template: `
    <div style="display: block;">
      <canvas #chart width="600" height="200"></canvas>
    </div>
  `,
  styles: [],
})
export class SimplePlotComponent implements OnInit {
  @ViewChild("chart")
  private chartRef!: ElementRef;
  private chart!: Chart;
  private data: Point[] = [];

  @Input() title: string = "";

  addPoint(x: number, y: number) {
    this.data.push({ x, y });
    this.chart.update();
  }

  clear() {
    this.data.length = 0;
  }

  constructor() {}

  ngOnInit(): void {}

  ngAfterViewInit() {
    this.data = [];

    this.chart = new Chart(this.chartRef.nativeElement, {
      type: "scatter",
      data: {
        datasets: [
          {
            label: this.title,
            data: this.data,
            fill: false,
            backgroundColor: "black",
          },
        ],
      },
      options: {
        events: [],
        responsive: false,
        animation: false,
        scales: {
          y: {
            // min: -20000,
            suggestedMax: 0,
          },
        },
      },
    });
  }
}
