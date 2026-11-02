# Observability Engineering - Foundation

## Table of Contents

## Abbreviations

- **API** - Application Programming Interface
- **BI** - Business Intelligence
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

But modern software systems do not concern themselves over infrastructure components when developing and delivering features to end users. Developers focus more on code functionality and code standard and in the rise of AI managed development, more processes involving the SDLC address issues in the code base. This prominent shift from infrastructure components to code base highlights the need to adopt a different telemetry collection approach

### Case for new approach to telemetry collection - unified event

For software systems delivering a huge range of features handled with varying complexities like feature flags, deployment slots, regional provisions, continuous security and data compliance, managing the code base becomes complicated for developers building the products. Every feature and decision during development has to be made on the basis of logic and specifications that adhere to **first principles**.

AI managed development tends to hallucinate when provided incorrect prompts and context regarding the software project even with extensive documentations and guidelines for instructions. Course correcting agentic errors in all phases can only be performed efficiently using first principle explanations.

A similar model has to be followed when establishing observability in the product. Any telemetry data that is collected must provide developers the capability to reason with the data using first principles. The only data type that provides such a capability is called an event, which is a collection of arbitrarily wide attributes stored in a dictionary format, with preference to high cardinal attributes. This provides an ability to filter and correlate among various dimensions to obtain insight and visibility into the system state that can cover unforeseen or complex perspectives. Events can be collected as either canonical/structured logs or spans in traces but the decision to determine the format of events depends solely on the system complexity and whether the event telemetry data is capable of explaining said complexity.

The importance of storing the telemetry data in a unified data source is best explained when the properties of an event are listed out and how event telemetry enables observability. One of the major benefits of such a data type is that it provides developers with a high degree of flexibility on what needs to be tracked and collected. In addition, the level of detail that one needs to capture in an event can be calibrated with high precision due to the limitless possibility and acceptance of collecting attributes.

### Properties of event telemetry

Some of the properties of event telemetry data type are as follows

- Attribute : Additional event attribute leads to exponential contributions due to enabling better filtering of data for internal system state identification
- Detail : High cardinal (possible set of values) attributes enhance observability as per ability to filter uniqueness of incident
- Aggregation : Aggregation of data points is flexible and in some cases, creates novel possibilities of analysis
- Incident visibility : Pre-defined structure for telemetry forces visibility into internal state only for predictable and known system conditions. Flexible structure for telemetry makes it capable of describing unforeseen system conditions
- Dynamic conversation : Events consisting of wide attributes allow focus and expansion in real time varying from aggregation to individual record, creating a dynamic conversation between telemetry and developer
- Feedback loop : Queries used for analysis must return results in seconds in order to make it feasible to ask more questions for clarity
