import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { BrowserModule } from "@angular/platform-browser";
import { NgChartsModule } from "ng2-charts";

import { AppComponent } from "./app.component";
import { EnergyPlotComponent } from './components/energy-plot/energy-plot.component';
import { MagnetismPlotComponent } from './components/magnetism-plot/magnetism-plot.component';

@NgModule({
  declarations: [AppComponent, EnergyPlotComponent, MagnetismPlotComponent],
  imports: [BrowserModule, FormsModule, NgChartsModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
