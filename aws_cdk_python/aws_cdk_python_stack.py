from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
)
from constructs import Construct

class AwsCdkPythonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Reemplaza con tu Account ID
        account_id = "248056481657"
        region = cdk.Aws.REGION

        # Utiliza el Rol de servicio IAM existente
        ec2_role = iam.Role.from_role_arn(
            self,
            "LabRole",
            f"arn:aws:iam::{account_id}:role/LabRole",
            mutable=False  # Asegura que el rol no se modifique
        )

        # Busca la AMI de Cloud9 Ubuntu 22.04 (ajusta el filtro según tu región)
        ami = ec2.MachineImage.lookup(
            name="Cloud9ubuntu22*",
            owners=["amazon"] # Los dueños de las AMIs de AWS suelen ser "amazon"
        )

        if not ami:
            raise Exception("No se encontró la AMI Cloud9ubuntu22 en esta región.")

        # Crea el grupo de seguridad para permitir SSH y HTTP
        security_group = ec2.SecurityGroup(
            self,
            "VockeySG",
            vpc=ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True),
            allow_all_outbound=True,
            description="Grupo de seguridad para la instancia vockey",
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Permitir SSH"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Permitir HTTP"
        )

        # Crea la instancia EC2
        instance = ec2.Instance(
            self,
            "VockeyInstance",
            instance_type=ec2.InstanceType("t2.micro"), # Puedes elegir un tipo de instancia diferente
            machine_image=ami,
            security_group=security_group,
            key_name="vockey",
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/sda1",
                    volume=ec2.BlockDeviceVolume.ebs(20, delete_on_termination=True)
                )
            ],
            role=ec2_role # Asocia el rol de servicio IAM
        )

app = cdk.App()
AwsCdkPythonStack(app, "AwsCdkPythonStack") # Usamos el nombre por defecto
app.synth()
