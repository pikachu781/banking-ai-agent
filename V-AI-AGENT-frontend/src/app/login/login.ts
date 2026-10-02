import {
  AfterViewInit,
  Component,
  ElementRef,
  HostListener,
  NgZone,
  OnDestroy,
  OnInit,
  ViewChild,
  inject,
  signal
} from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../services/auth.service';

const GREETING = 'Please log in to continue.';
const REMEMBER_KEY = 'voiceai.rememberedEmail';

interface Particle {
  x: number;
  y: number;
  z: number;
  vx: number;
  vy: number;
  hue: number;
}

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class LoginComponent implements OnInit, AfterViewInit, OnDestroy {
  private fb = inject(FormBuilder);
  private authService = inject(AuthService);
  private router = inject(Router);
  private zone = inject(NgZone);
  private host = inject<ElementRef<HTMLElement>>(ElementRef);

  @ViewChild('fx', { static: true }) fxCanvas!: ElementRef<HTMLCanvasElement>;

  loginForm: FormGroup;

  // Signals so the view updates reliably (also under zoneless change detection).
  loading = signal(false);
  errorMessage = signal('');
  speaking = signal(false);
  showPassword = signal(false);

  private greeted = false;
  private greetTimer?: number;
  private raf = 0;
  private particles: Particle[] = [];
  private resizeObserver?: ResizeObserver;
  private mouse = { x: 0, y: 0, tx: 0, ty: 0 };

  constructor() {
    this.loginForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      remember: [false]
    });
  }

  ngOnInit(): void {
    try {
      const saved = localStorage.getItem(REMEMBER_KEY);
      if (saved) {
        this.loginForm.patchValue({ email: saved, remember: true });
      }
    } catch {
      /* storage unavailable */
    }

    // Browsers may block speech until the user interacts; we retry on first gesture.
    this.greetTimer = window.setTimeout(() => this.greet(), 1400);
  }

  ngAfterViewInit(): void {
    this.startParticles();
  }

  ngOnDestroy(): void {
    clearTimeout(this.greetTimer);
    cancelAnimationFrame(this.raf);
    this.resizeObserver?.disconnect();
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  }

  /* ---------- Parallax ---------- */

  @HostListener('document:mousemove', ['$event'])
  onMouseMove(e: MouseEvent): void {
    this.mouse.tx = (e.clientX / window.innerWidth - 0.5) * 2;
    this.mouse.ty = (e.clientY / window.innerHeight - 0.5) * 2;
  }

  /* ---------- Voice ---------- */

  @HostListener('document:pointerdown')
  @HostListener('document:keydown')
  onFirstGesture(): void {
    if (!this.greeted) {
      this.greet();
    }
  }

  replay(): void {
    this.greet(true);
  }

  private greet(force = false): void {
    if (!('speechSynthesis' in window)) return;
    if (this.greeted && !force) return;

    const synth = window.speechSynthesis;
    synth.cancel();

    const utterance = new SpeechSynthesisUtterance(GREETING);
    utterance.lang = 'en-US';
    utterance.rate = 0.94;
    utterance.pitch = 1.12;

    const voice = this.pickVoice(synth.getVoices());
    if (voice) utterance.voice = voice;

    utterance.onstart = () => {
      this.greeted = true;
      this.zone.run(() => this.speaking.set(true));
    };
    const stop = () => this.zone.run(() => this.speaking.set(false));
    utterance.onend = stop;
    utterance.onerror = stop; // "not-allowed" before a gesture: we retry on the first click/key

    synth.speak(utterance);
  }

  private pickVoice(voices: SpeechSynthesisVoice[]): SpeechSynthesisVoice | undefined {
    const english = voices.filter(v => v.lang.toLowerCase().startsWith('en'));
    const preferred = /(aria|jenny|zira|samantha|serena|female|google uk english female)/i;
    return english.find(v => preferred.test(v.name)) ?? english[0];
  }

  /* ---------- Particles (canvas, runs outside Angular's zone) ---------- */

  private startParticles(): void {
    const canvas = this.fxCanvas.nativeElement;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const { clientWidth: w, clientHeight: h } = canvas;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const count = Math.round(Math.min(110, (w * h) / 16000));
      this.particles = Array.from({ length: count }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        z: Math.random(),
        vx: (Math.random() - 0.5) * 0.12,
        vy: -0.04 - Math.random() * 0.22,
        hue: Math.random() < 0.7 ? 190 : Math.random() < 0.6 ? 265 : 315
      }));
    };

    resize();
    this.resizeObserver = new ResizeObserver(resize);
    this.resizeObserver.observe(canvas);

    const root = this.host.nativeElement.querySelector<HTMLElement>('.scene');

    const frame = () => {
      const w = canvas.clientWidth;
      const h = canvas.clientHeight;

      // Ease the mouse so the parallax feels weighty, then publish as CSS variables.
      this.mouse.x += (this.mouse.tx - this.mouse.x) * 0.06;
      this.mouse.y += (this.mouse.ty - this.mouse.y) * 0.06;
      root?.style.setProperty('--mx', this.mouse.x.toFixed(4));
      root?.style.setProperty('--my', this.mouse.y.toFixed(4));

      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = 'lighter';

      for (const p of this.particles) {
        if (!reduced) {
          p.x += p.vx + this.mouse.x * 0.08 * p.z;
          p.y += p.vy;
        }
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        if (p.x < -10) p.x = w + 10;
        if (p.x > w + 10) p.x = -10;

        const r = 0.6 + p.z * 2.2;
        const a = 0.15 + p.z * 0.6;
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r * 5);
        g.addColorStop(0, `hsla(${p.hue}, 100%, 75%, ${a})`);
        g.addColorStop(1, `hsla(${p.hue}, 100%, 60%, 0)`);
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(p.x, p.y, r * 5, 0, Math.PI * 2);
        ctx.fill();
      }

      this.raf = requestAnimationFrame(frame);
    };

    this.zone.runOutsideAngular(() => {
      this.raf = requestAnimationFrame(frame);
    });
  }

  /* ---------- Form ---------- */

  togglePassword(): void {
    this.showPassword.update(v => !v);
  }

  login(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.loading.set(true);
    this.errorMessage.set('');

    const { email, password, remember } = this.loginForm.value;

    try {
      if (remember) {
        localStorage.setItem(REMEMBER_KEY, email);
      } else {
        localStorage.removeItem(REMEMBER_KEY);
      }
    } catch {
      /* storage unavailable */
    }

    this.authService.login({ email, password }).subscribe({
      next: (response) => {
        this.authService.saveLogin(response);
        this.loading.set(false);
        this.router.navigate(['/chat']);
      },
      error: (error: HttpErrorResponse) => {
        this.loading.set(false);
        this.errorMessage.set(
          error.error?.message || 'Something went wrong. Please try again.'
        );
      }
    });
  }
}