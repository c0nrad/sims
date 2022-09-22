import { Component } from "@angular/core";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";

@Component({
  selector: "app-root",
  template: `
    <div class="container-fluid g-0">
      <div class="row g-1">
        <div class="col-md-10">
          <!--The content below is only a placeholder and can be replaced.-->
          <div style="border:1px solid" id="canvasDiv"></div>
        </div>

        <div class="col-md-2">
          <h2>Teleray</h2>
          <p><i>Simple ray tracing with a Cassegrain telescope.</i></p>

          <h4>Controls</h4>

          <h5>Primary Mirror</h5>
          <div class="form-group">
            <label for="exampleInputEmail1">primaryMirror.z</label>
            <input type="number" class="form-control" placeholder="primary mirror z" [(ngModel)]="primaryMirror.position.y" (change)="redraw()" />
          </div>
          <div class="form-group">
            <label for="exampleInputEmail1">primaryMirror.radius</label>
            <input type="number" class="form-control" placeholder="primary mirror radius" [(ngModel)]="primaryMirror.radius" (change)="redraw()" />
          </div>
          <div class="form-group">
            <label for="exampleInputEmail1">primaryMirror.phiStart (inner rim)</label>
            <input type="number" class="form-control" step=".01" [(ngModel)]="primaryMirror.phiStart" (change)="redraw()" />
          </div>
          <div class="form-group">
            <label for="exampleInputEmail1">primaryMirror.phiEnd (outer rim)</label>
            <input type="number" class="form-control" step=".01" [(ngModel)]="primaryMirror.phiEnd" (change)="redraw()" />
          </div>

          <hr />

          <h5>Secondary Mirror</h5>
          <div class="form-group">
            <label for="exampleInputEmail1">secondaryMirror.z</label>
            <input type="number" class="form-control" placeholder="primary mirror z" [(ngModel)]="secondaryMirror.position.y" (change)="redraw()" />
          </div>
          <div class="form-group">
            <label for="exampleInputEmail1">secondaryMirror.radius</label>
            <input type="number" class="form-control" placeholder="primary mirror radius" [(ngModel)]="secondaryMirror.radius" (change)="redraw()" />
          </div>
          <div class="form-group">
            <label for="exampleInputEmail1">secondaryMirror.phiStart (inner rim)</label>
            <input type="number" class="form-control" step=".01" [(ngModel)]="secondaryMirror.phiStart" (change)="redraw()" />
          </div>
          <div class="form-group">
            <label for="exampleInputEmail1">secondaryMirror.phiEnd (outer rim)</label>
            <input type="number" class="form-control" step=".01" [(ngModel)]="secondaryMirror.phiEnd" (change)="redraw()" />
          </div>

          <h5>Light Source</h5>
          <div class="form-group">
            <label for="exampleInputEmail1">rayCount</label>
            <input type="number" class="form-control" placeholder="primary mirror z" [(ngModel)]="rayCount" (change)="initRays(); redraw()" />
          </div>

          <div class="form-check">
            <input class="form-check-input" type="checkbox" value="" [(ngModel)]="showNormals" (change)="initRays(); redraw()" />
            <label class="form-check-label" for="flexCheckDefault"> Show Normals </label>
          </div>

          <button class="btn btn-secondary" (click)="initRays(); redraw()">Redraw Rays</button>
          <hr />

          <h5>CCD</h5>
          <table>
            <tr *ngFor="let r of ccd.counts">
              <td
                *ngFor="let c of r"
                style="width:10px; height:10px; margin:00px; padding:0px; text-align: center; font-size: 5px"
                [ngClass]="{ 'bg-danger': c > rayCount / 8, 'bg-warning': c > rayCount / 16, 'bg-info': c >= 1 }"
              >
                <small>{{ c }}</small>
              </td>
            </tr>
          </table>
          <!-- {{ ccd.counts }} -->
        </div>
      </div>
    </div>
  `,
  styles: [],
})
export class AppComponent {
  title = "teleray";

  container: any;
  camera: THREE.Camera;
  scene: THREE.Scene;
  renderer: THREE.Renderer;
  controls: OrbitControls;

  primaryMirror!: Mirror;
  secondaryMirror!: Mirror;
  ccd!: CCD;

  rays: Ray[] = [];

  rayCount = 32;
  showNormals: boolean = true;

  constructor() {
    this.camera = new THREE.Camera();
    this.scene = new THREE.Scene();
    this.renderer = {} as THREE.Renderer;
    this.controls = {} as OrbitControls;
    this.initMirrors();
    this.initRays();
  }

  ngInit() {}

  initMirrors() {
    this.primaryMirror = new Mirror();
    this.secondaryMirror = new Mirror();

    this.primaryMirror.name = "Primary Mirror";
    this.primaryMirror.position.y = 0;
    this.primaryMirror.radius = 100;
    this.primaryMirror.phiStart = Math.PI / 64;
    this.primaryMirror.phiEnd = 0.22;

    this.secondaryMirror.name = "Secondary Mirror";
    this.secondaryMirror.position = new THREE.Vector3(0, 40, 0);
    this.secondaryMirror.phiEnd = 0.2;
    this.secondaryMirror.phiStart = 0;
    this.secondaryMirror.radius = 25;
  }

  initRays() {
    let l = 2 * (this.primaryMirror.radius * Math.sin(this.primaryMirror.phiEnd));
    this.rays = [];
    for (let i = 0; i < this.rayCount; i++) {
      let r = new Ray();
      r.start = new THREE.Vector3(Math.random() * l - l / 2, BOUNDS, Math.random() * l - l / 2);
      this.rays.push(r);
    }

    this.initCCD();
  }

  initCCD() {
    this.ccd = new CCD();
    this.ccd.grid = 20;

    for (var i: number = 0; i < this.ccd.grid; i++) {
      this.ccd.counts[i] = [];
      for (var j: number = 0; j < this.ccd.grid; j++) {
        this.ccd.counts[i][j] = 0;
      }
    }
  }

  ngAfterViewInit() {
    this.container = document.getElementById("canvasDiv");

    this.camera = new THREE.PerspectiveCamera(75, this.container.offsetWidth / window.innerHeight, 0.1, 1000);

    this.scene = new THREE.Scene();

    // const geometry = new THREE.BoxGeometry();
    // const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    // const cube = new THREE.Mesh(geometry, material);
    // this.scene.add(cube);

    this.camera.position.z = 150;
    this.camera.position.y = 60;

    console.log(this.container.offsetWidth);
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setSize(this.container.offsetWidth, window.innerHeight);

    this.container.appendChild(this.renderer.domElement);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.autoRotateSpeed = 2;
    this.controls.autoRotate = true;

    this.drawScene();
    this.animate();
  }

  animate() {
    // console.log("Nice");
    requestAnimationFrame(() => this.animate());
    this.controls.update();

    this.render();
    // this.stats.end();
  }

  render() {
    // this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }

  drawScene() {
    const size = BOUNDS * 4;
    const divisions = 10;

    const gridHelper = new THREE.GridHelper(size, divisions);
    this.scene.add(gridHelper);

    let m1 = this.drawMirror(this.primaryMirror);
    m1.updateMatrixWorld();
    console.log("m1.position", m1.position);

    let m2 = this.drawMirror(this.secondaryMirror);
    m2.rotateY(Math.PI);

    this.drawObstructions();
    this.drawCCD();

    // secondaryMirror.phiEnd =

    // Ray;
    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0x0000ff,
    });

    for (let ray of this.rays) {
      let linePoints: THREE.Vector3[] = [];
      // linePoints = calculateRay(new THREE.Vector3(12, BOUNDS, 3), new THREE.Vector3(0, -1, 0), this.scene);
      // this.scene.add(new THREE.ArrowHelper(new THREE.Vector3(0, -1, 0), new THREE.Vector3(0, BOUNDS, 3), 5, 0x0000ff));
      // linePoints = calculateRay(
      //   new THREE.Vector3(9.606730077992689, 2.0145502148114645, 2.885954090820143),
      //   new THREE.Vector3(-0.39326992200731103, 0.9123224753581949, -0.11404590917985706),
      //   this.scene
      // );
      linePoints = calculateRay(ray.start, ray.direction, this.scene, this.showNormals, this.ccd);

      const lineGeometry = new THREE.BufferGeometry().setFromPoints(linePoints);
      const line = new THREE.Line(lineGeometry, lineMaterial);
      this.scene.add(line);
    }

    console.log(this.ccd.counts);
  }

  redraw() {
    this.clear();
    this.initCCD();
    this.drawScene();
  }

  clear() {
    while (this.scene.children.length > 0) {
      this.scene.remove(this.scene.children[0]);
    }
  }

  drawMirror(mirror: Mirror) {
    const points: any = [];

    for (let phi = mirror.phiStart; phi < mirror.phiEnd; phi += Math.PI / 2048) {
      points.push(new THREE.Vector2(Math.abs(Math.sin(phi) * mirror.radius), Math.abs(Math.cos(phi) * mirror.radius - mirror.radius)));
    }
    const geometry = new THREE.LatheGeometry(points, 256);
    // const gometry = new THREE.SphereGeometry(mirror.radius, 256, 256, 0, 2 * Math.PI, mirror.phiStart, mirror.phiEnd);

    const material = new THREE.MeshBasicMaterial();
    if (mirror.doubleSided) {
      material.side = THREE.DoubleSide;
    }
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.set(mirror.position.x, mirror.position.y, mirror.position.z);
    sphere.name = mirror.name;

    if (mirror.invert) {
      sphere.rotateX(Math.PI);
    }

    this.scene.add(sphere);
    sphere.updateMatrixWorld();
    return sphere;
  }

  drawObstructions() {
    let color = 0x222222;
    let height = this.secondaryMirror.position.y + 2;

    const geometry = new THREE.PlaneGeometry(10, 10);
    const material = new THREE.MeshBasicMaterial({ color: color, side: THREE.DoubleSide });
    const plane = new THREE.Mesh(geometry, material);
    plane.name = "Wall";
    plane.rotateX(Math.PI / 2);
    plane.position.y = height;
    this.scene.add(plane);
    plane.updateMatrixWorld();

    const strutGeometry = new THREE.PlaneGeometry(2, (this.primaryMirror.radius * Math.cos(this.primaryMirror.phiEnd)) / 2);
    const structPlane = new THREE.Mesh(strutGeometry, material);
    structPlane.name = "Wall";
    structPlane.rotateX(Math.PI / 2);
    structPlane.position.y = height;
    this.scene.add(structPlane);
    structPlane.updateMatrixWorld();

    const strutGeometry2 = new THREE.PlaneGeometry(2, (this.primaryMirror.radius * Math.cos(this.primaryMirror.phiEnd)) / 2);
    const structPlane2 = new THREE.Mesh(strutGeometry2, material);
    structPlane2.name = "Wall";
    structPlane2.rotateX(Math.PI / 2);
    structPlane2.rotateZ(Math.PI / 2);

    structPlane2.position.y = height;
    this.scene.add(structPlane2);
    structPlane2.updateMatrixWorld();
  }

  drawCCD() {
    let size = this.ccd.length;

    const geometry = new THREE.PlaneGeometry(size, size);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, side: THREE.DoubleSide });
    const ccd = new THREE.Mesh(geometry, material);
    ccd.name = "CCD";
    ccd.rotateX(Math.PI / 2);

    this.scene.add(ccd);
    ccd.updateMatrixWorld();

    const gridHelper = new THREE.GridHelper(size, this.ccd.grid);
    this.scene.add(gridHelper);
  }
}

var BOUNDS = 200;

function calculateRay(position: THREE.Vector3, direction: THREE.Vector3, scene: THREE.Scene, showNormals: boolean, ccd: CCD) {
  let r = new THREE.Raycaster(position.clone(), direction.clone());
  let out = [position.clone()];

  let attempts = 5;
  let i = 0;

  let intersections = r.intersectObjects(scene.children, true);

  while (intersections.length >= 1 && i < attempts) {
    i++;

    let intersection = intersections[0];
    intersections = intersections.sort((a, b) => a.distance - b.distance);
    for (let intersectionIndex = 0; intersectionIndex < intersections.length; intersectionIndex++) {
      intersection = intersections[intersectionIndex];

      if (intersection.distance < 1) {
        continue;
      }

      if (intersection.object.name == "CCD") {
        break;
      }
      if (intersection.object.name == "Wall") {
        break;
      }

      if (intersection.object.name == "Primary Mirror" || intersection.object.name == "Secondary Mirror") {
        break;
      }
    }

    if (intersection.object.name == "CCD") {
      let x = intersection.point.x;
      let z = intersection.point.z;
      let gridX = Math.floor(x / (ccd.length / ccd.grid)) + ccd.grid / 2;
      let gridZ = Math.floor(z / (ccd.length / ccd.grid)) + ccd.grid / 2;
      ccd.counts[gridX][gridZ] += 1;

      out.push(intersection.point);
      return out;
    }

    if (intersection.object.name == "Wall") {
      out.push(intersection.point);
      return out;
    }

    if (intersection.object.name != "Primary Mirror" && intersection.object.name != "Secondary Mirror") {
      console.log("intersectoin is not a Primary Mirror or Secondary Mirror...");
      // console.log(intersections, intersection.object);
      continue;
    }

    let intersectionPoint = intersection.point.clone();
    out.push(intersectionPoint);

    position = intersectionPoint.clone();
    let normal = intersection.face!.normal.clone().multiplyScalar(-1);
    direction = direction.clone().reflect(normal).clone();
    position.add(direction.clone());

    if (showNormals) {
      const arrowHelper = new THREE.ArrowHelper(normal, intersectionPoint, 5, 0xff0000);
      scene.add(arrowHelper);
    }

    r.set(position, direction.clone().normalize());
    intersections = r.intersectObjects(scene.children, true);
  }

  out.push(position.clone().add(direction.multiplyScalar(BOUNDS)));

  return out;
}

class Mirror {
  name = "";
  position: THREE.Vector3 = new THREE.Vector3(0, -20, 0);
  radius: number = 40;

  phiStart: number = Math.PI / 32;
  phiEnd: number = Math.PI / 8;

  invert = false;
  doubleSided = true;
}

class Ray {
  start: THREE.Vector3 = new THREE.Vector3(0, 0, 0);
  direction: THREE.Vector3 = new THREE.Vector3(0, -1, 0);
}

class CCD {
  counts: number[][] = [[]];
  grid = 10;
  length = 10;
}
