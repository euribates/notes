gcloud
========================================================================


Notes on Google Cloud Build
---------------------------

Cloud Build is a service that **executes your builds on Google Cloud
Platform infrastructure**. Cloud Build can import source code from
Google Cloud Storage, Cloud Source Repositories, GitHub, or Bitbucket,
execute a build to your specifications, and produce artifacts such as
Docker containers.

Cloud Build executes your build as a series of build steps, where each
**build step is run in a Docker container**. A build step can do
anything that can be done from a container irrespective of the
environment. To perform your tasks, you can either use the supported
build steps provided by Cloud Build or wite your own build steps.

Managing VMs in GCP
-------------------

Over the last few videos we learned how to create and use virtual
machines running on GCP. We then explored how we can use one VM as a
template for creating many more VMs with the same setup. You can find a
lot more information about this in the following tutorials:

-  https://cloud.google.com/compute/docs/quickstart-linux
-  https://cloud.google.com/compute/docs/instances/create-vm-from-instance-template
-  https://cloud.google.com/sdk/docs

Terraform with Goofgle cloud
----------------------------

-  `Getting started with Terraform on Google Cloud
Platform <https://cloud.google.com/community/tutorials/getting-started-on-gcp-with-terraform>`__

Interesting articles about hybrid setups:

-  https://blog.inkubate.io/create-a-centos-7-terraform-template-for-vmware-vsphere/
-  https://www.terraform.io/docs/enterprise/before-installing/reference-architecture/gcp.html
-  https://www.hashicorp.com/resources/terraform-on-premises-hybrid-cloud-wayfair

More About Cloud Providers
--------------------------

Here are some links to some common Quotas you’ll find in various cloud
providers

-  https://cloud.google.com/compute/quotas#understanding_vm_cpu_and_ip_address_quotas

-  https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html

-  https://docs.microsoft.com/en-us/azure/azure-subscription-service-limits#service-specific-limits

More Information on Monitoring and Alerting
-------------------------------------------

Check out the following links for more information:

::

https://www.datadoghq.com/blog/monitoring-101-collecting-data/

https://www.digitalocean.com/community/tutorials/an-introduction-to-metrics-monitoring-and-alerting

https://en.wikipedia.org/wiki/High_availability

https://landing.google.com/sre/books/

Reading: Debugging Problems on the Cloud
----------------------------------------

Check out the following links for more information:

-  https://cloud.google.com/compute/docs/troubleshooting/troubleshooting-instances

-  https://docs.microsoft.com/en-us/azure/virtual-machines/troubleshooting/

-  https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-troubleshoot.htm
