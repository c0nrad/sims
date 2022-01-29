import { Component, ElementRef, Input, OnInit, Output, SimpleChanges, ViewChild } from "@angular/core";
import { Chart, Point } from "chart.js";

@Component({
  selector: "app-energy-plot",
  template: `
    <div style="display: block;">
      <canvas #chart width="600" height="200"></canvas>
    </div>
  `,
  styles: [],
})
export class EnergyPlotComponent implements OnInit {
  @ViewChild("chart")
  private chartRef!: ElementRef;
  private chart!: Chart;
  private data: Point[] = [];

  @Input() prevEnergies: number[] = [];
  @Input() prevSteps: number[] = [];

  addPoint(x: number, y: number) {
    this.data.push({ x, y });
    this.chart.update();
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
            label: "Energy",
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
            min: -20000,
            suggestedMax: 0,
          },
        },
      },
    });
  }
}
