import re

with open('frontend/preview/spider_showcase.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update viewBox to square 1:1 centered at (479, 450)
c = c.replace('id="svg-preview-tribal" viewBox="200 20 560 860"', 'id="svg-preview-tribal" viewBox="49 20 860 860"')

# 2. Exclude tribal from abdomen wobble in crawlSpiderTo
old_abdomen = '''      // Quán tính đàn hồi bụng
      if (abdomen) {'''
new_abdomen = '''      // Quán tính đàn hồi bụng
      if (abdomen && currentSkinId !== 'mecha' && currentSkinId !== 'tribal') {'''
c = c.replace(old_abdomen, new_abdomen)

# 3. Update turn and move timing in crawlSpiderTo for smooth crawl
old_move = '''      // Di chuyển GPU transforms
      masterTl.to(actor, {
        x: targetX,
        y: targetY,
        duration: moveDuration,
        ease: isSync ? "power2.inOut" : "sine.inOut"
      }, turnDuration * 0.3);'''

new_move = '''      // Di chuyển GPU transforms (bắt đầu sau khi xoay êm ái)
      masterTl.to(actor, {
        x: targetX,
        y: targetY,
        duration: moveDuration,
        ease: isSync ? "power2.inOut" : "power1.inOut"
      }, turnDuration * 0.6);'''

c = c.replace(old_move, new_move)

# 4. Update updateLiveSpiderSvg() sizing for tribal to 104x104
old_tribal_size = '''        } else if (currentSkinId === 'tribal') {
          actor.classList.remove('mecha-mode');
          stopMechaIdleAnimation();
          actor.classList.add('tribal-mode');
          liveSvg.setAttribute('width', '100');
          liveSvg.setAttribute('height', '100');
          actor.style.width = '100px';
          actor.style.height = '100px';
          actor.style.marginLeft = '-50px';
          actor.style.marginTop = '-50px';
          setTimeout(startTribalIdleAnimation, 120);'''

new_tribal_size = '''        } else if (currentSkinId === 'tribal') {
          actor.classList.remove('mecha-mode');
          stopMechaIdleAnimation();
          actor.classList.add('tribal-mode');
          liveSvg.setAttribute('width', '104');
          liveSvg.setAttribute('height', '104');
          actor.style.width = '104px';
          actor.style.height = '104px';
          actor.style.marginLeft = '-52px';
          actor.style.marginTop = '-52px';
          setTimeout(startTribalIdleAnimation, 120);'''

c = c.replace(old_tribal_size, new_tribal_size)

# 5. Update startTribalWalkAnimation with gait ramp-up
old_walk_step = '''      function walkStep(now) {
        if (!isCrawling) return;
        const t = ((now - tribalWalkStartTime) / 380) * strideSpeed;

        const phi_A = t;
        const phi_B = t + Math.PI;

        const lift_A = Math.max(0, Math.cos(phi_A));
        const lift_B = Math.max(0, Math.cos(phi_B));

        // Group A: L1, R2, L3, R4
        setJ('tribal_L1_s1', Math.sin(phi_A) * 15);
        setJ('tribal_L1_s2', -22 * lift_A);
        setJ('tribal_L1_s3', Math.sin(phi_A) * 12 + 8 * lift_A);

        setJ('tribal_R2_s1', Math.sin(phi_A) * 12);
        setJ('tribal_R2_s2', 18 * lift_A);
        setJ('tribal_R2_s3', -Math.sin(phi_A) * 10 - 6 * lift_A);

        setJ('tribal_L3_s1', Math.sin(phi_A) * 14);
        setJ('tribal_L3_s2', 18 * lift_A);
        setJ('tribal_L3_s3', -Math.sin(phi_A) * 12 - 8 * lift_A);

        setJ('tribal_R4_s1', Math.sin(phi_A) * 16);
        setJ('tribal_R4_s2', -22 * lift_A);
        setJ('tribal_R4_s3', Math.sin(phi_A) * 14 + 10 * lift_A);

        // Group B: R1, L2, R3, L4
        setJ('tribal_R1_s1', -Math.sin(phi_B) * 15);
        setJ('tribal_R1_s2', 22 * lift_B);
        setJ('tribal_R1_s3', -Math.sin(phi_B) * 12 - 8 * lift_B);

        setJ('tribal_L2_s1', -Math.sin(phi_B) * 12);
        setJ('tribal_L2_s2', -18 * lift_B);
        setJ('tribal_L2_s3', Math.sin(phi_B) * 10 + 6 * lift_B);

        setJ('tribal_R3_s1', -Math.sin(phi_B) * 14);
        setJ('tribal_R3_s2', -18 * lift_B);
        setJ('tribal_R3_s3', Math.sin(phi_B) * 12 + 8 * lift_B);

        setJ('tribal_L4_s1', -Math.sin(phi_B) * 16);
        setJ('tribal_L4_s2', 22 * lift_B);
        setJ('tribal_L4_s3', -Math.sin(phi_B) * 14 - 10 * lift_B);

        // Body bob
        const master = liveSvg.querySelector('#tribal-spider-master');
        if (master) {
          const bobY = Math.sin(t * 2) * 2.8;
          const roll = Math.sin(t) * 1.4;
          master.setAttribute('transform', `translate(0, ${bobY}) rotate(${roll}, 479, 500)`);
        }'''

new_walk_step = '''      function walkStep(now) {
        if (!isCrawling) return;
        const ramp = Math.min(1, (now - tribalWalkStartTime) / 200);
        const t = ((now - tribalWalkStartTime) / 380) * strideSpeed;

        const phi_A = t;
        const phi_B = t + Math.PI;

        const lift_A = Math.max(0, Math.cos(phi_A)) * ramp;
        const lift_B = Math.max(0, Math.cos(phi_B)) * ramp;

        // Group A: L1, R2, L3, R4 (vung êm ái kèm ramp gia tốc)
        setJ('tribal_L1_s1', Math.sin(phi_A) * 15 * ramp);
        setJ('tribal_L1_s2', -22 * lift_A);
        setJ('tribal_L1_s3', (Math.sin(phi_A) * 12 + 8 * Math.max(0, Math.cos(phi_A))) * ramp);

        setJ('tribal_R2_s1', Math.sin(phi_A) * 12 * ramp);
        setJ('tribal_R2_s2', 18 * lift_A);
        setJ('tribal_R2_s3', (-Math.sin(phi_A) * 10 - 6 * Math.max(0, Math.cos(phi_A))) * ramp);

        setJ('tribal_L3_s1', Math.sin(phi_A) * 14 * ramp);
        setJ('tribal_L3_s2', 18 * lift_A);
        setJ('tribal_L3_s3', (-Math.sin(phi_A) * 12 - 8 * Math.max(0, Math.cos(phi_A))) * ramp);

        setJ('tribal_R4_s1', Math.sin(phi_A) * 16 * ramp);
        setJ('tribal_R4_s2', -22 * lift_A);
        setJ('tribal_R4_s3', (Math.sin(phi_A) * 14 + 10 * Math.max(0, Math.cos(phi_A))) * ramp);

        // Group B: R1, L2, R3, L4
        setJ('tribal_R1_s1', -Math.sin(phi_B) * 15 * ramp);
        setJ('tribal_R1_s2', 22 * lift_B);
        setJ('tribal_R1_s3', (-Math.sin(phi_B) * 12 - 8 * Math.max(0, Math.cos(phi_B))) * ramp);

        setJ('tribal_L2_s1', -Math.sin(phi_B) * 12 * ramp);
        setJ('tribal_L2_s2', -18 * lift_B);
        setJ('tribal_L2_s3', (Math.sin(phi_B) * 10 + 6 * Math.max(0, Math.cos(phi_B))) * ramp);

        setJ('tribal_R3_s1', -Math.sin(phi_B) * 14 * ramp);
        setJ('tribal_R3_s2', -18 * lift_B);
        setJ('tribal_R3_s3', (Math.sin(phi_B) * 12 + 8 * Math.max(0, Math.cos(phi_B))) * ramp);

        setJ('tribal_L4_s1', -Math.sin(phi_B) * 16 * ramp);
        setJ('tribal_L4_s2', 22 * lift_B);
        setJ('tribal_L4_s3', (-Math.sin(phi_B) * 14 - 10 * Math.max(0, Math.cos(phi_B))) * ramp);

        // Body bob nhịp nhàng quanh tâm chuẩn (479, 450)
        const master = liveSvg.querySelector('#tribal-spider-master');
        if (master) {
          const bobY = Math.sin(t * 2) * 2.2 * ramp;
          const roll = Math.sin(t) * 1.2 * ramp;
          master.setAttribute('transform', `translate(0, ${bobY}) rotate(${roll}, 479, 450)`);
        }'''

c = c.replace(old_walk_step, new_walk_step)

with open('frontend/preview/spider_showcase.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Applied tribal smooth kinematics fix to spider_showcase.html!")
