import { NgModule } from "@angular/core";
import { FormsModule } from "@angular/forms";
import { BrowserModule } from "@angular/platform-browser";
import { KatexModule } from "ng-katex";

import { AppComponent } from "./app.component";

@NgModule({
  declarations: [AppComponent],
  imports: [BrowserModule, KatexModule, FormsModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
