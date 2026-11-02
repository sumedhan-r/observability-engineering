# Observability Engineering - Foundation

## Table of Contents

- [Abbreviations](#abbreviations)
- [Overview](#overview)
- [Definition](#definition)
- [Legacy vs Modern Software](#legacy-vs-modern-software)
  - [Obsolete Observability approach for Modern software](#obsolete-observability-approach-for-modern-software)
- [Observability components](#observability-components)
  - [Cardinality](#cardinality)
  - [Dimensionality](#dimensionality)
- [Drawbacks of Traditional Monitoring](#drawbacks-of-traditional-monitoring)
  - [Consequences of Monitoring applied to Modern Software](#consequences-of-monitoring-applied-to-modern-software)
  - [Comparison of Monitoring vs Observability](#comparison-of-monitoring-vs-observability)
- [Example use case](#example-use-case)
  - [Mobile Backend as a Service](#mobile-backend-as-a-service)
- [Monolithic vs Microservice Architecture](#monolithic-vs-microservice-architecture)
  - [Monolithic](#monolithic)
    - [Characteristics](#characteristics)
    - [Experiences](#experiences)
  - [Microservice](#microservice)
    - [Characteristics](#characteristics-1)
    - [Experiences](#experiences-1)
- [Technical team benefits obtained from Observability](#technical-team-benefits-obtained-from-observability)

## Abbreviations

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

## Overview



## Definition

Observability is defined as the ability to determine the internal state of a system using external outputs/signals regardless of how fuzzy or bizarre the internal state is. Irrespective of whether the internal state is predictable or unpredictable, unprecedented, chaotic, the internal state must be determined with full certainty when using an Observability tool/method.

To break it down further into granular detail, Observability system must allow engineers to

- Understand inner workings of application
- Understand internal states no matter the condition, type and predictability
- Understand inner workings and internal state solely using external outputs
- Understand internal state without shipping custom code

Shipping custom code implies that a separate standalone feature is developed for the purpose of Observing previously built features. This is not the ideal way to understand how the internal state of the software system changes since the new custom code could bring additional complexity to the internal state even if it has simple logic attached to it.

## Legacy vs Modern Software