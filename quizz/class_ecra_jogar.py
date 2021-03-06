import random
import pygame
import pygame_widgets
from pygame_widgets.button import Button
from .quizz import gerarPerguntas, guardarRegisto, avaliarPontuacao
from .class_cores import Cores as cor
from .components.textWrap import wrapline

class Jogar():

    jogo = None
    total_perguntas = 1
    respostas_corretas = 0
    pontuacao = 0
    perguntas = []
    posicao_pergunta = 0
    primeiro_render = True
    botoes = []
    validar_resposta = None
    mensagem_visivel = False
    fim_do_jogo = False
    guardar = True

    def __init__(self, jogo):
        self.jogo = jogo
        
    def construir(self, jogo):
        self.jogo = jogo
        self.jogo.ecra.fill(cor().azul_cueca)
        
        if self.primeiro_render:
            self.perguntas = gerarPerguntas(self.total_perguntas, self.jogo.categorias_seleccionadas)
            for i in range(len(self.perguntas)):
                random.shuffle(self.perguntas[i]["opcoes"])
            self.primeiro_render = False
            #Mudar para True quando volta ao menu!!!!

        if self.fim_do_jogo == False:
            self.info_jogo()
            y_pos = self.fazerPergunta(self.perguntas[self.posicao_pergunta])
            self.barra_progresso()

            if self.mensagem_visivel == True:
                self.finalizar_pergunta()
                
            if self.validar_resposta != None:
                self.mensagem(y_pos)
            
        else:
            if self.guardar == True :
                guardarRegisto(self.jogo.nome_utilizador, self.pontuacao)
                self.guardar = False
            
            mensagem, cor_pontuacao = avaliarPontuacao(self.jogo.nome_utilizador, self.pontuacao, self.total_perguntas)
            
            fim_do_jogo_fonte = pygame.font.SysFont("arial", 40, bold=True, italic=False)           
            fim_do_jogo_texto = fim_do_jogo_fonte.render("FIM DO JOGO!", 
                True, cor().preto_cueca)
            self.jogo.ecra.blit(
                fim_do_jogo_texto, (fim_do_jogo_texto.get_rect(center=self.jogo.centro_ecra)[0], 200))
            
            pontuacao_fonte = pygame.font.SysFont("arial", 40, bold=True, italic=False)           
            pontuacao_texto = pontuacao_fonte.render("Conseguiste " + str(self.pontuacao) + " Pontos", 
                True, cor_pontuacao)
            self.jogo.ecra.blit(
                pontuacao_texto, (pontuacao_texto.get_rect(center=self.jogo.centro_ecra)[0], 300))

            mensagem_fonte = pygame.font.SysFont("arial", 35, bold=False, italic=False)           

            lista_mensagem_avaliacao = wrapline(mensagem, pontuacao_fonte, 700)
            y_pos=380
            
            for linha in lista_mensagem_avaliacao :
                mensagem_avaliacao = mensagem_fonte.render(linha, 
                    True, cor_pontuacao)
                self.jogo.ecra.blit(
                    mensagem_avaliacao, (mensagem_avaliacao.get_rect(center=self.jogo.centro_ecra)[0], y_pos))
                y_pos += 41

            botaoNovaPartida = Button(
                self.jogo.ecra,
                self.jogo.centro_ecra[0] + 40,
                y_pos+60,
                240,
                75,
                text="Nova Partida",
                fontSize=40,  # Size of font
                margin=20,  # Minimum distance between text/image and edge of button
                inactiveColour=cor().cinzento_cueca,  # Colour of button when not being interacted with
                hoverColour=cor().cinzento_escuro_cueca, # Colour of button when being hovered over
                pressedColour=cor().cinzento_escuro_cueca,  # Colour of button when being clicked
                onClick=self.novaPartida  # Function to call when clicked on
                )
            self.botoes.append(botaoNovaPartida)
                        
            botaoVoltarMenu = Button(
                self.jogo.ecra,
                self.jogo.centro_ecra[0] - 240 - 40,
                y_pos+60,
                240,
                75,
                text="Voltar ao Menu",
                fontSize=40,  # Size of font
                margin=20,  # Minimum distance between text/image and edge of button
                inactiveColour=cor().cinzento_cueca,  # Colour of button when not being interacted with
                hoverColour=cor().cinzento_escuro_cueca, # Colour of button when being hovered over
                pressedColour=cor().cinzento_escuro_cueca,  # Colour of button when being clicked
                onClick=self.voltarMenu  # Function to call when clicked on
                )
            
            self.botoes.append(botaoVoltarMenu)
            
        pygame_widgets.update(self.jogo.eventos)

    
    def fazerPergunta(self, pergunta):
        pergunta_fonte = pygame.font.SysFont("arial", 32, bold=True, italic=False)

        questao = wrapline(pergunta["questao"], pergunta_fonte, 600)
        y_pos=130
        
        for linha in questao:
            textoPergunta = pergunta_fonte.render(linha, 
                True, cor().vermelho_cueca)
            self.jogo.ecra.blit(
                textoPergunta, (textoPergunta.get_rect(center=self.jogo.centro_ecra)[0], y_pos))
            y_pos += 38

        y_pos = self.imprimirOpcoes(pergunta["opcoes"], y_pos)
        return y_pos

    def imprimirOpcoes(self, respostas, y_pos):
        
        pergunta_fonte = pygame.font.SysFont("arial", 28, bold=True, italic=False)
        y_pos += 60
        for i in range(len(respostas)):
            opcao = respostas[i]            

            butt = Button(
                    self.jogo.ecra,
                    84,
                    y_pos,
                    100,
                    50,
                    text=chr(i+65),
                    fontSize=40,  # Size of font
                    margin=20,  # Minimum distance between text/image and edge of button
                    inactiveColour=cor().cinzento_cueca,  # Colour of button when not being interacted with
                    # Colour of button when being hovered over
                    hoverColour=cor().cinzento_escuro_cueca,
                    pressedColour=cor().cinzento_escuro_cueca,  # Colour of button when being clicked
                    onClickParams=(self.perguntas[self.posicao_pergunta], opcao),
                    onClick=self.validarResposta, # Function to call when clicked on)
                )
            
            self.botoes.append(butt)

            textoOpcao = pergunta_fonte.render(opcao, 
                True, cor().preto_cueca)
            self.jogo.ecra.blit(
                textoOpcao, (84+100+20, y_pos + 11))
            y_pos += 75
        return y_pos

    def info_jogo(self):
        #gerar texto: tipo Fonte, Cor e Posicao
        menu_fonte = pygame.font.SysFont("arial", 24, bold=True, italic=False)
        textoNomeUtilizador = menu_fonte.render(
            self.jogo.nome_utilizador, True, cor().verde_cueca)
        self.jogo.ecra.blit(
            textoNomeUtilizador, (20, 15))
            
        textoPontuacao = menu_fonte.render(
            str(self.pontuacao), True, cor().laranja_cueca)
        self.jogo.ecra.blit(
            textoPontuacao, (textoNomeUtilizador.get_width() + 80, 15))
    
    def barra_progresso(self):
        menu_fonte = pygame.font.SysFont("arial", 24, bold=True, italic=False)
        barra_incremento=self.jogo.tamanho_ecra[0]/self.total_perguntas
        tamanho_barra=barra_incremento*(self.posicao_pergunta + 1)
        pygame.draw.rect(self.jogo.ecra, cor().vermelho_cueca, pygame.Rect(0, 0, tamanho_barra, 10))

        textoProgresso = menu_fonte.render(
            str(self.posicao_pergunta+1) + "/" + str(self.total_perguntas), True, cor().vermelho_cueca)
        self.jogo.ecra.blit(
            textoProgresso, (self.jogo.tamanho_ecra[0] - textoProgresso.get_width() - 20, 15))

    def validarResposta(self, pergunta, resposta):
        if resposta == pergunta["respostaCerta"]:
            self.pontuacao += 1
            self.respostas_corretas += 1
            self.validar_resposta = True
        else:
            self.validar_resposta = False
        
    def finalizar_pergunta(self):
        # Esperar
        pygame.time.delay(2500)
        # Limpar a mensagem
        self.mensagem_visivel = False
        self.validar_resposta = None
        
        self.fim_do_jogo = True if self.posicao_pergunta == self.total_perguntas - 1 else False
        if not self.fim_do_jogo:
            self.posicao_pergunta += 1
        
        for botao in self.botoes:
            pygame_widgets.WidgetHandler().getWidgets().remove(botao)
        self.botoes.clear()
                
    def mensagem(self, y_pos):
        # Render da mensagem
        mensagem_fonte = pygame.font.SysFont("arial", 24, bold=True, italic=False)
        textoMensagem = mensagem_fonte.render(
            ("Resposta correcta"  if self.validar_resposta == True else "Resposta errada" ),
            True,
            (cor().verde_cueca if self.validar_resposta == True else cor().vermelho_cueca)
        )
                
        self.jogo.ecra.blit(
            textoMensagem, (textoMensagem.get_rect(center=self.jogo.centro_ecra)[0], y_pos))
            
        self.mensagem_visivel = True        

    def removerWidget(self):
        for botao in self.botoes:
            pygame_widgets.WidgetHandler().getWidgets().remove(botao)
        self.botoes.clear()

    def novaPartida(self):
        self.removerWidget()
        self.jogo.estado = self.jogo.ecras["jogar"](self.jogo)

    def voltarMenu(self):
        self.removerWidget()
        self.jogo.estado = self.jogo.ecras["menu"](self.jogo)