#Check if config file called deployment-config.txt is present and if inside we find REGION and ACCOUNT
#If yes, display them and ask for confirmation
#If no, ask for AWS Account ID and AWS Region and save them in the config file

if [ -f deployment-config.txt ]; then
    echo "Config file found"
    echo "Reading config file"
    AWS_SEGMENT_REGION=$(cat deployment-config.txt | grep REGION | cut -d "=" -f2)
    AWS_SEGMENT_ACCOUNT=$(cat deployment-config.txt | grep ACCOUNT | cut -d "=" -f2)
    echo "AWS Account ID: $AWS_SEGMENT_ACCOUNT"
    echo "AWS Region: $AWS_SEGMENT_REGION"
    read -p "Are these values correct? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "Starting deployment"
    else
        echo "Please enter AWS Account ID"
        read AWS_SEGMENT_ACCOUNT
        echo "Please enter AWS Region"
        read AWS_SEGMENT_REGION
        echo "ACCOUNT=$AWS_SEGMENT_ACCOUNT" > deployment-config.txt
        echo "REGION=$AWS_SEGMENT_REGION" >> deployment-config.txt
        echo "Starting deployment"
    fi
else
    echo "Config file not found"
    echo "Please enter AWS Account ID"
    read AWS_SEGMENT_ACCOUNT
    echo "Please enter AWS Region"
    read AWS_SEGMENT_REGION
    echo "ACCOUNT=$AWS_SEGMENT_ACCOUNT" > deployment-config.txt
    echo "REGION=$AWS_SEGMENT_REGION" >> deployment-config.txt
    echo "Starting deployment"
fi

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap aws://$AWS_SEGMENT_ACCOUNT/$AWS_SEGMENT_REGION
cdk deploy