---
title: Config Validator
order: 104
---

# {{ page.title }}

This guide helps to set up Config Validator to secure your environment.

---

## **Overview**

Config Validator allows your administrators to enforce constraints that validate 
whether deployments can be provisioned while still enabling developers to move 
quickly within these safe guardrails. Validator accomplishes this through a 
three key components:

### One way to define constraints

Constraints are defined so that they can work across an ecosystem of 
pre-deployment and monitoring tools. These constraints live in your 
organization's repository as the source of truth for your security and 
governance requirements. You can obtain constraints from the 
[Policy Library](https://github.com/forseti-security/policy-library/blob/f65b2e67badca43caa68396b9c007f1ee12453e0/docs/user_guide.md#how-to-set-up-constraints-with-policy-library), 
or [build your own constraint templates](https://github.com/forseti-security/policy-library/blob/master/docs/constraint_template_authoring.md).

### Pre-deployment check

Check for constraint violations during pre-deployment and provide warnings or 
halt invalid deployments before they reach production. The pre-deployment logic 
that Config Validator uses will be built into a number of deployment tools. 
For details, [check out Terraform Validator](https://github.com/forseti-security/policy-library/blob/master/docs/user_guide.md#how-to-use-terraform-validator).

### Ongoing monitoring

Frequently scan the platform for constraint violations and send notifications 
when a violation is found. The monitoring logic that Config Validator uses will 
be built into a number of monitoring tools. For details, check out [Forseti 
Validator](https://github.com/forseti-security/policy-library/blob/master/docs/user_guide.md#how-to-use-forseti-config-validator).

[Policy Library repository](https://github.com/forseti-security/policy-library) contains a library of constraint templates and
sample constraints. It contains the following directories:

- `policies`
    - `constraints`: This is initially empty. You should place your constraint
     files here.
    - `templates`: This directory contains pre-defined constraint templates.
- `validator`: This directory contains the `.rego` files and their associated
   unit tests. You do not need to touch this directory unless you intend to
   modify existing constraint templates or create new ones.

---

## **How to use Config Validator**

1. To be able to use Config Validator, set the `config_validator_enabled` 
variable to `true` as part of the Terraform configuration. 
2. Choose how to provide policies to Forseti Server.

The default behavior of Forseti is to sync the Policy Library from the Forseti 
Server GCS bucket.

### **Policy Library Sync from Git Repository**

This requires work to store the Policy Library in a GitHub or other git 
repository and connect it with Forseti. Once the repository is setup, Forseti 
will automatically [sync](https://github.com/kubernetes/git-sync) policy updates to the Forseti Server to be used by 
future scans. Follow the steps below to set up Policy Library Sync from Git
repository.

As part of the Terraform configuration, few additional variables need to be 
supplied in your `main.tf` to enable the git-sync feature.

- `policy_library_sync_enabled`: Set to true to enable git-sync
- `policy_library_repository_url`: Provide the URL for your Policy Library 
repository; git protocol is recommended. 
Example: `git@github.com:forseti-security/policy-library`
- (OPTIONAL) `policy_library_sync_ssh_known_hosts`: Provide the 
[known host keys](https://www.ssh.com/ssh/host-key) for the git repository. 
This can be obtained by running `ssh-keyscan ${YOUR_GIT_HOST}`.

You should also setup an `outputs.tf` configuration file for Terraform to obtain 
the auto-generated public SSH key.

``` 
output "forseti-server-git-public-key-openssh" {
  description = "The public OpenSSH key generated to allow the Forseti Server to clone the policy library repository."
  value       = module.server.forseti-server-git-public-key-openssh
}
```

**IMPORTANT:** After applying the Terraform configuration, you will need to add 
the generated SSH key to the git user account. The SSH key will be provided as 
an output from Terraform. If the Policy Library repository is hosted on GitHub, 
you can [follow these steps to add the SSH key to your account](https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account).

To obtain the generated SSH key from Terraform run this command:

`terraform output forseti-server-git-public-key-openssh`

You can view any logs related to this process from Stackdriver Logging by 
searching for `git-sync`.

### **Policy Library Sync from GCS**

To sync policies from GCS to the Forseti server, you will need to create the 
GCS folder.

Open the Forseti project in the [Google Cloud Console](https://console.cloud.google.com/) 
and go to Storage in the menu. The Forseti Server bucket will be named 
`forseti-server-{SUFFIX}` where `{SUFFIX}` is a random 8 character suffix setup 
at the time Forseti is deployed. Create a folder with the name `policy-library` 
inside the Forseti Server bucket and make note of the suffix.

Assuming you have a local copy of your policy library repository, you can follow 
these steps to copy them to GCS (replace `{SUFFIX}` with the suffix noted above):

```
export FORSETI_BUCKET=forseti-server-{SUFFIX}
export POLICY_LIBRARY_PATH=path/to/local/policy-library
gsutil -m rsync -d -r ${POLICY_LIBRARY_PATH}/policies gs://${FORSETI_BUCKET}/policy-library/policies
gsutil -m rsync -d -r ${POLICY_LIBRARY_PATH}/lib gs://${FORSETI_BUCKET}/policy-library/lib
```

If you do not have your own constraints, you can use the sample constraints
provided by Google. Follow these steps to copy sample constraints to GCS 
(replace `{SUFFIX}` with the suffix noted above). 

```
export FORSETI_BUCKET=forseti-server-{SUFFIX}
export POLICY_LIBRARY_PATH=path/to/local/policy-library
gsutil -m rsync -d -r ${POLICY_LIBRARY_PATH}/samples gs://${FORSETI_BUCKET}/policy-library/policies/constraints
gsutil -m rsync -d -r ${POLICY_LIBRARY_PATH}/lib gs://${FORSETI_BUCKET}/policy-library/lib
```
After this is done, Forseti will pick up the new policy library content in the 
next scanner run.

Follow these steps to copy another constraint to GCS.

```
export FORSETI_BUCKET=forseti-server-{SUFFIX}
export POLICY_LIBRARY_PATH=path/to/local/policy-library
gsutil -m cp ${POLICY_LIBRARY_PATH}/policies/constraint/<CONSTRAINT_NAME> gs://${FORSETI_BUCKET}/policy-library/policies/constraints/
```

Follow these steps to copy another sample constraint to GCS.
 
```
export FORSETI_BUCKET=forseti-server-{SUFFIX}
export POLICY_LIBRARY_PATH=path/to/local/policy-library
gsutil -m cp ${POLICY_LIBRARY_PATH}/policies/samples/<CONSTRAINT_NAME> gs://${FORSETI_BUCKET}/policy-library/policies/constraints/
```

After this is done, Forseti will pick up the new policy library content in the 
next scanner run

**Note:** [Follow these steps](https://forsetisecurity.org/docs/latest/configure/notifier/index.html#cloud-scc-notification) 
to configure Forseti to send violations to Cloud Security Command Center (Cloud SCC).

## **Instantiate constraints** ##

The constraint template library only contains templates. Templates specify the 
constraint logic, and you must create constraints based on those templates 
in order to enforce them. Constraint parameters are defined as YAML files in 
the following format:

```
apiVersion: constraints.gatekeeper.sh/v1alpha1
kind: # place constraint template kind here
metadata:
  name: # place constraint name here
spec:
  severity: # low, medium, or high
  match:
    target: [] # put the constraint application target here
    exclude: [] # optional, default is no exclusions
  parameters: # put the parameters defined in constraint template her
```

- `target`: The target field is specified in a path-like format. It specifies 
where in the GCP resources hierarchy the constraint is to be applied. 
For example:

{: .table .table-striped}
| Target             | Description
| -------------------| -----------
| organization/*     | All organizations
| organization/123/* | Everything in organization 123


- `exclude`: The exclude field follows the same pattern and has precedence over 
the `target` field. If a resource is in both, it will be excluded.
- `parameters`: The schema of the parameters field is defined in the constraint 
template, using the OpenAPI V3 schema. Every template contains a validation 
section that looks like the following:

```
validation:
  openAPIV3Schema:
    properties:
      mode:
        type: string
      instances:
        type: array
        items: string
```
According to the template above, the `parameter` field in the constraint file 
should contain a string named `mode` and a string array named `instances`. 
For example:
```
parameters:
  mode: whitelist
  instances:
    - //compute.googleapis.com/projects/test-project/zones/us-east1-b/instances/one
    - //compute.googleapis.com/projects/test-project/zones/us-east1-b/instances/two
```

Here is a complete example of a sample external IP address constraint file:

```
apiVersion: constraints.gatekeeper.sh/v1alpha1
kind: GCPExternalIpAccessConstraintV1
metadata:
  name: forbid-external-ip-whitelist
spec:
  severity: high
  match:
    target: ["organization/*"]
  parameters:
    mode: "whitelist"
    instances:
    - //compute.googleapis.com/projects/test-project/zones/us-east1-b/instances/one
    - //compute.googleapis.com/projects/test-project/zones/us-east1-b/instances/two
```

## **End to end workflow with sample constraint** ##

This walkthrough allows you to apply a constraint that enforces IAM policy member 
domain restriction using Cloud Shell.

[Click  here](https://console.cloud.google.com/cloudshell/open?cloudshell_image=gcr.io/graphite-cloud-shell-images/terraform:latest&cloudshell_git_repo=https://github.com/forseti-security/policy-library.git) 
to open a new Cloud Shell session. The Cloud Shell session has Terraform 
pre-installed and the Policy Library repository cloned. Once you have the 
session open, the next step is to copy over the sample IAM domain restriction 
constraint:

`cp policy-library/samples/iam_service_accounts_only.yaml policy-library/policies/constraints`

Let's take a look at this constraint:

```
apiVersion: constraints.gatekeeper.sh/v1alpha1
kind: GCPIAMAllowedPolicyMemberDomainsConstraintV1
metadata:
  name: service_accounts_only
spec:
  severity: high
  match:
    target: ["organization/*"]
  parameters:
    domains:
      - gserviceaccount.com
```

It specifies that only members from gserviceaccount.com domain can be present 
in an IAM policy. To verify that it works, let's attempt to create a project. 
Create the following Terraform `main.tf` file:

```
provider "google" {
  version = "~> 5.0.0"
  project = "your-terraform-provider-project"
}

resource "random_id" "proj" {
  byte_length = 8
}

resource "google_project" "sample_project" {
  project_id      = "validator-${random_id.proj.hex}"
  name            = "config validator test project"
}

resource "google_project_iam_binding" "sample_iam_binding" {
  project = "${google_project.sample_project.project_id}"
  role    = "roles/owner"

  members = [
    "user:your-email@your-domain"
  ]
}

```

Make sure to specify your Terraform provider project and email address. Then 
initialize Terraform and generate a Terraform plan:

```
terraform init
terraform plan -out=test.tfplan
```

Since your email address is in the IAM policy binding, the plan should result 
in a violation. Let's try this out:

```
gsutil cp gs://terraform-validator/releases/2019-03-28/terraform-validator-linux-amd64 .
chmod 755 terraform-validator-linux-amd64
./terraform-validator-linux-amd64 validate test.tfplan --policy-path=policy-library
```

The Terraform validator should return a violation. As a test, you can relax the 
constraint to make the violation go away. Edit the 
`policy-library/policies/constraints/iam_service_accounts_only.yaml` file and 
append your email domain to the domains whitelist:

```
apiVersion: constraints.gatekeeper.sh/v1alpha1
kind: GCPIAMAllowedPolicyMemberDomainsConstraintV1
metadata:
  name: service_accounts_only
spec:
  severity: high
  match:
    target: ["organization/*"]
  parameters:
    domains:
      - gserviceaccount.com
      - your-domain-here
```

Then run Terraform plan and validate the output again:

```
terraform plan -out=test.tfplan
./terraform-validator-linux-amd64 validate test.tfplan --policy-path=policy-library
```

The command above should result in no violations found.
