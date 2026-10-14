import os

# ==============================================================================
# 1. UPGRADE test_mecha_vector_rig.html
# ==============================================================================
with open('frontend/preview/test_mecha_vector_rig.html', 'r', encoding='utf-8') as f:
    mecha_html = f.read()

old_mecha_walk = '''        if (currentPreset === 'walk') {
          // Preset 2: Quadrature Gait Kinematics (Chân Dài L4/R4 Là Phần Đầu Dẫn Đường)
          const pA = t;
          const pB = t + Math.PI;
          const sA = Math.sin(pA), sB = Math.sin(pB);
          const lA = Math.max(0, Math.cos(pA)), lB = Math.max(0, Math.cos(pB));

          // Chân trước dài L4/R4 (5 phân đoạn pít-tông lồng nhau)
          setJoint('L4_s1', -18 * sB);
          setJoint('L4_s2', -24 * lB + (sB < -0.2 ? 6 : 0));
          setJoint('L4_s3', 15 * sB - 9 * lB);
          setJoint('L4_s4', 11 * sB);
          setJoint('L4_s5', 8 * sB - 6 * lB);

          setJoint('R4_s1', 18 * sA);
          setJoint('R4_s2', 24 * lA - (sA < -0.2 ? 6 : 0));
          setJoint('R4_s3', -15 * sA + 9 * lA);
          setJoint('R4_s4', -11 * sA);
          setJoint('R4_s5', -8 * sA + 6 * lA);

          // Chân giữa L3/R3 và L2/R2
          setJoint('L3_s1', 15 * sA); setJoint('L3_s2', -18 * lA); setJoint('L3_s3', 12 * sA);
          setJoint('R3_s1', -15 * sB); setJoint('R3_s2', 18 * lB); setJoint('R3_s3', -12 * sB);
          setJoint('L2_s1', -14 * sB); setJoint('L2_s2', -16 * lB); setJoint('L2_s3', 10 * sB);
          setJoint('R2_s1', 14 * sA); setJoint('R2_s2', 16 * lA); setJoint('R2_s3', -10 * sA);

          // Càng sau L1/R1
          setJoint('L1_s1', 16 * sA); setJoint('L1_s2', -14 * lA); setJoint('L1_s3', 12 * sA);
          setJoint('R1_s1', -16 * sB); setJoint('R1_s2', 14 * lB); setJoint('R1_s3', -12 * sB);

          // Đuôi cân bằng ANT_s1
          setJoint('ANT_s1', 8 * Math.sin(t * 1.5));
          spiderRoot.setAttribute('transform', `translate(0, ${2.8 * Math.sin(t * 2)}) rotate(${1.2 * Math.sin(t)})`);
          document.getElementById('telem-psi').innerText = `${(3600 + 450 * Math.sin(t * 2)).toFixed(0)} PSI`;
        }'''

new_mecha_walk = '''        if (currentPreset === 'walk') {
          // Preset 2: 4-Phase Arachnid Ripple Wave Gait (Chân Dài L4/R4 Là Phần Đầu Dẫn Đường)
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

          const calcMotion = (phi) => {
            const norm = ((phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
            const isSwing = norm < Math.PI;
            if (isSwing) {
              return { swing: -Math.cos(norm), lift: Math.sin(norm), ext: Math.sin(norm) };
            } else {
              return { swing: Math.cos(norm - Math.PI), lift: 0, ext: -0.2 };
            }
          };

          // Front Lead Tactical Scythes L4 & R4 (5-segment telescoping pistons)
          const mL4 = calcMotion(t + phases.L4);
          setJoint('L4_s1', -18 * mL4.swing);
          setJoint('L4_s2', -24 * mL4.lift);
          setJoint('L4_s3', 14 * mL4.swing + 10 * mL4.lift);
          setJoint('L4_s4', 10 * mL4.swing + 8 * mL4.lift);
          setJoint('L4_s5', 8 * mL4.swing + 6 * mL4.lift);

          const mR4 = calcMotion(t + phases.R4);
          setJoint('R4_s1', 18 * mR4.swing);
          setJoint('R4_s2', 24 * mR4.lift);
          setJoint('R4_s3', -14 * mR4.swing - 10 * mR4.lift);
          setJoint('R4_s4', -10 * mR4.swing - 8 * mR4.lift);
          setJoint('R4_s5', -8 * mR4.swing - 6 * mR4.lift);

          // Middle Upper Legs L3 & R3
          const mL3 = calcMotion(t + phases.L3);
          setJoint('L3_s1', -14 * mL3.swing);
          setJoint('L3_s2', -18 * mL3.lift);
          setJoint('L3_s3', 10 * mL3.swing + 6 * mL3.lift);

          const mR3 = calcMotion(t + phases.R3);
          setJoint('R3_s1', 14 * mR3.swing);
          setJoint('R3_s2', 18 * mR3.lift);
          setJoint('R3_s3', -10 * mR3.swing - 6 * mR3.lift);

          // Middle Lower Legs L2 & R2
          const mL2 = calcMotion(t + phases.L2);
          setJoint('L2_s1', -15 * mL2.swing);
          setJoint('L2_s2', -18 * mL2.lift);
          setJoint('L2_s3', 12 * mL2.swing + 8 * mL2.lift);

          const mR2 = calcMotion(t + phases.R2);
          setJoint('R2_s1', 15 * mR2.swing);
          setJoint('R2_s2', 18 * mR2.lift);
          setJoint('R2_s3', -12 * mR2.swing - 8 * mR2.lift);

          // Rear Pusher Claws L1 & R1
          const mL1 = calcMotion(t + phases.L1);
          setJoint('L1_s1', -16 * mL1.swing);
          setJoint('L1_s2', 20 * mL1.lift);
          setJoint('L1_s3', -12 * mL1.swing - 8 * mL1.lift);

          const mR1 = calcMotion(t + phases.R1);
          setJoint('R1_s1', 16 * mR1.swing);
          setJoint('R1_s2', -20 * mR1.lift);
          setJoint('R1_s3', 12 * mR1.swing + 8 * mR1.lift);

          // Radar Tail Antenna Balance
          setJoint('ANT_s1', Math.sin(t * 1.5) * 5.5);
          spiderRoot.setAttribute('transform', `translate(0, ${2.2 * Math.sin(t * 2)}) rotate(${1.2 * Math.sin(t)})`);
          const psiVal = document.getElementById('telem-psi');
          if (psiVal) psiVal.innerText = `${(3600 + 450 * Math.sin(t * 2)).toFixed(0)} PSI`;
        }'''

mecha_html = mecha_html.replace(old_mecha_walk, new_mecha_walk)
with open('frontend/preview/test_mecha_vector_rig.html', 'w', encoding='utf-8') as f:
    f.write(mecha_html)
print("Updated test_mecha_vector_rig.html successfully!")

# ==============================================================================
# 2. UPGRADE test_tribal_vector_rig.html
# ==============================================================================
with open('frontend/preview/test_tribal_vector_rig.html', 'r', encoding='utf-8') as f:
    tribal_html = f.read()

idx_t_start = tribal_html.find("if (currentPreset === 'walk') {")
idx_t_end = tribal_html.find("} else if (currentPreset === 'idle') {")

new_tribal_lab_walk = '''if (currentPreset === 'walk') {
          // --- 4-PHASE ARACHNID RIPPLE WAVE WALK ---
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

          const calcMotion = (phi) => {
            const norm = ((phi % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
            const isSwing = norm < Math.PI;
            if (isSwing) {
              return { swing: -Math.cos(norm), lift: Math.sin(norm), ext: Math.sin(norm) };
            } else {
              return { swing: Math.cos(norm - Math.PI), lift: 0, ext: -0.25 };
            }
          };

          // Front Sickle Legs L1 & R1
          const mL1 = calcMotion(t + phases.L1);
          applyJointTransform('L1_s1', -16 * mL1.swing);
          applyJointTransform('L1_s2', -22 * mL1.lift);
          applyJointTransform('L1_s3', 14 * mL1.swing + 10 * mL1.lift);

          const mR1 = calcMotion(t + phases.R1);
          applyJointTransform('R1_s1', 16 * mR1.swing);
          applyJointTransform('R1_s2', 22 * mR1.lift);
          applyJointTransform('R1_s3', -14 * mR1.swing - 10 * mR1.lift);

          // Middle Upper Legs L2 & R2
          const mL2 = calcMotion(t + phases.L2);
          applyJointTransform('L2_s1', -13 * mL2.swing);
          applyJointTransform('L2_s2', -18 * mL2.lift);
          applyJointTransform('L2_s3', 11 * mL2.swing + 7 * mL2.lift);

          const mR2 = calcMotion(t + phases.R2);
          applyJointTransform('R2_s1', 13 * mR2.swing);
          applyJointTransform('R2_s2', 18 * mR2.lift);
          applyJointTransform('R2_s3', -11 * mR2.swing - 7 * mR2.lift);

          // Middle Lower Legs L3 & R3
          const mL3 = calcMotion(t + phases.L3);
          applyJointTransform('L3_s1', -14 * mL3.swing);
          applyJointTransform('L3_s2', 18 * mL3.lift);
          applyJointTransform('L3_s3', -12 * mL3.swing - 8 * mL3.lift);

          const mR3 = calcMotion(t + phases.R3);
          applyJointTransform('R3_s1', 14 * mR3.swing);
          applyJointTransform('R3_s2', -18 * mR3.lift);
          applyJointTransform('R3_s3', 12 * mR3.swing + 8 * mR3.lift);

          // Rear Sickle Sweepers L4 & R4
          const mL4 = calcMotion(t + phases.L4);
          applyJointTransform('L4_s1', -18 * mL4.swing);
          applyJointTransform('L4_s2', 24 * mL4.lift);
          applyJointTransform('L4_s3', -15 * mL4.swing - 10 * mL4.lift);

          const mR4 = calcMotion(t + phases.R4);
          applyJointTransform('R4_s1', 18 * mR4.swing);
          applyJointTransform('R4_s2', -24 * mR4.lift);
          applyJointTransform('R4_s3', 15 * mR4.swing + 10 * mR4.lift);

          // Body sway & heave centered at (479, 450)
          const master = document.getElementById('tribal-spider-master');
          if (master) {
            const bobY = Math.sin(t * 2) * 2.2;
            const roll = Math.sin(t) * 1.3;
            master.setAttribute('transform', `translate(0, ${bobY}) rotate(${roll}, 479, 450)`);
          }

          // Abdomen breathing & Fangs twitch
          const body = document.getElementById('tribal-body-core');
          if (body) {
            const scaleY = 1.0 + Math.sin(t * 1.5) * 0.035;
            body.style.transform = `scaleY(${scaleY})`;
          }
          const fangL = document.getElementById('tribal_fang_l');
          const fangR = document.getElementById('tribal_fang_r');
          if (fangL && fangR) {
            const fangAngle = Math.sin(t * 2) * 8;
            fangL.style.transform = `rotate(${fangAngle}deg)`;
            fangR.style.transform = `rotate(${-fangAngle}deg)`;
          }'''

tribal_html = tribal_html[:idx_t_start] + new_tribal_lab_walk + '\n        ' + tribal_html[idx_t_end:]
with open('frontend/preview/test_tribal_vector_rig.html', 'w', encoding='utf-8') as f:
    f.write(tribal_html)
print("Updated test_tribal_vector_rig.html successfully!")
