import pygame
import random
import csv

pygame.init()

font = pygame.font.SysFont("italic", 40)
header_font = pygame.font.SysFont("comic sans", 60)

pygame.display.set_caption("Hirsipuu")

WIDTH, HEIGHT = 1000, 800
ikkuna = pygame.display.set_mode((WIDTH, HEIGHT))

kuvat = [pygame.image.load(f"hirsipuu{i}.png") for i in range(1, 8)]

def sanat_tiedostosta(tiedosto):
    sanat = []
    with open(tiedosto, newline="") as csvfile:
        lukija = csv.reader(csvfile)
        for rivi in lukija:
            sana = rivi[0].strip()
            if sana:
                sanat.append(sana.upper())
    return sanat

sanat = sanat_tiedostosta("sanalista.csv")

class Peli:

    def __init__(self):
        self.restart_game()

    def restart_game(self):
        self.arvattava_sana = random.choice(sanat)
        self.arvatut_kirjaimet = []
        self.vaarat_yritykset = 0
        self.suorita = True
        self.voitto = False
        self.havio = False
        self.kello = pygame.time.Clock()

    def piirra(self):
        ikkuna.fill((255, 255, 255))
        header_text = header_font.render("HIRSIPUU", True, (0, 0, 0))
        ikkuna.blit(header_text, (WIDTH // 2 - header_text.get_width() // 2, 20))

        if self.vaarat_yritykset >= 1:
            ikkuna.blit(kuvat[0], (150, 100))
        if self.vaarat_yritykset >= 2:
            ikkuna.blit(kuvat[1], (145, 152))
        if self.vaarat_yritykset >= 3:
            ikkuna.blit(kuvat[2], (170, 190))
        if self.vaarat_yritykset >= 4:
            ikkuna.blit(kuvat[3], (120, 290))
        if self.vaarat_yritykset >= 5:
            ikkuna.blit(kuvat[4], (170, 290))
        if self.vaarat_yritykset >= 6:
            ikkuna.blit(kuvat[5], (120, 190))
        if self.vaarat_yritykset >= 7:
            ikkuna.blit(kuvat[6], (170, 190))

        tekstipalkit = ""
        for kirjain in self.arvattava_sana:
            if kirjain in self.arvatut_kirjaimet:
                tekstipalkit += kirjain + " "
            else:
                tekstipalkit += "_ "
        teksti = font.render(tekstipalkit.strip(), True, (0, 0, 0))
        ikkuna.blit(teksti, (400, 600))

        pygame.display.update()

    def pelin_looppi(self):
        while self.suorita:
            self.kello.tick(60)
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    pygame.quit()
                    return False
                elif tapahtuma.type == pygame.KEYDOWN:
                    kirjain = tapahtuma.unicode.upper()
                    if kirjain.isalpha() and kirjain not in self.arvatut_kirjaimet:
                        self.arvatut_kirjaimet.append(kirjain)
                        if kirjain not in self.arvattava_sana:
                            self.vaarat_yritykset += 1
            self.piirra()
            self.tarkista_voitto()
            if self.voitto:
                self.lopetus("Voitit! Press 'R' to restart or 'Q' to quit.")
                if not self.restart_or_quit():
                    return False
                self.restart_game()  
            elif self.havio:
                self.lopetus(f"Hävisit! Sana oli: {self.arvattava_sana}. Press 'R' to restart or 'Q' to quit.")
                if not self.restart_or_quit():
                    return False
                self.restart_game()  

    def tarkista_voitto(self):
        self.voitto = all(kirjain in self.arvatut_kirjaimet for kirjain in self.arvattava_sana)
        self.havio = self.vaarat_yritykset >= 7

    def lopetus(self, viesti):
        teksti = font.render(viesti, True, (0, 0, 0))
        ikkuna.blit(teksti, (WIDTH // 2 - teksti.get_width() // 2, HEIGHT // 2))
        pygame.display.update()

    def restart_or_quit(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_r:  
                        return True
                    elif tapahtuma.key == pygame.K_q:  
                        pygame.quit()
                        return False
            pygame.time.delay(100)  

if __name__ == "__main__":
    peli = Peli()
    peli.pelin_looppi()

