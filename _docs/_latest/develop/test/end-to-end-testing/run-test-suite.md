---
title: Run The End-to-end Test Suite
order: 402
---

# {{ page.title }}

This page describes how to run the end-to-end test suite for your Forseti
contributions on your local development environment. 

## Set up your development environment and run the test suite

- Create a new project in the organization. 
- Terraform uses an IAM Service Account to deploy and configure resources on 
behalf of the user. You can run the [helper script](https://github.com/terraform-google-modules/terraform-google-project-factory/blob/master/helpers/setup-sa.sh) 
to create the Service Account, grant the necessary roles to the Service Account, 
and enable the necessary APIs in the project.
- In order to execute this script, you must have an account with the following 
list of permissions: 
* resourcemanager.organizations.list
* resourcemanager.projects.list
* billing.accounts.list
* iam.serviceAccounts.create
* iam.serviceAccountKeys.create
* resourcemanager.organizations.setIamPolicy
* resourcemanager.projects.setIamPolicy
* serviceusage.services.enable on the project
* servicemanagement.services.bind on following services:
  * cloudresourcemanager.googleapis.com
  * cloudbilling.googleapis.com
  * iam.googleapis.com
  * admin.googleapis.com
  * appengine.googleapis.com
* billing.accounts.getIamPolicy on a billing account.
* billing.accounts.setIamPolicy on a billing account.
- `Billing Account Administrator` role to the admin account to be able to
create the Service Account using the helper script. You can revoke this role
after the service account is created.
- Run the script as follows:

`./helpers/setup-sa.sh <ORGANIZATION_ID> <PROJECT_NAME> [BILLING_ACCOUNT]`

- Alternatively, you can grant the following roles and enable the APIs manually.

On the organization:

* roles/resourcemanager.organizationAdmin
* roles/iam.securityReviewer

On the project:

* roles/owner
* roles/compute.instanceAdmin
* roles/compute.networkViewer
* roles/compute.securityAdmin
* roles/iam.serviceAccountAdmin
* roles/serviceusage.serviceUsageAdmin
* roles/iam.serviceAccountUser
* roles/storage.admin
* roles/cloudsql.admin

For this module to work, you need the following APIs enabled on the Forseti project.

* cloudresourcemanager.googleapis.com
* compute.googleapis.com
* serviceusage.googleapis.com

On the host project (when using shared VPC)

* roles/compute.securityAdmin
* roles/compute.networkAdmin

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
