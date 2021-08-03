import pygame,sys
from pygame.locals import *
from random import randint

#variáveis globais
comprimento=900
altura=480
listaInimigos=[]

class NaveEspacial(pygame.sprite.Sprite):
    '''Classe para as naves'''

    def __init__(self,comprimento,altura):
        pygame.sprite.Sprite.__init__(self)
        self.ImagemNave= pygame.image.load("imagens/nave.jpg")

        self.rect = self.ImagemNave.get_rect()
        self.rect.centerx=comprimento/2
        self.rect.centery=altura-30

        self.listaDisparo=[]
        self.Vida=True

        self.velocidade=20
        self.somDisparo=pygame.mixer.Sound("musicas/4magnusn.WAV")

    def movimentoDireita(self):
        self.rect.right+=self.velocidade
        self.movimento()
    def movimentoEsquerda(self):
        self.rect.left-=self.velocidade
        self.movimento()
    def movimento(self):
        if self.Vida==True:
            if self.rect.left<=0:
                self.rect.left=0
            elif self.rect.right>870:
                self.rect.right=870
    
    def disparar(self,x,y):
        meuProjetil=Projetil(x,y,"imagens/disparoa.jpg",True)
        self.listaDisparo.append(meuProjetil)
        self.somDisparo.play()
        
    def Desenhar(self,superficie):
        superficie.blit(self.ImagemNave,self.rect)
         
class Projetil(pygame.sprite.Sprite):
    def __init__(self,posX,posY,rota,personagem): 
        pygame.sprite.Sprite.__init__(self)

        self.imagemProjetil=pygame.image.load(rota)

        self.rect=self.imagemProjetil.get_rect()

        self.velocidadeDisparo=1

        self.rect.top=posY
        self.rect.left=posX

        self.disparoPersonagem=personagem
        
    def Trajetoria(self):
        if self.disparoPersonagem==True:
            self.rect.top=self.rect.top - self.velocidadeDisparo
        else:
            self.rect.top=self.rect.top + self.velocidadeDisparo
    def Desenhar(self, superficie):
        superficie.blit(self.imagemProjetil, self.rect)
class Invasor(pygame.sprite.Sprite):
    def __init__(self,posX,posY,distancia,imagemUm,imagemDois):
        pygame.sprite.Sprite.__init__(self)

        self.imagemA=pygame.image.load(imagemUm)
        self.imagemB=pygame.image.load(imagemDois)

        self.listaImagens=[self.imagemA, self.imagemB]
        self.posImagem=0

        self.imagemInvasor=self.listaImagens[self.posImagem]
        self.rect=self.imagemInvasor.get_rect()

        self.listaDisparo=[]
        self.velocidade= 20
        self.rect.top=posY
        self.rect.left=posX

        self.fileiraDisparo=1
        self.tempoTroca=1

        self.direita=True
        self.contador=0
        self.MaxDescida=self.rect.top+40

        self.limiteDireita=posX+distancia
        self.limiteEsquerda=posX-distancia       

    
    def Desenhar(self, superficie):
        self.imagemInvasor=self.listaImagens[self.posImagem] 
        superficie.blit(self.imagemInvasor, self.rect)
    
    def comportamento(self, tempo):
        self.movimentos()
        self.ataque()
        if self.tempoTroca == tempo:
            self.posImagem+=1
            self.tempoTroca+=1

            if self.posImagem > len(self.listaImagens)-1:
                self.posImagem=0
    def movimentos(self):
        if self.contador<3:
            self.movimentosLateral()
        else:
            self.descida()
    def descida(self):
        if self.MaxDescida==self.rect.top:
            self.contador=0
            self.MaxDescida=self.rect.top+40
        else:
            self.rect.top+=1
            
    def movimentosLateral(self):
        if self.direita==True:
            self.rect.left=self.rect.left+self.velocidade
            if self.rect.left>self.limiteDireita:
                self.direita=False

                self.contador+=1
        else:
            self.rect.left=self.rect.left-self.velocidade
            if self.rect.left<self.limiteEsquerda:
                self.direita=True
            
        
    def ataque(self):
        if (randint(0,100)<self.fileiraDisparo):
            self.disparo()
    def disparo(self):
        x,y=self.rect.center
        meuProjetil=Projetil(x,y,"imagens/disparob.jpg",False)
        self.listaDisparo.append(meuProjetil)
        


def inserirInimigos():
    posX=100
    for x in range(1,5):
        inimigos=Invasor(posX,100,40,'imagens/marcianoA.jpg', 'imagens/MarcianoB.jpg',)
        listaInimigos.append(inimigos)
        posX=posX+200
    posX=100
    for x in range(1,5):
        inimigos=Invasor(posX,0,40,'imagens/Marciano2A.jpg', 'imagens/Marciano2B.jpg',)
        listaInimigos.append(inimigos)
        posX=posX+200
    posX=100
    for x in range(1,5):
        inimigos=Invasor(posX,-100,40,'imagens/Marciano3A.jpg', 'imagens/Marciano3B.jpg',)
        listaInimigos.append(inimigos)
        posX=posX+200
        
def SpaceInvader():
    pygame.init()
       
    janela = pygame.display.set_mode((comprimento,altura))

    pygame.display.set_caption("Space Invader")

    ImagemFundo=pygame.image.load("imagens/Fondo.jpg") 

    pygame.mixer.music.load("musicas/trilha.mp3")
    pygame.mixer.music.play(5)
    
    jogador=NaveEspacial(comprimento,altura)
    inserirInimigos()
    
    

    
    
    emjogo = True
    relogio=pygame.time.Clock()
    while True:

        relogio.tick(60)
        
        tempo=pygame.time.get_ticks()/1000 
        
        for event in pygame.event.get(): # verifica se há clique no botão fechar e se sim finaliza a janela
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if emjogo==True:
                if event.type==pygame.KEYDOWN: 
                    if event.key==K_LEFT: # mover nave para esquerda quando tecla esquerda for pressionada
                        jogador.movimentoEsquerda()
                        
                    elif event.key==K_RIGHT: # mover nave para direita quando tecla direita for pressionada
                        jogador.movimentoDireita()
                        
                    elif event.key==K_s: # disparar tiro quando tecla s for pressionada
                        x,y=jogador.rect.center
                        jogador.disparar(x,y)
        janela.blit(ImagemFundo,(0,0))
        
        jogador.Desenhar(janela)
        
        
        if len(jogador.listaDisparo)>0:
            for x in jogador.listaDisparo:
                x.Desenhar(janela)
                x.Trajetoria()

                if x.rect.top<-10:
                    jogador.listaDisparo.remove(x)
                else:
                    for inimigos in listaInimigos:
                        if x.rect.colliderect(inimigos.rect):
                            listaInimigos.remove(inimigos)
                            jogador.listaDisparo.remove(x)

        if len(listaInimigos)>0:
            for inimigos in listaInimigos:
                inimigos.comportamento(tempo)
                inimigos.Desenhar(janela)

                if inimigos.rect.colliderect(jogador.rect):
                    pass 
                
                if len(inimigos.listaDisparo)>0:
                    for x in inimigos.listaDisparo:
                        x.Desenhar(janela)
                        x.Trajetoria()
                        if x.rect.colliderect(jogador.rect):
                            pass
                        
                        if x.rect.top>900:
                            inimigos.listaDisparo.remove(x)
                        else:
                            for disparo in jogador.listaDisparo:
                                if x.rect.colliderect(disparo.rect):
                                    jogador.listaDisparo.remove(disparo)
                                    inimigos.listaDisparo.remove(x) 
                            
        pygame.display.update()
SpaceInvader()
