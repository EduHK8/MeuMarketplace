import json
import os
import boto3

# Obtendo a URL da fila SQS da variável de ambiente
queue_url = os.getenv('SQS_QUEUE_URL')

# Criando um cliente para o SQS
sqs_client = boto3.client('sqs', endpoint_url=os.getenv('LOCALSTACK_SQS_URL'))

def lambda_handler(event, context):
    try:
        # Recebendo mensagens da fila SQS
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,  # Receber no máximo uma mensagem por vez
            WaitTimeSeconds=20  # Esperar até 20 segundos por novas mensagens
        )

        if 'Messages' in response:
            message = response['Messages'][0]
            receipt_handle = message['ReceiptHandle']

            # Extraindo informações da mensagem
            message_body = json.loads(message['Body'])
            product_name = message_body.get('product_name')
            purchase_status = message_body.get('purchase_status')

            # Deletando a mensagem da fila após processamento
            sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'product_name': product_name,
                    'purchase_status': purchase_status
                })
            }
        else:
            # Não há novas mensagens na fila
            return {
                'statusCode': 204,
                'body': json.dumps({
                    'message': 'Sem novas mensagens na fila.'
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro ao verificar o status da compra: {}'.format(str(e))
            })
        }
