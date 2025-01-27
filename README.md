# AAI Robotics
![Logo](images/logo.jpeg?raw=true "Logo")
Repository to participate on SBAI ROSI challenge.

## Introdução ##
Repositório GitHub que contém um pacote ROS para participar do desafio ROSI no Simpósio Brasileiro de Automação Inteligente (SBAI). O desafio consiste em criar um pacote com algoritmos que irão controlar o robô inspetor de transportadores de correia, ROSI (RObô para Serviços de Inspeção), para cumprir algumas tarefas.

## Ficha Técnica ##
Este pacote foi feito utilizando ROS Kinetic Kame e Ubuntu 16.04 LTS, enquanto que o desafio foi preparado em ROS Melodic Morenia e Ubuntu 18.04.

A versão do V-REP utilizada é a mesma que a do desafio (3.6.2, PRO EDU), bem como a comunicação vrep-ros-interface.
Até então, não houveram quaisquer conflitos de versões do pacote.

Os arquivos com o prefixo "old_" não são mais utilizados e ainda estão no repositório apenas por segurança, por favor ignore-os.

## Instruções ##
**0)** Caso não tenha, instale a biblioteca Numpy com o comando `$ pip install numpy`

**1)** Baixe, ou clone, o pacote ROS e coloque-o na workspace desejada.

**2)** Compile o pacote usando a ferramenta catkin build. (Até o momento, não estão sendo usados nós feitos em c++).

**3)** Certifique-se de que a workspace está devidademente sourceada. ($ source devel/setup.bash).

**4)** Execute a última versão do launch. A versão é indicada pelo prefixo "vX_" no nome, onde X é a versão. Portanto, a última versão do launch é a que tiver o nome "vX_rosi_challenge.launch", com o maior valor no lugar do X.

```
$ roslaunch aai_robotics vX_rosi_challenge.launch
```


## Launchs ##
Os launchs que executam as tarefas designadas como desafios são os nomeados como "vX_rosi_challenge.launch". Aquele que deve ser executado é o launch com o maior número no lugar do X, isto é, a última versão do launch que controla o robô para realizar as tarefas.

Abaixo segue a descrição do que fazem, e quais as mudanças, em cada launch disponível no pacote.

- `rosi_teleop.launch` --> Movimenta o robô pelo teclado.

- `rosi_teleop_v2.launch` --> Movimenta o robô pelo teclado enquanto que mostra em abas separadas o que o kinect está visualizando enquanto cores (RGB) e enquanto profundidade (DEPTH).

- `rosi_control1.launch` --> Recebe do usuário uma coordenada gps (x, y) e manda o robô para ela.

- `rosi_control2.launch` --> Mesmo que o control1, mas utiliza a técnica de planejamento de campos potenciais artificiais. OBS: O campo repulsor não está devidamente implementado pois precisa da leitura do kinect para a identificação dos obstáculos, a saber, precisa da coordenada do obstáculo mais próximo.

- `v1_rosi_challenge.launch` --> Usa alguns nós para fazer com que o robô complete a tarefa da coleta andando no mapa.

- `v2_rosi_challenge.launch` --> Similar ao v1, no entanto, o robô é capaz de ir e voltar em uma parte do mapa por tempo infinito.

- `v3_rosi_challenge.launch` --> Similar ao v2, no entanto, utilizando os dados do sensor hokuyo, o braço ur5 sempre vira para o TC, de modo que a coleta é sempre realizada, independente da orientação do robô. OBS: Há alguns casos excepcionais para serem tratados.

- `v4_rosi_challenge.launch` --> Controla o robô para que dê a volta na esteira, fazendo sempre a coleta, controlada pelo hokuyo, e desviando de obstáculos, controlado pelo kinect.

- `v5_rosi_challenge.launch` --> v4 adicionado de um nó que detecta quando a câmera no ur5 vê fogo.

- `v6_rosi_challenge.launch` --> Adicionado um nó que irá cobrir os desafios de subir e descer a escada.

- `v7_rosi_challenge.launch` --> Agora o fogo detectado é marcado em um mapa da escolha da equipe (images/mapa_rosi.jpg) e foi adicionada a tarefa do toque.
![Relação entre nós e tópicos](images/v7_rqt_graph.png?raw=true "v4_rqt_graph")

## Nodes ##
Sugere-se abrir o nó de interesse para entender a implementação.

## Topics ##
Todos os tópicos criados pelos desenvolvedores começam com o prefixo aai, e têm a finalidade de facilitar as stream de dados, além de filtrar aqueles que são úteis.

- `/aai_rosi_pose` --> Tópico que contém a posição do robô filtrada, apenas a posição (x, y) e sua orientação.

- `/aai_rosi_cmd_vel` --> Tópico que contém os comandos de velocidade do robô divididos entre velocidade linear e angular.

- `/aai_depth_show` --> Tópico que contém a imagem de profundidade do kinect convertida para outra codificação.

- `/aai_fire_pose` --> Tópico que contém a posição (x, y) de um possível rolo em chamas.

## Equipe ##
Álvaro Rodrigues Araújo;

Arthur Henrique Dias Nunes;

Israel Filipe Silva Amaral.

AAI Robotics - Universidade Federal de Minas Gerais

Apostila de Simulações Robóticas(em desenvolvimento): https://pt.overleaf.com/read/mmvbybzdntcd

![Equipe](images/equipe.jpeg?raw=true "Equipe")
