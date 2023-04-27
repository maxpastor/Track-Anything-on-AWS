python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap aws://$AWS_SEGMENT_ACCOUNT/$AWS_SEGMENT_REGION
cdk destroy --region $AWS_SEGMENT_REGION