# Observability Engineering

# Table of Contents

- [Overview](#overview)
- [Content](#content)
- [Evolution of Software Development](#evolution-of-software-development)
- [Impact of Design Philosophy](#impact-of-design-philosophy)
  - [Traits](#traits)
  - [Behaviors](#behaviors)
- [Monitoring vs Observability Comparison Points](#monitoring-vs-observability-comparison-points)
- [Limitations to Monitoring](#limitations-to-monitoring)
- [Benefits of Observability](#benefits-of-observability)

## Overview

This page and the following child pages covers all the notes gathered from reading the book Observability Engineering. The book primarily focuses on modern software systems with reasons to why a clarification needs to be made between Monitoring and Observability. In addition, an accurate definition of Observability allows developers under a project to solve issues in modern software systems with ease and reliability.

Legacy software systems relied on a monolithic architecture. These architectures are simple to manage, assess, debug, reason over and understand as the components involved in the architecture are confined and simplistic. On the other hand, microservice architectures contain higher complexity and distributed setups which makes it cumbersome, unpredictable, chaotic and confusing to solve incidents or issues in the software system. Traditional Monitoring is not capable of performing the task of solving issues in microservice architectures since these systems were developed for monolithic architectures, providing simpler insights and solutions. 

When a team that is working on a software project involving a Microservice architecture use Traditional Monitoring approaches to maintain reliability, they are going to encounter more problems than they can handle ranging from technical, financial to organizational, cultural. Almost all of these problems can be solved if the team adopts an Observability approach.

- Incidents are resolved way faster, within minutes instead of hours
- Engineers in the team do not have to experience burnout due to alert fatigue and on-call systems
- Alerts can be set from a budget perspective rather than purely technical metrics and indicators.
- Organizations can further strengthen their relationships among technical and non-technical teams due to Observability processes

## Content

- [Observability System - Foundation](../../../../personal-space/sumedhan/observability-engineering/01_observability_engineering_foundation.md)
- [Observability System - Telemetry](../../../../personal-space/sumedhan/observability-engineering/02_observability_engineering_telemetry.md)

## Evolution of Software Development

In legacy projects under Monolithic architectures, teams approached the development phases based on following paradigms :

- Development team had to map the entire Infrastructure prior to developing features, including all the required components.
- Each component involved within the application was tied to the Confined Infrastructure setup such as Virtual machine and had the performance standards limited by the overall Virtual machine setup.
- Application logic was tightly coupled with various components in the Infrastructure
  - All dependencies had to be specified and collated at single source of compile
  - API layer had the outermost (Gateway layer) and innermost (Service + Repository layer) boundaries intersect and communicate more closely
  - All repository (storage) operations were performed with single connection as controlled by the tightly coupled Dependency pack
- Operations team imposed conservative standards for new feature development and deployment. Introducing a single bug meant that the entire application crashed. Application status was often measured by UP or DOWN indicators.
- Incidents were resolved based on approaches from previous encounters and runbook maintenance describing known failure scenarios of components.

As teams shifted their efforts from a monolithic architecture to a microservice architecture for better application performance and maintenance, following were the changes implemented

- Development team could focus primarily on building the features and assign secondary importance to components involved in the architecture.
- Components were highly decoupled and could be added independently. This also meant that each component could be optimized to its full capability, further allowing for application performance enhancement
- Application logic was written primarily for the business logic and feature requirements.
  - Dependencies were independently initialized and removed with customized build and execution abilities
  - API layer was only concerned with processing the requests whilst pushing the dependencies to the boundary layers of the Container app/Cluster node vs various Components involved
- Operations team did not catch up. Drastic changes in architecture precipitated by Distributed systems did not shine light on requirements for an alternative perspective on Application maintenance. System performance was not impacted frequently due to a single component failure, making the overall reliance of Development team on the Operations team minimal.

The inability to catch up with changing circumstances and practices in Software Development only increases the significance of adapting to a better practice for Operation tasks. This is realized through an Observability perspective when teams working on projects are deeply aligned with the fundamental principles responsible for obtaining Observability in software applications. 

## Impact of Design Philosophy

Great software projects ensure the code base maintained and constructed follows great design practices. At times, business or functional limitations pose trade-off decisions that teams would have to make in order to proceed with finalized specifications for a given development cycle, but in spite of these decisions, the overall cadence of the project relies on a strong foundation in great design philosophy.

To what extent the team and project incorporate good design philosophies provides an indication on the convenience and inclusion of Observability skillsets. When the code base has methods and classes with clear and deep implementation, there exists a prior comprehension of the internal states of the application. These are predictions or simulations at best and do not provide the actual view on what happens in Production, but nevertheless encourages the team to establish better Observability practices since it allows them to better tackle the concern of feature instrumentation.

The perspective that would provide the biggest benefit for teams having a pre-established great design philosophy is to view Units of Work within the running application in Production as a Component with a certain set of **Traits** and **Behaviors**, giving separate attention to each of these factors. All applications have dependencies that can map out to complex relations and each dependency can be viewed as a Component from an abstract view interacting with other Components from an abstract view under the assumption that this vision is restricted to a single user or a single request. Observability perspectives still need to be adaptive to various dimensions that are present in the telemetry data to obtain an exhaustive view, but approaches to simulated visions provide the team with incremental steps for improvement in their Observability practices.

### Traits

Traits indicate what the corresponding Unit of Work contains as fundamental properties and capabilites. Due to their nature being fundamental, the implication of Traits for a Unit of Work is to provide a base idea on what Behaviors can be expected from the same. Traits provide the abstract view required in the inital phases of Software design and in further stages of Refactoring, giving stability to the developers when the scope of any development task is assessed.

**Examples:**

**1. Text Editor Module**
- **Traits**: Contains a buffer (data structure), cursor position, undo/redo stack, file metadata

**2. HTTP Client Class**
- **Traits**: Has connection pool, timeout configuration, retry policy settings, SSL/TLS certificates

**3. Database Transaction Manager**
- **Traits**: Isolation level, lock table, transaction ID generator, rollback log

### Behaviors

Behaviors indicate what the corresponding Unit of Work performs when a certain input is provided with an expectation of a desired output after internal processing of the provided input. Perspectives from which the input is viewed can vary from an individual user situation to a request to a dependency call as described by the scope of the Unit of Work. Behaviors help the developers define what the purpose of a given Unit of Work is and to what extent does it benefit other components, dependencies and services in the application. Having a projection of value contributed by the Unit of Work clarifies the overall performance profile of the application.

**Examples:**

**1. Text Editor Module**
- **Behaviors**:
  - Input: Insert operation at position → Output: Updated buffer with character inserted
  - Input: Undo command → Output: Previous buffer state restored
  - Input: Save command → Output: Buffer persisted to disk

**2. HTTP Client Class**
- **Behaviors**:
  - Input: GET request with URL → Output: Response with status code and body
  - Input: Failed request → Output: Retry with backoff or error propagation
  - Input: Timeout threshold exceeded → Output: Connection termination

**3. Database Transaction Manager**
- **Behaviors**:
  - Input: BEGIN transaction → Output: New transaction context with ID
  - Input: Conflicting write operations → Output: Lock acquisition or deadlock detection
  - Input: COMMIT → Output: Persistent state change or rollback on failure 

## Monitoring vs Observability Comparison Points

| Aspect | Monitoring | Observability |
|--------|-----------|---------------|
| **Error Coverage** | Predictable errors (Infrastructure or Exception based in Grafana) | Unpredictable errors, capable of handling incidents and minimizing critical scenarios |
| **Data Processing** | Extracts data and stores in time-series with acceptable aggregation interval | Executes real-time slicing of high dimensional data for deductive root cause analysis |
| **Telemetry Focus** | Captures traces at best, logs providing additional detail if captured properly | Captures events with high dimensionality to provide accurate context on error cases |
| **Use Case** | Assess performance of infrastructure components or historical trends of services | Assess user experience and product usage in real-time with feature-level division; rapid incident handling (RCA in minutes) |

## Limitations to Monitoring

Some of the limitations that Traditional Monitoring faces when applied to Distributed systems are - 

- *Health checks* : In monolithic architectures, application status was measurable and observable using two indicators - UP and DOWN values. A single bug introduced during a new release led to a complete failure of the application and developers were on high alert to resolve the bug as soon as possible to bring the application back to the UP status. In microservice architectures, it is possible for the application to have an UP status and still have components with partial or complete failures which leads to application functionality loss and user's inability to access certain features. Assigning indicators for health check defeats the purpose of being able to readily describe the live performance status of the application.
- *Gateway* : Gateway and security logic have separated concerns in microservice applications. This means that requests that are administered and governed by the Gateway takes different approaches than in-built Authentication operations and being able to detect which component or which functional capability of a particular component contributed to a witnessed incident of requests failure becomes complicated.
- *Container apps* : Key metrics like CPU usage and Memory usage in Container apps can be impacted via one of two options (or even both of them). One contributor for the CPU and Memory usage levels appear from the OS operations involved underneath the Container app whereas the other contributor is any given feature of the application encountering unexpected scenario of high user base access, high payloads, high feature functionality computation and so on. Measuring a simple usage metric does not allow us to distinguish between whether the contributor is some OS operation or is due to the application feature built and deployed.  
- *Exception raises* : Being able to measure and view exception raises based on HTTP Status Code or even the name of the exception does not enable the team to be able to describe the overall state in verbose detail. One lacks the ability to differentiate between business logic exception vs downstream programming language propagated exceptions, ability to use trace IDs or correlation IDs to link together telemetry records and describe the failure state (even if these IDs are present, the problem source of the incident is assumed to be isolated to a single source which could be incorrect), ability to define partial state of all components involved in the application during the exception raise.

## Benefits of Observability

Benefits that developers and stakeholders under a project can obtain as a consequence of using Observability are -

- Developers are more confident with RCA procedures. Incidents are assessed with more accuracy using real-time slicing of data. Correlation between data fields are used to create a trail of breadcrumbs for the RCA.
- Developers need to deal with less burnouts due to Observability tool's capability of detecting issues in real-time and shorter time intervals thereby decreasing team performance metrics like MTTD, MTTR. 
- User experience and product usage determines the Objectives (SLOs) and alerts setup in the dashboards, rather than infrastructure performance/status.
- Incidents are detected in a proactive manner internally by the development team prior to customer complaints raised by end user. Observability platform provides an accurate representation of user experience under the incident use case encountered.
- Observability promotes open-ended inquiries rather than pattern recognition and years of experience. Developers with the least exposure and experience in a project also have opportunities in understanding and resolving incidents when using Observability. It democratizes system performance and reliability tasks among all developers, leading to more efficient development of new features, faster deployments and overall healthy SDLC.
- Observability platform capabilities tend to disperse to external stakeholders, empowering non technical teams to have better answers to business and project related questions without having to accumulate a large amount of technical skills. 
