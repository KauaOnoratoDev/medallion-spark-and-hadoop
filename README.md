# Projeto de Engenharia de Dados com Spark e Hadoop

Este projeto implementa um pipeline de dados utilizando Spark e Hadoop, baseado na arquitetura medallion para ETL, e finaliza gerando relatórios em Excel enviados por email.

---

## Como rodar o projeto

1. **Clone o repositório**

```bash
git clone https://github.com/KauaOnoratoDev/medallion-spark-and-hadoop.git
cd medallion-spark-and-hadoop
```


2. **Configure as variáveis de email**

Antes de executar, configure as variáveis de ambiente necessárias para o envio de email. Isso pode ser feito diretamente no docker-compose.yml. As variáveis típicas incluem:
Para gerar sua senha de app, acesse o seguinte link: https://support.google.com/accounts/answer/185833?hl=pt-BR

```bash
environment:
      REF: "email-remetente@gmail.com"
      ADD: "email-destinatario@any.com"
      PASS: "senha-app-email"
```

3. **Execute o Docker Compose**

```bash
docker-compose up
```

## Fluxo do projeto

Os containers sobem e o aplicativo Retail App inicia inserindo os dados.

O HDFS executa o processo de ETL utilizando a arquitetura medallion (bronze, silver, gold), realizando o tratamento dos dados.

Após o processamento, o container do Spark transforma os dados da camada gold em arquivos Excel.

Os arquivos Excel são enviados por email ao usuário, conforme as configurações definidas.

## Observações
Certifique-se de configurar corretamente as variáveis de email antes de rodar o projeto para garantir o envio dos relatórios.

Os logs dos containers mostrarão o andamento do processo de ingestão, ETL e envio de arquivos.

Localhost do web hadoop: http://localhost:9870
