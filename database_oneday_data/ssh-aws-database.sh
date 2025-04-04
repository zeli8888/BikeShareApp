ssh -i $EC2_PEM -L 3333:comp30830.cni206o6w92y.eu-west-1.rds.amazonaws.com:3306 ubuntu@ec2-34-255-195-249.eu-west-1.compute.amazonaws.com
# public ip address is keep changing, so update this url every time you restart your instance
# $EC2_PEM is the EC2 private key path on your local computer, set it as system variable