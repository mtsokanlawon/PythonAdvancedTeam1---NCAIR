import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0: idle, 1: run, 2: jump, 3: attack1, 4: attack2, 5: hit, 6: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.attack_has_hit = False
        self.hit = False
        self.health = 100
        self.alive = True
        self.is_ai = False  # Set externally if this fighter is computer-controlled

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        self.running = False
        self.attack_type = 0

        # Computer Logic
        if self.is_ai and self.alive and target.alive and not round_over:
            # Move toward the player
            if self.rect.centerx < target.rect.centerx - 100:
                dx = SPEED
                self.running = True
            elif self.rect.centerx > target.rect.centerx + 100:
                dx = -SPEED
                self.running = True
            else:
                if self.attack_cooldown == 0:
                    self.attack(target)
                    self.attack_type = 1# if pygame.time.get_ticks() % 2 == 0 else 2

        # === Player Control ===
        elif not self.is_ai and self.attacking == False and self.alive == True and round_over == False:
            key = pygame.key.get_pressed()
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2
            elif self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # Apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Stay within screen bounds
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom
        if self.rect.top + dy < 20:
            self.vel_y = 0

        # Face opponent
        self.flip = target.rect.centerx < self.rect.centerx

        # Cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Move fighter
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit:
            self.update_action(5)
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action in [3, 4]:
                    self.attacking = False
                    self.attack_cooldown = 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 20

        # during attack animation, apply hit damage once
        if self.attacking and not self.attack_has_hit and self.action in [3, 4]:
            attack_range = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                2 * self.rect.width,
                self.rect.height
            )
            if attack_range.colliderect(self.target.rect):
                self.target.health -= 10
                self.target.hit = True # updates self.hit attribute the target object
                self.attack_has_hit = True

    # def attack(self, target):
    #     if self.attack_cooldown == 0 and not self.attacking:
    #         self.attacking = True
    #         self.attack_sound.play()
    #         self.attack_has_hit = False
    #         attack_range = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
    #         if attack_range.colliderect(target.rect):
    #             target.health -= 10
    #             target.hit = True
    #             self.attack_has_hit = True

    def attack(self, target):
        if self.attack_cooldown == 0 and not self.attacking:
            self.attacking = True
            self.attack_sound.play()
            self.attack_has_hit = False  # reset damage marker
            self.target = target  # save the target for use in update()


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
