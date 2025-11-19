import boto3
import subprocess
import platform

class EC2ManagerX86Only:
    """
    EC2 management class that is NOT Graviton compatible.
    This code makes x86-specific assumptions and will fail on ARM64.
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.ec2_client = boto3.client('ec2', region_name=region)
        
        # PROBLEM 1: Hardcoded x86 architecture assumption
        if platform.machine() != 'x86_64':
            raise Exception("This application only supports x86_64 architecture!")
    
    def launch_x86_instance(self, key_name: str = None) -> dict:
        """
        Launch EC2 instance with hardcoded x86-specific configurations.
        This will NOT work with Graviton instances.
        """
        
        # PROBLEM 2: Hardcoded x86 AMI ID
        X86_ONLY_AMI = 'ami-0abcdef1234567890'  # Specific x86 AMI
        
        # PROBLEM 3: Hardcoded x86 instance types only
        X86_INSTANCE_TYPES = ['t3.micro', 't3.small', 'm5.large', 'c5.xlarge']
        
        launch_params = {
            'ImageId': X86_ONLY_AMI,  # Hardcoded x86 AMI
            'MinCount': 1,
            'MaxCount': 1,
            'InstanceType': 't3.micro',  # Hardcoded x86 instance type
            'UserData': self._get_x86_specific_user_data()  # x86-specific setup
        }
        
        if key_name:
            launch_params['KeyName'] = key_name
            
        try:
            response = self.ec2_client.run_instances(**launch_params)
            instance_id = response['Instances'][0]['InstanceId']
            
            # PROBLEM 4: x86-specific post-launch configuration
            self._configure_x86_specific_software(instance_id)
            
            return response
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def _get_x86_specific_user_data(self) -> str:
        """
        User data with x86-specific package installations and configurations.
        This will fail on ARM64/Graviton instances.
        """
        return """#!/bin/bash
yum update -y

# PROBLEM 5: Install x86-specific binary packages
wget example.com/x86_64/proprietary-software.rpm
rpm -i proprietary-software.rpm

# PROBLEM 6: Hardcoded x86 Docker image
docker pull --platform linux/amd64 nginx:latest
docker run -d --name web-server nginx:latest

# PROBLEM 7: x86-specific compilation flags
export CFLAGS="-march=x86-64 -mtune=intel"
export CXXFLAGS="-march=x86-64 -mtune=intel"

# PROBLEM 8: Install x86-only software
curl -O releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip
unzip terraform_1.0.0_linux_amd64.zip
mv terraform /usr/local/bin/

# PROBLEM 9: x86 assembly or architecture-specific code
cat > /tmp/x86_check.c << 'EOF'
#include <stdio.h>
#include <cpuid.h>  // x86-specific header

int main() {
    unsigned int eax, ebx, ecx, edx;
    __cpuid(0, eax, ebx, ecx, edx);  // x86-specific instruction
    printf("CPU Vendor: %.4s%.4s%.4s\
", (char*)&ebx, (char*)&edx, (char*)&ecx);
    return 0;
}
EOF

gcc -o /usr/local/bin/cpu_info /tmp/x86_check.c
"""
    
    def _configure_x86_specific_software(self, instance_id: str):
        """
        Configure software that only works on x86 architecture.
        """
        print(f"Configuring x86-specific software for instance {instance_id}")
        
        # PROBLEM 10: Assume x86 performance characteristics
        x86_optimizations = {
            'cpu_governor': 'performance',
            'numa_balancing': 'enable',
            'transparent_hugepages': 'always'  # May not be optimal for ARM64
        }
        
        # PROBLEM 11: x86-specific monitoring tools
        monitoring_commands = [
            'yum install -y intel-cmt-cat',  # Intel-specific tool
            'modprobe msr',  # x86 model-specific registers
            'wrmsr 0x1a0 0x850089'  # x86-specific MSR write
        ]
        
        print("Applied x86-specific optimizations")
    
    def install_x86_dependencies(self):
        """
        Install dependencies that are x86-specific and won't work on Graviton.
        """
        
        # PROBLEM 12: x86-specific package repositories
        x86_packages = [
            'intel-microcode',
            'amd64-microcode', 
            'libc6-dev-amd64',
            'gcc-multilib-x86-64-linux-gnu'
        ]
        
        # PROBLEM 13: Hardcoded binary downloads for x86
        binary_downloads = [
            'github.com/example/releases/download/v1.0/app-linux-amd64.tar.gz',
            'storage.googleapis.com/kubernetes-release/release/v1.21.0/bin/linux/amd64/kubectl'
        ]
        
        for package in x86_packages:
            try:
                subprocess.run(['yum', 'install', '-y', package], check=True)
            except subprocess.CalledProcessError:
                print(f"Failed to install {package} - may not be available on this architecture")
        
        print("Installed x86-specific dependencies")
    
    def get_x86_performance_metrics(self):
        """
        Collect performance metrics using x86-specific tools and assumptions.
        """
        
        # PROBLEM 14: x86-specific performance counters
        x86_counters = [
            'instructions',
            'cycles', 
            'cache-references',
            'cache-misses',
            'branch-instructions',
            'branch-misses'
        ]
        
        # PROBLEM 15: Intel/AMD specific features
        cpu_features = [
            'avx2',      # x86 SIMD extension
            'sse4_2',    # x86 SIMD extension  
            'aes',       # x86 AES instructions
            'rdrand'     # x86 random number generator
        ]
        
        print("Collecting x86-specific performance metrics...")
        return {
            'architecture': 'x86_64_only',
            'counters': x86_counters,
            'features': cpu_features
        }

# Example usage that will fail on Graviton
if __name__ == "__main__":
    try:
        # This will raise an exception if not running on x86_64
        ec2_manager = EC2ManagerX86Only()
        
        print("Launching x86-only instance...")
        result = ec2_manager.launch_x86_instance(key_name='my-key-pair')
        
        # These methods contain x86-specific code
        ec2_manager.install_x86_dependencies()
        metrics = ec2_manager.get_x86_performance_metrics()
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("This code is not compatible with ARM64/Graviton instances!")
