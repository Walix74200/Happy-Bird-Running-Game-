import pygame
import sys
import random
from Projectile import Gemme, Projectile

pygame.init()

largeur, hauteur = 900, 900
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Happy Bird")
clock = pygame.time.Clock()

fond = pygame.image.load("Happy_Bird_img.png").convert()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

couleur_blanc = (255, 165, 0)
couleur_blanc_survol = (255, 200, 0)
couleur_noir = (255, 255, 255)
police = pygame.font.Font(None, 36)

pygame.mixer.init()

son_clic = pygame.mixer.Sound("music_bouton.wav")
son_obstacle_passe = pygame.mixer.Sound("music_bouton.wav")

score = 0
obstacles = pygame.sprite.Group()
espace_min_tubes = 200
espace_min_ennemis = 100
delai_min_ennemi = 200

images_tubes_bas = ["demo_obstacle_bas.png", "obstacle4.png"]
images_tubes_haut = ["obstacle8.png", "obstacle5.png", "obstacle6.png", "obstacle7.png"]

images_ennemis = ["ennemi1.png", "ennemi2.png", "ennemi3.png"]


class Bouton:
    def __init__(self, x, y, largeur, hauteur, couleur, texte, action=None):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.couleur = couleur
        self.couleur_survol = couleur_blanc_survol
        self.texte = texte
        self.action = action

    def afficher(self):
        pygame.draw.rect(fenetre, self.couleur, self.rect)
        text_surf = police.render(self.texte, True, couleur_noir)
        text_rect = text_surf.get_rect(center=self.rect.center)
        fenetre.blit(text_surf, text_rect)

    def survol(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def afficher_score(self):
        score_surf = police.render(f"Score: {score}", True, couleur_noir)
        score_rect = score_surf.get_rect(topleft=(10, 10))
        fenetre.blit(score_surf, score_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("red2.png").convert_alpha()
        self.radius = 28
        self.rect = pygame.Rect(largeur // 4, hauteur // 2, 63, 64)
        self.rect.center = (largeur // 4, hauteur // 2)
        self.velocity_y = 0
        self.projectiles = pygame.sprite.Group()

    def update(self):
        global score

        self.velocity_y += 0.5
        self.rect.y += self.velocity_y
        if self.rect.bottom > hauteur:
            self.rect.bottom = hauteur
            self.velocity_y = 0

        hits = pygame.sprite.spritecollide(self, obstacles, True)
        if hits:
            score += 1
            son_obstacle_passe.play()

        self.projectiles.update()

    def jump(self):
        self.velocity_y = -10

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery)
        self.projectiles.add(projectile)
        all_sprites.add(projectile)

    def draw_hitbox(self):
        pygame.draw.circle(fenetre, (255, 0, 0), self.rect.center, self.radius, 2)


class Tube(pygame.sprite.Sprite):
    def __init__(self, start_from_top=False):
        super().__init__()

        if start_from_top:
            self.image_file = random.choice(images_tubes_haut)
        else:
            self.image_file = random.choice(images_tubes_bas)

        self.image = pygame.image.load(self.image_file).convert_alpha()
        self.rect = self.image.get_rect()

        if start_from_top:
            self.rect.x = largeur
            self.rect.y = 0
        else:
            self.rect.x = largeur
            self.rect.y = hauteur - self.rect.height

        self.velocity_x = -5
        self.is_top_tube = start_from_top

    def update(self):
        self.rect.x += self.velocity_x
        if self.rect.right < 0:
            self.kill()

class Ennemi(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_file = random.choice(images_ennemis)
        self.image = pygame.image.load(self.image_file).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = largeur
        self.rect.y = random.randint(100, hauteur - 100)
        self.velocity_x = -5
        self.velocity_y = 0

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.right < 0:
            self.rect.x = largeur
            self.rect.y = random.randint(100, hauteur - 100)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity_y = random.uniform(1, 3)
        elif self.rect.bottom >= hauteur:
            self.rect.bottom = hauteur
            self.velocity_y = random.uniform(-3, -1)

class LigneHaut(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((largeur, 2))
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)

def load_resources():
    global fond, son_clic, son_obstacle_passe
    fond = pygame.image.load("Happy_Bird_img.png").convert()
    son_clic = pygame.mixer.Sound("music_bouton.wav")
    son_obstacle_passe = pygame.mixer.Sound("music_bouton.wav")

def main():
    global obstacles
    load_resources()

    bouton_jouer = Bouton(345, 250, 300, 50, couleur_blanc, "Jouer", jouer)
    bouton_quitter = Bouton(345, 350, 300, 50, couleur_blanc, "Quitter", quitter)

    boutons = [bouton_jouer, bouton_quitter]

    jouer_musique()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for bouton in boutons:
                        if bouton.rect.collidepoint(event.pos):
                            if bouton.action:
                                bouton.action()
                                son_clic.play()

            if event.type == pygame.MOUSEMOTION:
                if bouton_jouer.survol() or bouton_quitter.survol():
                    pygame.mixer.music.set_volume(0.3)
                else:
                    pygame.mixer.music.set_volume(1.0)

        for bouton in boutons:
            if bouton.survol():
                bouton.couleur = bouton.couleur_survol
            else:
                bouton.couleur = couleur_blanc

        fenetre.blit(fond, (0, 0))

        for bouton in boutons:
            bouton.afficher()
            if bouton.action == jouer:
                bouton.afficher_score()

        pygame.display.flip()
        clock.tick(30)

def jouer():
    global score, all_sprites
    score = 0

    try:
        with open("meilleur_score.txt", "r") as file:
            contenu_fichier = file.read().strip()
            if contenu_fichier:
                meilleur_score = float(contenu_fichier)
            else:
                meilleur_score = 0
    except FileNotFoundError:
        meilleur_score = 0

    changer_musique()

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    ennemis = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    ligne_haut = LigneHaut()
    all_sprites.add(ligne_haut)

    fond_jeu = pygame.image.load("background.png").convert()
    fond_jeu2 = pygame.image.load("background_automne.png").convert()
    fond_jeu3 = pygame.image.load("background_hiver.png").convert()
    fond_jeu4 = pygame.image.load("background_printemps.png").convert()
    fond_jeu5 = pygame.image.load("background_ete.png").convert()
    fond_jeu6= pygame.image.load("background_apocalypse.png").convert()
    fond_jeu7= pygame.image.load("background_galaxie.png").convert()
    fond_x = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_a:
                    player.shoot()

        if random.randrange(100) < 5:
            if len(obstacles) == 0 or (len(obstacles) > 0 and obstacles.sprites()[-1].rect.x < largeur - espace_min_tubes):
                obstacle = Tube()
                obstacle_haut = Tube(start_from_top=True)
                all_sprites.add(obstacle, obstacle_haut)
                obstacles.add(obstacle, obstacle_haut)

        if random.randrange(100) < 2:
            if len(ennemis) == 0 or (len(ennemis) > 0 and ennemis.sprites()[-1].rect.x < largeur - delai_min_ennemi):
                ennemi_y = random.randint(100, hauteur - 100)
                while any(abs(e.rect.y - ennemi_y) < espace_min_ennemis for e in ennemis):
                    ennemi_y = random.randint(100, hauteur - 100)

                ennemi = Ennemi()
                ennemi.rect.y = ennemi_y
                ennemis.add(ennemi)
                all_sprites.add(ennemi)

        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, obstacles, True)
        if hits:
            fin_de_partie()

        hits_ennemis = pygame.sprite.spritecollide(player, ennemis, True)
        if hits_ennemis:
            fin_de_partie()

        # Check for projectile-ennemy collisions
        hits_projectiles_ennemis = pygame.sprite.groupcollide(ennemis, player.projectiles, True, True)
        for ennemi, projectiles in hits_projectiles_ennemis.items():
            ennemi.rect.x += 10
            ennemi.velocity_y = random.uniform(-3, 3)

        score += 0.1

        if pygame.sprite.spritecollide(player, [ligne_haut], False):
            fin_de_partie()

        ennemis_hits = pygame.sprite.groupcollide(ennemis, obstacles, False, False)
        for ennemi, obstacle in ennemis_hits.items():
            ennemi.rect.x += 10
            ennemi.velocity_y = random.uniform(-3, 3)
        
        if score >= 100:
            fond_jeu = fond_jeu2
        
        if score >= 200:
            fond_jeu2 = fond_jeu3
        
        if score >= 300:
            fond_jeu3 = fond_jeu4

        if score >= 400:
            fond_jeu4 = fond_jeu5
        
        if score >= 500:
            fond_jeu5 = fond_jeu6

        if score >= 600:
            fond_jeu6 = fond_jeu7
        

        fenetre.fill(BLACK)

        fenetre.blit(fond_jeu, (fond_x, 0))
        fenetre.blit(fond_jeu, (fond_x + fond_jeu.get_width(), 0))

        fond_x -= 1

        if fond_x <= -fond_jeu.get_width():
            fond_x = 0

        all_sprites.draw(fenetre)

        score_surf = police.render(f"Score: {int(score)}  Meilleur Score: {int(meilleur_score)}", True, BLACK)
        score_rect = score_surf.get_rect(topleft=(10, 10))
        fenetre.blit(score_surf, score_rect)

        pygame.display.flip()
        clock.tick(60)

meilleur_score = 0

try:
    with open("meilleur_score.txt", "r") as file:
        contenu_fichier = file.read().strip()
        if contenu_fichier:
            meilleur_score = float(contenu_fichier)
        else:
            meilleur_score = 0
except FileNotFoundError:
    pass
except ValueError:
    print("Erreur : Le contenu du fichier meilleur_score.txt n'est pas valide.")
    meilleur_score = 0

def fin_de_partie():
    global meilleur_score

    # Charger l'image du fond de fin de partie
    fond_fin_partie = pygame.image.load("Game_Over.png").convert()
    fenetre.blit(fond_fin_partie, (0, 0))

    if score > meilleur_score:
        meilleur_score = score
        with open("meilleur_score.txt", "w") as file:
            file.write(str(meilleur_score))


    score_surf = police.render(f"Score: {int(score)}", True, BLACK)
    score_rect = score_surf.get_rect(center=(largeur // 2, hauteur // 2 - 280))
    fenetre.blit(score_surf, score_rect)

    meilleur_score_surf = police.render(f"Meilleur Score: {int(meilleur_score)}", True, BLACK)
    meilleur_score_rect = meilleur_score_surf.get_rect(center=(largeur // 2, hauteur // 2 - 240))
    fenetre.blit(meilleur_score_surf, meilleur_score_rect)

    bouton_rejouer = Bouton(300, 550, 300, 50, couleur_blanc, "Rejouer", jouer)
    bouton_quitter = Bouton(300, 630, 300, 50, couleur_blanc, "Quitter", quitter)

    for bouton in [bouton_rejouer, bouton_quitter]:
        bouton.afficher()

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for bouton in [bouton_rejouer, bouton_quitter]:
                        if bouton.rect.collidepoint(event.pos):
                            if bouton.action:
                                bouton.action()
                                son_clic.play()



def quitter():
    pygame.quit()
    sys.exit()

def jouer_musique():
    pygame.mixer.music.load("Happy_B_Remix1.mp3")
    pygame.mixer.music.play(-1)

def changer_musique():
    pygame.mixer.music.load("Happy_B_Remix2.mp3")
    pygame.mixer.music.play(-1)

if __name__ == "__main__":
    main()
