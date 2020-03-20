---
title: Create Tests
order: 044
---

# {{ page.title }}

This page describes how to add end-to-end tests for your Forseti contributions.

---

## Overview

The stack used to run end-to-end tests consists of Kitchen, Kitchen Terraform, 
InSpec and Google Cloud Build.

[Kitchen](https://kitchen.ci/) provides a test harness to execute infrastructure 
code on one or more platforms in isolation. It supports many testing frameworks 
out of the box including InSpec.

[Kitchen-Terraform](https://github.com/newcontext-oss/kitchen-terraform) is an 
open source set of Test-Kitchen plugins for testing Terraform configuration. It 
is a tool that lets us test Terraform modules using InSpec. 

[InSpec](https://www.inspec.io/) is a free and open-source framework for testing 
and auditing applications and infrastructure. InSpec works by comparing the 
actual state of the system with the desired state expressed in InSpec code. It 
detects violations and displays findings in the form of a report, but puts us in 
control of remediation.

[Cloud Build](https://cloud.google.com/cloud-build/docs/) is a service that 
executes your builds on Google Cloud Platform infrastructure. Cloud Build can 
import source code from Google Cloud Storage, Cloud Source Repositories, GitHub, 
or Bitbucket, execute a build to your specifications, and produce artifacts such 
as Docker containers or Java archives. 

---

[Integration tests](https://github.com/forseti-security/forseti-security/tree/master/integration_tests/tests/forseti)  are hosted in the [forseti-security repository](https://github.com/forseti-security/forseti-security. InSpec framework is used to write integration tests.

- Determine if a new control need to be added for your Forseti contributions. 
- Modify the [.kitchen.yml](https://github.com/forseti-security/forseti-security/blob/master/.kitchen.yml) 
to add the new control if required. 