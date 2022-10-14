---
title: Notes on AWS Lambdas
---

## Notes on AWS lambdas

### AWS Lambda in a Nutshell

AWS Lambda is a serverless computing platform that allows engineers to create a
small function, configure the function in the AWS console, and have the code
executed without the need to provision servers—paying only for the resources
used during the execution. As many organizations move towards implementing
serverless architectures, AWS Lambda would be the central building block they’ll
use.

With AWS Lambda, you run **functions** to process **events**. You can send
events to your function by invoking it with the Lambda API, or by configuring an
AWS service or resource to invoke it.  A Lambda function has a few requirements.

- The first requirement you need to satisfy is to provide a **handler**. The
  handler is the entry point for the Lambda. A Lambda function accepts
  JSON-formatted input and will usually return the same.

- The second requirement is that you’ll need to specify the **runtime
  environment** for the Lambda. The runtime will usually correlate directly with
  the language you selected to write your function.

- The final requirement is a **trigger**. You can configure a Lambda invocation
  in response to an event, such as a new file uploaded to S3, a change in a
  DynamoDB table, or a similar AWS event.  You can also configure the Lambda to
  respond to requests to AWS API Gateway, or based on a timer triggered by AWS
  Cloudwatch.


### Function

A function is a resource that you can invoke to run your code in AWS Lambda. A
function has code that processes events, and a **runtime** that passes requests
and responses between Lambda and the function code. You provide the code, and
you can use the provided runtimes or create your own. 


### Runtime

Lambda runtimes allow functions in different languages to run in the same base
execution environment. You configure your function to use a runtime that matches
your programming language. 


### Event

An event is a JSON formatted document that contains data for a function to
process. The Lambda runtime converts the event to an object and passes it to
your function code. When you invoke a function, you determine the structure and
contents of the event. When an AWS service invokes your function, the service
defines the event.

For details on events from AWS services, see [Using AWS Lambda with Other
Services](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html). 


### Concurrency

Concurrency is the number of requests that your function is serving at any given
time. When your function is invoked, Lambda provisions an instance of it to
process the event. When the function code finishes running, it can handle
another request. If the function is invoked again while a request is still being
processed, another instance is provisioned, increasing the function's
concurrency. 


### Trigger

A trigger is a resource or configuration that invokes a Lambda function. This
includes AWS services that can be configured to invoke a function, applications
that you develop, and event source mappings. An event source mapping is a
resource in Lambda that reads items from a stream or queue and invokes a
function.




