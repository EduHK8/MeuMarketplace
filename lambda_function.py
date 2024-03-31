import json
import os
import boto3

# Obtendo a URL da fila SQS da variável de ambiente
queue_url = os.environ['SQS_QUEUE_URL']

# Criando um cliente para o SQS
sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    try:
        # Lógica para simular a compra
        # Aqui você pode adicionar a lógica para simular a compra do produto

        # Enviando uma mensagem para a fila SQS
        product_name = 'PS5'
        purchase_status = 'Concluída'
        message_body = {
            'product_name': product_name,
            'purchase_status': purchase_status
        }

        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(message_body)
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Compra simulada com sucesso! Mensagem enviada para a fila SQS.'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro ao simular a compra: {}'.format(str(e))
            })
        }

def check_status_handler(event, context):
    try:
        # Recebendo mensagens da fila SQS
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=1,
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )
        
        # Verificando se há mensagens recebidas
        messages = response.get('Messages', [])
        if messages:
            # Processando a mensagem recebida
            message = messages[0]
            body = json.loads(message['Body'])
            product_name = body.get('product_name')
            purchase_status = body.get('purchase_status')
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'product_name': product_name,
                    'purchase_status': purchase_status
                })
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'Nenhuma mensagem na fila.'
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro ao verificar o status da compra: {}'.format(str(e))
            })
        }