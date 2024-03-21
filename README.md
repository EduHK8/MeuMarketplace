# MeuMarketplace
Como usuário, desejo finalizar uma compra e ser notificado quanto ao status dessa compra.
Quanto a infraestrutura utilizada:
Deploy: Seu grupo deve fazer o deploy da solução em uma infraestrutura de nuvem, através do Localstack, utilizando Terraform.
Frontend Compra: O frontend deve ser armazenado no S3. Implemente uma interface de usuário simples com um botão para simular a compra. Quando o botão é clicado, o frontend envia uma solicitação para um endpoint do backend para simular a compra (este backend estará em um lambda).
Backend Compra: Crie um Lambda que será acionado pela solicitação do frontend. O Lambda realiza a compra (simulada) e envia uma mensagem para a fila SQS simulada contendo informações sobre a compra (nome do produto e status da compra).
Frontend Status: Pode estar no mesmo arquivo do Frontend Compra. Implemente uma parte do frontend que faz polling regularmente (ou usa websockets) para verificar o status da compra. Quando uma nova mensagem é detectada na fila SQS, o frontend é notificado e pode exibir informações relevantes ao usuário.
Backend Status - Consome o SQS e retorna o status da compra para o Frontend Status.
