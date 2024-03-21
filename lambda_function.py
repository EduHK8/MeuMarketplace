import json

def lambda_handler(event, context):
    # Aqui você pode adicionar lógica para simular a compra
    return {
        'statusCode': 200,
        'body': json.dumps('Compra simulada com sucesso!')
    }
