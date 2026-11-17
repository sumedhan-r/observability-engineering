# Observability Engineering - Foundation

## Table of Contents

## Abbreviations

- **Dev** - Development
- **Ops** - Operations
- **BI** - Business Intelligence
- **RCA** - Root Cause Analysis
- **SDLC** - Software Development Life Cycle
- **SRE** - Site Reliability Engineering

## Overview

## Definition

Observability is a concept derived from engineering disciplines that required an approach to measure changes during the process of system creation. Inspired by control theory, engineers under this discipline faced the obstacle of having to measure and understand what the system was encountering since the objective was to tailor and manage a blackbox system that could be steered into delivering a set of desired outputs irrespective of external factors such as noise, disturbance and unknown variables.

Applied to software systems, the definition is phrased as follows

> Ability to infer the complete internal state of a system using measurable outputs emitted from the system irrespective of how novel or bizarre the real world situation is

The definition brings to light certain pointers that make it easier to comprehend what observability is capable of and what observability should be capable of promising developers. Pointers being

- Partial internal state : If the system is only visible in a partial state, that means observability has not yet been achieved in the application.
- Circumstances : Real world conditions can vary along a large spectrum of stability and predictability to chaos and unpredictability. If any contributing variable to unforeseen circumstance hinders the ability to witness the internal system state, then observability has not yet been achieved in the application
- Outputs : Internal system state can only be determined using a particular source of data stored for the intended purpose. If the system does not collect such outputs or if the system has to manufacture the output using second order features and functions, then observability has not yet been achieved in the application

### Indicators of good observability

Some of the indicators that development teams can rely on to identify to what extent they have established observability in their products are

- Any worst case circumstance can be analysed and understood on the impact it causes the system, providing proof to developers the ability to have already done this during pact incidents encountered
- Compare features based on feature flag and filtering its state of operation in Production based on attributes such as endpoint, API key, user ID, query hash, job ID
- Explaining user interaction on the application with high degree of verbosity using individual trace walkthrough on application request, device sessions, chat history
- During incidents, being capable of detecting violating event records that strongly relate to SLO burns
- Detecting outlier situations using outlier events that do not necessarily escalate to an incident

## Software dependability

In the current global landscape, people have strong habits pertaining to the use of applications on various devices they own personally, which in turn rely on the internet for efficient and fast information management. For software products created and launched in the open market, users have grown to expect the product to be capable of delivering as expected to satisfy the functionalities abstracted away from human intervention. This paved way to a fundamental paradigm to assess how good a software product is for the end user called Dependability, which is defined as

> Trustworthiness of a system - how likely is the user willing to solve their pain points, purchase or subscribe to and recursively access the application

Some of the properties that describes software dependability are

- Availability : Ability of a system to deliver services **when requested**
- Reliability : Ability of a system to deliver services as per **requirement**
- Maintainability : Ability of a system to undergo **repairs and evolution**
- Safety : Ability of a system to **avoid catastrophic** incidents and consequences
- Confidentiality : Ability of a system to **prevent information leakage**
- Integrity : Ability of a system to **resist system defects**
- Observability (new) : Ability of a system to provide **system state comprehension** and enable debugging

## Old vs New telemetry

### Case for old approach to telemetry collection - three pillars

Older approaches to collecting telemetry involved separating the concerns into three pillars as defined by Opentelemetry and accepted by the wider industry. The three pillars constitute metrics, logs, and traces.

Legacy software systems relied heavily on the performance of hardware components with an approach to monitoring the software system in a Binary model. Whether or not a system component was successfully performing indicated the presence of bugs introduced into code. As a consequence, individual components were assessed with three separate perspectives but unexpectedly resulting in three separate data sources.

The shift to cloud platforms made the siloed approach to telemetry storage more solid. Infrastructure components provided by vendors were significantly managed by themselves and provided little to no flexibility for developers purchasing the resources. Along with the limited flexibility in component operations, telemetry data collected on the components were also limited in flexibility and pre-defined signals were collected and emitted in large volumes. Difficulties posed with handling large data volumes further justified the need to have siloed data stores for telemetry.

But modern software systems do not concern themselves over infrastructure components when developing and delivering features to end users. Developers focus more on code functionality and code standard and in the rise of AI driven development, more processes involving the SDLC address issues in the code base. This prominent shift from infrastructure components to code base highlights the need to adopt a different telemetry collection approach

### Case for new approach to telemetry collection - unified event

For software systems delivering a huge range of features handled with varying complexities like feature flags, deployment slots, regional provisions, continuous security and data compliance, managing the code base becomes complicated for developers building the products. Every feature and decision during development has to be made on the basis of logic and specifications that adhere to **first principles**.

AI driven development tends to hallucinate when provided incorrect prompts and context regarding the software project even with extensive documentations and guidelines for instructions. Course correcting agentic errors in all phases can only be performed efficiently using first principle explanations.

A similar model has to be followed when establishing observability in the product. Any telemetry data that is collected must provide developers the capability to reason with the data using first principles. The only data type that provides such a capability is called an event, which is a collection of arbitrarily wide attributes stored in a dictionary format, with preference to high cardinal attributes. This provides an ability to filter and correlate among various dimensions to obtain insight and visibility into the system state that can cover unforeseen or complex perspectives. Events can be collected as either canonical/structured logs or spans in traces but the decision to determine the format of events depends solely on the system complexity and whether the event telemetry data is capable of explaining said complexity.

The importance of storing the telemetry data in a unified data source is best explained when the properties of an event are listed out and how event telemetry enables observability. One of the major benefits of such a data type is that it provides developers with a high degree of flexibility on what needs to be tracked and collected. In addition, the level of detail that one needs to capture in an event can be calibrated with high precision due to the limitless possibility and acceptance of collecting attributes.

### Properties of event telemetry

Some of the properties of event telemetry data type are as follows

- High-dimensionality data: Rich, wide structured events organized around a unit of work capable of covering all the context. Ideally, hundreds of attributes per event.
- High-cardinality data: Preserving as much detail as required within a project including unique IDs regardless of the volume of cardinality
- Aggregation: Storing raw events and aggregate at read time, with flexible, inferred schemas and indexes. Pre-aggregation is a one-way street, and every key should be fast to query.
- Analysis: Zoom in to individual requests, and zoom out to the whole system, or any level of granularity in between. Visualize events over time as a trace.
- Visuals: Exploratory, open-ended user interfaces a team can interact with, instead of static dashboards.
- Time to detection: Queries must return within seconds, not minutes, so it is fast and interactive.

The tactical description of how observability needs to be implemented in software systems is the same as how BI works. Wide and structured event records stored in columnar database for faster querying and explorative analysis. Various factors were explored and demonstrated to respective teams for business objectives. With the current paradigm shift of software logic favouring more business-oriented agreements for server interactions, the existing procedure in BI naturally fits into observability

## Demand in AI driven code

With the integration of AI agents in the coding process, the entire SDLC has shifted for all teams across the industry. Development and deployment processes are faster and efficient with little attention given to observability due to the lack of staying updated with the processes. The biggest bottlenecks faced during the SDLC are

- Deployed application management regardless of product and infrastructure complexity
- Human initiated action steps such as PR review, pipeline validation

For a long time, there has been a common belief in the industry that deployed software systems encounter breakdowns due to bugs introduced during development. But with deeper business and logic relations in software systems, often containing improved and automated mechanisms for race conditions, long tail race conditions are not the consequence of bugs introduced in application code. This is not to mention that bugs do not introduce problems in deployed code but assuming all race conditions originate from bugs rather than production behaviour misses the overall set of possible error cases.

As teams developing products proceeded to incorporate features into the application while relying on services provided by vendors which were also going through steady transformation, a lot of practices during the SDLC cycle were determined and organized based on experience facing recurring problems and loosely documented as intuition. Most of these intuitive deductions made sense and were useful for the teams developing the product, but it did not give concrete evidence on its capability to solve problems under unforeseen conditions. With AI incorporated into the SDLC, these intuitions undergo second handed validation while pressing development teams to reconsider the need to document the same.

Observability addresses these procedural drifts and the two bottlenecks along with providing a higher leverage for AI driven development as follows:

- Rich, wide and unified telemetry collected from application in production is used to validate or invalidate the presence of bugs and confirm if there is unchartered territory pertaining to running code that needs to be addressed to reduce race conditions
- Intuitions pertaining to the software system and associated processes have to be validated with the production system-tied-procedure and documented not just for the development team’s reference but also for the agentic context. Across the entire SDLC cycle, agents can use the guidelines to minimize hallucinations

Incorporating AI into the SDLC is bound to face hallucinative problems that can be introduced despite having strong guidelines for the agentic reference. This mandates the presence and addition of guardrails in the SDLC that consist of human intervention and verification. Guardrails can also be automated depending on the task and scope. Regardless, addition of guardrails also needs to consider the fact that AI driven development leads to interlinked disciplines and a consistent coding operation similar to a factory assembly line. Observability stands as the crucial pillar ensuring agentic development do not get stalled when ensuring dependability for end users

With adequate guardrails set in place for the software system, it must become imperative for development teams to embrace production analysis using observability data to have clear visibility into the system state and always make sure that the overall SDLC velocity is kept high. AI driven development must encourage teams to deliver features as soon as possible with minimal technical debt in maintenance tasks.

## Software quality

Running efficient code in production relies on software being of high quality. Two primary factors that determine the quality of software are

- Purpose : The overall purpose of the project determines the code functions and service layer that needs to be deployed, refactored and maintained. If the purpose is loose such as validating a MVP for a startup, the code can be expected to have certain tolerable faults. If on the other hand the purpose is to cater to high stakes user requirements (such as a web browser), certain properties of the code base need to be upheld at all times (such as availability)
- Constraints : Throughout the SDLC, developers face scenarios where code does not cover edge cases or certain logical operations across boundaries. This stalls the development process and adds time and resource cost. Being able to maintain a code base in a timely manner leads to efficient deployment of the software system and the delivery of the features.

Code base is never pre determined in its properties and is also never static. User base, system component performance, vendor relations change over time, which in turn influences the purpose and constraints. Code is defined by the extent to which the team governing it can manage the change process. Change management for code bases consists of two types

- Durable : Functions that define the main features of the code base. Applying changes to these parts of the code base poses significant risk to the dependability that users, callers, vendors have over the software. Such type of code is defined by its stability in the deployed servers and any change required to their functionality can only be performed in smaller diffs against the baseline stable system in order to minimize risk in production
- Disposable : Functions that are more likely to be one-off such as scripts, upgrades or migrations. As well as prototypes or experiments. Such type of code is highly tied to the contribution it has in production and quality as per tests and security needs to be upheld accordingly

Release of a product to the market defines a touchpoint in the condition of the code base. Code maintenance undergoes a continuous process of evolving from disposable code to durable code as well as refactoring of legacy durable code. As both development and maintenance processes are worked upon concurrently, the factors defining the code base quality after the touchpoint shifts to that of the following two described below

- Critical paths : Certain functions and service boundary layers are essential for the application to provide requirements to users, callers or vendors in the form of fundamental pillars whereas others do not pose a high severity level in its availability or performance. The severity levels can be described in three categories
- Scaffold : Code is rarely used, invisible and minimal business impact upon breakdown
- Post office caliber : Code is occasionally used and invisible, but offers important business value like billing, security
- Cathedral caliber : Code is constantly used, users are sensitive to associated feature’s performance and the entire business relies on these functionalities
- Data persistence : Usage of the application in production is bound to contain data associated with users, callers or vendors for successful interactions. Code associated with system components such as databases, file systems, medical devices, operating systems are strongly linked to the hardware layer and contain predefined behaviours and relations. As such changes need to be handled with utmost care because data is always sensitive and irreversible

## Toolkit for code crossover

As code consistently crosses over from development to production, teams need to equip themselves with appropriate tools that would help them validate their features in real world systems and assess user interactions, which increases observability. These tools are to be used in a cyclical manner due to its contribution to the SDLC. The tools are

### Telemetry data

The objective here would be to collect rich, wide and arbitrarily large events and store them in columnar databases for efficient retrieval and filtering. It is highly likely for teams to follow the conventional three pillar model and store them in time series arrangement. In order to transcend this, two factors that can be considered when adopting collection of the appropriate telemetry data are

- Shift to columnar database : Restrictions in teams could make the shift to database the biggest bottleneck. If such is the case, any open source provision of the database would minimize the constraints. Columnar database is the primary factor to tackle due to the necessity to slice and dice telemetry data quickly
- Choice of event telemetry : Teams subscribed to the three pillar model would be challenging to convince transiting to collecting rich and wide events. In such cases the team can pick either logs or traces or convert them to an event datatype but the choice has to be one of them. Logs can be converted to canonical (structured) logs and traces can be converted to intentional wide span samples in the traces

### Feedback loop

New features and functionalities that are shipped into production need to be observed in the real world interactions in order to detect any arising bugs and discrepancies. Detecting these is paramount to ensuring the application performance is at par since early detection would lead to faster code improvements for the associated feature. Given the rise of AI driven development, feedback loops must prioritize factors relevant to such development teams, those being

- Developer intent
- Function behaviors
- Service boundary relations

### Testing

The purpose of incorporating tests would be to obtain confidence in code validation and prevention of recurring errors. Testing has always followed a conventional approach in software development. But with AI driven development, the scope of testing is expected to change in order to ensure high standards for code quality.

Older suit of tests consist of

- Unit tests : Checks function logic and any regression of newer logic refactored in existing functions
- Contract tests : Checks the availability and necessary interactions with third party vendors and adhering to established contracts
- Integration tests : Checks the service layer interaction between system components to ensure client-server relations are delivered as required of the product

Newer suite of tests would need to consider

- Property based tests : Checks the aspects of code that is expected to respect the properties of software systems described under dependability
- Behaviour tests : Checks the code functions that satisfy user expectations while tracing the system interactions underneath the user action
- Characterization tests : Checks the description of what the code function is supposed to execute and deliver to ensure refactoring respects the older description

### Instrumentation

Proactive collection of essential indicators and data values in the event telemetry must be capable of achieving observability in the software system. Code written for the sole purpose of collecting these data values is called instrumentation. Done the right way, instrumentation would only be incorporated in the code base but applied and expanded to the entire system describing code, infrastructure components, operators, user interactions and data.

All opportunities must be capitalized in collecting essential event data values. Granularity at the code line, code function signature, query comment, file byte processing level would need to be explored. Opentelemetry auto-instrumentation sources as well as standards for log/trace instrumentation needs to be followed for easier adoption in AI driven development since all AI models have been trained at the open source code contributions of Opentelemetry.

### Feature flags

This needs to be introduced as per project requirement to separate deployment from release. Deployment consists of building the new image as per latest code version and introducing it in the server architecture whereas release consists of user interactions with the application and how that affects system performance.

These need to function like a toggle switch that can provide on time flexibility to developers in enabling or disabling access to a set of features in production to ensure any possible production regression is minimised. Benefits of using feature flag as per requirement are

- Deployment : Since the primary goal of any new code version deployment is to maintain system stability, diff changes to the code base can be assessed using feature flag restrictions and make it easier to revert code changes or proceed with hotfixes if the latest code release is responsible for application crash
- Release : Since this is closely associated with changing user experience, development teams can use feature flag to release new features to users at a desired timestamp or region zone that might be closely tied to major press release or product launch
- Other : Feature flags can also be used dynamically to rollout features in a continuous approach by segregating the user base and launching to each subset before proceeding to the next user base. Continuous approach to feature release decreases the stress associated with heavy system loads and carefully assessing race condition emergence

### Enhanced CICD

The mechanism with which one decides to deploy an application can be enhanced by using various options such as

- Blue green : Deploy to a given slot and use a router to switch all incoming traffic to the slot containing new deployment
- Canary : Deploy to a given node that is accessed by a subset of users to validate the system performance for the new features before allowing complete deployment to all allotted notes in the cluster
- Rolling : Deploy a completely new image or instance into a resource such as Container App with a maintenance downtime during the deployment job run

An enhanced CICD would provide options to the developer team as to how they can ship new features into production to end users and validate feature usage and system performance. When the objective to pick a desired CICD workflow is to validate production system conditions, the indicators to determine the best CICD would be detection of novel mistakes and comprehension of developer intent, which brings it back full circle to Telemetry data tool

### Bonus tools

Certain additional tools that development teams can use as per their constraints and requirements are

- Capture/replay : Snapshot of a system captured and tested at any random timestamp against varying real world conditions. The snapshot approach to testing system state is done iteratively to ensure newer system states are tested to obtain accurate results
- Traffic splitter : Given two options for API server provisions, split the traffic between the two and compare the responses to decide which one is better
- Strangler fig : Code refactoring of legacy code. The approach consists of the following steps
- Transitional architecture for legacy code
- New interfaces
- Extracting parts
- Link old and new code
- Decouple data logically inside system
- Write shift to new data source
- Backfill data
- Read shift to new data source -> deprecate old code.

## Industry disruptions

With the emergence of AI driven development, teams are forced to adopt AI into the development tasks across all projects because of increasing competitor adoption of the same and faster SDLCs in spite of AI models committing mistakes like hallucinations, context mismatch, severity unawareness, system disassociation. Some of the major fronts in which the status quo have been challenged are

- Technical enabler : Helps in closing the gap between development and production by providing production system analysis to developers in terms that explain code base problems
- Ecosystem : Teams are undergoing a massive change in the tech stack and tools employed in a project along with pressure on the three pillar telemetry model for software system analysis
- Executive decisions : Higher level decisions in divisions are taken to ensure reliability and guardrails take high priority
- Context : AI models are gluttons for context and teams that take responsibility on storing the relevant data values capitalize on maintaining good quality context for AI model responses/actions
- Bottleneck : Projects have shifted to automating code writing and the bottleneck has shifted to system comprehension
