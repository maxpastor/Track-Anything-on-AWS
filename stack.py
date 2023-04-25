from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core,
)

class Ec2GpuStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        vpc = ec2.Vpc(self, "Vpc", max_azs=2)

        # Configure security group
        security_group = ec2.SecurityGroup(
            self,
            "SecurityGroup",
            vpc=vpc,
            description="Allow access to port 80",
            allow_all_outbound=True,
        )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80))

        # Create an IAM role for the instance
        instance_role = iam.Role(
            self,
            "InstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )

        # Grant permissions to access Amazon S3
        instance_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )

        # Define the user data script
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "apt-get update",
            "apt-get -y upgrade",
            "apt-get -y install docker.io",
            "systemctl start docker",
            "systemctl enable docker",
            "docker pull nvidia/cuda:latest",
            "mkdir -p /app",
            "curl -o /app/docker-compose.yml https://raw.githubusercontent.com/maxpastor/Track-Anything-on-AWS/main/docker-compose.yml",
            "docker-compose -f /app/docker-compose.yml up -d",
        )

        # Create the EC2 instance
        instance = ec2.Instance(
            self,
            "Instance",
            instance_type=ec2.InstanceType("g4dn.xlarge"),
            machine_image=ec2.MachineImage.latest_amazon_linux(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                edition=ec2.AmazonLinuxEdition.STANDARD,
                virtualization=ec2.AmazonLinuxVirt.HVM,
                storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE,
            ),
            vpc=vpc,
            security_group=security_group,
            role=instance_role,
            user_data=user_data,
        )
