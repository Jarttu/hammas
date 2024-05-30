import csv
import pygame
import random
#pitäis tehä se pygame ruutu ja semmoset tän tekstin alle
pygame.init()
    
font = pygame.font.SysFont("italic", 40)

ikkuna = pygame.display.set_mode(1000, 800)
pygame.display.set_caption("Hirsipuu")

for i in range(7):
    kuvat = pygame.image.load(f"hirsipuu{i}.png")
    
def sanat_tiedostosta(tiedosto):
    sanat = []
    with open(tiedosto, newline="") as csvfile:
        lukija = csv.reader(csvfile)
        for rivi in lukija:
            sana = rivi[0].strip().strip(",")
            if sana:
                sanat.append(sana)
    return sanat

sanat = sanat_tiedostosta("sanalista.csv")
class peli:
    def __init__(self):
        self.arvattava_sana = random.choice(sanat)
        self.arvatut_kirjaimet = []
        self.vaarat_yritykset = []
        self.suorita = True
        self.voitto = False
        self.havio = False
        self.kello = pygame.time.Clock()
    
    