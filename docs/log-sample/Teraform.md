```
ubuntu@DESKTOP-REF6HHU:~/repos/study-gcp-teraform-elastic-search$ make deploy-all
make tf-apply-infra
make[1]: Entering directory '/home/ubuntu/repos/study-gcp-teraform-elastic-search'
PYTHONPATH=scripts python3 scripts/tf_ops.py apply-infra
Initializing the backend...
Initializing provider plugins...
- Finding hashicorp/google versions matching "~> 5.0"...
- Finding elastic/ec versions matching "~> 0.12"...
- Installing hashicorp/google v5.45.2...
- Installed hashicorp/google v5.45.2 (signed by HashiCorp)
- Installing elastic/ec v0.12.4...
- Installed elastic/ec v0.12.4 (signed by a HashiCorp partner, key ID 7FE579EDEC6DAA7B)
Partner and community providers are signed by their developers.
If you'd like to know more about provider signing, you can read about it here:
https://developer.hashicorp.com/terraform/cli/plugins/signing
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
data.google_project.project: Reading...
data.google_project.project: Read complete after 1s [id=projects/mlops-dev-a]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # ec_deployment.hello will be created
  + resource "ec_deployment" "hello" {
      + alias                  = (known after apply)
      + deployment_template_id = "gcp-storage-optimized"
      + elasticsearch          = {
          + autoscale      = (known after apply)
          + cloud_id       = (known after apply)
          + hot            = {
              + autoscaling                           = {
                  + autoscale            = (known after apply)
                  + max_size             = (known after apply)
                  + max_size_resource    = (known after apply)
                  + min_size             = (known after apply)
                  + min_size_resource    = (known after apply)
                  + policy_override_json = (known after apply)
                }
              + instance_configuration_id             = (known after apply)
              + instance_configuration_version        = (known after apply)
              + latest_instance_configuration_id      = (known after apply)
              + latest_instance_configuration_version = (known after apply)
              + node_roles                            = (known after apply)
              + node_type_data                        = (known after apply)
              + node_type_ingest                      = (known after apply)
              + node_type_master                      = (known after apply)
              + node_type_ml                          = (known after apply)
              + size                                  = "1g"
              + size_resource                         = "memory"
              + zone_count                            = 1
            }
          + http_endpoint  = (known after apply)
          + https_endpoint = (known after apply)
          + ref_id         = "main-elasticsearch"
          + region         = (known after apply)
          + resource_id    = (known after apply)
          + snapshot       = (known after apply)
          + trust_account  = (known after apply)
          + trust_external = (known after apply)
        }
      + elasticsearch_password = (sensitive value)
      + elasticsearch_username = (known after apply)
      + id                     = (known after apply)
      + kibana                 = {
          + elasticsearch_cluster_ref_id          = "main-elasticsearch"
          + http_endpoint                         = (known after apply)
          + https_endpoint                        = (known after apply)
          + instance_configuration_id             = (known after apply)
          + instance_configuration_version        = (known after apply)
          + latest_instance_configuration_id      = (known after apply)
          + latest_instance_configuration_version = (known after apply)
          + ref_id                                = "main-kibana"
          + region                                = (known after apply)
          + resource_id                           = (known after apply)
          + size                                  = "1g"
          + size_resource                         = "memory"
          + zone_count                            = 1
        }
      + name                   = "hello-elastic"
      + region                 = "gcp-asia-northeast1"
      + request_id             = (known after apply)
      + traffic_filter         = []
      + version                = "9.3.2"
    }

  # google_artifact_registry_repository.hello will be created
  + resource "google_artifact_registry_repository" "hello" {
      + create_time      = (known after apply)
      + effective_labels = (known after apply)
      + format           = "DOCKER"
      + id               = (known after apply)
      + location         = "asia-northeast1"
      + mode             = "STANDARD_REPOSITORY"
      + name             = (known after apply)
      + project          = "mlops-dev-a"
      + repository_id    = "hello-elastic-repo"
      + terraform_labels = (known after apply)
      + update_time      = (known after apply)
    }

  # google_secret_manager_secret.elastic will be created
  + resource "google_secret_manager_secret" "elastic" {
      + create_time           = (known after apply)
      + effective_annotations = (known after apply)
      + effective_labels      = (known after apply)
      + expire_time           = (known after apply)
      + id                    = (known after apply)
      + name                  = (known after apply)
      + project               = "mlops-dev-a"
      + secret_id             = "hello-elastic-api-key"
      + terraform_labels      = (known after apply)

      + replication {
          + user_managed {
              + replicas {
                  + location = "asia-northeast1"
                }
            }
        }
    }

  # google_secret_manager_secret_iam_member.hello will be created
  + resource "google_secret_manager_secret_iam_member" "hello" {
      + etag      = (known after apply)
      + id        = (known after apply)
      + member    = "serviceAccount:941178142366-compute@developer.gserviceaccount.com"
      + project   = (known after apply)
      + role      = "roles/secretmanager.secretAccessor"
      + secret_id = (known after apply)
    }

  # google_secret_manager_secret_version.elastic will be created
  + resource "google_secret_manager_secret_version" "elastic" {
      + create_time           = (known after apply)
      + deletion_policy       = "DELETE"
      + destroy_time          = (known after apply)
      + enabled               = true
      + id                    = (known after apply)
      + is_secret_data_base64 = false
      + name                  = (known after apply)
      + secret                = (known after apply)
      + secret_data           = (sensitive value)
      + version               = (known after apply)
    }

Plan: 5 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + elasticsearch_endpoint = (known after apply)
  + secret_name            = "hello-elastic-api-key"
google_secret_manager_secret.elastic: Creating...
google_artifact_registry_repository.hello: Creating...
ec_deployment.hello: Creating...
google_secret_manager_secret.elastic: Creation complete after 1s [id=projects/mlops-dev-a/secrets/hello-elastic-api-key]
google_secret_manager_secret_iam_member.hello: Creating...
google_secret_manager_secret_iam_member.hello: Creation complete after 6s [id=projects/mlops-dev-a/secrets/hello-elastic-api-key/roles/secretmanager.secretAccessor/serviceAccount:941178142366-compute@developer.gserviceaccount.com]
google_artifact_registry_repository.hello: Still creating... [00m10s elapsed]
ec_deployment.hello: Still creating... [00m10s elapsed]
google_artifact_registry_repository.hello: Creation complete after 11s [id=projects/mlops-dev-a/locations/asia-northeast1/repositories/hello-elastic-repo]
ec_deployment.hello: Still creating... [00m20s elapsed]
ec_deployment.hello: Still creating... [00m30s elapsed]
ec_deployment.hello: Still creating... [00m40s elapsed]
ec_deployment.hello: Still creating... [00m50s elapsed]
ec_deployment.hello: Still creating... [01m00s elapsed]
ec_deployment.hello: Still creating... [01m10s elapsed]
ec_deployment.hello: Still creating... [01m20s elapsed]
ec_deployment.hello: Still creating... [01m30s elapsed]
ec_deployment.hello: Still creating... [01m40s elapsed]
ec_deployment.hello: Still creating... [01m50s elapsed]
ec_deployment.hello: Still creating... [02m00s elapsed]
ec_deployment.hello: Still creating... [02m10s elapsed]
ec_deployment.hello: Still creating... [02m20s elapsed]
ec_deployment.hello: Still creating... [02m30s elapsed]
ec_deployment.hello: Still creating... [02m40s elapsed]
ec_deployment.hello: Creation complete after 2m45s [id=306aa711c9a9d0fe396117e708259ef4]
google_secret_manager_secret_version.elastic: Creating...
google_secret_manager_secret_version.elastic: Creation complete after 2s [id=projects/941178142366/secrets/hello-elastic-api-key/versions/1]
╷
│ Warning: Resource targeting is in effect
│ 
│ You are creating a plan with the -target option, which means that the result of this plan may not represent all of the changes requested by the current configuration.
│ 
│ The -target option is not for routine use, and is provided only for exceptional situations such as recovering from errors or mistakes, or when Terraform specifically suggests to use it as part of an error message.
╵
╷
│ Warning: Applied changes may be incomplete
│ 
│ The plan was created with the -target option in effect, so some changes requested in the configuration may have been ignored and the output values may not be fully updated. Run the following command to verify that no other changes are pending:
│     terraform plan
│ 
│ Note that the -target option is not suitable for routine use, and is provided only for exceptional situations such as recovering from errors or mistakes, or when Terraform specifically suggests to use it as part of an error message.
╵

Apply complete! Resources: 5 added, 0 changed, 0 destroyed.

Outputs:

elasticsearch_endpoint = "https://a1dce6802640427c9adb5217c418aa62.asia-northeast1.gcp.cloud.es.io:443"
secret_name = "hello-elastic-api-key"
make[1]: Leaving directory '/home/ubuntu/repos/study-gcp-teraform-elastic-search'
make push
make[1]: Entering directory '/home/ubuntu/repos/study-gcp-teraform-elastic-search'
PYTHONPATH=scripts python3 scripts/docker_ops.py push
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/

Sending build context to Docker daemon  6.656kB
Step 1/6 : FROM python:3.11-slim
 ---> e67db9b14d09
Step 2/6 : WORKDIR /app
 ---> Using cache
 ---> bdc24ac17627
Step 3/6 : COPY requirements.txt .
 ---> 7e445b2ffa2c
Step 4/6 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Running in 4e880b6cd4ae
Collecting elasticsearch==8.13.0 (from -r requirements.txt (line 1))
  Downloading elasticsearch-8.13.0-py3-none-any.whl.metadata (6.3 kB)
Collecting google-cloud-secret-manager==2.22.0 (from -r requirements.txt (line 2))
  Downloading google_cloud_secret_manager-2.22.0-py2.py3-none-any.whl.metadata (5.3 kB)
Collecting elastic-transport<9,>=8.13 (from elasticsearch==8.13.0->-r requirements.txt (line 1))
  Downloading elastic_transport-8.17.1-py3-none-any.whl.metadata (3.8 kB)
Collecting google-api-core!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading google_api_core-2.30.2-py3-none-any.whl.metadata (3.1 kB)
Collecting google-auth!=2.24.0,!=2.25.0,<3.0.0dev,>=2.14.1 (from google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading google_auth-2.49.1-py3-none-any.whl.metadata (6.2 kB)
Collecting proto-plus<2.0.0dev,>=1.22.3 (from google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading proto_plus-1.27.2-py3-none-any.whl.metadata (2.2 kB)
Collecting protobuf!=4.21.0,!=4.21.1,!=4.21.2,!=4.21.3,!=4.21.4,!=4.21.5,<6.0.0dev,>=3.20.2 (from google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading protobuf-5.29.6-cp38-abi3-manylinux2014_x86_64.whl.metadata (592 bytes)
Collecting grpc-google-iam-v1<1.0.0dev,>=0.12.4 (from google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading grpc_google_iam_v1-0.14.4-py3-none-any.whl.metadata (9.1 kB)
Collecting urllib3<3,>=1.26.2 (from elastic-transport<9,>=8.13->elasticsearch==8.13.0->-r requirements.txt (line 1))
  Downloading urllib3-2.6.3-py3-none-any.whl.metadata (6.9 kB)
Collecting certifi (from elastic-transport<9,>=8.13->elasticsearch==8.13.0->-r requirements.txt (line 1))
  Downloading certifi-2026.2.25-py3-none-any.whl.metadata (2.5 kB)
Collecting googleapis-common-protos<2.0.0,>=1.63.2 (from google-api-core!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading googleapis_common_protos-1.74.0-py3-none-any.whl.metadata (9.2 kB)
Collecting requests<3.0.0,>=2.20.0 (from google-api-core!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading requests-2.33.1-py3-none-any.whl.metadata (4.8 kB)
Collecting grpcio<2.0.0,>=1.33.2 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading grpcio-1.80.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (3.8 kB)
Collecting grpcio-status<2.0.0,>=1.33.2 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading grpcio_status-1.80.0-py3-none-any.whl.metadata (1.3 kB)
Collecting pyasn1-modules>=0.2.1 (from google-auth!=2.24.0,!=2.25.0,<3.0.0dev,>=2.14.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading pyasn1_modules-0.4.2-py3-none-any.whl.metadata (3.5 kB)
Collecting cryptography>=38.0.3 (from google-auth!=2.24.0,!=2.25.0,<3.0.0dev,>=2.14.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading cryptography-46.0.6-cp311-abi3-manylinux_2_34_x86_64.whl.metadata (5.7 kB)
Collecting cffi>=2.0.0 (from cryptography>=38.0.3->google-auth!=2.24.0,!=2.25.0,<3.0.0dev,>=2.14.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.6 kB)
Collecting typing-extensions~=4.12 (from grpcio<2.0.0,>=1.33.2->google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
INFO: pip is looking at multiple versions of grpcio-status to determine which version is compatible with other requirements. This could take a while.
Collecting grpcio-status<2.0.0,>=1.33.2 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading grpcio_status-1.78.0-py3-none-any.whl.metadata (1.3 kB)
  Downloading grpcio_status-1.76.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.75.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.75.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.74.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.73.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.73.0-py3-none-any.whl.metadata (1.1 kB)
INFO: pip is still looking at multiple versions of grpcio-status to determine which version is compatible with other requirements. This could take a while.
  Downloading grpcio_status-1.72.2-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.72.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.71.2-py3-none-any.whl.metadata (1.1 kB)
Collecting pyasn1<0.7.0,>=0.6.1 (from pyasn1-modules>=0.2.1->google-auth!=2.24.0,!=2.25.0,<3.0.0dev,>=2.14.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading pyasn1-0.6.3-py3-none-any.whl.metadata (8.4 kB)
Collecting charset_normalizer<4,>=2 (from requests<3.0.0,>=2.20.0->google-api-core!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading charset_normalizer-3.4.7-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 40.9/40.9 kB 1.9 MB/s eta 0:00:00
Collecting idna<4,>=2.5 (from requests<3.0.0,>=2.20.0->google-api-core!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Collecting pycparser (from cffi>=2.0.0->cryptography>=38.0.3->google-auth!=2.24.0,!=2.25.0,<3.0.0dev,>=2.14.1->google-cloud-secret-manager==2.22.0->-r requirements.txt (line 2))
  Downloading pycparser-3.0-py3-none-any.whl.metadata (8.2 kB)
Downloading elasticsearch-8.13.0-py3-none-any.whl (451 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 451.0/451.0 kB 9.7 MB/s eta 0:00:00
Downloading google_cloud_secret_manager-2.22.0-py2.py3-none-any.whl (208 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 208.2/208.2 kB 74.4 MB/s eta 0:00:00
Downloading elastic_transport-8.17.1-py3-none-any.whl (64 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65.0/65.0 kB 285.2 MB/s eta 0:00:00
Downloading google_api_core-2.30.2-py3-none-any.whl (173 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 173.2/173.2 kB 114.5 MB/s eta 0:00:00
Downloading google_auth-2.49.1-py3-none-any.whl (240 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 240.7/240.7 kB 108.7 MB/s eta 0:00:00
Downloading grpc_google_iam_v1-0.14.4-py3-none-any.whl (32 kB)
Downloading proto_plus-1.27.2-py3-none-any.whl (50 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 50.5/50.5 kB 213.9 MB/s eta 0:00:00
Downloading protobuf-5.29.6-cp38-abi3-manylinux2014_x86_64.whl (320 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 320.5/320.5 kB 73.5 MB/s eta 0:00:00
Downloading cryptography-46.0.6-cp311-abi3-manylinux_2_34_x86_64.whl (4.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 49.9 MB/s eta 0:00:00
Downloading googleapis_common_protos-1.74.0-py3-none-any.whl (300 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 300.7/300.7 kB 145.9 MB/s eta 0:00:00
Downloading grpcio-1.80.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (6.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.8/6.8 MB 87.4 MB/s eta 0:00:00
Downloading grpcio_status-1.71.2-py3-none-any.whl (14 kB)
Downloading pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 181.3/181.3 kB 253.2 MB/s eta 0:00:00
Downloading requests-2.33.1-py3-none-any.whl (64 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 64.9/64.9 kB 295.2 MB/s eta 0:00:00
Downloading certifi-2026.2.25-py3-none-any.whl (153 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 153.7/153.7 kB 183.5 MB/s eta 0:00:00
Downloading urllib3-2.6.3-py3-none-any.whl (131 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 131.6/131.6 kB 234.7 MB/s eta 0:00:00
Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (215 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 215.6/215.6 kB 243.3 MB/s eta 0:00:00
Downloading charset_normalizer-3.4.7-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (214 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 214.1/214.1 kB 237.4 MB/s eta 0:00:00
Downloading idna-3.11-py3-none-any.whl (71 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 71.0/71.0 kB 268.9 MB/s eta 0:00:00
Downloading pyasn1-0.6.3-py3-none-any.whl (83 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 84.0/84.0 kB 236.6 MB/s eta 0:00:00
Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 44.6/44.6 kB 289.3 MB/s eta 0:00:00
Downloading pycparser-3.0-py3-none-any.whl (48 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 48.2/48.2 kB 159.4 MB/s eta 0:00:00
Installing collected packages: urllib3, typing-extensions, pycparser, pyasn1, protobuf, idna, charset_normalizer, certifi, requests, pyasn1-modules, proto-plus, grpcio, googleapis-common-protos, elastic-transport, cffi, grpcio-status, elasticsearch, cryptography, grpc-google-iam-v1, google-auth, google-api-core, google-cloud-secret-manager
Successfully installed certifi-2026.2.25 cffi-2.0.0 charset_normalizer-3.4.7 cryptography-46.0.6 elastic-transport-8.17.1 elasticsearch-8.13.0 google-api-core-2.30.2 google-auth-2.49.1 google-cloud-secret-manager-2.22.0 googleapis-common-protos-1.74.0 grpc-google-iam-v1-0.14.4 grpcio-1.80.0 grpcio-status-1.71.2 idna-3.11 proto-plus-1.27.2 protobuf-5.29.6 pyasn1-0.6.3 pyasn1-modules-0.4.2 pycparser-3.0 requests-2.33.1 typing-extensions-4.15.0 urllib3-2.6.3
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv

[notice] A new release of pip is available: 24.0 -> 26.0.1
[notice] To update, run: pip install --upgrade pip
 ---> Removed intermediate container 4e880b6cd4ae
 ---> 7f772a35edde
Step 5/6 : COPY main.py .
 ---> f47bcb4e866e
Step 6/6 : CMD ["python", "main.py"]
 ---> Running in 356cd3fce989
 ---> Removed intermediate container 356cd3fce989
 ---> 3138346d618a
Successfully built 3138346d618a
Successfully tagged asia-northeast1-docker.pkg.dev/mlops-dev-a/hello-elastic-repo/hello-elastic-job:latest
The push refers to repository [asia-northeast1-docker.pkg.dev/mlops-dev-a/hello-elastic-repo/hello-elastic-job]
9fa30ced0dc2: Pushed 
6a37de562e10: Pushed 
c76b7f8c98ab: Pushed 
225feb097fe8: Mounted from mlops-dev-a/mlops-dev-a-docker/todo-app 
8347a0657a00: Mounted from mlops-dev-a/mlops-dev-a-docker/todo-app 
34b037810a00: Mounted from mlops-dev-a/mlops-dev-a-docker/todo-app 
188695d9eb1d: Mounted from mlops-dev-a/mlops-dev-a-docker/todo-app 
188c9b34dfbe: Mounted from mlops-dev-a/mlops-dev-a-docker/todo-app 
latest: digest: sha256:a0f952ca0fb604ed15fca8ef8095488683bda7ec799b04abf82dabf0b9d07b77 size: 1992
make[1]: Leaving directory '/home/ubuntu/repos/study-gcp-teraform-elastic-search'
make tf-apply
make[1]: Entering directory '/home/ubuntu/repos/study-gcp-teraform-elastic-search'
PYTHONPATH=scripts python3 scripts/tf_ops.py apply
ec_deployment.hello: Refreshing state... [id=306aa711c9a9d0fe396117e708259ef4]
data.google_project.project: Reading...
google_secret_manager_secret.elastic: Refreshing state... [id=projects/mlops-dev-a/secrets/hello-elastic-api-key]
google_artifact_registry_repository.hello: Refreshing state... [id=projects/mlops-dev-a/locations/asia-northeast1/repositories/hello-elastic-repo]
data.google_project.project: Read complete after 1s [id=projects/mlops-dev-a]
google_secret_manager_secret_iam_member.hello: Refreshing state... [id=projects/mlops-dev-a/secrets/hello-elastic-api-key/roles/secretmanager.secretAccessor/serviceAccount:941178142366-compute@developer.gserviceaccount.com]
google_secret_manager_secret_version.elastic: Refreshing state... [id=projects/941178142366/secrets/hello-elastic-api-key/versions/1]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_cloud_run_v2_job.hello will be created
  + resource "google_cloud_run_v2_job" "hello" {
      + conditions               = (known after apply)
      + create_time              = (known after apply)
      + creator                  = (known after apply)
      + delete_time              = (known after apply)
      + effective_annotations    = (known after apply)
      + effective_labels         = (known after apply)
      + etag                     = (known after apply)
      + execution_count          = (known after apply)
      + expire_time              = (known after apply)
      + generation               = (known after apply)
      + id                       = (known after apply)
      + last_modifier            = (known after apply)
      + latest_created_execution = (known after apply)
      + launch_stage             = (known after apply)
      + location                 = "asia-northeast1"
      + name                     = "hello-elastic-job"
      + observed_generation      = (known after apply)
      + project                  = "mlops-dev-a"
      + reconciling              = (known after apply)
      + terminal_condition       = (known after apply)
      + terraform_labels         = (known after apply)
      + uid                      = (known after apply)
      + update_time              = (known after apply)

      + template {
          + parallelism = (known after apply)
          + task_count  = (known after apply)

          + template {
              + execution_environment = (known after apply)
              + max_retries           = 3
              + service_account       = (known after apply)
              + timeout               = (known after apply)

              + containers {
                  + image = "asia-northeast1-docker.pkg.dev/mlops-dev-a/hello-elastic-repo/hello-elastic-job:latest"

                  + env {
                      + name  = "GCP_PROJECT"
                      + value = "mlops-dev-a"
                    }
                  + env {
                      + name  = "ES_SECRET_NAME"
                      + value = "hello-elastic-api-key"
                    }

                  + resources (known after apply)
                }
            }
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + artifact_registry_url  = "asia-northeast1-docker.pkg.dev/mlops-dev-a/hello-elastic-repo"
  + cloud_run_job_name     = "hello-elastic-job"
google_cloud_run_v2_job.hello: Creating...
google_cloud_run_v2_job.hello: Still creating... [00m10s elapsed]
google_cloud_run_v2_job.hello: Creation complete after 11s [id=projects/mlops-dev-a/locations/asia-northeast1/jobs/hello-elastic-job]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.

Outputs:

artifact_registry_url = "asia-northeast1-docker.pkg.dev/mlops-dev-a/hello-elastic-repo"
cloud_run_job_name = "hello-elastic-job"
elasticsearch_endpoint = "https://a1dce6802640427c9adb5217c418aa62.asia-northeast1.gcp.cloud.es.io:443"
secret_name = "hello-elastic-api-key"
make[1]: Leaving directory '/home/ubuntu/repos/study-gcp-teraform-elastic-search'
```