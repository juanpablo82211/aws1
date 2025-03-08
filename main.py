import boto3

# Crear cliente EC2
ec2 = boto3.client(
    'ec2',
    region_name='us-east-1',
  )

# Parámetros de la instancia
image_id = 'ami-08b5b3a93ed654d19'
instance_type = 't2.micro'
subnet_id = 'subnet-0b81895bcd3d1986e'
security_group_id = 'sg-0e3953b123bceb276'

tags = [{'Key': 'Name', 'Value': 'EC2_creada_en_linux'}]

# Crear instancia EC2
response = ec2.run_instances(ImageId=image_id,
                             InstanceType=instance_type,
                             MinCount=1,
                             MaxCount=1,
                             TagSpecifications=[{
                                 'ResourceType': 'instance',
                                 'Tags': tags
                             }],
                             NetworkInterfaces=[{
                                 'AssociatePublicIpAddress': True,
                                 'SubnetId': subnet_id,
                                 'DeviceIndex': 0,
                                 'Groups': [security_group_id]
                             }])

# Obtener el ID de la instancia creada
instance_id = response['Instances'][0]['InstanceId']
print(f'Instancia EC2 creada con ID: {instance_id}')

# Configurar cliente S3 con credenciales explícitas
s3 = boto3.client(
    's3',
    region_name='us-east-1',
)

bucket_name = 'juancopruebaexamenawsinstanciacreada'

try:
    # Crear el bucket correctamente (us-east-1 doesn't need LocationConstraint)
    s3.create_bucket(Bucket=bucket_name)
    print(f"El depósito '{bucket_name}' se creó correctamente.")
    # Verificar la existencia del depósito
    response = s3.head_bucket(Bucket=bucket_name)
    print(f"El depósito '{bucket_name}' existe y es accesible.")
except Exception as e:
    print(f"Ocurrió un error al crear el depósito: {e}")

#sin llaves