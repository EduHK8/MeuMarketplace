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