---
title: Run Test Suite
order: 045
---

# {{ page.title }}

This page describes how to run the end-to-end test suite for your Forseti
contributions on your local development environment. 

## Set up your development environment and run the test suite

- Create a new project in the organization. 
- Terraform uses an IAM Service Account to deploy and configure resources on 
behalf of the user. You can create the Service Account and grant the necessary
roles/permissions or run the helper script that does it for you. To create the service account by 
running the helper script, `Billing Account Administrator` role needs to be granted to 
the admin account. This permission is only required to create the Service 
Account, and can be revoked afterwards.
- If you are creating Service Account by running the helper script, most of the
necessary roles will be granted and APIs will be enabled by default. You can run
the helper script by running the following command:

`./helpers/setup-sa.sh <ORGANIZATION_ID> <PROJECT_NAME> [BILLING_ACCOUNT]`

- If you are not using the helper script, you will need to grant
the roles and enable the APIs documented on the [Terraform Google Forseti 
repository](https://github.com/forseti-security/terraform-google-forseti#service-account) 
and [Terraform Google Project Factory repository](https://github.com/terraform-google-modules/terraform-google-project-factory#permissions)
to the Service Account.

- Set the following environment variables from bash shell:
```
export TF_VAR_billing_account=<YOUR_BILLING_ACCOUNT> \

export TF_VAR_domain=<YOUR_DOMAIN> \

export TF_VAR_org_id=<YOUR_ORGANIZATION_ID> \

export TF_VAR_project_id=<YOUR_PROJECT_ID> \

export SERVICE_ACCOUNT_JSON=<SERVICE_ACCOUNT_KEY>
```
- Run the following command after setting the above environment variables:

```
docker container run -it -e KITCHEN_TEST_BASE_PATH="integration_tests/tests" -e 
SERVICE_ACCOUNT_JSON -e TF_VAR_project_id -e TF_VAR_org_id -e 
TF_VAR_billing_account -e TF_VAR_domain 
-v $(pwd):/workspace gcr.io/cloud-foundation-cicd/cft/developer-tools:0.4.1
/bin/bash
```

- Run `kitchen create --test-base-path="integration_tests/tests"`. This is similar 
to terraform init and should be run once in the beginning and whenever there 
are configuration/provider changes.


- Run `kitchen converge --test-base-path="integration_tests/tests"` to setup the 
test environment, deploy Forseti and create the resources in the test 
environment.

- Run `kitchen verify --test-base-path="integration_tests/tests"` to run the 
InSpec tests.

- Run `kitchen destroy --test-base-path="integration_tests/tests"` to deconstruct 
the test environment.
