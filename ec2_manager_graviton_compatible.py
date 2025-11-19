import boto3
import json
from typing import List, Dict, Any

class EC2Manager:
    """
    EC2 management class that works with both x86 and ARM64 (Graviton) instances.
    This code is architecture-agnostic and Graviton compatible.
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.ec2_resource = boto3.resource('ec2', region_name=region)
    
    def launch_instance(self, 
                       instance_type: str = 't3.micro',  # x86 instance by default
                       ami_id: str = None,
                       key_name: str = None,
                       security_groups: List[str] = None) -> Dict[str, Any]:
        """
        Launch an EC2 instance with architecture-agnostic configuration.
        Works with both x86 and ARM64 instances.
        """
        
        # Auto-detect appropriate AMI if not provided
        if not ami_id:
            ami_id = self._get_compatible_ami(instance_type)
        
        launch_params = {
            'ImageId': ami_id,
            'MinCount': 1,
            'MaxCount': 1,
            'InstanceType': instance_type,
            'UserData': self._get_universal_user_data()
        }
        
        if key_name:
            launch_params['KeyName'] = key_name
        if security_groups:
            launch_params['SecurityGroups'] = security_groups
            
        try:
            response = self.ec2_client.run_instances(**launch_params)
            instance_id = response['Instances'][0]['InstanceId']
            
            print(f"Successfully launched instance: {instance_id}")
            return response
            
        except Exception as e:
            print(f"Error launching instance: {str(e)}")
            return None
    
    def _get_compatible_ami(self, instance_type: str) -> str:
        """
        Get AMI that's compatible with the instance architecture.
        Automatically selects x86 or ARM64 AMI based on instance type.
        """
        # Determine architecture based on instance type
        graviton_families = ['t4g', 'c6g', 'c6gn', 'c7g', 'm6g', 'm6gd', 'r6g', 'r6gd', 'x2gd']
        is_graviton = any(instance_type.startswith(family) for family in graviton_families)
        
        architecture = 'arm64' if is_graviton else 'x86_64'
        
        # Search for latest Amazon Linux 2 AMI for the architecture
        response = self.ec2_client.describe_images(
            Owners=['amazon'],
            Filters=[
                {'Name': 'name', 'Values': ['amzn2-ami-hvm-*']},
                {'Name': 'architecture', 'Values': [architecture]},
                {'Name': 'state', 'Values': ['available']},
                {'Name': 'virtualization-type', 'Values': ['hvm']}
            ]
        )
        
        # Sort by creation date and return the latest
        images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
        return images[0]['ImageId'] if images else 'ami-0abcdef1234567890'  # fallback
    
    def _get_universal_user_data(self) -> str:
        """
        User data script that works on both x86 and ARM64 architectures.
        Uses architecture-agnostic commands and package managers.
        """
        return """#!/bin/bash
yum update -y
yum install -y docker htop curl wget

# Install Docker and start service (works on both architectures)
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user

# Install architecture-appropriate packages
ARCH=$(uname -m)
echo "Detected architecture: $ARCH" > /var/log/setup.log

# Install Node.js (architecture detection handled by installer)
curl -fsSL rpm.nodesource.com/setup_18.x | bash -
yum install -y nodejs

# Create a simple web server
cat > /home/ec2-user/server.js << 'EOF'
const http = require('http');
const os = require('os');

const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.end(\`
        <h1>Hello from EC2!</h1>
        <p>Architecture: \${os.arch()}</p>
        <p>Platform: \${os.platform()}</p>
        <p>Hostname: \${os.hostname()}</p>
    \`);
});

server.listen(3000, () => {
    console.log('Server running on port 3000');
});
EOF

chown ec2-user:ec2-user /home/ec2-user/server.js
"""

    def list_instances(self) -> List[Dict[str, Any]]:
        """
        List all EC2 instances with their architecture information.
        """
        instances = []
        
        for instance in self.ec2_resource.instances.all():
            # Get instance type details to determine architecture
            instance_type = instance.instance_type
            graviton_families = ['t4g', 'c6g', 'c6gn', 'c7g', 'm6g', 'm6gd', 'r6g', 'r6gd', 'x2gd']
            is_graviton = any(instance_type.startswith(family) for family in graviton_families)
            
            instances.append({
                'InstanceId': instance.id,
                'InstanceType': instance_type,
                'State': instance.state['Name'],
                'Architecture': 'ARM64 (Graviton)' if is_graviton else 'x86_64',
                'LaunchTime': instance.launch_time
            })
        
        return instances

# Example usage
if __name__ == "__main__":
    ec2_manager = EC2Manager()
    
    # This will launch a t3.micro (x86) instance but the code is Graviton compatible
    print("Launching x86 instance with Graviton-compatible code...")
    result = ec2_manager.launch_instance(
        instance_type='t3.micro',  # x86 instance
        key_name='my-key-pair'
    )
    
    # The same code can launch Graviton instances without modification
    print("The same code can launch Graviton instances:")
    print("ec2_manager.launch_instance(instance_type='t4g.micro')  # ARM64 Graviton")
