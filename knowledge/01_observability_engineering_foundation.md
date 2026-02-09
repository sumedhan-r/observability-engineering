# Abbreviations

- **API** - Application Programming Interface
- **CPU** - Central Processing Unit
- **Dev** - Development
- **ID** - Identifier
- **IP** - Internet Protocol
- **MoBaaS** - Mobile Backend as a Service
- **Ops** - Operations
- **OS** - Operating System
- **RCA** - Root Cause Analysis
- **SDLC** - Software Development Life Cycle
- **SRE** - Site Reliability Engineering
- **UUID** - Universally Unique Identifier

# Definition

Observability is defined as the ability to determine the internal state of a system using external outputs/signals regardless of how fuzzy or bizarre the internal state is. Irrespective of whether the internal state is predictable or unpredictable, unprecedented, chaotic, the internal state must be determined with full certainty when using an Observability tool/method.

To break it down further into granular detail, Observability system must allow engineers to

- Understand inner workings of application
- Understand internal states no matter the condition, type and predictability
- Understand inner workings and internal state solely using external outputs
- Understand internal state without shipping custom code

Shipping custom code implies that a separate standalone feature is developed for the purpose of Observing previously built features. This is not the ideal way to understand how the internal state of the software system changes since the new custom code could bring additional complexity to the internal state even if it has simple logic attached to it.

# Legacy vs Modern Software

Legacy software relied on a Monolithic architecture. These architectures were simpler to understand, reason about and debug in times of production incidents. More often, an incident in production brought the whole application down and as such, feature development was constrained by the total amount of existing features and the business relations between Dev team and Ops team, since Ops team was responsible for maintaining the health of the application.

In contrast, modern software system relies on a Microservice architecture. This architecture decouples all the components inside a Monolith and allows for more flexibility with resources utilized for building an application. This flexibility created opportunities and novel solutions to handling hardware resource constraints and issues with automation, almost completely removing the reliance of human intervention. 

And it is exactly due to the increased flexibility that has led to an increase in complexity and difficulty in developing Observability for the modern software system. Dev teams have modified their approach to writing functions and logic but the Ops team have been left behind with Legacy tools and approaches to Observability, which at this point has become obsolete.

## Obsolete Observability approach for Modern software

Current observability approaches that are founded on Legacy Monitoring and Observability are as followed

- Approximations/Assumptions/Predictions are made to internal state and these in particular are monitored
- Performance thresholds are set to determine a binary Good or Bad application status
- Monitoring is outsourced to external team that performs fixed Monitoring task management and execution.
- Alerts set only garners attention of developers when the application status is Bad
- Thresholds are manually modified using heuristics, rather than reliability.
- More alerts are setup which creates more noise based on false alarms, leading to Ops team mental overload and alert ignorance based on past experience biases.

The reality of modern systems contain important differentiating factors making Legacy Observability obsolete, which are

- App has many services to end user
- Architecture has a polyglot persistence (multiple databases and storage accounts)
- Infrastructure is dynamic with resource allocation having elastic and automatic changes.
- Many far and loosely coupled components are managed, most of which are under the control of the Cloud Service Provider
- Developers own the code deployed to production and are incentivized to monitor their own features developed instead of outsourcing it to Ops team
- Examination of correlation of software system features for Observability spans an infinite amount of dimensions.

# Observability components

Observability for modern software system depends on two important components - Cardinality and Dimensionality

## Cardinality

Cardinality implies the uniqueness of data under a particular attribute/column. Higher cardinality implies that the attribute contains more unique values. High cardinal data allows for easier segregation and batch-wise analysis of internal state of system across the high cardinal dimension such as UUID or name. This allows for an abstraction of first possible variables to consider for querying the Observability data in order to perform RCA on a given failure state.

## Dimensionality

Dimensionality implies the total collection of key-value pairs in a dictionary type data structure. An event, which is the fundamental building block of Observability, should ideally be very high dimensional in order to capture as many data points as possible. This will allow developers to assess the internal state of system using diverse correlation possibilities and would allow for efficient diagnosis during Unknown Unknown failure cases.

# Drawbacks of Traditional Monitoring

Traditional Monitoring systems were setup for the demands of Legacy software products/applications. Legacy software products involved a Monolithic architecture with all the necessary hardware components (or virtualized system components) within a single entity/machine. This allowed for simpler approaches of setting up metrics for each components within the machine to assess the internal state of the system. Any code developed for the purpose of providing features to end users was limited in complexity to the capabilities of all components involved in the machine and the development team responsible for maintaining a functioning application at all times.

In Modern software systems, there has been a shift from Monolithic to Microservices architecture. This has allowed for multiple benefits in Development and Deployment of software applications but at the same time, has increased the complexity of Monitoring any issues in the application. The purpose of Monitoring does not hold merit in modern software systems due to the following reasons

- Metrics - Metrics are aggregated numeric values providing information on the performance of a given component under the assumption that the component is either completely Hardware or is a simpler extension of a Hardware Component at the OS layer (e.g. Virtual memory). But under a Microservice architecture, a component has a higher abstraction(virtualization) layer than a simple Hardware component, primarily determined by Software logic (e.g. Replicas with capabilities like autoscaling). As such, a metric is not going to capture the behavior of the component being monitored.
- Alerts - Alerts are tools that are constructed using a rudimentary approach of setting a threshold using intuition-based navigation of error cases. The threshold value is approximated to represent an Error situation of the software systems. Under the case of metrics representing the internal state of system components accurately, thresholds for alerts are capable of capturing Error situations since the Hardware component is no longer running/working when the alert is being triggered. But for a Microservice architecture, components do not have a binary UP or DOWN status of execution, rather a broad spectrum of possibilities due to large amount of variables influencing the behavior, either predictable or unpredictable, controllable or uncontrollable. Hence a simple threshold is incapable of representing a spectrum of possibilities.

## Consequences of Monitoring applied to Modern Software

Below are three consequences described that highlight how applying Traditional Monitoring to a Microservice architecture based application can hinder the overall approach of debugging and solving Error cases

- Insufficient correlation - Traditional Monitoring relies on a fixed amount of indexes to use as source of diagnosis for failures such as CPU, load, counters etc. In order to assess the behavior of Modern software systems, new indexes would need to be included that varies across different systems. These new indexes need to allow for open-ended inquiries to better understand and obtain the correlations in the Failure state. Some of the new indexes being user ID, IP, requests
- Lack of efficient RCA - Metrics are used to make decisions on a specified component based on a limited and predictable set of variables. But this does not consider variables out of scope of established Monitoring setup that are in control of external Cloud service providers or inherent to Real-world chaotic stressors and out of control of any party involved in the entire software system. Hence the results obtained in RCA using Monitoring turns out to be incorrect in the vast majority of cases.
    - E.g. : a bug is present in code that has weaker configuration for data expiration in storage. Data expires before write operations due to disk space consumption. But the disk space consumption could either be due to the Software system performing read/write operations or Cloud provider OS performing maintenance operations. Hence configuration categorized as a bug cannot be determined as such with certainty
- Tool hopping - In order to diagnose the issue using Traditional Monitoring approach, developers would often have to extract information regarding Failure state from various metrics along with Error logs filtered with insufficient query conditions. Context regarding traces is absent during the information retrieval for the encountered Failure state or a set of traces is extracted using a particular Trace ID obtained from the Error logs. The traces extracted may or may not describe the Failure state of the Software system. This leads to an uncertain set of results obtained for reasons or causes pertaining to the Failure state.

## Comparison of Monitoring vs Observability

Following the above three consequences of Monitoring applies to Modern software systems, we can compare how Observability approach performs in contrast to Traditional Monitoring.

- Correlation -
    - Traditional monitoring : Correlations are obtained for metrics indicating performance of system components. This requires a deeper understanding of how each system component works and also how each system component could contribute to the overall performance of the application. This restricts the number of developers capable of diagnosing the Failure state to the one who has the most experience both in general software development and involvement in the given project.
    - Observability : The approach relies on using various indexes to perform open-ended inquiries on the Failure state without having to rely on a knowledge base on system component performance since the performance is not determined by a fixed set of predictable and controllable variables. This allows for more developers in the team to perform diagnosis on the Failure state and promoting the person with Curiosity to be able to diagnose existing and future Failure states more efficiently.
- RCA -
    - Traditional monitoring : Failure states are assessed based on the assumption that past incidents have followed similar conditions and behaviors. This leads to the developer relying on pattern recognition between past Failure state and existing Failure state. Conclusions obtained from the pattern recognition approach leads to inconsistencies due to ignorance of unpredictable or uncontrollable variables. It also creates a Confirmation bias within the developer performing the diagnosis.
    - Observability : This ignores the comparison of past Failure states to existing Failure states and performs the diagnosis with a fresh perspective, keeping in consideration the possible contributions from unpredictable or uncontrollable variables. Each set of possible variables are narrowed down in a breadcrumb fashion (building stack of evidences) leading to the potential reason for the Failure state. Due to the cumulative acquisition of evidences, the RCA is more efficient and accurate.
- Visualization -
    - Traditional monitoring : Panels or Dashboards are setup in various places under various telemetry like metrics, logs and traces. Division of data visualization leads to the developer performing the diagnosis using a filtered set of metrics indicating the Failure state of the system. With minimal correlation, the evidences obtained from the metrics is linked to Error logs filtered with pre-determined queries that provides insufficient context on the Failure state since the logs are smeared with information outside the scope of the Failure state. Traces are assessed based on the IDs obtained from Error logs with the assumption that there exists a direct relationship between the error logs and traces. Once again, correlations are not taken into consideration, rather relationships between telemetry data is created inaccurately for the Failure state for the purpose of diagnosis. This leads to the developer making human errors due to exhaustive context switching between Visualization tools.
    - Observability : Platforms under observability provides the telemetry data with all context regarding the Failure state in a single location in the form of Correlation charts and Dependency graphs. Charts and graphs allow for real-time filtering of data points in addition to providing correlations between different dimensions in the telemetry data. Or one can obtain additional information under a high dimensional variable by dividing the data source to chunks/aggregations and determining which chunk describes the anomalous situation encountered. Having all Visualization panels under a single Dashboard reduces human errors when obtaining insights into the Failure state and makes the entire process less burdensome.

# Example use case

Obtained from the book, one of the examples of need for Observability that was discovered as a consequence of multiple incidents faced is listed below:

## Mobile Backend as a Service

The project involved providing a platform to developers building a mobile application for simple end users. Some of the features that were provided by the Mobile Backend as a Service platform included user management, push notifications and integration with social networking services.

This platform was built using a Microservices architecture. Some of the problems encountered by the project members of the platform were:

- Random mobile application in the platform shot up to the top 10 mobile apps performance and ratings with unpredictable patterns in their rankings.
- It was inferred from data sources that the load coming from any single mobile application in the top 10 highly used applications was not the cause of platform site going down.
- A list of slow query performance was obtained but was concluded that the slowness of performance was a symptom, not a cause of site outages.
- Most hardware consumption behavior resided in the extreme capacities. If a hardware component was available, the capacity consumed had percentages in single digits. If the hardware component was occupied/unavailable, the capacity consumed reached close to 100%. E.g. 99.9% site reliability meant that 0.1% shard of database was 100% down, causing data write loss to that shard of database. In addition, relevance or priority of the database shard could not be figured out.
- Bot accounts created more performance issues in the platform. They were responsible for saturating the lock percentage of a database.

# Monolithic vs Microservice Architecture

The pressing need for Observability was discovered from the numerous issues faced in the MoBaaS platform described above. Most modern software systems in current market utilises a Microservice architecture in the Backend [Legacy vs Modern Software](#legacy-vs-modern-software). Following content describes in detail characteristics and performance attributes of each architecture.

## Monolithic

Monolithic architecture involves a simple orchestration of hardware components within a limited and predictable specification. This also meant that complexity of software written were minimal and user demands for the application could not be satisfied with architectural upgrades. Any performance drawback in the software system such as Latency, Request fails, etc. could only be improved to a certain higher ceiling.

This led to Development teams limiting the number of features developed and deployed to Production. All developers were responsible for having a deeper understanding of the entire monolithic application, thereby restricting the possibility of distribution/delegation of SDLC tasks among team members. This was primarily because a single bug introduced into Production could cause the entire application to crash and it generally took longer for developers to debug the bug and push a fix to bring the service back up. Development team also got restrictions from the Operations team to not push complex code changes since the Objective of Operations team was to keep the application in Up status. This limited the overall Development cycle in the project.

### Characteristics

- Application status was determined by Binary indicators - UP or DOWN
- Code deployments were meticulously structured with maximum awareness to no bugs crashing the application in Production
- Application always consisted of a single version in a given time instance within the monolith
- In-house Operations team was responsible for Monitoring the status of the application along with the hardware components
- Errors or incidents faced in the application was predictable or generalized for future occurrences and followed templates/runbooks for troubleshooting

### Experiences

- User experience was homogeneous due to the application being deployed inside a monolith.
- Aggregated metrics were capable of indicating application performance with higher levels of reliability and correlation to real-world execution. E.g. Application Status, CPU usage, memory usage
- Alerts were set based on the performance of hardware components using thresholds. Since hardware components have deterministic performance, setting up heuristic thresholds provided accurate information on application performance.
- Dependencies were limited to the monolith environment. Integrations with external service providers were minimal and the interaction of the application with outside network was easier to track.
- Errors or incidents encountered were predictable and repeatable. As a result, runbooks were developed to mitigate and troubleshoot recurring problems and outsourced to Operations team. On-call engineers had to deal with lesser burden and time spent resolving incidents.

## Microservice

Microservice architecture allowed to split the components present inside a monolith to an entity of its own. This meant that each component had more privilege, more capabilities and better solutions to dealing with recursive issues through modularization and virtualization of hardware components. E.g. - Autoscaling in container replicas is a virtualized way to handle resource exhaustion of containers in the architecture with graceful handling of resources utilized by the application along with efficient load balancing of backend processes/requests.

Creating dedicated components capable of handling specialized operations meant that applications could be developed with more complexity. This allowed developers to experiment and ship new features with broad capabilities. In addition, bugs present in the code base did not cause the entire application to crash since the components were decoupled from a single source of centralization. 

But along with improved performance and capabilities brought along higher complexity levels in the architecture, creating unprecedented problems for the software system.

### Characteristics

- Application status migrated to a Spectrum of possibilities (since one bug does not cause entire application to crash)
- Code deployments shifted to progressive delivery (blue/green, canarying)
- Code deployments were decoupled from feature releases (via feature flags)
- Applications were capable of having multiple versions in Production cluster networks
- Operations team within an organization were incapable of providing effective solutions to incidents faced due to Cloud providers managing and controlling critical infrastructure components via API. This limited access to architecture component performance data for the developers involved within a project, including the Operations team.
- Errors and incidents faced by the application were unprecedented and unpredictable, both in terms of occurrence instance and incident characteristics/factors. Unknown unknown became the standard of modern software applications.

### Experiences

- User experience became heterogeneous, meaning that different subset of users started experiencing different application performance conditions. An incident encountered by one or a set of users did not mean that all users were facing the same issue. This is because routing happens in different ways among different components in the backend.
- Aggregated metrics represent the performance of a single component by ignoring correlations to other components and outside contributors like network. In modern distributed systems, interactions between components usually involve multiple requests being sent and received with each request providing incomplete information on the behavior of the processes. Metrics end up providing incomplete information on the status or behavior of the application as a consequence of having to deal with complex nature of modern software systems and networks.
- Application status shifted to a spectrum of possibilities indicating its availability. In addition, components inside the architecture became more modularized & virtualized, leading to spectrum of possibilities for its availability and performance as well. This meant that legacy alerting methods relying on thresholds were incapable of capturing the real-world status of either a given component or the entire application, the incapability leaning more towards the application (it is still possible with reasonable levels of accuracy to determine performance of components using legacy alerts)
- Dependencies on external service providers started to increase, with each service provider relying on multiple other service providers to create their final product. In addition, outside networks also started to have modularization and virtualization, leading to complex methods of process handling and completion. Overall, complexity for debugging increased beyond manageable limits and became increasing inaccurate for RCA.
- Errors and incidents faced by the application were unprecedented and unpredictable. Standard runbook methods became meaningless since a standard approach to solving unknown unknown problems cannot be devised. Instead, problems like these need to be assessed with real time data filtering and open-ended inquiries.

# Technical team benefits obtained from Observability

Technical teams, depending on the size of the project, consist of Development, DevOps and SRE teams. Each team involved in the project have a certain level of responsibility in understanding the internal state of the system and how the application is affecting end users. Having a clear picture of this empowers each team to perform their tasks with certainty.

Some of the benefits obtained are as follows -

- Chaos Engineering : Chaos Engineering is an approach to introduce controlled failure cases to an application simulating real-world scenarios to assess how the application performs during times of distress. Observability provides technical teams an accurate representation of the steady-state of the application. When the steady-state representation is available, it can be used as the baseline to understand what are the possible deviations that an application can undergo due to Chaos engineering.
- Feature flagging : Depending on the number of feature flags implemented and the flag configurations, multiple combinations of feature flags can exist. Observability allows developers to assess how a given combination of feature flags impact user experience from customer base subset-to-subset. This would provide necessary insights on fine-tuning the configurations of the feature flags rather than having to rely on request/endpoint based analysis obtained from Monitoring approaches where a single endpoint could impact multiple features.
- Progressive release patterns : Progressive release allows teams to deploy features to a small subset of test users to assess application performance and feature adoption before releasing to overall customer base. Observability provides the baseline steady-state of the application and during release (using approaches like blue/green, canarying), observe any deviations encountered by the application. Deviations would indicate that the release was the contributor and future releases can be iteratively improved based on deductive analysis.
- Incident analysis : After an incident, necessary retrospectives need to be performed to understand the issue faced. Clear trail of evidences need to be present in order to create detailed reports on the same. Observability forces the engineers involved in the process to iteratively reflect on any implicit biases present in the retrospective process to mitigate any incorrect conclusions to be written into the reports, thereby improving the sociotechnical systems in the project.
