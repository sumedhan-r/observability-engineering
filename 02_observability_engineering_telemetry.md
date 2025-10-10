# Abbreviations

- **API** - Application Programming Interface
- **OS** - Operating System
- **PII** - Personally Identifiable Information
- **PICs** - Persons In Charge
- **RCA** - Root Cause Analysis
- **UoW** - Unit of Work
- **UUID** - Universally Unique Identifier

# Building Block of Observability

In order to adopt Observability as a standard practice across a project, the application needs to be built such that the ideal source of data/information is captured from the distributed system and stored in a remote storage suited for analytical purposes. Such data is categorized as telemetry data. 

Telemetry is the automatic operation of collecting analytical data of any system and transmitting it to a remote storage location. Telemetry operations have been applied in various indsutries prior to Software industry such as Aerospace, Automotive and Healthcare. The primary objective that prompted engineers to implement this functionality was to detect and understand potential failure points and failure sources of the mechanical device/human body. Failure scenarios that lie on long tail of event distributions (unknown unknowns) cannot be predicted by any means and can be efficiently addressed only with timely and noise-free raise of awareness to the critical situation and depending on the data points gathered in the critical situation, PICs can take responsible actions.

For a software application in a distributed system (built with Microservice architecture), the ideal source of telemetry data that can be gathered is called a Structured Event. A structured event represents a snapshot of the application at any given time instance, describing the internal state based on a broad range of parameters (fields). 

## Structured Events

Structured events consist of

- Unique IDs (UUID)
- Variable values (rate limits, retry counts, pagination)
- Headers
- Query parameters
- Execution time
- Remote/external API calls
- Execution time of remote/external API calls

Caution must be taken that any PII such as API keys, name of user, email of user are not stored in any telemetry data. But after masking those data values, an attempt must be made to capture as many data points as possible. The reason for this is because the more data points present in an event, the more functionalities of the application gets captured (requests, background tasks, jobs, dependency interactions). In addition, obtaining correlations between two or more sources for a given incident becomes attainable, allowing for accurate RCA. 

A structured event must not be small enough to ignore crucial pieces of information describing the application internal state, nor should it be too wide to appear cluttered with information and make it cumbersome to navigate. But the collection of data points has to fall closer to the wider spectrum since it is always convenient to obtain more information without having to determine a fixed schema or perform predictions on possible sources of shifts in application dynamics. This mandates defining the right level of Abstractions before deciding on the wide collection of data points that need to be captured. An Abstraction does not have to provide the entire exhaustive list of fields to capture, but must be clear enough to allow engineers understand the overarching objective and make decisions on the successive steps to be taken from the starting point within the abstraction. 

A technical-based abstraction that gives us a starting point to determine the data points to be captured is

- Agnostic runtime information : Consists of
    - Container
    - Host
    - App version
    - DB version
- Request based information : Consists of
    - User ID
    - Session token
    - Headers
    - Query parameters

A software application can be broken down and represented as a collection of unit of works performing a required task. A unit of work is analogous to a process in an OS, meaning that the definition can vary depending on the context, requirements of various operations and features of the application. Sometimes, a simple function performing an input-output operation could be called a unit of work, other times it could be a process relying on remote calls, input-output, data storage and intermediate data processing to constitue in entirety a unit of work. 

Taking the definition and practical utility of an OS process, we can define the lifecyle of a process to clearly understand how an event needs to be structured. A process lifecycle consists of

- Input
- Processing (schema validation, type casting)
- Execution
- Output

Based on the above four stages of a lifecycle, structure of an event can be created as  

- Input of UoW
- Attributes of UoW
    - Computed
    - Resolved
    - Discovered
- Execution conditions of UoW
- Output of UoW

The benefits of collecting structured events lie along two lines

- Anomaly detection : Failure cases that are deemed unknown unknowns are anomalies (long tail) in any distribution of events. As such, humans need the ability to detect that at a given time instance, the application is in an anomalous state. The most easiest approach (and ideally, complexity levels in the approach need to be kept as low as possible in order to avoid downstream biases influencing the decision) is to take the baseline/stable state, take the anomalous state and see any deviations based on difference between stable state and anomalous state. Over a long time duration, enough events can be captured and collected that would facilitate in performing this deviation calculation. In most cases, relying on historical events might not provide the ncessary analysis for noticing the deviation, in which case the application must be capable of sampling events at a higher rate (say 1000 events per second) which would further increase the volume of events being captured.
- Correlations : Having decided on different abstractions using different angles of perception for the application, events can be created to capture an arbitrarily wide range of data points. These data points can be used to determine multiple sources involved in a given scenario (not necessarily a failure scenario). Narrowing down on the multiple sources involved allows engineers to deductively determine which of those sources are correlated in their contribution to the application internal state. One does not need to limit themselves in apprehending the multiple sources to agnostic data points of a software system but rather expand the viewpoint to obtain correlations between agnostic information and request-based information (like page load time to replica), or any combination of abstractions present within the captured event.

## Limitations of Metrics

Traditional metrics that are captured in telemetry data consists of obtaining a numeric value based on overall performance of a given component and pre-aggregating it based on defined buckets of time intervals. The pre-aggreagation also involves a collection of standard mathematical functions applied to the collected metric value such as MIN, MAX, TOTAL, AVG, MEAN, MEDIAN, STD, p90, p99. Often times, most of the mathematical computations are not deemed necessary for determining the performance of the application, but the overall goal adopted is to obtain a level of granularity that can be used as an absolute indicator. Making this absolute enables engineers to comfortably depend on making deterministic decisions on application performance/status. But this defeats the purpose of Observability which aims to understand the internal state, not necessarily make deterministic conclusions (conclusions can be made subsequently after having a clear depiction of a failure scenario)

Traditional Metrics poses two problems :

- Pre-aggregation : Keeping aside the absolute nature of pre-aggregated metrics, the operation of aggregating a numeric describing system performance over a time interval bucket ignores and misses information that provides a description for each possible snapshot within the time interval bucket. Assuming one snapshot is obtained by one-tenth of a second and a bucket being 5 minutes, the pre-aggregation gives one value within the 5 minute interval where snapshots represented by events could provide 10 * 60 * 5 = 3000 numeric values within the same 5 minute interval. In addition, performing the mathematical computation over the 3000 numeric values obtained from events is going to provide the same pre-aggregated metric obtained with the Traditional approach
- Overall application performance : Traditional metrics provided value for Legacy software systems that were built using Monolithic architectures. Since all components of the application were condensed in location and simpler in architecture, any single component failing indicated the entire application was crashing. Engineers were capable of storing the internal state of the application inside their minds and using these mental models, make decisions on what metrics would provide valuable information for a failure scenario. But modern software systems with Microservoice architecture in s Distributed system consists of decoupled and independent components. Failure in one component does not mean the enitre application is crashing. In addition, within a single component, certain process/UoW could be failing without having to cause the entire component to crash. As such, metrics cannot be defined based on overall performance.

Metrics captured for modern software systems must consist of numeric values based on the collection of Abstractions employed to construct the event and must be stored inside each event (if possible). This allows the metric to provide an accurate representation of the internal state and facilitates deductive analysis leading to high probable conclusions rather than deterministic conclusions (limiting in nature).

## Limitations of Logs

Logs are sources of telemetry data that consist of operations, activities and usage of software application often stored as historical records. The term historical is key, as it depicts the process engineers take to debug an issue in an application. These issues can either be known unknowns or unknown unknowns since the scope of historical records has to cover all possible scenarios. There are no limitations to what data can be stored in logs (considering that general security standards and business standards are followed), thereby allowing engineers to rely on these sources of data for delayed debugging of issues in applications. Observability is not limited to delayed analysis, it allows engineers to perform real-time analysis of application performance and user impact and as such, logs cannot be extended for the purpose of real-time debugging.

Even for the purpose of delayed analysis, modern software systems raise problems in constrast to legacy software systems which can be addressed using a conversion from Unstructured logs to Structured logs. 