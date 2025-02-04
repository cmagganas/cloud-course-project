Decision:
- `PUT /v1/files/:filePath?type=image&prompt=...`
- 
- `PUT /v1/generated/files/:filePath?type=image&prompt=...` 

Points to cover:
- cold starts and state in the global scope of the function, e.g. `global state += 1`

Resources:
- 10-min presentation on reserved concurrency (max total concurrent lambdas in whole account/region) vs. provisioned concurrency (scaling rate) https://www.youtube.com/watch?v=7Bc97tAySkU
- 21-min video about IAM policies: https://www.youtube.com/watch?v=_ZCTvmaPgao&t=989s
- Guille's guide to AWS IAM: https://newsletter.simpleaws.dev/p/aws-iam-permissions-a-comprehensive-guide

## Introduce - ("lambda is firecracker containers in Rust" [source](https://blog.bytebytego.com/p/how-does-aws-lambda-work-behind-the)--the lifecycle)
1. Introduce AWS lambda
   1. Official intro: https://www.youtube.com/watch?v=GEABePyhFPA&list=PLJo-rJlep0EDrsfYmx6ygsqWKeHEW188j&index=9
   2. My intro: "Basically you upload scripts. AWS waits for an event. When that happens, AWS quickly prepares an "execution environment"--basically a server with your code's programming language installed and RAM/CPU that you asked for. The server quickly downloads and runs the script. Then waits a period before shutting it down. If another event happens before shut down, the existing environment is reused and the next request is much faster.

    > ![IMPORTANT]
    > When we actually deploy our app and look at dependencies THEN bring up lambda lith vs not. It felt out of
    > place in this video.

      1. My take: you should always start with it if you can since it's not running all the time. Unless you know from the outset
        your project will have high traffic.
      2. You can put REST APIs in lambdas. Ours is a lambda-lith, technically that means longer coldstarts and more billed time.
         But the benefit is our code is extremely portable. And if we can stay <250MB is we avoid paying for "always on" servers.  We can go to 10GB with docker, but
         I hear those coldstart times are a lot longer/more expensive since the full image has to be installed.
   3. Here's are diagrams of the billing:
      1. Many visuals on cold starts: https://docs.aws.amazon.com/lambda/latest/operatorguide/execution-environments.html#cold-start-latency
      2. Many visuals on execution environment lifecycle: https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html
      3. AWS Lambda pricing calculator: https://calculator.aws/#/createCalculator/Lambda (makes more sense after creating one in the UI and playing with it a bit)

1. execute - where do the logs go
2. state and cold starts
3. environment variables

## Use the UI
2. Create a lambda function in the UI
   1. test invoke
   2. show logs
   3. show environment variables
   4. show the different event types--talk about triggers
3. Execution environments
   1. `global state; state += 1`
   2. Cold starts
4. Use boto3 in the UI to try and put an object in a bucket
5. Point out weaknesses of the UI DevEx
   1. We need to grant it more **permissions** (try to hit an s3 bucket)
   2. We want to code in **our editor** (how can I work without github copilot???)
   3. we want to add our own **libraries** (don't mention x64 vs ARM yet besides that ARM is cheaper)
   4. We'll want a quick way to **update** the function for iteration
   5. Later: reproducibility of setup. "What are all the settings you set in the UI to make this function back in the day???"
      1. We'll **script** the creation/updating of the infra

## Permissions
1. Go to the IAM role created in the console. Add a policy to the role. Talk about
   1. Role -> Policy = one-to-many
   2. Role has a trust policy allowing AWS lambda to assume it
   3. Anatomy of policies: Allow/Deny, Principal, Action, Resource(s), Condition
       4. Action: show the API endpoints of AWS, e.g. PutObject, GetObject.
       5. Resource: which buckets? Which objects in those buckets?
       6. Condition: fancier selectors, e.g. tags on the objects or bucket
    4. Show the policy creation UI: wizard vs JSON
    5. Show the policy simulator: https://policysim.aws.amazon.com/home/index.jsp?#roles/test-func-role

## Bring it local
1. Create the same s3 function, but locally. 
   1. Talk about the handler/function `index.handler()`
   2. Give it 2 files to demonstrate. 
   3. Don't give it deps. Rely on boto3 already being there.
   4. Zip and use the CLI to upload it.

## How to do this with our app
1. Introduce Mangum
2. Wrap our app with an `index.handler`
3. Craft an example event and test it against real AWS.

## Add dependencies
1. Anatomy of the virtual environment. 250 MB limit.
2. Pip install a package with no compiled deps... like what?
3. Pip install a package with compiled deps. Numpy.
   1. Watch it fail on ARM vs x86. Use public ECR / docker to get the deps compatible.

## Publish our code
4. Pip install our packages and code all in one file. Upload.
   1. Reveal: we can't see our code in the UI. Segue to layers.
5. Layers.
   1. Create a layer with our dependencies (`pip install --editable ./`)
   2. Publish only our source code + our handler as the code package
   3. We can see our code in the UI again!!!

## Get our code working
1. Now that it's up, construct an HTTP API Gateway event to send it
2. Get it all working when sending our test event in the console

## Secrets
1. Compare secrets manager and parameter store
2. Compare access patterns for secrets
   1. Use boto3 in code to fetch them--control access via roles
      1. rotate: change the secret
      2. pro: no need to have .env file locally!
      3. con: more locked in and expensive. Coupled to particular secrets store.
   2. Use environment variables
      1. rotate: change the environment variable (I *think* no redeploy is necessary)
      2. con: you need a .env file locally
      3. pro: code is less locked-in
      4. pro: code is faster and cheaper. One less network call.
3. Reference a parameter in the environment variables section