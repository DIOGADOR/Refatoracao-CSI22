# Exercício de Laboratório 6 - ExLab2

**Autores:**  
- Samuel Jales Terrinha Guimarães  
- Rafaela Buainain Luiz  
- João Pedro Claro Garcia  
- Diogo Castro Lopes de Paula  

**Data:** Maio de 2026  

**Disciplina:** Computação T28  
**Professora:** Karla Donato Fook  
**Instituto Tecnológico de Aeronáutica – ITA**

---

## Introdução

Este relatório documenta as etapas de um projeto de refatoração do código de um jogo simples em **pygame**.  
Nessa etapa inicial, o grupo estudou e testou na prática o funcionamento do código, fazendo uma breve descrição de sua funcionalidade e um diagrama de classes. Além disso, listou-se os problemas do código-fonte e algumas refatorações propostas.

---

## Breve Descrição

Esse repositório implementa um jogo arcade simples em que o cenário parece mover-se verticalmente enquanto a nave permanece próxima da base da tela e o jogador a desloca só para os lados usando as teclas direcionais.  

O mundo visual combina um fundo contínuo com faixas laterais que também rolam, criando impressão de viagem pelo espaço. Obstáculos diferentes descem em posições horizontais aleatórias, variando tipo a cada ciclo.  

Há pontuação ligada a quantos obstáculos “passam” pela área jogável e mensagens grandes quando há colisão com as laterais ou com um obstáculo, com pausa breve antes de encerrar ou reiniciar o fluxo conforme o tipo de falha.  

Tudo está construído com **Pygame**, carregando imagens raster e texto renderizado por fontes do sistema ou personalizadas, num laço principal com clock para limitar a cadência em relação a um valor de tempo fixo equivalente ao passo entre frames.

---

## Diagrama de Classes

![Diagrama de Classes](images/Projeto%202%20de%20CSI-22.drawio_V4.png)

---

## Problemas de Manutenibilidade Identificados

- **[Código duplicado em Background.move()](ca://s?q=C%C3%B3digo_duplicado_em_Background.move)**  
  O método repete chamadas a `screen.blit()` manualmente 14 vezes para cada uma das três imagens, totalizando 42 linhas quase idênticas.  
  → Solução: substituir por um laço `for`.

- **[Hazards como atributos individuais](ca://s?q=Hazards_como_atributos_individuais)**  
  Obstáculos declarados como `hazard_1` até `hazard_5`, exigindo alterações em múltiplos locais.  
  → Solução: usar lista `self.hazards = []`.

- **[Método loop() com múltiplas responsabilidades](ca://s?q=M%C3%A9todo_loop_com_m%C3%BAltiplas_responsabilidades)**  
  Concentra inicialização, física, colisão, renderização e pontuação em 80+ linhas.  
  → Solução: extrair métodos auxiliares.

- **[Atributos de classe usados incorretamente](ca://s?q=Atributos_de_classe_usados_incorretamente)**  
  Declarados no corpo da classe em vez do `__init__`.  
  → Solução: mover para atributos de instância.

- **[Posição não gerenciada pelos objetos](ca://s?q=Posi%C3%A7%C3%A3o_n%C3%A3o_gerenciada_pelos_objetos)**  
  `x` e `y` nunca consultados, posição passada externamente.  
  → Solução: encapsular posição e criar `update()`.

- **[Constantes mágicas sem nomenclatura](ca://s?q=Constantes_m%C3%A1gicas_sem_nomenclatura)**  
  Valores como `125`, `650`, `760` aparecem sem significado.  
  → Solução: extrair para constantes nomeadas.

- **[Fonte recriada a cada frame](ca://s?q=Fonte_recriada_a_cada_frame)**  
  `pygame.font.SysFont()` instanciada em cada chamada.  
  → Solução: criar uma vez no `__init__`.

- **[Parâmetros ignorados](ca://s?q=Par%C3%A2metros_size_e_fullscreen_ignorados)**  
  `size` e `fullscreen` não usados.  
  → Solução: usar ou remover.

- **[Draw() e move() redundantes](ca://s?q=Draw_e_Move_redundantes)**  
  `draw()` chamado e sobrescrito por `move()`.  
  → Solução: consolidar em um único método.

- **[Dupla chamada a clock.tick()](ca://s?q=Dupla_chamada_a_clock.tick)**  
  Invocado duas vezes por iteração.  
  → Solução: remover redundância.

- **[Variáveis mortas](ca://s?q=Vari%C3%A1veis_mortas_no_loop)**  
  `faixaA_x` e `faixaA_y` nunca usadas.  
  → Solução: remover.

- **[Nomenclatura de constantes](ca://s?q=Nomenclatura_de_constantes)**  
  `width` e `height` em minúsculo.  
  → Solução: renomear para `WIDTH` e `HEIGHT`.

---

## Lista de Refatoração Proposta

1. Substituição de código duplicado em `Background.move()` → *Remove Duplication*  
2. Substituição de atributos individuais de hazard por coleção → *Replace Data Value with Collection*  
3. Extração de responsabilidades do método `loop()` → *Extract Method*  
4. Migração de atributos de classe para atributos de instância → *Replace Class Variables with Instance Variables*  
5. Encapsulamento da posição em `Player` e `Hazard` → *Encapsulate Field*  
6. Substituição de constantes mágicas por nomes simbólicos → *Replace Magic Number with Symbolic Constant*  
7. Criação única da fonte em `score_card()` → *Introduce Instance Variable*  
8. Remoção ou uso dos parâmetros `size` e `fullscreen` → *Remove Parameter* / *Parameterize Method*  
9. Consolidação de `draw()` e `move()` em `Background` → *Inline Method*  
10. Remoção da segunda chamada a `clock.tick()` → *Remove Dead Code*  
11. Remoção de variáveis mortas no `loop()` → *Remove Dead Code*  
12. Padronização da nomenclatura de constantes de classe → *Rename Field*

---
