import React, { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';
import { SpiderEvent, SpiderSkinId } from '../types';
import { tribalSvgTemplate } from '../assets/skins/tribalVectorSvg';
import { mechaSvgTemplate } from '../assets/skins/mechaVectorSvg';

interface Filament {
  id: string;
  startX: number;
  startY: number;
  endX: number;
  endY: number;
  skin: SpiderSkinId;
  color: string;
}

interface SpiderCanvasProps {
  currentSkin: SpiderSkinId;
  onSpiderCrawlComplete?: (event: SpiderEvent) => void;
}

export const SpiderCanvas: React.FC<SpiderCanvasProps> = ({
  currentSkin,
  onSpiderCrawlComplete
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const actorRef = useRef<HTMLDivElement>(null);
  const rotatorRef = useRef<HTMLDivElement>(null);
  const carrierRef = useRef<HTMLDivElement>(null);
  const spiderSvgContainerRef = useRef<HTMLDivElement>(null);
  const [filaments, setFilaments] = useState<Filament[]>([]);
  const filamentsRef = useRef<Filament[]>([]);

  // Coordinate and orientation tracking
  const spiderPos = useRef({ x: 140, y: 190, angle: 0 });
  const isCrawling = useRef(false);

  // Animation RAF handles
  const mechaWalkRaf = useRef<number | null>(null);
  const mechaIdleRaf = useRef<number | null>(null);
  const mechaWalkStartTime = useRef(0);
  const mechaIdleStartTime = useRef(0);

  const tribalWalkRaf = useRef<number | null>(null);
  const tribalIdleRaf = useRef<number | null>(null);
  const tribalWalkStartTime = useRef(0);
  const tribalIdleStartTime = useRef(0);

  // Active master GSAP tween
  const activeMasterTl = useRef<gsap.core.Timeline | null>(null);

  // Continuous wandering / patrol state
  const isPatrollingRef = useRef(false);
  const patrolTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Load SVG skin template and start idle
  useEffect(() => {
    if (!spiderSvgContainerRef.current) return;

    // Stop all running loops before swapping template
    stopAllGaitLoops();

    if (currentSkin === 'mecha') {
      spiderSvgContainerRef.current.innerHTML = mechaSvgTemplate;
      const svg = spiderSvgContainerRef.current.querySelector('svg');
      if (svg) {
        svg.id = 'live-spider-svg';
        svg.setAttribute('width', '104');
        svg.setAttribute('height', '104');
      }
      setTimeout(startMechaIdle, 100);
    } else {
      spiderSvgContainerRef.current.innerHTML = tribalSvgTemplate;
      const svg = spiderSvgContainerRef.current.querySelector('svg');
      if (svg) {
        svg.id = 'live-spider-svg';
        svg.setAttribute('width', '104');
        svg.setAttribute('height', '104');
      }
      setTimeout(startTribalIdle, 100);
    }

    return () => {
      stopAllGaitLoops();
    };
  }, [currentSkin]);

  // Clean all animation loops
  const stopAllGaitLoops = () => {
    if (mechaWalkRaf.current) {
      cancelAnimationFrame(mechaWalkRaf.current);
      mechaWalkRaf.current = null;
    }
    if (mechaIdleRaf.current) {
      cancelAnimationFrame(mechaIdleRaf.current);
      mechaIdleRaf.current = null;
    }
    if (tribalWalkRaf.current) {
      cancelAnimationFrame(tribalWalkRaf.current);
      tribalWalkRaf.current = null;
    }
    if (tribalIdleRaf.current) {
      cancelAnimationFrame(tribalIdleRaf.current);
      tribalIdleRaf.current = null;
    }
    if (patrolTimerRef.current) {
      clearTimeout(patrolTimerRef.current);
      patrolTimerRef.current = null;
    }
    isPatrollingRef.current = false;
  };

  // --- 1. TRIBAL KINEMATICS ENGINE (24 JOINTS) ---
  // Mô phỏng sinh học loài nhện (Arachnid Biomechanics & Locomotion):
  // - Alternating Tetrapod Gait với sóng Metachronal lan truyền từ chân sau ra chân trước
  // - Bất đối xứng Duty Factor: 62% Stance (chịu tải & đẩy lực) : 38% Swing (nhấc vươn aerial)
  // - Cơ chế co gập thủy lực (Hydraulic flexor knee snap & S-curve extension)
  // - 4 cặp chân chuyên hóa chức năng: Chân 1 (thăm dò & kéo), Chân 2-3 (ổn định ngang), Chân 4 (động cơ đẩy chính)
  // - Chuyển động đa trục thân mình (Heave 2w, Yaw w, Roll w, Abdomen soft-inertia lag)
  const startTribalIdle = () => {
    if (isCrawling.current || currentSkin !== 'tribal') return;
    if (tribalIdleRaf.current) cancelAnimationFrame(tribalIdleRaf.current);
    tribalIdleStartTime.current = performance.now();

    const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
    if (!liveSvg) return;

    const setJ = (id: string, delta: number) => {
      const el = liveSvg.querySelector<HTMLElement>(`#${id}`);
      if (el) el.style.transform = `rotate(${delta}deg)`;
    };

    const idleStep = (now: number) => {
      if (isCrawling.current || currentSkin !== 'tribal') return;
      const t = (now - tribalIdleStartTime.current) / 1000;

      // Nhịp thở sinh học chậm rãi (0.9Hz)
      const breath = Math.sin(t * 1.1);
      // Rung xúc biện / nanh vi mô
      const fangMicro = Math.sin(t * 2.2) * 1.5;

      // Chân trước L1/R1 nhấc nhẹ thăm dò địa hình ngẫu nhiên (Sensory Palpation)
      const palpL = Math.max(0, Math.sin(t * 0.7 - 0.5)) * 3.5;
      const palpR = Math.max(0, Math.sin(t * 0.65 + 1.2)) * 3.5;

      setJ('tribal_L1_s1', Math.sin(t * 0.6) * 1.5);
      setJ('tribal_L1_s2', -breath * 1.8 - palpL);
      setJ('tribal_L1_s3', breath * 1.2 + palpL * 0.8);

      setJ('tribal_R1_s1', -Math.sin(t * 0.6) * 1.5);
      setJ('tribal_R1_s2', breath * 1.8 + palpR);
      setJ('tribal_R1_s3', -breath * 1.2 - palpR * 0.8);

      // Chân giữa co dãn giữ trọng tâm
      setJ('tribal_L2_s2', -breath * 1.0);
      setJ('tribal_R2_s2', breath * 1.0);
      setJ('tribal_L3_s2', breath * 1.0);
      setJ('tribal_R3_s2', -breath * 1.0);

      // Chân sau điều chỉnh thế đứng
      setJ('tribal_L4_s1', -Math.sin(t * 0.5) * 1.2);
      setJ('tribal_L4_s2', breath * 2.0);
      setJ('tribal_L4_s3', -breath * 1.5);

      setJ('tribal_R4_s1', Math.sin(t * 0.5) * 1.2);
      setJ('tribal_R4_s2', -breath * 2.0);
      setJ('tribal_R4_s3', breath * 1.5);

      // Nanh hé mở vi mô
      const fangL = liveSvg.querySelector<HTMLElement>('#tribal_fang_l');
      const fangR = liveSvg.querySelector<HTMLElement>('#tribal_fang_r');
      if (fangL) fangL.style.transform = `rotate(${fangMicro}deg)`;
      if (fangR) fangR.style.transform = `rotate(${-fangMicro}deg)`;

      // Bụng phập phồng hô hấp sinh học
      const body = liveSvg.querySelector<HTMLElement>('#tribal-body-core');
      if (body) {
        body.style.transform = `scaleY(${1.0 + breath * 0.035}) scaleX(${1.0 - breath * 0.015})`;
      }
      const aura = liveSvg.querySelector<SVGElement>('#tribal-aura');
      if (aura) {
        aura.setAttribute('rx', String(145 + breath * 6));
        aura.setAttribute('ry', String(185 + breath * 8));
      }

      tribalIdleRaf.current = requestAnimationFrame(idleStep);
    };

    tribalIdleRaf.current = requestAnimationFrame(idleStep);
  };

  const stopTribalIdle = () => {
    if (tribalIdleRaf.current) {
      cancelAnimationFrame(tribalIdleRaf.current);
      tribalIdleRaf.current = null;
    }
  };

  const startTribalWalk = (speedMultiplier = 1.0) => {
    stopTribalIdle();
    if (tribalWalkRaf.current) cancelAnimationFrame(tribalWalkRaf.current);
    tribalWalkStartTime.current = performance.now();

    const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
    if (!liveSvg) return;

    const setJ = (id: string, delta: number) => {
      const el = liveSvg.querySelector<HTMLElement>(`#${id}`);
      if (el) el.style.transform = `rotate(${delta}deg)`;
    };

    const isSprint = speedMultiplier > 1.2;
    const strideSpeed = 3.2 * speedMultiplier;
    const amp = isSprint ? 1.25 : 1.0;

    // Chuỗi pha Metachronal sinh học:
    // Nhóm A: R4 (chân sau phải) dẫn đầu -> L3 -> R2 -> L1 (chân trước trái vươn kéo)
    // Nhóm B: Đối xứng ngược pha 180° (PI): L4 -> R3 -> L2 -> R1
    const bioPhases = {
      R4: 0.00 * Math.PI,
      L3: 0.16 * Math.PI,
      R2: 0.32 * Math.PI,
      L1: 0.48 * Math.PI,

      L4: 1.00 * Math.PI,
      R3: 1.16 * Math.PI,
      L2: 1.32 * Math.PI,
      R1: 1.48 * Math.PI,
    };

    // Hàm tính toán động học chi nhện sinh học chính xác
    const calcBioMotion = (phi: number, ramp: number) => {
      const norm = (((phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)) / (2 * Math.PI);
      const SWING_RATIO = 0.38; // 38% Pha Lăng : 62% Pha Trụ

      let swing: number;
      let lift: number;
      let clawTuck: number;

      if (norm < SWING_RATIO) {
        // --- SWING: Nhấc vươn aerial ---
        const u = norm / SWING_RATIO;
        // Gập gối nhấc bổng nhanh tới đỉnh ở u ~ 0.40 (flexor contraction) rồi hạ êm
        lift = Math.sin(Math.PI * Math.pow(u, 0.72)) * ramp;
        // Vươn chân theo đường cong S-curve mượt mà bằng áp suất thủy lực
        const sCurve = 3 * u * u - 2 * u * u * u;
        swing = (-1.0 + 2.0 * sCurve) * ramp;
        // Móng vuốt khép lại lúc vừa nhấc để tránh va chạm, xòe ra trước khi tiếp đất
        clawTuck = (u < 0.5 ? -1.0 : 0.6) * lift;
      } else {
        // --- STANCE: Tiếp đất miết đẩy lực ---
        const v = (norm - SWING_RATIO) / (1.0 - SWING_RATIO);
        // Chân bám đất, nhún giảm chấn sinh học vi mô
        lift = (-0.06 * Math.sin(Math.PI * v)) * ramp;
        // Miết chân đều đặn đẩy cơ thể tiến tới
        swing = (1.0 - 2.0 * v) * ramp;
        // Vuốt bám chặt mặt sàn
        clawTuck = 0.25 * Math.sin(Math.PI * v) * ramp;
      }

      return { swing, lift, clawTuck };
    };

    const walkStep = (now: number) => {
      if (!isCrawling.current) return;
      const ramp = isSprint ? 1.0 : Math.min(1, (now - tribalWalkStartTime.current) / 180);
      const t = ((now - tribalWalkStartTime.current) / 360) * strideSpeed;

      // 1. CẶP CHÂN 1 (Prolegs - Thăm dò & Kéo): Khớp gối gập cao nhất, có vi rung thăm dò
      const mL1 = calcBioMotion(t + bioPhases.L1, ramp);
      const mR1 = calcBioMotion(t + bioPhases.R1, ramp);
      const feelerFlutter = Math.sin(t * 3.5) * 1.5 * ramp;

      setJ('tribal_L1_s1', (-19 * mL1.swing + feelerFlutter) * amp);
      setJ('tribal_L1_s2', (-28 * mL1.lift + 4 * mL1.swing) * amp);
      setJ('tribal_L1_s3', (16 * mL1.swing + 16 * mL1.lift + 6 * mL1.clawTuck) * amp);

      setJ('tribal_R1_s1', (19 * mR1.swing - feelerFlutter) * amp);
      setJ('tribal_R1_s2', (28 * mR1.lift - 4 * mR1.swing) * amp);
      setJ('tribal_R1_s3', (-16 * mR1.swing - 16 * mR1.lift - 6 * mR1.clawTuck) * amp);

      // 2. CẶP CHÂN 2 (Anterior Lateral - Nâng đỡ & Cân bằng xoay)
      const mL2 = calcBioMotion(t + bioPhases.L2, ramp);
      const mR2 = calcBioMotion(t + bioPhases.R2, ramp);

      setJ('tribal_L2_s1', -15 * mL2.swing * amp);
      setJ('tribal_L2_s2', (-22 * mL2.lift + 2 * mL2.swing) * amp);
      setJ('tribal_L2_s3', (13 * mL2.swing + 10 * mL2.lift) * amp);

      setJ('tribal_R2_s1', 15 * mR2.swing * amp);
      setJ('tribal_R2_s2', (22 * mR2.lift - 2 * mR2.swing) * amp);
      setJ('tribal_R2_s3', (-13 * mR2.swing - 10 * mR2.lift) * amp);

      // 3. CẶP CHÂN 3 (Posterior Lateral - Đòn bẩy chống lật)
      const mL3 = calcBioMotion(t + bioPhases.L3, ramp);
      const mR3 = calcBioMotion(t + bioPhases.R3, ramp);

      setJ('tribal_L3_s1', -16 * mL3.swing * amp);
      setJ('tribal_L3_s2', (22 * mL3.lift - 3 * mL3.swing) * amp);
      setJ('tribal_L3_s3', (-14 * mL3.swing - 11 * mL3.lift) * amp);

      setJ('tribal_R3_s1', 16 * mR3.swing * amp);
      setJ('tribal_R3_s2', (-22 * mR3.lift + 3 * mR3.swing) * amp);
      setJ('tribal_R3_s3', (14 * mR3.swing + 11 * mR3.lift) * amp);

      // 4. CẶP CHÂN 4 (Posterior Pushers - Động cơ đẩy chính về phía trước)
      const mL4 = calcBioMotion(t + bioPhases.L4, ramp);
      const mR4 = calcBioMotion(t + bioPhases.R4, ramp);

      setJ('tribal_L4_s1', -22 * mL4.swing * amp);
      setJ('tribal_L4_s2', (28 * mL4.lift - 5 * mL4.swing) * amp);
      setJ('tribal_L4_s3', (-18 * mL4.swing - 14 * mL4.lift) * amp);

      setJ('tribal_R4_s1', 22 * mR4.swing * amp);
      setJ('tribal_R4_s2', (-28 * mR4.lift + 5 * mR4.swing) * amp);
      setJ('tribal_R4_s3', (18 * mR4.swing + 14 * mR4.lift) * amp);

      // 5. ĐỘNG HỌC THÂN MÌNH (Cephalothorax 3D Heave, Yaw & Roll)
      const master = liveSvg.querySelector<SVGElement>('#tribal-spider-master');
      if (master) {
        // Nhấp nhô đứng tần số kép (2 nhịp / chu kỳ)
        const bobY = Math.sin(t * 2) * 2.6 * ramp;
        // Đầu nhện lắc nhẹ theo hướng chân trước đang kéo (Yaw)
        const headYaw = Math.sin(t) * 1.8 * ramp;
        // Thân nghiêng nhẹ đối xứng theo nhóm chân tiếp đất (Roll)
        const roll = Math.cos(t) * 1.1 * ramp;
        master.setAttribute('transform', `translate(0, ${bobY}) rotate(${headYaw + roll}, 479, 450)`);
      }

      // 6. ĐỘ ĐÀN HỒI BỤNG NHỆN (Viscoelastic Opisthosoma Lag)
      const body = liveSvg.querySelector<HTMLElement>('#tribal-body-core');
      if (body) {
        const abdomenJiggle = Math.sin(t - 0.4) * 1.8 * ramp;
        const abdomenScaleY = 1.0 + Math.sin(t * 2 - 0.3) * 0.03 * ramp;
        body.style.transform = `scaleY(${abdomenScaleY}) rotate(${abdomenJiggle}deg)`;
      }

      // 7. RUNG NAI & BẮN RÂU (Chelicerae micro-flutter)
      const fangL = liveSvg.querySelector<HTMLElement>('#tribal_fang_l');
      const fangR = liveSvg.querySelector<HTMLElement>('#tribal_fang_r');
      if (fangL) fangL.style.transform = `rotate(${Math.sin(t * 2.5) * 3 * ramp}deg)`;
      if (fangR) fangR.style.transform = `rotate(${-Math.sin(t * 2.5) * 3 * ramp}deg)`;

      tribalWalkRaf.current = requestAnimationFrame(walkStep);
    };

    tribalWalkRaf.current = requestAnimationFrame(walkStep);
  };

  const stopTribalWalk = () => {
    if (tribalWalkRaf.current) {
      cancelAnimationFrame(tribalWalkRaf.current);
      tribalWalkRaf.current = null;
    }
    const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
    if (liveSvg) {
      liveSvg.querySelectorAll<HTMLElement>('.sp-tribal-joint').forEach(el => {
        el.style.transform = 'rotate(0deg)';
      });
      const master = liveSvg.querySelector('#tribal-spider-master');
      if (master) {
        master.setAttribute('transform', 'translate(0, 0)');
      }
    }
  };

  // --- 2. MECHA CAD RIG KINEMATICS ENGINE (29 JOINTS) ---
  // Thiết kế động học rô-bốt nhện sinh học (Bio-Robotic Spider Articulation):
  // - 29 khớp chuyển động độc lập (5 bậc tự do cho mỗi chân: s1 -> s5)
  // - Sóng bước Alternating Tetrapod Metachronal đối xứng
  // - Tỷ lệ 62% Stance (xi lanh miết sàn) : 38% Swing (nâng servo gối)
  // - Bù trừ góc tiếp đất tự động ở khớp cẳng s4 và vuốt s5 (Auto-leveling end-effector)
  // - Thân ngực nhấp nhô Heave tần số kép, xoay đầu Yaw & nghiêng Roll đồng bộ
  const startMechaIdle = () => {
    if (isCrawling.current || currentSkin !== 'mecha') return;
    if (mechaIdleRaf.current) cancelAnimationFrame(mechaIdleRaf.current);
    mechaIdleStartTime.current = performance.now();

    const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
    if (!liveSvg) return;

    const restAngles: Record<string, number> = {};
    liveSvg.querySelectorAll<SVGElement>('.sp-joint').forEach(el => {
      restAngles[el.id] = parseFloat(el.getAttribute('data-rest') || '0');
    });

    const spiderRoot = liveSvg.querySelector('#spider-root');
    const antEl = liveSvg.querySelector('#ANT_s1');

    const setJ = (id: string, delta: number) => {
      const el = liveSvg.querySelector(`#${id}`);
      if (el && restAngles[id] !== undefined) {
        el.setAttribute('transform', `rotate(${restAngles[id] + delta})`);
      }
    };

    const idleStep = (now: number) => {
      if (isCrawling.current || currentSkin !== 'mecha') return;
      const t = (now - mechaIdleStartTime.current) / 1000;

      // Nhịp thở hệ thống thủy lực (0.8Hz)
      const breath = Math.sin(t * 1.0);
      // Quét radar râu sensor
      const radarSweep = Math.sin(t * 0.9) * 3.5;

      if (spiderRoot) {
        spiderRoot.setAttribute('transform', `translate(0, ${1.2 * breath}) rotate(${0.4 * Math.sin(t * 0.5)})`);
      }
      if (antEl && restAngles['ANT_s1'] !== undefined) {
        antEl.setAttribute('transform', `rotate(${restAngles['ANT_s1'] + radarSweep})`);
      }

      // Vi điều chỉnh servo các chân khi đứng nghỉ (Micro-actuator holding torque)
      const micro1 = Math.sin(t * 0.6) * 1.5;
      const micro4 = Math.cos(t * 0.7) * 1.8;

      setJ('L1_s1', micro1);
      setJ('L1_s2', -breath * 1.5);
      setJ('L1_s3', breath * 1.2);

      setJ('R1_s1', -micro1);
      setJ('R1_s2', breath * 1.5);
      setJ('R1_s3', -breath * 1.2);

      setJ('L4_s1', -micro4);
      setJ('L4_s2', breath * 1.6);
      setJ('R4_s1', micro4);
      setJ('R4_s2', -breath * 1.6);

      mechaIdleRaf.current = requestAnimationFrame(idleStep);
    };

    mechaIdleRaf.current = requestAnimationFrame(idleStep);
  };

  const stopMechaIdle = () => {
    if (mechaIdleRaf.current) {
      cancelAnimationFrame(mechaIdleRaf.current);
      mechaIdleRaf.current = null;
    }
  };

  const startMechaWalk = (speedMultiplier = 1.0) => {
    stopMechaIdle();
    if (mechaWalkRaf.current) cancelAnimationFrame(mechaWalkRaf.current);
    mechaWalkStartTime.current = performance.now();

    const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
    if (!liveSvg) return;

    const restAngles: Record<string, number> = {};
    liveSvg.querySelectorAll<SVGElement>('.sp-joint').forEach(el => {
      restAngles[el.id] = parseFloat(el.getAttribute('data-rest') || '0');
    });

    const spiderRoot = liveSvg.querySelector('#spider-root');
    const isSprint = speedMultiplier > 1.2;
    const strideSpeed = 3.2 * speedMultiplier;
    const amp = isSprint ? 1.25 : 1.0;

    const setJ = (id: string, delta: number) => {
      const el = liveSvg.querySelector(`#${id}`);
      if (el && restAngles[id] !== undefined) {
        el.setAttribute('transform', `rotate(${restAngles[id] + delta})`);
      }
    };

    // Sóng bước Metachronal sinh học chính xác
    const bioPhases = {
      R4: 0.00 * Math.PI,
      L3: 0.16 * Math.PI,
      R2: 0.32 * Math.PI,
      L1: 0.48 * Math.PI,

      L4: 1.00 * Math.PI,
      R3: 1.16 * Math.PI,
      L2: 1.32 * Math.PI,
      R1: 1.48 * Math.PI,
    };

    const calcBioMotion = (phi: number, ramp: number) => {
      const norm = (((phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI)) / (2 * Math.PI);
      const SWING_RATIO = 0.38;

      let swing: number;
      let lift: number;
      let clawTuck: number;

      if (norm < SWING_RATIO) {
        const u = norm / SWING_RATIO;
        lift = Math.sin(Math.PI * Math.pow(u, 0.72)) * ramp;
        const sCurve = 3 * u * u - 2 * u * u * u;
        swing = (-1.0 + 2.0 * sCurve) * ramp;
        clawTuck = (u < 0.5 ? -1.0 : 0.6) * lift;
      } else {
        const v = (norm - SWING_RATIO) / (1.0 - SWING_RATIO);
        lift = (-0.06 * Math.sin(Math.PI * v)) * ramp;
        swing = (1.0 - 2.0 * v) * ramp;
        clawTuck = 0.25 * Math.sin(Math.PI * v) * ramp;
      }

      return { swing, lift, clawTuck };
    };

    const step = (now: number) => {
      if (!isCrawling.current) return;
      const ramp = isSprint ? 1.0 : Math.min(1, (now - mechaWalkStartTime.current) / 180);
      const t = ((now - mechaWalkStartTime.current) / 360) * strideSpeed;

      // 1. CẶP CHÂN 4 (Pushers - Xi lanh đẩy công suất lớn)
      const mL4 = calcBioMotion(t + bioPhases.L4, ramp);
      const mR4 = calcBioMotion(t + bioPhases.R4, ramp);

      setJ('L4_s1', -20 * mL4.swing * amp);
      setJ('L4_s2', -26 * mL4.lift * amp);
      setJ('L4_s3', (16 * mL4.swing + 12 * mL4.lift) * amp);
      setJ('L4_s4', (12 * mL4.swing + 10 * mL4.lift) * amp);
      setJ('L4_s5', (9 * mL4.swing + 8 * mL4.lift + 6 * mL4.clawTuck) * amp);

      setJ('R4_s1', 20 * mR4.swing * amp);
      setJ('R4_s2', 26 * mR4.lift * amp);
      setJ('R4_s3', (-16 * mR4.swing - 12 * mR4.lift) * amp);
      setJ('R4_s4', (-12 * mR4.swing - 10 * mR4.lift) * amp);
      setJ('R4_s5', (-9 * mR4.swing - 8 * mR4.lift - 6 * mR4.clawTuck) * amp);

      // 2. CẶP CHÂN 3 (Posterior Lateral - Đòn bẩy chống xoay)
      const mL3 = calcBioMotion(t + bioPhases.L3, ramp);
      const mR3 = calcBioMotion(t + bioPhases.R3, ramp);

      setJ('L3_s1', -16 * mL3.swing * amp);
      setJ('L3_s2', -20 * mL3.lift * amp);
      setJ('L3_s3', (12 * mL3.swing + 8 * mL3.lift) * amp);
      setJ('L3_s4', (9 * mL3.swing + 6 * mL3.lift) * amp);
      setJ('L3_s5', (7 * mL3.swing + 5 * mL3.lift) * amp);

      setJ('R3_s1', 16 * mR3.swing * amp);
      setJ('R3_s2', 20 * mR3.lift * amp);
      setJ('R3_s3', (-12 * mR3.swing - 8 * mR3.lift) * amp);
      setJ('R3_s4', (-9 * mR3.swing - 6 * mR3.lift) * amp);
      setJ('R3_s5', (-7 * mR3.swing - 5 * mR3.lift) * amp);

      // 3. CẶP CHÂN 2 (Anterior Lateral - Ổn định nâng đỡ)
      const mL2 = calcBioMotion(t + bioPhases.L2, ramp);
      const mR2 = calcBioMotion(t + bioPhases.R2, ramp);

      setJ('L2_s1', -15 * mL2.swing * amp);
      setJ('L2_s2', -21 * mL2.lift * amp);
      setJ('L2_s3', (13 * mL2.swing + 9 * mL2.lift) * amp);
      setJ('L2_s4', (10 * mL2.swing + 7 * mL2.lift) * amp);
      setJ('L2_s5', (8 * mL2.swing + 6 * mL2.lift) * amp);

      setJ('R2_s1', 15 * mR2.swing * amp);
      setJ('R2_s2', 21 * mR2.lift * amp);
      setJ('R2_s3', (-13 * mR2.swing - 9 * mR2.lift) * amp);
      setJ('R2_s4', (-10 * mR2.swing - 7 * mR2.lift) * amp);
      setJ('R2_s5', (-8 * mR2.swing - 6 * mR2.lift) * amp);

      // 4. CẶP CHÂN 1 (Prolegs - Dò đường & Kéo tới)
      const mL1 = calcBioMotion(t + bioPhases.L1, ramp);
      const mR1 = calcBioMotion(t + bioPhases.R1, ramp);
      const feelerFlutter = Math.sin(t * 3.5) * 1.5 * ramp;

      setJ('L1_s1', (-18 * mL1.swing + feelerFlutter) * amp);
      setJ('L1_s2', (24 * mL1.lift - 4 * mL1.swing) * amp);
      setJ('L1_s3', (-14 * mL1.swing - 12 * mL1.lift) * amp);
      setJ('L1_s4', (-11 * mL1.swing - 9 * mL1.lift) * amp);
      setJ('L1_s5', (-8 * mL1.swing - 7 * mL1.lift - 5 * mL1.clawTuck) * amp);

      setJ('R1_s1', (18 * mR1.swing - feelerFlutter) * amp);
      setJ('R1_s2', (-24 * mR1.lift + 4 * mR1.swing) * amp);
      setJ('R1_s3', (14 * mR1.swing + 12 * mR1.lift) * amp);
      setJ('R1_s4', (11 * mR1.swing + 9 * mR1.lift) * amp);
      setJ('R1_s5', (8 * mR1.swing + 7 * mR1.lift + 5 * mR1.clawTuck) * amp);

      // 5. RADAR ANTENNA SCANNER
      setJ('ANT_s1', Math.sin(t * 1.8) * 6 * ramp);

      // 6. KHUNG GẦM RÔ-BỐT (Chassis 3D Heave, Yaw & Roll)
      if (spiderRoot) {
        const heaveY = Math.sin(t * 2) * 2.8 * ramp;
        const yaw = Math.sin(t) * 1.9 * ramp;
        const roll = Math.cos(t) * 1.2 * ramp;
        spiderRoot.setAttribute('transform', `translate(0, ${heaveY}) rotate(${yaw + roll})`);
      }

      mechaWalkRaf.current = requestAnimationFrame(step);
    };

    mechaWalkRaf.current = requestAnimationFrame(step);
  };

  const stopMechaWalk = () => {
    if (mechaWalkRaf.current) {
      cancelAnimationFrame(mechaWalkRaf.current);
      mechaWalkRaf.current = null;
    }
    const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
    if (!liveSvg) return;

    liveSvg.querySelectorAll<SVGElement>('.sp-joint').forEach(el => {
      (el as any).style.transform = '';
      const rest = parseFloat(el.getAttribute('data-rest') || '0');
      el.setAttribute('transform', `rotate(${rest})`);
    });

    const spiderRoot = liveSvg.querySelector('#spider-root');
    if (spiderRoot) {
      spiderRoot.setAttribute('transform', 'translate(0, 0) rotate(0)');
    }
  };

  // Footprint / Reticle effects (Disabled to keep spider body clean without distracting blinking target reticles)
  const leaveFootprint = (_x: number, _y: number) => {
    // Disabled as requested: no blinking target pointer / reticle on spider
    return;
  };

  // Parabolic shockwave
  const spawnShockwave = (x: number, y: number) => {
    if (!containerRef.current) return;
    const wave = document.createElement('div');
    wave.className = `leap-shockwave ${currentSkin === 'mecha' ? 'mecha-shockwave' : 'tribal-shockwave'}`;
    wave.style.left = `${x}px`;
    wave.style.top = `${y}px`;
    containerRef.current.appendChild(wave);
    setTimeout(() => wave.remove(), 450);
  };

  // Predatory In-Flight Claw Stance during Pounce Leap
  const triggerPounceFlightStance = () => {
    const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
    if (!liveSvg) return;

    if (currentSkin === 'mecha') {
      if (mechaWalkRaf.current) { cancelAnimationFrame(mechaWalkRaf.current); mechaWalkRaf.current = null; }
      const restAngles: Record<string, number> = {};
      liveSvg.querySelectorAll<SVGElement>('.sp-joint').forEach(el => {
        restAngles[el.id] = parseFloat(el.getAttribute('data-rest') || '0');
      });
      const setJ = (id: string, delta: number) => {
        const el = liveSvg.querySelector(`#${id}`);
        if (el && restAngles[id] !== undefined) {
          el.setAttribute('transform', `rotate(${restAngles[id] + delta})`);
        }
      };
      // Front scythes flare open forward to grasp prey
      setJ('L4_s1', 22); setJ('L4_s2', -18); setJ('L4_s3', 14);
      setJ('R4_s1', -22); setJ('R4_s2', 18); setJ('R4_s3', -14);
      // Middle legs aerodynamic tuck
      setJ('L3_s1', -10); setJ('R3_s1', 10);
      setJ('L2_s1', -8);  setJ('R2_s1', 8);
      // Rear claws stretch backward for thrust
      setJ('L1_s1', -16); setJ('L1_s2', 18);
      setJ('R1_s1', 16);  setJ('R1_s2', -18);

    } else {
      if (tribalWalkRaf.current) { cancelAnimationFrame(tribalWalkRaf.current); tribalWalkRaf.current = null; }
      const setJ = (id: string, delta: number) => {
        const el = liveSvg.querySelector<HTMLElement>(`#${id}`);
        if (el) el.style.transform = `rotate(${delta}deg)`;
      };
      // Front sickles splay aggressively
      setJ('tribal_L1_s1', -26); setJ('tribal_L1_s2', -24); setJ('tribal_L1_s3', 18);
      setJ('tribal_R1_s1', 26);  setJ('tribal_R1_s2', 24);  setJ('tribal_R1_s3', -18);
      // Rear sickles flare
      setJ('tribal_L4_s1', -20); setJ('tribal_R4_s1', 20);
      const fangL = liveSvg.querySelector<HTMLElement>('#tribal_fang_l');
      const fangR = liveSvg.querySelector<HTMLElement>('#tribal_fang_r');
      if (fangL) fangL.style.transform = 'rotate(22deg)';
      if (fangR) fangR.style.transform = 'rotate(-22deg)';
    }
  };

  // Predatory Impact Settling when landing on keyword
  const triggerPounceImpactStance = () => {
    if (currentSkin === 'mecha') {
      stopMechaWalk();
      setTimeout(startMechaIdle, 300);
    } else {
      stopTribalWalk();
      setTimeout(startTribalIdle, 300);
    }
  };

  // Reset previous motion safely
  const abortPreviousMotionAndReset = () => {
    isPatrollingRef.current = false;
    if (patrolTimerRef.current) {
      clearTimeout(patrolTimerRef.current);
      patrolTimerRef.current = null;
    }
    if (activeMasterTl.current) {
      activeMasterTl.current.kill();
      activeMasterTl.current = null;
    }
    const actor = actorRef.current;
    const rotator = rotatorRef.current;
    const carrier = carrierRef.current;

    if (actor) {
      gsap.killTweensOf(actor);
      actor.classList.remove('spider-in-flight', 'spider-landed');
      const curX = gsap.getProperty(actor, 'x');
      const curY = gsap.getProperty(actor, 'y');
      if (typeof curX === 'number' && !isNaN(curX)) spiderPos.current.x = curX;
      if (typeof curY === 'number' && !isNaN(curY)) spiderPos.current.y = curY;
      gsap.set(actor, { scale: 1 });
    }
    if (rotator) gsap.killTweensOf(rotator);
    if (carrier) {
      gsap.killTweensOf(carrier);
      gsap.set(carrier, { y: 0 });
    }

    if (currentSkin === 'mecha') stopMechaWalk();
    else stopTribalWalk();

    document.querySelectorAll('mark.spider-target').forEach(m => {
      m.classList.remove('spider-struck');
    });

    isCrawling.current = false;
  };

  // Start rapid cadence leg gait
  const startLegSprintAnimation = (speedMult = 2.4) => {
    if (currentSkin === 'mecha') {
      startMechaWalk(speedMult);
    } else {
      startTribalWalk(speedMult);
    }
  };

  // Apply sentiment lighting to eyes/sensors
  const applySentimentEyes = (sentiment?: string) => {
    const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
    if (!liveSvg) return;

    if (currentSkin === 'mecha') {
      let color = '#00E5FF';
      if (sentiment === 'negative') color = '#FF1744';
      else if (sentiment === 'neutral') color = '#FFEA00';
      liveSvg.querySelectorAll<HTMLElement>('.mecha-sensor').forEach(s => {
        gsap.to(s, { fill: color, duration: 0.3 });
      });
    } else {
      let color = '#00E5FF';
      if (sentiment === 'negative') color = '#EC4899';
      else if (sentiment === 'neutral') color = '#C084FC';
      const fangL = liveSvg.querySelector('#tribal_fang_l polygon');
      const fangR = liveSvg.querySelector('#tribal_fang_r polygon');
      const nozzle = liveSvg.querySelector('#silk-nozzle');
      if (fangL) gsap.to(fangL, { fill: color, duration: 0.3 });
      if (fangR) gsap.to(fangR, { fill: color, duration: 0.3 });
      if (nozzle) gsap.to(nozzle, { fill: color, duration: 0.3 });
    }
  };

  // --- UNIFIED CONTINUOUS SPRINT & PARABOLIC POUNCE LEAP ENGINE ---
  const executeContinuousSprintAndLeap = (
    destX: number,
    destY: number,
    onImpactCallback?: () => void,
    onCompleteCallback?: () => void
  ) => {
    isCrawling.current = true;
    const actor = actorRef.current;
    const rotator = rotatorRef.current;
    const carrier = carrierRef.current;
    if (!actor || !rotator || !carrier) return;

    const startX = spiderPos.current.x;
    const startY = spiderPos.current.y;
    const deltaX = destX - startX;
    const deltaY = destY - startY;
    const totalDist = Math.hypot(deltaX, deltaY);

    if (totalDist < 5) {
      isCrawling.current = false;
      if (onImpactCallback) onImpactCallback();
      if (onCompleteCallback) onCompleteCallback();
      return;
    }

    let targetAngle = Math.atan2(deltaY, deltaX) * (180 / Math.PI) + 90;
    let angleDiff = targetAngle - spiderPos.current.angle;
    while (angleDiff > 180) angleDiff -= 360;
    while (angleDiff < -180) angleDiff += 360;
    targetAngle = spiderPos.current.angle + angleDiff;

    // Footprints tracking during movement
    const footprintInterval = 140;
    const footprintTimer = setInterval(() => {
      if (!isCrawling.current || !actorRef.current || !containerRef.current) {
        clearInterval(footprintTimer);
        return;
      }
      const aRect = actorRef.current.getBoundingClientRect();
      const cRect = containerRef.current.getBoundingClientRect();
      leaveFootprint(aRect.left - cRect.left + 52, aRect.top - cRect.top + 52);
    }, footprintInterval);

    const unifiedTl = gsap.timeline({
      onComplete: () => {
        clearInterval(footprintTimer);
        if (currentSkin === 'mecha') stopMechaWalk();
        else stopTribalWalk();
        spiderPos.current.x = destX;
        spiderPos.current.y = destY;
        spiderPos.current.angle = targetAngle;
        actor.classList.remove('spider-in-flight', 'spider-landed');
        isCrawling.current = false;
        activeMasterTl.current = null;
        if (onCompleteCallback) onCompleteCallback();
      }
    });
    activeMasterTl.current = unifiedTl;

    // 1. Instant turn towards target keyword (50ms)
    unifiedTl.to(rotator, {
      rotation: targetAngle,
      duration: 0.05,
      ease: 'power2.out'
    }, 0);

    if (totalDist > 75) {
      // Long distance: Sprint until 50px away then parabolic leap
      const leapDist = 50;
      const sprintX = destX - (deltaX / totalDist) * leapDist;
      const sprintY = destY - (deltaY / totalDist) * leapDist;
      const sprintRunDist = Math.hypot(sprintX - startX, sprintY - startY);
      const sprintDuration = Math.max(0.24, Math.min(0.40, sprintRunDist / 550));
      const leapDuration = 0.16;

      // Start rapid leg sprint (2.4x frequency)
      unifiedTl.call(() => {
        startLegSprintAnimation(2.4);
      }, undefined, 0.04);

      // Sprint to (sprintX, sprintY)
      unifiedTl.to(actor, {
        x: sprintX,
        y: sprintY,
        duration: sprintDuration,
        ease: 'power2.inOut'
      }, 0.04);

      const launchTime = 0.04 + sprintDuration;

      // At launch point: switch to predatory In-Flight stance & lift into air
      unifiedTl.call(() => {
        actor.classList.add('spider-in-flight');
        triggerPounceFlightStance();
      }, undefined, launchTime);

      // Parabolic jump to (destX, destY)
      unifiedTl.to(actor, {
        x: destX,
        y: destY,
        duration: leapDuration,
        ease: 'power3.out'
      }, launchTime);

      // 3D Z-Axis scale: apex 1.28x -> impact compression 0.90x -> rebound 1.0x
      unifiedTl.to(actor, {
        scale: 1.28,
        duration: leapDuration * 0.45,
        ease: 'power2.out'
      }, launchTime)
      .to(actor, {
        scale: 0.90,
        duration: leapDuration * 0.55,
        ease: 'power3.in',
        onComplete: () => {
          actor.classList.remove('spider-in-flight');
          actor.classList.add('spider-landed');
          triggerPounceImpactStance();
          spawnShockwave(destX, destY);
          leaveFootprint(destX, destY);
          if (onImpactCallback) onImpactCallback();
        }
      }, launchTime + leapDuration * 0.45)
      .to(actor, {
        scale: 1.0,
        duration: 0.22,
        ease: 'elastic.out(1.3, 0.35)'
      }, launchTime + leapDuration);

      // Chassis suspension recoil
      unifiedTl.to(carrier, { y: -9, duration: leapDuration * 0.45, ease: 'power2.out' }, launchTime)
               .to(carrier, { y: 5, duration: leapDuration * 0.55, ease: 'power3.in' }, launchTime + leapDuration * 0.45)
               .to(carrier, { y: 0, duration: 0.22, ease: 'elastic.out(1.2, 0.3)' }, launchTime + leapDuration);

    } else {
      // Short distance (<= 75px): Direct pounce leap
      const leapDuration = 0.16;
      const launchTime = 0.04;

      unifiedTl.call(() => {
        actor.classList.add('spider-in-flight');
        triggerPounceFlightStance();
      }, undefined, launchTime);

      unifiedTl.to(actor, {
        x: destX,
        y: destY,
        duration: leapDuration,
        ease: 'power3.out'
      }, launchTime);

      unifiedTl.to(actor, {
        scale: 1.28,
        duration: leapDuration * 0.45,
        ease: 'power2.out'
      }, launchTime)
      .to(actor, {
        scale: 0.90,
        duration: leapDuration * 0.55,
        ease: 'power3.in',
        onComplete: () => {
          actor.classList.remove('spider-in-flight');
          actor.classList.add('spider-landed');
          triggerPounceImpactStance();
          spawnShockwave(destX, destY);
          leaveFootprint(destX, destY);
          if (onImpactCallback) onImpactCallback();
        }
      }, launchTime + leapDuration * 0.45)
      .to(actor, {
        scale: 1.0,
        duration: 0.22,
        ease: 'elastic.out(1.3, 0.35)'
      }, launchTime + leapDuration);

      unifiedTl.to(carrier, { y: -9, duration: leapDuration * 0.45, ease: 'power2.out' }, launchTime)
               .to(carrier, { y: 5, duration: leapDuration * 0.55, ease: 'power3.in' }, launchTime + leapDuration * 0.45)
               .to(carrier, { y: 0, duration: 0.22, ease: 'elastic.out(1.2, 0.3)' }, launchTime + leapDuration);
    }
  };

  // --- CRAWL TO TARGET KEYWORD WITH RECOIL AND TRANSIENT SILK ---
  const crawlToKeyword = (
    targetEl: HTMLElement,
    targetIndex: number,
    decisionNodeEl?: HTMLElement,
    eventData?: Partial<SpiderEvent>
  ) => {
    if (!containerRef.current || !actorRef.current || !rotatorRef.current) return;

    // Reset previous motion safely
    abortPreviousMotionAndReset();

    const containerRect = containerRef.current.getBoundingClientRect();
    const targetRect = targetEl.getBoundingClientRect();

    // Landing position: elevated 8px so front fangs grasp word cleanly
    const landingX = targetRect.left + targetRect.width / 2 - containerRect.left;
    const landingY = targetRect.top + targetRect.height / 2 - containerRect.top - 8;

    applySentimentEyes(eventData?.sentiment);

    executeContinuousSprintAndLeap(
      landingX,
      landingY,
      // onImpactCallback:
      () => {
        targetEl.classList.add('spider-struck');

        // Silk nozzle pulse and leg recoil
        const liveSvg = spiderSvgContainerRef.current?.querySelector('svg');
        if (liveSvg) {
          if (currentSkin === 'mecha') {
            const l4 = liveSvg.querySelector('#L4_s1');
            const r4 = liveSvg.querySelector('#R4_s1');
            if (l4 && r4) {
              const l4Rest = parseFloat(l4.getAttribute('data-rest') || '0');
              const r4Rest = parseFloat(r4.getAttribute('data-rest') || '0');
              const recoilObj = { angle: 0 };
              gsap.to(recoilObj, {
                angle: 18,
                duration: 0.14,
                yoyo: true,
                repeat: 1,
                ease: 'power2.out',
                onUpdate: () => {
                  l4.setAttribute('transform', `rotate(${l4Rest - recoilObj.angle})`);
                  r4.setAttribute('transform', `rotate(${r4Rest + recoilObj.angle})`);
                },
                onComplete: () => {
                  l4.setAttribute('transform', `rotate(${l4Rest})`);
                  r4.setAttribute('transform', `rotate(${r4Rest})`);
                }
              });
            }
          } else {
            const fangL = liveSvg.querySelector<HTMLElement>('#tribal_fang_l');
            const fangR = liveSvg.querySelector<HTMLElement>('#tribal_fang_r');
            if (fangL && fangR) {
              gsap.fromTo(fangL, { rotate: 26 }, { rotate: 0, duration: 0.22, ease: 'elastic.out(1.5, 0.3)' });
              gsap.fromTo(fangR, { rotate: -26 }, { rotate: 0, duration: 0.22, ease: 'elastic.out(1.5, 0.3)' });
            }
          }
          const nozzle = liveSvg.querySelector('#silk-nozzle');
          if (nozzle) {
            gsap.fromTo(nozzle, { scale: 1.8, transformOrigin: 'center' }, { scale: 1.0, duration: 0.3, ease: 'power2.out' });
          }
        }

        // Shoot transient silk filament to decision arc
        if (decisionNodeEl) {
          shootFilament(landingX, landingY, decisionNodeEl);
        }
      },
      // onCompleteCallback:
      () => {
        if (onSpiderCrawlComplete && eventData) {
          onSpiderCrawlComplete(eventData as SpiderEvent);
        }
      }
    );
  };

  // --- THEMED TRANSIENT SILK ENGINE ---
  const shootFilament = (
    startX: number,
    startY: number,
    targetNodeEl: HTMLElement
  ) => {
    if (!containerRef.current) return;
    const containerRect = containerRef.current.getBoundingClientRect();
    const nodeRect = targetNodeEl.getBoundingClientRect();

    const endX = nodeRect.left + 24 - containerRect.left;
    const endY = nodeRect.top + nodeRect.height / 2 - containerRect.top;

    const newFilament: Filament = {
      id: Math.random().toString(36).substring(7),
      startX,
      startY,
      endX,
      endY,
      skin: currentSkin,
      color: currentSkin === 'mecha' ? '#00e5ff' : '#c084fc'
    };

    // Hard Invariant: max 2 active filaments
    const nextList = [...filamentsRef.current, newFilament].slice(-2);
    filamentsRef.current = nextList;
    setFilaments(nextList);

    // Flash receiving effect on target decision node
    const flashClass = currentSkin === 'mecha' ? 'node-flash-mecha' : 'node-flash-tribal';
    targetNodeEl.classList.add(flashClass);
    setTimeout(() => {
      targetNodeEl.classList.remove(flashClass);
    }, 450);

    // Auto-remove filament after 1.2s
    setTimeout(() => {
      filamentsRef.current = filamentsRef.current.filter(f => f.id !== newFilament.id);
      setFilaments([...filamentsRef.current]);
    }, 1200);
  };

  // --- NATURAL STEADY WALKING MOTION (KHÔNG NHẢY VỒ, BƯỚC ĐI ĐỀU TỰ NHIÊN) ---
  const walkToPoint = (
    destX: number,
    destY: number,
    speed: number = 135,
    onComplete?: () => void
  ) => {
    if (!containerRef.current || !actorRef.current || !rotatorRef.current) return;
    abortPreviousMotionAndReset();

    const actor = actorRef.current;
    const rotator = rotatorRef.current;

    const curX = gsap.getProperty(actor, 'x') as number;
    const curY = gsap.getProperty(actor, 'y') as number;
    const startX = typeof curX === 'number' && !isNaN(curX) ? curX : spiderPos.current.x;
    const startY = typeof curY === 'number' && !isNaN(curY) ? curY : spiderPos.current.y;

    const deltaX = destX - startX;
    const deltaY = destY - startY;
    const dist = Math.hypot(deltaX, deltaY);

    if (dist < 15) {
      if (onComplete) onComplete();
      return;
    }

    let targetAngle = Math.atan2(deltaY, deltaX) * (180 / Math.PI) + 90;
    let currentAngle = (gsap.getProperty(rotator, 'rotation') as number) || spiderPos.current.angle || 0;
    let diff = (targetAngle - currentAngle) % 360;
    if (diff > 180) diff -= 360;
    if (diff < -180) diff += 360;
    const smoothTargetAngle = currentAngle + diff;

    isCrawling.current = true;
    const turnDuration = Math.min(0.22, Math.max(0.08, (Math.abs(diff) / 360) * 0.28));
    const walkDuration = Math.max(0.45, dist / speed);

    // Kích hoạt nhịp chân đi bộ tự nhiên (0.95x speed)
    if (currentSkin === 'mecha') startMechaWalk(0.95);
    else startTribalWalk(0.95);

    const footprintInterval = 120;
    const footprintTimer = setInterval(() => {
      if (!actorRef.current || !containerRef.current) return;
      const aRect = actorRef.current.getBoundingClientRect();
      const cRect = containerRef.current.getBoundingClientRect();
      leaveFootprint(aRect.left - cRect.left + 52, aRect.top - cRect.top + 52);
    }, footprintInterval);

    const walkTl = gsap.timeline({
      onComplete: () => {
        clearInterval(footprintTimer);
        spiderPos.current.x = destX;
        spiderPos.current.y = destY;
        spiderPos.current.angle = smoothTargetAngle;
        isCrawling.current = false;
        activeMasterTl.current = null;
        if (currentSkin === 'mecha') {
          stopMechaWalk();
          startMechaIdle();
        } else {
          stopTribalWalk();
          startTribalIdle();
        }
        if (onComplete) onComplete();
      }
    });
    activeMasterTl.current = walkTl;

    // 1. Xoay người mượt mà theo góc di chuyển
    walkTl.to(rotator, {
      rotation: smoothTargetAngle,
      duration: turnDuration,
      ease: 'power1.out'
    }, 0);

    // 2. Đi bộ tịnh tiến thẳng đều, nhịp nhàng (ease: none)
    walkTl.to(actor, {
      x: destX,
      y: destY,
      duration: walkDuration,
      ease: 'none'
    }, turnDuration * 0.4);
  };

  // --- DI CHUYỂN TUẦN TRA LIÊN TỤC (CONTINUOUS PATROL / WANDERING) ---
  const stopContinuousPatrol = () => {
    isPatrollingRef.current = false;
    if (patrolTimerRef.current) {
      clearTimeout(patrolTimerRef.current);
      patrolTimerRef.current = null;
    }
  };

  const startContinuousPatrol = (
    getBounds: () => { left: number; top: number; width: number; height: number },
    onStep?: (stepCount: number) => void
  ) => {
    isPatrollingRef.current = true;
    let stepCount = 0;

    const patrolNext = () => {
      if (!isPatrollingRef.current || !containerRef.current) return;
      const b = getBounds();
      if (!b || b.width <= 100 || b.height <= 100) return;

      const containerRect = containerRef.current.getBoundingClientRect();
      // Chọn điểm đích an toàn trong khung bài báo (cách mép 50-70px để nhện không bị lọt ra ngoài)
      const minX = Math.max(30, b.left - containerRect.left + 50);
      const maxX = Math.min(containerRect.width - 50, b.left - containerRect.left + b.width - 70);
      const minY = Math.max(30, b.top - containerRect.top + 50);
      const maxY = Math.min(containerRect.height - 50, b.top - containerRect.top + b.height - 70);

      const targetX = minX + Math.random() * Math.max(30, maxX - minX);
      const targetY = minY + Math.random() * Math.max(30, maxY - minY);

      stepCount++;
      if (onStep) onStep(stepCount);

      // Đi bộ vững vàng với tốc độ 125px/s
      walkToPoint(targetX, targetY, 125, () => {
        if (!isPatrollingRef.current) return;
        // Dừng nghỉ 200ms tạo cảm giác tự nhiên rồi bước tiếp liên tục
        patrolTimerRef.current = setTimeout(patrolNext, 200);
      });
    };

    patrolNext();
  };

  const crawlToPoint = (clientX: number, clientY: number, onDone?: () => void) => {
    if (!containerRef.current || !actorRef.current || !rotatorRef.current) return;
    const containerRect = containerRef.current.getBoundingClientRect();
    const landingX = clientX - containerRect.left;
    const landingY = clientY - containerRect.top;
    walkToPoint(landingX, landingY, 140, onDone);
  };

  // Expose API via window for DOM keyword mark clicks and continuous free wandering
  useEffect(() => {
    (window as any).__spiderCrawlToKeyword = crawlToKeyword;
    (window as any).__spiderCrawlToPoint = crawlToPoint;
    (window as any).__spiderWalkToPoint = walkToPoint;
    (window as any).__spiderStartContinuousPatrol = startContinuousPatrol;
    (window as any).__spiderStopContinuousPatrol = stopContinuousPatrol;
    return () => {
      delete (window as any).__spiderCrawlToKeyword;
      delete (window as any).__spiderCrawlToPoint;
      delete (window as any).__spiderWalkToPoint;
      delete (window as any).__spiderStartContinuousPatrol;
      delete (window as any).__spiderStopContinuousPatrol;
    };
  }, [currentSkin]);

  // Ref giữ function crawlToKeyword mà không làm effect khởi tạo lại mỗi render
  const crawlRef = useRef<(t: HTMLElement, i: number, n?: HTMLElement, e?: any) => void>();
  crawlRef.current = crawlToKeyword;

  // ==========================================================
  // HỢP ĐỒNG HÀNG ĐỢI HOẠT ẢNH TỰ TIÊU THỤ (FIFO Animation Queue)
  // Nhện là Consumer độc lập: nhận SpiderEvent từ SSE qua
  // window.__spiderStreamEvent, xếp vào animationQueue và tự bò.
  // ==========================================================
  useEffect(() => {
    const queue: SpiderEvent[] = [];
    let busy = false;
    let timer: ReturnType<typeof setTimeout> | null = null;

    const findMarkEl = (ev: SpiderEvent): HTMLElement | null => {
      const root = document.getElementById('spider-article-content');
      if (!root) return null;
      // 1) Ưu tiên khớp chính xác theo target_index
      const byIndex = root.querySelector(
        `mark[data-spider-index="${ev.target_index}"]`
      ) as HTMLElement | null;
      if (byIndex) return byIndex;
      // 2) Thử khớp theo từ khóa (không phân biệt hoa thường, escape ký tự đặc biệt)
      const safeWord = (ev.target_word || '').replace(/["\\]/g, '\\$&');
      if (!safeWord) return null;
      const marks = Array.from(
        root.querySelectorAll('mark[data-spider-index]')
      ) as HTMLElement[];
      const lower = safeWord.toLowerCase();
      return (
        marks.find(
          (m) =>
            (m.dataset.word || '').toLowerCase() === lower ||
            (m.textContent || '').toLowerCase() === lower
        ) || null
      );
    };

    const finishCurrent = () => {
      busy = false;
      processNext();
    };

    const processNext = () => {
      if (busy) return;
      if (queue.length === 0) return;
      busy = true;

      const ev = queue.shift()!;

      // Adaptive Pacing: hàng đợi càng dài -> nhện càng nhanh
      let delay = ev.pacing_delay_ms || 400;
      if (queue.length > 12) delay = Math.min(delay, 180);       // Fast-Forward
      else if (queue.length > 4) delay = Math.min(delay, 220);  // Sprint Mode

      // Fast-Forward (>12): bỏ qua từ phụ, chỉ bò qua 3 từ rồi sang bài tiếp theo
      if (queue.length > 12 && Math.random() > 0.34) {
        busy = false;
        timer = setTimeout(processNext, delay);
        return;
      }

      const nodeId =
        ev.category === 'vang'
          ? 'node-gold'
          : ev.category === 'chung_khoan'
          ? 'node-stocks'
          : ev.category === 'chinh_tri'
          ? 'node-policy'
          : ev.category === 'crypto'
          ? 'node-breaking'
          : 'node-macro';
      const nodeEl = document.getElementById(nodeId) || undefined;

      let attempts = 0;
      const tryCrawl = () => {
        const el = findMarkEl(ev);
        if (!el) {
          attempts += 1;
          if (attempts < 6) {
            timer = setTimeout(tryCrawl, 200); // chờ DOM render bài mới
            return;
          }
          busy = false;
          processNext();
          return;
        }
        crawlRef.current?.(el, ev.target_index, nodeEl, ev);
        timer = setTimeout(finishCurrent, delay);
      };

      timer = setTimeout(tryCrawl, 60);
    };

    const enqueue = (ev: SpiderEvent) => {
      if (!ev || !ev.target_word) return;
      if (queue.length > 60) queue.splice(0, queue.length - 60);
      queue.push(ev);
      processNext();
    };

    (window as any).__spiderEnqueueEvent = enqueue;

    return () => {
      (window as any).__spiderEnqueueEvent = undefined;
      if (timer) clearTimeout(timer);
      queue.length = 0;
    };
  }, []);

  return (
    <div
      ref={containerRef}
      style={{
        position: 'absolute',
        inset: 0,
        pointerEvents: 'none',
        overflow: 'hidden',
        zIndex: 50
      }}
    >
      {/* Laser Gradient Defs for SVG Filaments */}
      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
        <defs>
          <linearGradient id="laser-cyan-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="30%" stopColor="#00E5FF" />
            <stop offset="100%" stopColor="#00B4D8" />
          </linearGradient>
          <linearGradient id="tribal-silk-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#C084FC" />
            <stop offset="60%" stopColor="#7C3AED" />
            <stop offset="100%" stopColor="#00F2FE" />
          </linearGradient>
          <filter id="laser-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3.5" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
          <filter id="tribal-silk-glow" x="-30%" y="-30%" width="160%" height="160%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feColorMatrix type="matrix" values="
              0.7 0 0 0 0.6
              0 0.3 0 0 0.1
              0.9 0 1 0 0.95
              0 0 0 1 0" in="blur" result="coloredBlur"/>
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>
      </svg>

      {/* Transient SVG Silk Filaments Overlay */}
      <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
        {filaments.map(f => {
          const midX = (f.startX + f.endX) / 2;
          const midY = Math.min(f.startY, f.endY) - 35;
          const d = `M ${f.startX} ${f.startY} Q ${midX} ${midY} ${f.endX} ${f.endY}`;
          const isMecha = f.skin === 'mecha';
          return (
            <path
              key={f.id}
              d={d}
              className="filament-line"
              stroke={isMecha ? 'url(#laser-cyan-grad)' : 'url(#tribal-silk-grad)'}
              strokeWidth={isMecha ? '1.6' : '1.7'}
              filter={isMecha ? 'url(#laser-glow)' : 'url(#tribal-silk-glow)'}
              style={{
                strokeDasharray: '400',
                strokeDashoffset: '0',
                animation: 'filamentFade 1.2s ease-out forwards'
              }}
            />
          );
        })}
      </svg>

      {/* Live Spider Actor Container */}
      <div
        ref={actorRef}
        className={currentSkin === 'mecha' ? 'spider-actor-mecha' : 'spider-actor-tribal'}
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '104px',
          height: '104px',
          marginLeft: '-52px',
          marginTop: '-52px',
          transform: `translate(${spiderPos.current.x}px, ${spiderPos.current.y}px)`,
          willChange: 'transform'
        }}
      >
        <div
          ref={rotatorRef}
          style={{
            width: '100%',
            height: '100%',
            willChange: 'transform'
          }}
        >
          <div
            ref={carrierRef}
            style={{
              width: '100%',
              height: '100%',
              willChange: 'transform'
            }}
          >
            <div
              ref={spiderSvgContainerRef}
              style={{
                width: '100%',
                height: '100%',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};
