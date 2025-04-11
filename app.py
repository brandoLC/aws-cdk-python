
#!/usr/bin/env python3
import os
import aws_cdk as cdk  # Importamos aws-cdk desde aws-cdk-lib

from aws_cdk_python.aws_cdk_python_stack import AwsCdkPythonStack

app = cdk.App()
AwsCdkPythonStack(app, "AwsCdkPythonStack",
    # Si no especificas 'env', esta stack será agnóstica de la región/cuenta.
    # Las características dependientes de la cuenta/región y las búsquedas de contexto no funcionarán,
    # pero una plantilla sintetizada única se puede desplegar en cualquier parte.

    # Descomenta la siguiente línea para especializar esta stack para la Cuenta y Región
    # que se implican por la configuración actual de la CLI.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Descomenta la siguiente línea si sabes exactamente la Cuenta y Región
    # a la que quieres desplegar la stack.

    env=cdk.Environment(account='248056481657', region='us-east-1'),

    # Para más información, consulta la documentación oficial: 
    # https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

app.synth()

