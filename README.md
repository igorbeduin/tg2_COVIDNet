# COVID-XRay

Este projeto tem como objetivo a criação de um dataset unificado para pronto
uso e testes de classificação de imagens de Raio-X de possíveis casos de **COVID-19**.

Baseado nos trabalhos em <https://github.com/lindawangg/COVID-Net>, o dataset
criado utiliza como base e unifica os seguintes datasets:

- <https://github.com/ieee8023/covid-chestxray-dataset>
- <https://github.com/agchung/Figure1-COVID-chestxray-dataset>
- <https://github.com/agchung/Actualmed-COVID-chestxray-dataset>
- <https://www.kaggle.com/tawsifurrahman/covid19-radiography-database>
- <https://www.kaggle.com/c/rsna-pneumonia-detection-challenge>

## Instruções para uso

Faça *download* de cada um dos datasets de acordo com seus links respectivos.
Para cada um, guarde seu *path* e utilize o script do Jupyter notebook ```data_generator.ipynb``` passando os argumentos de *path* corretamente. Por padrão, o script espera a estrutura:

```
tg2_COVIDNet/
        |__ data_generator.ipynb
        ...
        |__ datasets/
            |__ Actualmed-COVID-chestxray-dataset/
            |__ COVID-19 Radiography Database/
            |__ covid-chestxray-dataset/
            |__ Figure1-COVID-chestxray-dataset/
            |__ rsna-pneumonia-detection-challenge/
```

Execute ```data_generator.ipynb``` definindo o path onde deseja criar o dataset em ```dst_path```. Por padrão, ```dst_path = "./target_dataset"```.

Ao final espera-se uma estrura similar à seguinte:

```
tg2_COVIDNet/
        |__ data_generator.ipynb
        |__ datasets/
            ...
        |__ target_dataset/
            |__ test/
                (classes)
            |__ train/
                (classes)
```

## TODO:
- [x] Ler cada um dos datasets corretamente (diferentes datasets exigem diferentes tipos de leitura)
- [x] Unificar todos os datasets em uma única estrutura
- [x] Aplicação de pré-filtragem
- [x] Aplicação de pós-filtragem
- [x] Separação por id de dados específicos para teste
- [x] Filtragem de imagens que estão simultaneamente em dois datasets (cohen e sirm)
- [x] Split do dataset
- [x] Criar dataset
  - [x] Criar os diretorios requeridos (destino, train/test e *classes*)
  - [x] Copiar imagens a partir do path de origem para path destino
  - [x] Para imagens em formatos não compatíveis com leitura usual, ler e salvá-la em disco no destino correto em ```.png```. Ex.: RSNA possui imagens em ```.dcm```.
- [x] Generator para leitura do ```target_dataset```
- [ ] Rotina de testes com arqs de redes
- [x] Treinamento
- [ ] Montar uma rede custom do zero pra se usar com Autokeras
- [ ] Leitura dos pesos do Autokeras e validação dos resultados
- [ ] Rotina de avaliação de resultados de treinamento