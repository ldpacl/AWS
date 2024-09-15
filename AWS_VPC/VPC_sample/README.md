# SCENARIO

### Set up a two-tier architecture with public and private subnets. The public subnet should host a web server accessible via the internet, while the private subnet hosts a server that can communicate outbound through a NAT Gateway. Security groups should allow HTTP/SSH traffic to the public server, while keeping the private server isolated and only accessible within the VPC.