
from aws_cdk import App, Stack  # Importa App y Stack desde aws-cdk-lib
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam

class AwsCdkPythonStack(Stack):  # Usar Stack de aws-cdk-lib en lugar de core.Stack
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Aquí defines los recursos, como instancias EC2, roles IAM, etc.
        # Por ejemplo, una instancia EC2:

        role = iam.Role.from_role_arn(self, "LabRole",
                                      role_arn="arn:aws:iam::248056481657:role/LabRole")  # Reemplaza con tu ARN real

        # Crear la VPC
        vpc = ec2.Vpc(self, "VPC", max_azs=3)  # Crea una VPC con 3 zonas de disponibilidad

        # Crear una instancia EC2
        instance = ec2.Instance(self, "MyEC2Instance",
                                instance_type=ec2.InstanceType("t2.micro"),  # Tipo de instancia
                                machine_image=ec2.MachineImage.generic_linux({"us-east-1": "ami-0b898040803850657"}),  # AMI de Cloud9ubuntu22
                                vpc=vpc,  # Asocia la instancia a la VPC creada
                                role=role,  # Asocia el rol IAM
                                key_name="vockey",  # Nombre de la clave SSH
                                security_group=ec2.SecurityGroup(self, "SecurityGroup", vpc=vpc),  # Seguridad
                                block_devices=[ec2.BlockDevice(
                                    device_name="/dev/sdh",  # Nombre del dispositivo
                                    volume=ec2.BlockDeviceVolume.ebs(20)  # Tamaño del disco (20GB)
                                )]
                                )

        # Abre puertos SSH (22) y HTTP (80)
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(22))  # Permite el acceso por SSH
        instance.connections.allow_from_any_ipv4(ec2.Port.tcp(80))  # Permite el acceso por HTTP

