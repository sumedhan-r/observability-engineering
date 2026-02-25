# Overview

This page and the following child pages covers all the notes gathered from reading the book Observability Engineering. The book primarily focuses on modern software systems with reasons to why a clarification needs to be made between Monitoring and Observability. In addition, an accurate definition of Observability allows developers under a project to solve issues in modern software systems with ease and reliability.

Legacy software systems relied on a monolithic architecture. These architectures are simple to manage, assess, debug, reason over and understand as the components involved in the architecture are confined and simplistic. On the other hand, microservice architectures contain higher complexity and distributed setups which makes it cumbersome, unpredictable, chaotic and confusing to solve incidents or issues in the software system. Traditional Monitoring is not capable of performing the task of solving issues in microservice architectures since these systems were developed for monolithic architectures, providing simpler insights and solutions. 

# Content

- [Observability System - Foundation](../../../../personal-space/sumedhan/observability-engineering/01_observability_engineering_foundation.md)
- [Observability System - Telemetry](../../../../personal-space/sumedhan/observability-engineering/02_observability_engineering_telemetry.md)

# Evolution of Software Development

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
  - Dependencies were independently initialized and removed with customized build and execution abilites
  - API layer was only concerned with processing the requests whilst pushing the dependencies to the boundary layers of the Container app/Cluster node vs various Components involved
- Operations team did not catch up. Drastic changes in architecture precipitated by Distributed systems did not shine light on requirements for an alternative perspective on Application maintenance. System performance was not impacted frequently due to a single component failure, making the overall reliance of Development team on the Operations team minimal.

The inability to catch up with changing circumstances and practices in Software Development only increases the significance of adapting to a better practice for Operation tasks. This is realized through an Observability perspective when teams working on projects are deeply aligned with the fundamental principles responsible for obtaining Observability in software applications. 

# Monitoring vs Observability Comparison Points

Some of the key points to consider when comparing current Monitoring approaches to proposed Observability method are -

- Application errors that are monitored are **predictable** in Monitoring (Infrastructure or Exception based in Grafana). Observability covers **unpredictable** errors, which is capable of handling incidents and minimizing critical scenarios.
- Monitoring approach extracts application performance data and stores it in **time-series** and in acceptable aggregation interval. Observability extracts data and executes **real-time slicing** of high dimensional data for deductive root cause analysis.
- Telemetry for Monitoring only captures **traces** at best, logs providing additional detail if captured properly. Telemetry for Observability captures **events** with high dimensionality in order to provide accurate context on the error case encountered in the application incident.
- Monitoring is best suited to assess the performance of **infrastructure components** of an application, or **historical trends** of services offered to users. Observability is capable of assessing **user experience** and product usage in **real-time** with feature-level division and handles incidents rapidly (with time intervals of RCA spanning minutes at best)

# Limitations to Monitoring

Some of the limitations that Traditional Monitoring faces when applied to Distributed systems are - 

- *Health checks* : In monolithic architectures, application status was measurable and observable using two indicators - UP and DOWN values. A single bug introduced during a new release led to a complete failure of the application and developers were on high alert to resolve the bug as soon as possible to bring the application back to the UP status. In microservice architectures, it is possible for the application to have an UP status and still have components with partial or complete failures which leads to applciation functionality loss and user's inability to access certain features. Assigning indicators for health check defeats the purpose of being able to readily describe the live performance status of the application.
- *Gateway* : Gateway and security logic have separated concerns in microservice applications. This means that requests that are administered and governed by the Gateway takes different approaches than in-built Authentication operations and being able to detect which component or which functional capability of a particular component contributed to a witnessed incident of requests failure becomes complicated.
- *Container apps* : Key metrics like CPU usage and Memory usage in Container apps can be impacted via one of two options (or even both of them). One contributor for the CPU and Memory usage levels appear from the OS operations involved underneath the Container app whereas the other contributor is any given feature of the application encountering unexpected scenario of high user base acces, high payloads, high feature functionality computation and so on. Measuring a simple usage metric does not allow us to distinguish between whether the contributor is some OS operation or is due to the application feature built and deployed.  
- *Exception raises* : Being able to measure and view exception raises based on HTTP Status Code or even the name of the exception does not enable the team to be able to describe the overall state in verbose detail. One lacks the ability to differentiate between business logic exception vs downstream programming language propagated exceptions, ability to use trace IDs or correlation IDs to link together telemetry records and describe the failure state (even if these IDs are present, the problem source of the incident is assumed to be isolated to a single source which could be incorrect), ability to define partial state of all components involved in the application during the exception raise.

# Benefits of Observability

Benefits that developers and stakeholders under a project can obtain as a consequence of using Observability are -

- Developers are more confident with RCA procedures. Incidents are assessed with more accuracy using real-time slicing of data. Correlation between data fields are used to create a trail of breadcrumbs for the RCA.
- Developers need to deal with less burnouts due to Observability tool's capability of detecting issues in real-time and shorter time intervals thereby decreasing team performance metrics like MTTD, MTTR. 
- User experience and product usage determines the Objectives (SLOs) and alerts setup in the dashboards, rather than infrastructure performance/status.
- Incidents are detected in a proactive manner internally by the development team prior to customer complaints raised by end user. Observability platform provides an accurate representation of user experience under the incident use case encountered.
- Observability promotes open-ended inquires rather than pattern recognition and years of experience. Developers with the least exposure and experience in a project also have opportunities in understanding and resolving incidents when using Observability. It democratizes system performance and reliability tasks among all developers, leading to more efficient development of new features, faster deployments and overall healthy SDLC.
- Observability platform capabilities tend to disperse to external stakeholders, empowering non technical teams to have better answers to business and project related questions without having to accumulate a large amount of technical skills. 
