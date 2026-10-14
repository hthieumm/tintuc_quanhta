import re
import os

# ==============================================================================
# 1. UPGRADE spider_showcase.html
# ==============================================================================
with open('frontend/preview/spider_showcase.html', 'r', encoding='utf-8') as f:
    showcase = f.read()

# Replace startMechaWalkAnimation in spider_showcase.html
new_mecha_walk = '''    function startMechaWalkAnimation() {
      stopMechaIdleAnimation();
      if (mechaWalkRaf) cancelAnimationFrame(mechaWalkRaf);
      mechaWalkStartTime = performance.now();

      const restAngles = {};
      const liveSvg = document.getElementById('live-spider-svg');
      if (!liveSvg) return;

      liveSvg.querySelectorAll('.sp-joint').forEach(el => {
        restAngles[el.id] = parseFloat(el.dataset.rest) || 0;
      });

      const spiderRoot = liveSvg.querySelector('#spider-root');
      const isSync = (currentPacingMode === 'sync');
      const strideSpeed = isSync ? 3.2 : 2.0;

      const setJ = (id, delta) => {
        const el = liveSvg.querySelector(`#${id}`);
        if (el && restAngles[id] !== undefined) {
          el.setAttribute('transform', `rotate(${restAngles[id] + delta})`);
        }
      };

      // 4-Phase Arachnid Ripple Gait Phase Offsets
      const phases = {
        L4: 0.0,
        L2: 0.5 * Math.PI,
        L3: 1.0 * Math.PI,
        L1: 1.5 * Math.PI,
        R4: 1.0 * Math.PI,
        R2: 1.5 * Math.PI,
        R3: 0.0,
        R1: 0.5 * Math.PI
      };

      function calcMotion(phi, ramp) {
        const norm = ((phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
        const isSwing = norm < Math.PI;
        let swing, lift, ext;
        if (isSwing) {
          swing = -Math.cos(norm);
          lift = Math.sin(norm) * ramp;
          ext = Math.sin(norm) * ramp;
        } else {
          const phiStance = norm - Math.PI;
          swing = Math.cos(phiStance);
          lift = 0;
          ext = -0.2 * ramp;
        }
        return { swing: swing * ramp, lift, ext };
      }

      function step(now) {
        if (!isCrawling) return;
        const ramp = Math.min(1, (now - mechaWalkStartTime) / 220);
        const t = ((now - mechaWalkStartTime) / 400) * strideSpeed;

        // Front Lead Tactical Scythes L4 & R4 (5-segment telescoping pistons)
        const mL4 = calcMotion(t + phases.L4, ramp);
        setJ('L4_s1', -18 * mL4.swing);
        setJ('L4_s2', -24 * mL4.lift);
        setJ('L4_s3', 14 * mL4.swing + 10 * mL4.lift);
        setJ('L4_s4', 10 * mL4.swing + 8 * mL4.lift);
        setJ('L4_s5', 8 * mL4.swing + 6 * mL4.lift);

        const mR4 = calcMotion(t + phases.R4, ramp);
        setJ('R4_s1', 18 * mR4.swing);
        setJ('R4_s2', 24 * mR4.lift);
        setJ('R4_s3', -14 * mR4.swing - 10 * mR4.lift);
        setJ('R4_s4', -10 * mR4.swing - 8 * mR4.lift);
        setJ('R4_s5', -8 * mR4.swing - 6 * mR4.lift);

        // Middle Upper Legs L3 & R3 (3-segment)
        const mL3 = calcMotion(t + phases.L3, ramp);
        setJ('L3_s1', -14 * mL3.swing);
        setJ('L3_s2', -18 * mL3.lift);
        setJ('L3_s3', 10 * mL3.swing + 6 * mL3.lift);

        const mR3 = calcMotion(t + phases.R3, ramp);
        setJ('R3_s1', 14 * mR3.swing);
        setJ('R3_s2', 18 * mR3.lift);
        setJ('R3_s3', -10 * mR3.swing - 6 * mR3.lift);

        // Middle Lower Legs L2 & R2 (3-segment)
        const mL2 = calcMotion(t + phases.L2, ramp);
        setJ('L2_s1', -15 * mL2.swing);
        setJ('L2_s2', -18 * mL2.lift);
        setJ('L2_s3', 12 * mL2.swing + 8 * mL2.lift);

        const mR2 = calcMotion(t + phases.R2, ramp);
        setJ('R2_s1', 15 * mR2.swing);
        setJ('R2_s2', 18 * mR2.lift);
        setJ('R2_s3', -12 * mR2.swing - 8 * mR2.lift);

        // Rear Pusher Claws L1 & R1 (3-segment)
        const mL1 = calcMotion(t + phases.L1, ramp);
        setJ('L1_s1', -16 * mL1.swing);
        setJ('L1_s2', 20 * mL1.lift);
        setJ('L1_s3', -12 * mL1.swing - 8 * mL1.lift);

        const mR1 = calcMotion(t + phases.R1, ramp);
        setJ('R1_s1', 16 * mR1.swing);
        setJ('R1_s2', -20 * mR1.lift);
        setJ('R1_s3', 12 * mR1.swing + 8 * mR1.lift);

        // Radar Tail Antenna Balance
        setJ('ANT_s1', Math.sin(t * 1.5) * 4.5 * ramp);

        // Chassis Suspension (Pitch / Heave / Roll)
        if (spiderRoot) {
          const heaveY = Math.sin(t * 2) * 2.2 * ramp;
          const roll = Math.sin(t) * 1.2 * ramp;
          spiderRoot.setAttribute('transform', `translate(0, ${heaveY}) rotate(${roll})`);
        }

        mechaWalkRaf = requestAnimationFrame(step);
      }

      mechaWalkRaf = requestAnimationFrame(step);
    }'''

# Replace startMechaWalkAnimation in showcase
idx_m_start = showcase.find('function startMechaWalkAnimation()')
idx_m_end = showcase.find('function stopMechaWalkAnimation()')
showcase = showcase[:idx_m_start] + new_mecha_walk + '\n\n    ' + showcase[idx_m_end:]

# Replace startTribalWalkAnimation in spider_showcase.html
new_tribal_walk = '''    function startTribalWalkAnimation() {
      stopTribalIdleAnimation();
      if (tribalWalkRaf) cancelAnimationFrame(tribalWalkRaf);
      tribalWalkStartTime = performance.now();

      const liveSvg = document.getElementById('live-spider-svg');
      if (!liveSvg) return;

      const setJ = (id, delta) => {
        const el = liveSvg.querySelector(`#${id}`);
        if (el) el.style.transform = `rotate(${delta}deg)`;
      };

      const isSync = (currentPacingMode === 'sync');
      const strideSpeed = isSync ? 3.4 : 2.2;

      // 4-Phase Arachnid Ripple Wave Offsets for Fluid Scuttling
      const phases = {
        L4: 0.0,
        L2: 0.5 * Math.PI,
        L3: 1.0 * Math.PI,
        L1: 1.5 * Math.PI,
        R4: 1.0 * Math.PI,
        R2: 1.5 * Math.PI,
        R3: 0.0,
        R1: 0.5 * Math.PI
      };

      function calcMotion(phi, ramp) {
        const norm = ((phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
        const isSwing = norm < Math.PI;
        let swing, lift, ext;
        if (isSwing) {
          swing = -Math.cos(norm);
          lift = Math.sin(norm) * ramp;
          ext = Math.sin(norm) * ramp;
        } else {
          const phiStance = norm - Math.PI;
          swing = Math.cos(phiStance);
          lift = 0;
          ext = -0.25 * ramp;
        }
        return { swing: swing * ramp, lift, ext };
      }

      function walkStep(now) {
        if (!isCrawling) return;
        const ramp = Math.min(1, (now - tribalWalkStartTime) / 200);
        const t = ((now - tribalWalkStartTime) / 380) * strideSpeed;

        // Front Sickle Legs L1 & R1 (Scythes probing forward)
        const mL1 = calcMotion(t + phases.L1, ramp);
        setJ('tribal_L1_s1', -16 * mL1.swing);
        setJ('tribal_L1_s2', -22 * mL1.lift);
        setJ('tribal_L1_s3', 14 * mL1.swing + 10 * mL1.lift);

        const mR1 = calcMotion(t + phases.R1, ramp);
        setJ('tribal_R1_s1', 16 * mR1.swing);
        setJ('tribal_R1_s2', 22 * mR1.lift);
        setJ('tribal_R1_s3', -14 * mR1.swing - 10 * mR1.lift);

        // Middle Upper Legs L2 & R2
        const mL2 = calcMotion(t + phases.L2, ramp);
        setJ('tribal_L2_s1', -13 * mL2.swing);
        setJ('tribal_L2_s2', -18 * mL2.lift);
        setJ('tribal_L2_s3', 11 * mL2.swing + 7 * mL2.lift);

        const mR2 = calcMotion(t + phases.R2, ramp);
        setJ('tribal_R2_s1', 13 * mR2.swing);
        setJ('tribal_R2_s2', 18 * mR2.lift);
        setJ('tribal_R2_s3', -11 * mR2.swing - 7 * mR2.lift);

        // Middle Lower Legs L3 & R3
        const mL3 = calcMotion(t + phases.L3, ramp);
        setJ('tribal_L3_s1', -14 * mL3.swing);
        setJ('tribal_L3_s2', 18 * mL3.lift);
        setJ('tribal_L3_s3', -12 * mL3.swing - 8 * mL3.lift);

        const mR3 = calcMotion(t + phases.R3, ramp);
        setJ('tribal_R3_s1', 14 * mR3.swing);
        setJ('tribal_R3_s2', -18 * mR3.lift);
        setJ('tribal_R3_s3', 12 * mR3.swing + 8 * mR3.lift);

        // Rear Sickle Sweepers L4 & R4 (Powerful backward stroke)
        const mL4 = calcMotion(t + phases.L4, ramp);
        setJ('tribal_L4_s1', -18 * mL4.swing);
        setJ('tribal_L4_s2', 24 * mL4.lift);
        setJ('tribal_L4_s3', -15 * mL4.swing - 10 * mL4.lift);

        const mR4 = calcMotion(t + phases.R4, ramp);
        setJ('tribal_R4_s1', 18 * mR4.swing);
        setJ('tribal_R4_s2', -24 * mR4.lift);
        setJ('tribal_R4_s3', 15 * mR4.swing + 10 * mR4.lift);

        // Biological Body Heave & Roll centered at (479, 450)
        const master = liveSvg.querySelector('#tribal-spider-master');
        if (master) {
          const bobY = Math.sin(t * 2) * 2.0 * ramp;
          const roll = Math.sin(t) * 1.3 * ramp;
          master.setAttribute('transform', `translate(0, ${bobY}) rotate(${roll}, 479, 450)`);
        }

        // Fangs snapping twitch
        const fangL = liveSvg.querySelector('#tribal_fang_l');
        const fangR = liveSvg.querySelector('#tribal_fang_r');
        if (fangL && fangR) {
          const fangAngle = Math.sin(t * 2) * 8 * ramp;
          fangL.style.transform = `rotate(${fangAngle}deg)`;
          fangR.style.transform = `rotate(${-fangAngle}deg)`;
        }

        tribalWalkRaf = requestAnimationFrame(walkStep);
      }

      tribalWalkRaf = requestAnimationFrame(walkStep);
    }'''

# Replace startTribalWalkAnimation in showcase
idx_t_start = showcase.find('function startTribalWalkAnimation()')
idx_t_end = showcase.find('function stopTribalWalkAnimation()')
showcase = showcase[:idx_t_start] + new_tribal_walk + '\n\n    ' + showcase[idx_t_end:]

with open('frontend/preview/spider_showcase.html', 'w', encoding='utf-8') as f:
    f.write(showcase)

print("Updated spider_showcase.html with 4-phase ripple wave gaits!")
