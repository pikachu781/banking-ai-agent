import { Component, ElementRef, NgZone, OnDestroy, AfterViewInit, ViewChild, inject } from '@angular/core';

type B = { x: number; w: number; h: number; hue: number; neon: boolean; seed: number };
type Layer = { depth: number; cell: number; lit: number; lum: number; bs: B[] };

const rng = (a: number) => () => {
  a |= 0; a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
const hash = (a: number, b: number, c: number) =>
  (Math.imul(a ^ Math.imul(b, 40503), 2654435761) ^ Math.imul(c, 97531)) >>> 0;

@Component({
  selector: 'app-cyber-bg',
  standalone: true,
  template: '<canvas #c></canvas>',
  styles: [`
    :host { position: fixed; inset: 0; z-index: 0; pointer-events: none; display: block; background: #05010f; }
    canvas { width: 100%; height: 100%; display: block; }
  `]
})
export class CyberBgComponent implements AfterViewInit, OnDestroy {
  @ViewChild('c', { static: true }) ref!: ElementRef<HTMLCanvasElement>;
  private zone = inject(NgZone);
  private scene = document.createElement('canvas');
  private raf = 0; private t0 = 0; private last = 0;
  private w = 0; private h = 0; private H = 0; private u = 1;
  private layers: Layer[] = [];
  private drops: any[] = []; private dust: any[] = []; private cars: any[] = [];
  private reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  private onResize = () => { this.resize(); if (this.reduce) this.draw(0, 0); };

  private signs = [
    { x: .06, y: .22, w: .06, h: .15, hue: 320 }, { x: .17, y: .3, w: .05, h: .1, hue: 185 },
    { x: .80, y: .26, w: .06, h: .13, hue: 280 }, { x: .90, y: .2, w: .05, h: .16, hue: 330 }
  ];

  ngAfterViewInit() {
    this.resize();
    addEventListener('resize', this.onResize);
    if (this.reduce) { this.draw(0, 0); return; }
    this.zone.runOutsideAngular(() => {
      const loop = (now: number) => {
        if (!this.t0) { this.t0 = now; this.last = now; }
        const t = (now - this.t0) / 1000, dt = Math.min((now - this.last) / 1000, .05);
        this.last = now;
        this.draw(t, dt);
        this.raf = requestAnimationFrame(loop);
      };
      this.raf = requestAnimationFrame(loop);
    });
  }

  ngOnDestroy() { cancelAnimationFrame(this.raf); removeEventListener('resize', this.onResize); }

  private resize() {
    const d = Math.min(devicePixelRatio || 1, 1.5), c = this.ref.nativeElement;
    this.w = c.width = Math.round(innerWidth * d);
    this.h = c.height = Math.round(innerHeight * d);
    this.u = this.h / 900;
    this.H = Math.round(this.h * 0.72);
    this.scene.width = this.w; this.scene.height = this.H;
    const r = rng(7), { w, H, u } = this;
    const cfg = [
      { depth: .15, cell: 7, lit: .12, lum: 9, hMin: .25, hMax: .6, wMin: 60, wMax: 120 },
      { depth: .4, cell: 9, lit: .2, lum: 7, hMin: .3, hMax: .8, wMin: 80, wMax: 160 },
      { depth: .8, cell: 12, lit: .25, lum: 5, hMin: .4, hMax: 1, wMin: 110, wMax: 200 }
    ];
    this.layers = cfg.map(c => {
      const bs: B[] = []; let x = -w * .1;
      while (x < w * 1.15) {
        const bw = (c.wMin + r() * (c.wMax - c.wMin)) * u * 1.2;
        bs.push({ x, w: bw, h: (c.hMin + r() * (c.hMax - c.hMin)) * H * .85,
          hue: [190, 280, 320][Math.floor(r() * 3)], neon: r() < .35, seed: Math.floor(r() * 1e6) });
        x += bw * (.9 + r() * .2);
      }
      return { depth: c.depth, cell: c.cell, lit: c.lit, lum: c.lum, bs };
    });
    this.drops = Array.from({ length: 120 }, () => ({ x: r() * w, y: r() * this.h, l: (10 + r() * 20) * u, v: (600 + r() * 500) * u }));
    this.dust = Array.from({ length: 70 }, () => ({ x: r() * w, y: r() * this.h, r: (.6 + r() * 1.6) * u, v: (4 + r() * 10) * u }));
    this.cars = Array.from({ length: 7 }, () => ({ x: r() * w, y: H * (.15 + r() * .4), v: (30 + r() * 60) * u * (r() < .5 ? -1 : 1), hue: r() < .5 ? 185 : 330 }));
  }

  private drawLayer(c: CanvasRenderingContext2D, L: Layer, t: number, drift: number) {
    const { H, u } = this, cw = L.cell * u, ch = cw * 1.5;
    c.save(); c.translate(-drift * L.depth, 0);
    L.bs.forEach((b, i) => {
      const top = H - b.h;
      c.fillStyle = `hsl(${b.hue} 40% ${L.lum}%)`;
      c.fillRect(b.x, top, b.w, b.h);
      let j = 0;
      for (let y = top + ch; y < H - ch; y += ch * 1.6, j++) {
        let k = 0;
        for (let x = b.x + cw * .8; x < b.x + b.w - cw; x += cw * 1.9, k++) {
          const hv = hash(b.seed, j, k), p = (hv % 1000) / 1000;
          if (p > L.lit) continue;
          let a = .75;
          if (p < .02) a = .5 + .5 * Math.sin(t * 3 + hv);
          c.fillStyle = `hsla(${[40, 190, 320][hv % 3]},90%,65%,${a * (.5 + L.depth * .5)})`;
          c.fillRect(x, y, cw, ch);
        }
      }
      if (b.neon) {
        const a = .5 + .2 * Math.sin(t * 1.3 + i);
        c.globalCompositeOperation = 'lighter';
        c.fillStyle = `hsla(${b.hue},100%,60%,${a * .12})`; c.fillRect(b.x - 3 * u, top, 8 * u, b.h);
        c.fillStyle = `hsla(${b.hue},100%,65%,${a})`; c.fillRect(b.x, top, 2 * u, b.h);
        c.globalCompositeOperation = 'source-over';
      }
    });
    c.restore();
  }

  private drawSigns(c: CanvasRenderingContext2D, t: number, drift: number) {
    const { w, H, u } = this;
    c.save(); c.translate(-drift * .4, 0); c.globalCompositeOperation = 'lighter';
    this.signs.forEach((s, i) => {
      const x = s.x * w, y = s.y * H, sw = s.w * w, sh = s.h * H, f = .7 + .3 * Math.sin(t * 2 + i * 2);
      c.fillStyle = `hsla(${s.hue},100%,60%,${.12 * f})`; c.fillRect(x, y, sw, sh);
      c.strokeStyle = `hsla(${s.hue},100%,70%,${.7 * f})`; c.lineWidth = 1.5 * u; c.strokeRect(x, y, sw, sh);
      for (let k = 0; k < 5; k++) {
        const bw = sw * (.3 + .6 * Math.abs(Math.sin(t * .8 + k + i)));
        c.fillStyle = `hsla(${s.hue},100%,75%,${.5 * f})`;
        c.fillRect(x + sw * .08, y + sh * (.12 + k * .17), bw * .84, 2 * u);
      }
      const sy = y + ((t * 40 * u + i * 30) % sh);
      c.fillStyle = 'rgba(255,255,255,.18)'; c.fillRect(x, sy, sw, 2 * u);
    });
    c.restore();
  }

  private girl(c: CanvasRenderingContext2D, x: number, gy: number, s: number, t: number, ph: number, hue: number, flip: number) {
    c.save(); c.translate(x, gy); c.scale(flip * s, s);
    c.rotate(Math.sin(t * .45 + ph) * .012);
    c.scale(1, 1 + Math.sin(t * 1.5 + ph) * .006);
    const wd = Math.sin(t * 1.2 + ph) * 10 + 6, nod = Math.sin(t * .35 + ph) * 1.2;
    const p = new Path2D();
    p.rect(-11, -70, 8, 70); p.rect(3, -70, 8, 70);
    p.moveTo(-17, -150); p.lineTo(17, -150); p.lineTo(27, -62); p.lineTo(-27, -62); p.closePath();
    p.moveTo(-17, -148); p.lineTo(-25, -92); p.lineTo(-20, -90); p.lineTo(-12, -140); p.closePath();
    p.moveTo(17, -148); p.lineTo(25, -92); p.lineTo(20, -90); p.lineTo(12, -140); p.closePath();
    p.moveTo(10 + nod, -165); p.ellipse(nod, -165, 10, 12, 0, 0, 7);
    p.moveTo(-10 + nod, -170);
    p.bezierCurveTo(-18 + nod, -185, 14 + nod, -188, 12 + nod, -168);
    p.bezierCurveTo(16 + wd * .5, -140, 10 + wd, -110, 4 + wd * 1.4, -95);
    p.bezierCurveTo(-4 + wd * .4, -120, -12, -140, -10 + nod, -170);
    c.fillStyle = '#070412'; c.fill(p);
    c.strokeStyle = `hsla(${hue},100%,65%,.65)`; c.lineWidth = 1.6; c.stroke(p);
    c.restore();
  }

  private draw(t: number, dt: number) {
    const { w, h, H, u } = this, s = this.scene.getContext('2d')!, m = this.ref.nativeElement.getContext('2d')!;
    const zoom = 1 + .07 * (.5 - .5 * Math.cos((t * Math.PI * 2) / 60));
    const drift = Math.sin(t * .08) * w * .02;

    s.setTransform(1, 0, 0, 1, 0, 0); s.clearRect(0, 0, w, H);
    const sky = s.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, '#05010f'); sky.addColorStop(.6, '#1a0838'); sky.addColorStop(1, '#4a1266');
    s.fillStyle = sky; s.fillRect(0, 0, w, H);
    const glow = s.createRadialGradient(w * .7, H, 0, w * .7, H, w * .5);
    glow.addColorStop(0, 'rgba(255,60,170,.3)'); glow.addColorStop(1, 'rgba(255,60,170,0)');
    s.fillStyle = glow; s.fillRect(0, 0, w, H);

    s.save();
    s.translate(w * .6, H * .6); s.scale(zoom, zoom); s.translate(-w * .6, -H * .6);
    this.drawLayer(s, this.layers[0], t, drift);

    s.globalCompositeOperation = 'lighter';
    for (const c of this.cars) {
      c.x += c.v * dt; if (c.x > w * 1.1) c.x = -w * .1; if (c.x < -w * .1) c.x = w * 1.1;
      const d = Math.sign(c.v), tr = s.createLinearGradient(c.x, 0, c.x - d * 60 * u, 0);
      tr.addColorStop(0, `hsla(${c.hue},100%,70%,.8)`); tr.addColorStop(1, `hsla(${c.hue},100%,70%,0)`);
      s.fillStyle = tr; s.fillRect(Math.min(c.x, c.x - d * 60 * u), c.y, 60 * u, 2 * u);
    }
    s.globalCompositeOperation = 'source-over';

    this.drawLayer(s, this.layers[1], t, drift);
    this.drawSigns(s, t, drift);
    s.save(); s.translate(-drift * .6, 0);
    const sc = (H * .32) / 180;
    this.girl(s, w * .1, H, sc, t, 0, 190, 1);
    this.girl(s, w * .93, H, sc, t, 2.1, 320, -1);
    s.restore();
    this.drawLayer(s, this.layers[2], t, drift);
    s.restore();

    m.setTransform(1, 0, 0, 1, 0, 0);
    m.drawImage(this.scene, 0, 0);
    const gr = m.createLinearGradient(0, H, 0, h);
    gr.addColorStop(0, '#12082a'); gr.addColorStop(1, '#04010a');
    m.fillStyle = gr; m.fillRect(0, H, w, h - H);

    const st = Math.max(2, Math.round(3 * u)), span = h - H;
    for (let y = H; y < h; y += st) {
      const k = y - H, sy = H - k - st; if (sy < 0) break;
      m.globalAlpha = .35 * (1 - k / span);
      m.drawImage(this.scene, 0, sy, w, st, Math.sin(y * .15 + t * 2) * (2 + k * .02), y, w, st);
    }
    m.globalAlpha = 1;

    for (let i = 0; i < 5; i++) {
      const x = ((i * w * .33 + t * (6 + i * 2) * u) % (w * 1.4)) - w * .2, y = H * (.8 + (i % 3) * .08), r = w * .35;
      const f = m.createRadialGradient(x, y, 0, x, y, r);
      f.addColorStop(0, 'rgba(130,90,210,.10)'); f.addColorStop(1, 'rgba(130,90,210,0)');
      m.fillStyle = f; m.fillRect(x - r, y - r, r * 2, r * 2);
    }

    m.fillStyle = 'rgba(150,230,255,.45)';
    for (const p of this.dust) {
      p.y -= p.v * dt; p.x += Math.sin(t + p.y * .01) * .15 * u;
      if (p.y < 0) { p.y = h; p.x = Math.random() * w; }
      m.beginPath(); m.arc(p.x, p.y, p.r, 0, 7); m.fill();
    }

    m.strokeStyle = 'rgba(180,220,255,.22)'; m.lineWidth = Math.max(1, u); m.beginPath();
    for (const d of this.drops) {
      d.y += d.v * dt; d.x -= d.v * dt * .12;
      if (d.y > h) { d.y = -d.l; d.x = Math.random() * w * 1.1; }
      m.moveTo(d.x, d.y); m.lineTo(d.x + d.l * .12, d.y - d.l);
    }
    m.stroke();

    const cg = m.createRadialGradient(w * .62, h * .5, 0, w * .62, h * .5, w * .38);
    cg.addColorStop(0, 'rgba(3,1,10,.6)'); cg.addColorStop(1, 'rgba(3,1,10,0)');
    m.fillStyle = cg; m.fillRect(0, 0, w, h);
    const vg = m.createRadialGradient(w / 2, h / 2, h * .45, w / 2, h / 2, w * .75);
    vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,.55)');
    m.fillStyle = vg; m.fillRect(0, 0, w, h);
  }
}