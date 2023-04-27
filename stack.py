from aws_cdk import (
    aws_ec2 as ec2,
    aws_iam as iam,
    core,
)

class SegmentAnythingStack(core.Stack):

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


        # Define the user data script
        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
    "yum update -y",
    "yum install -y docker",
    "systemctl start docker",
    "systemctl enable docker",
    "yum install -y git",
    "amazon-linux-extras install -y amazon-ssm-agent",
    "systemctl start amazon-ssm-agent",
    "systemctl enable amazon-ssm-agent",
    "curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose",
    "chmod +x /usr/local/bin/docker-compose",
    "git clone https://github.com/maxpastor/Track-Anything-on-AWS.git /app",
    "cd /app",
    "docker-compose up -d",
)
        instance_role = iam.Role(
            self,
            "InstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )
        # Grant permissions for Systems Manager (SSM) access and reporting
        instance_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore")
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
            user_data=user_data,
            role=instance_role,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            block_devices=[
                ec2.BlockDevice(
                    device_name="/dev/xvda",
                    volume=ec2.BlockDeviceVolume.ebs(
                        200,  # Volume size in GiB
                        volume_type=ec2.EbsDeviceVolumeType.GP3,  # General Purpose SSD
                    ),
                ),
            ],
        )
        core.CfnOutput(
            self,
            "InstancePublicDnsName",
            value=instance.instance_public_dns_name,
            description="The public DNS address of the instance",
        )
