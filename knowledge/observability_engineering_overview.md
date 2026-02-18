# Overview

This page and the following child pages covers all the notes gathered from reading the book Observability Engineering. The book primarily focuses on modern software systems with reasons to why a clarification needs to be made between Monitoring and Observability. In addition, an accurate definition of Observability allows developers under a project to solve issues in modern software systems with ease and reliability.

Legacy software systems relied on a monolithic architecture. These architectures are simple to manage, assess, debug, reason over and understand as the components involved in the architecture are confined and simplistic. On the other hand, microservice architectures contain higher complexity and distributed setups which makes it cumbersome, unpredictable, chaotic and confusing to solve incidents or issues in the software system. Traditional Monitoring is not capable of performing the task of solving issues in microservice architectures since these systems were developed for monolithic architectures, providing simpler insights and solutions. 

# Content

- [Observability System - Foundation](../../../../personal-space/sumedhan/observability-engineering/01_observability_engineering_foundation.md)
- [Observability System - Telemetry](../../../../personal-space/sumedhan/observability-engineering/02_observability_engineering_telemetry.md)

# Comparison Points

Some of the key points to consider when comparing current Monitoring approaches to proposed Observability method are -

- Application errors that are monitored are **predictable** in Monitoring (Infrastructure or Exception based in Grafana). Observability covers **unpredictable** errors, which is capable of handling incidents and minimizing critical scenarios.
- Monitoring approach extracts application performance data and stores it in **time-series** and in acceptable aggregation interval. Observability extracts data and executes **real-time slicing** of high dimensional data for deductive root cause analysis.
- Telemetry for Monitoring only captures **traces** at best, logs providing additional detail if captured properly. Telemetry for Observability captures **events** with high dimensionality in order to provide accurate context on the error case encountered in the application incident.
- Monitoring is best suited to assess the performance of **infrastructure components** of an application, or **historical trends** of services offered to users. Observability is capable of assessing **user experience** and product usage in **real-time** with feature-level division and handles incidents rapidly (with time intervals of RCA spanning minutes at best)

# Benefits of Observability

Benefits that developers and stakeholders under a project can obtain as a consequence of using Observability are -

- Developers are more confident with RCA procedures. Incidents are assessed with more accuracy using real-time slicing of data. Correlation between data fields are used to create a trail of breadcrumbs for the RCA.
- Developers need to deal with less burnouts due to Observability tool's capability of detecting issues in real-time and shorter time intervals. 
- User experience and product usage determines the Objectives (SLOs) and alerts setup in the dashboards, rather than infrastructure performance/status.
- Incidents are detected in a proactive manner prior to customer complaints raised by end user. Observability platform provides an accurate representation of user experience under the incident use case encountered.
- Incidents are detected internally by the development team first before having to notice customer complaints raised by end user.
- Observability promotes open-ended inquires rather than pattern recognition and years of experience. Developers with the least exposure and experience in a project also have opportunities in understanding and resolving incidents when using Observability. It democratizes system performance and reliability tasks among all developers, leading to more efficient development of new features, faster deployments and overall healthy SDLC.
- Observability platform capabilities tend to disperse to external stakeholders, empowering non technical teams to have better answers to business and project related questions without having to accumulate a large amount of technical skills. 
