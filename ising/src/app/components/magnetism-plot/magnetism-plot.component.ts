import { Component, ElementRef, Input, OnInit, Output, SimpleChanges, ViewChild } from "@angular/core";
import { Chart, Point } from "chart.js";

@Component({
  selector: "app-magnetism-plot",
  template: `
    <div style="display: block">
      <canvas #chart width="600" height="200"></canvas>
    </div>
  `,
  styles: [],
})
export class MagnetismPlotComponent implements OnInit {
  @ViewChild("chart")
  private chartRef!: ElementRef;
  private chart!: Chart;
  private data: Point[] = [];

  addPoint(x: number, y: number) {
    this.data.push({ x, y });
    // this.data = this.data.slice(-100);
    // this.chart.data.datasets[0].data = this.data.slice(-100);
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
            label: "Magnetism",
            data: this.data,
            fill: false,
            backgroundColor: "black",
          },
        ],
      },
      options: {
        responsive: false,
        animation: false,
        scales: {
          y: {
            suggestedMin: -2000,
            suggestedMax: 2000,
          },
        },
      },
    });
  }
}
