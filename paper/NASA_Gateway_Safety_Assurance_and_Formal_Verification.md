The Interface Between Safety Assurance and Formal Verification in NASA Gateway Autonomous Systems: A Traceability Gap in Public Documentation

Samir Baladi
Principal Investigator, Author, and Protocol Designer
Ronin Institute / Rite of Renaissance
Email: gitdeeper@gmail.com
ORCID: "0009-0003-8903-0029" (https://orcid.org/0009-0003-8903-0029)
Project Website: "NASA-GATEWAY" (https://nasa-gateway.netlify.app)
Project Zenodo Record: "https://doi.org/10.5281/zenodo.24559255" (https://doi.org/10.5281/zenodo.24559255)

---

Abstract

Autonomous spacecraft systems must operate within safety constraints while retaining sufficient decision-making capability to respond to failures, degraded conditions, and interruptions in communication with ground operators. In NASA's Gateway architecture, these requirements involve multiple levels of system responsibility, including local autonomy within modules, vehicle-level coordination through the Vehicle System Manager (VSM), and formal verification mechanisms intended to establish confidence in system behavior.

This study examines the relationship between safety assurance and formal verification in NASA Gateway autonomous systems. Its central question is whether safety-derived boundaries of local autonomy can be traced to operational decision and escalation rules at the interface between Module System Managers (MSMs) and the VSM, and whether these rules are represented and verified through formal contracts or fault-management mechanisms.

The investigation identifies two established and independently documented pathways. The first is a safety-assurance pathway involving hazard analysis, catastrophic hazard controls, autonomous operation requirements, and documented safety responsibilities. The second is a verification pathway involving Assume-Guarantee Contracts (AGCs), formal specification methods, model checking, and runtime verification using R2U2.

The reviewed documentation also establishes that Gateway autonomy is not exclusively centralized. Local control and fault-response responsibilities are distributed across system and subsystem levels, while the VSM provides vehicle-level coordination and integrated fault management. However, the public documentation reviewed does not establish a complete traceability chain connecting hazard-derived autonomy boundaries to specific MSM decision rules, escalation conditions, and corresponding verification properties.

The study therefore does not conclude that such mechanisms are absent or unimplemented. Rather, it identifies an unresolved documentation and traceability question at the interface between safety assurance and formal verification. This distinction is important because the existence of safety requirements and formal verification mechanisms does not, by itself, demonstrate how the former are translated into the latter at operational decision boundaries.

Keywords: NASA Gateway; Autonomous Systems; Safety Assurance; Formal Verification; Vehicle System Manager; Module System Manager; Fault Management; Assume-Guarantee Contracts; Runtime Verification; Control Authority; Traceability.

---

1. Introduction

Autonomous operation in complex spacecraft systems requires more than the ability to execute predefined sequences or respond to individual component failures. It requires a structured distribution of decision-making responsibilities, mechanisms for managing abnormal conditions, and assurance that autonomous actions remain within established safety constraints.

These requirements become particularly significant in systems composed of multiple interconnected modules. A failure originating within one module may remain within that module's operational domain, or it may affect resources, activities, or safety conditions at the vehicle level. Consequently, autonomous systems must distinguish between conditions that can be handled locally and those that require coordination or intervention by a higher-level management system.

NASA Gateway provides a relevant context for examining this problem. Its autonomous system management architecture includes the Vehicle System Manager (VSM), which performs vehicle-level management functions, and Module System Managers (MSMs), which provide management capabilities for individual modules.

Gateway documentation describes autonomous operation, distributed fault management, formal contracts, and runtime verification. Separate safety requirements establish obligations concerning hazard identification, hazard controls, and autonomous functions necessary to control catastrophic hazards.

These documented capabilities raise a specific architectural and methodological question: how are safety-derived boundaries of local autonomy translated into operational rules governing the decisions and escalation behavior of module-level management systems?

This question concerns the relationship between two established engineering activities:

1. Safety assurance, which identifies hazards, establishes safety requirements, and defines controls intended to prevent or mitigate hazardous conditions.
2. Formal verification, which represents expected system behavior through formal properties, contracts, or models and evaluates whether specified behaviors satisfy those properties.

The presence of both activities does not automatically establish their operational connection. A safety requirement may specify that a function must remain independent of communication with Earth, while a formal contract may specify assumptions and guarantees governing an interface. The important question is whether a demonstrable relationship exists between the safety requirement, the resulting allocation of authority, the operational decision rule, and the property used to verify that rule.

This study investigates that relationship using publicly available NASA documentation and technical publications concerning Gateway architecture, safety requirements, fault management, and formal verification.

The objective is not to propose a replacement architecture or to claim that NASA lacks mechanisms for managing autonomy. Instead, the study examines what can be established from the available documentation and identifies where the relationship between safety assurance and formal verification remains insufficiently demonstrated.

2. Research Problem and Central Question

2.1 Research Problem

The Gateway architecture distributes autonomous functions across multiple system levels. Local systems can perform certain control and fault-response activities, while the VSM provides vehicle-level management and coordination.

Safety requirements establish that functions necessary for controlling catastrophic hazards must not depend on communication with Earth. Other requirements address the identification of hazards, the implementation of controls, and the verification of their effectiveness.

In parallel, Gateway verification work documents the use of formal contracts, model checking, and runtime verification. These mechanisms provide ways to specify and evaluate expected system behavior.

However, the existence of these elements does not establish how safety-derived autonomy boundaries are represented as specific operational rules governing local decision-making.

For example, a safety analysis may identify a condition requiring autonomous action at the module level. The corresponding operational architecture must determine which system is authorized to act, which conditions permit local action, when an issue must be escalated, and how conflicting or unsafe commands are handled.

The verification architecture must then provide a means of establishing that the relevant decision rules behave as intended.

The research problem is therefore located at the interface between safety-derived authority allocation and the formal representation of operational behavior.

2.2 Central Research Question

The central research question is:

How are safety-derived boundaries of local autonomy translated into formally verifiable decision and escalation rules at the interface between Module System Managers and the Vehicle System Manager in NASA Gateway?

This question is examined through four subordinate questions:

1. How does the Gateway architecture define the distribution of control responsibilities between module-level and vehicle-level management?
2. What safety requirements establish the need for autonomous operation and independent hazard control?
3. What formal verification and runtime verification mechanisms are documented for Gateway autonomous systems?
4. Does the publicly available documentation establish a traceability relationship between safety-derived autonomy boundaries and the decision rules verified at the MSM–VSM interface?

2.3 Research Objective

The objective is to identify the documented relationships between:

- Hazard identification and safety analysis.
- Safety requirements and autonomous functions.
- Allocation of control authority and operational responsibility.
- MSM–VSM interaction and escalation behavior.
- Formal contracts and verification properties.
- Runtime monitoring and fault-management responses.

The study seeks to distinguish between the existence of individual mechanisms and the documentation of a complete traceability relationship connecting them.

3. Research Scope and Methodology

3.1 Scope

The investigation focuses on NASA Gateway autonomous system management, particularly the relationship between the VSM and MSM architectural levels.

The principal areas examined are:

- Gateway autonomous system architecture.
- Local autonomy and distributed fault management.
- Safety requirements and hazard-control obligations.
- Control authority and locus-of-control concepts.
- Assume-Guarantee Contracts.
- Development-time formal verification.
- Runtime verification and fault-management integration.
- Operational scenarios involving module-level and vehicle-level coordination.

The study does not attempt to evaluate every subsystem or establish the implementation status of every Gateway safety and autonomy mechanism.

It also distinguishes between architectural descriptions, system requirements, research prototypes, risk-reduction activities, and descriptions of intended operational behavior.

3.2 Documentary Research Method

The research follows a documentary analysis approach based on publicly available NASA requirements, technical papers, architecture descriptions, and engineering publications.

Documents were examined according to their relevance to the central research question.

The analysis used five principal categories:

A. Architectural evidence

Documents describing system responsibilities, management hierarchy, control domains, and interactions between VSM and MSM components.

B. Safety-assurance evidence

Requirements and safety documentation addressing hazard analysis, catastrophic hazard control, autonomous operation, and the independence of safety-critical functions from communication with Earth.

C. Authority-allocation evidence

Descriptions of control authority, locus of control, local fault response, command validation, and escalation between management levels.

D. Formal-verification evidence

Documents describing formal contracts, temporal logic, model checking, state-machine verification, and runtime verification.

E. Operational and experimental evidence

Engineering examples, risk-reduction studies, and operational scenarios illustrating how local and vehicle-level management responsibilities interact.

3.3 Analytical Approach

The documentary analysis examines whether the following traceability sequence can be established:

1. A hazard or hazardous condition is identified.
2. A safety requirement or control obligation is derived.
3. The required autonomous function is allocated to a system or subsystem.
4. The allocation defines an operational authority boundary.
5. The authority boundary is translated into a decision or escalation rule.
6. The rule is represented through an appropriate formal property, contract, or fault-management mechanism.
7. The resulting behavior is verified or monitored.

This sequence is used as an analytical structure for examining the available evidence. It is not presented as an existing NASA process unless the reviewed documentation explicitly establishes that relationship.

3.4 Evidence Classification

To avoid conflating different levels of engineering evidence, the study distinguishes among:

- Requirement evidence: establishes what a system is required to do.
- Architectural evidence: describes the intended organization and distribution of responsibilities.
- Formal specification evidence: describes properties or contracts used to express expected behavior.
- Verification evidence: documents the application of verification methods to specified models or properties.
- Operational evidence: documents behavior in an operational context or describes an operational procedure.
- Experimental evidence: demonstrates a concept or mechanism within a research or risk-reduction environment.

This distinction is essential. A requirement does not independently prove implementation, and an experimental demonstration does not independently establish operational deployment.

4. Findings

4.1 Gateway Architecture and the Distribution of Control Responsibilities

NASA Gateway documentation identifies the VSM as a central element of the autonomous system management architecture.

The VSM is responsible for vehicle-level functions that include:

- Mission management and timeline execution.
- Resource management.
- Fault management.
- Vehicle control and operation.

The architecture also includes module-level management capabilities through MSMs.

This organization indicates that autonomous control is not exclusively centralized within the VSM. Individual modules retain management responsibilities for their own systems, while the VSM provides a vehicle-level perspective and coordination capability.

Gateway architecture therefore involves multiple levels of control responsibility.

The VSM is not simply a remote command relay for module-level systems. It maintains an integrated view of vehicle conditions and coordinates activities that require vehicle-level awareness.

At the same time, module-level systems are not merely passive execution interfaces. They participate in local management and fault-response activities.

This distribution creates an important distinction between local control and vehicle-level control.

A condition affecting a single component may be handled within its local management domain. A condition involving shared resources, cross-module dependencies, or vehicle-level mission constraints may require coordination by the VSM.

The architecture establishes the existence of these different management levels. However, the existence of a hierarchy alone does not fully specify the operational conditions under which authority or responsibility must move from one level to another.

4.2 Control Authority and Locus of Control

The distinction between control authority and locus of control provides additional context for understanding the Gateway management architecture.

The paper When the Eyes Don’t Have It: Autonomous Control of Deep Space Vehicles for Human Spaceflight (2020) discusses the relationship between human operators and autonomous vehicle management.

It distinguishes between:

- Locus of Control: the entity or system that holds logical control of the vehicle as a whole.
- Control Authority: the authority to control a particular system or component.

The paper describes circumstances in which the VSM manages the vehicle during nominal autonomous operation, while human operators retain ultimate authority.

It also discusses conditions involving the transfer of control between the VSM, crew, ground operators, and module-level management systems.

The VSM can evaluate operator commands according to vehicle state, configuration, and operating conditions. It can also resolve conflicts between commands and verify conditions before returning from manual control to autonomous management.

These descriptions demonstrate that control authority is not a single, undifferentiated property.

An entity may hold authority over an individual component without holding the logical control of the entire vehicle. Conversely, vehicle-level management may coordinate system behavior without necessarily replacing every local control function.

This distinction is relevant to the MSM–VSM interface because it provides a conceptual basis for examining how local authority and vehicle-level coordination coexist.

However, the 2020 paper must be interpreted within its own architectural and documentary context. It does not, by itself, establish the exact operational rules governing every Gateway MSM–VSM interaction in later architecture descriptions.

4.3 Domain of Control

NASA's 2023 presentation Trustworthy Autonomy for Gateway Vehicle System Manager describes the concept of a Domain of Control.

The presentation establishes two relevant principles:

1. The control domain should remain at the lowest possible level.
2. Control authority should be elevated to a level that possesses the appropriate perspective or visibility.

The presentation also describes abstraction layers through which different management levels operate with limited views of system data and models.

These principles support an architecture in which control responsibilities are distributed according to the scope of the condition and the information required to manage it.

A local system can manage conditions within its own domain, while broader conditions can require higher-level authority.

The concept therefore provides architectural support for hierarchical autonomy.

However, the reviewed presentation does not provide a complete operational decision function specifying when a condition becomes external to a local control domain.

In particular, the public material reviewed does not establish a complete set of executable rules defining:

- The precise conditions under which local authority must be retained.
- The conditions that require escalation to the VSM.
- The criteria for determining whether a local recovery action is sufficient.
- The conditions under which a higher-level system may override or constrain a local action.
- The formal properties corresponding to each authority transition.

The resulting finding is:

The control domain is architecturally bounded and context-sensitive, but the operational rules governing changes to its boundaries remain unspecified in the reviewed public material.

This statement concerns the level of detail available in the reviewed documentation. It does not imply that such rules do not exist in implementation documents or internal engineering artifacts.

4.4 Local Autonomy as a Formal Safety Requirement

A particularly important source is the Gateway System Requirements document, DSG-RQMT-001 (2019).

The document includes requirements concerning hazard identification, hazard controls, and autonomous operation.

Among the relevant requirements are:

- L2-GW-0111: verification of fault tolerance associated with catastrophic hazards through integrated hazard analysis.
- L2-GW-0112: identification of catastrophic hazard causes and controls, together with verification of control effectiveness.
- L2-GW-0113: analysis of critical hazards and verification of their controls.
- L2-GW-0199: autonomous operation.

Requirement L2-GW-0199 states:

«The system and subsystem functions required for catastrophic hazard control do not depend on communication with Earth.»

This requirement is particularly significant for the present investigation.

It establishes that the functions necessary to control catastrophic hazards must be capable of operating independently of communication with Earth.

Consequently, local autonomy is not merely an architectural preference or a convenience for reducing communication dependence. It is connected to a formal safety obligation.

The requirement also implies that hazard-control capability must be available at the system or subsystem level when communication with Earth is unavailable.

However, the requirement does not independently identify which management entity makes every operational decision, nor does it specify the complete conditions under which local action must be escalated to the VSM.

It establishes an autonomy obligation, but the operational translation of that obligation requires additional architectural and implementation-level information.

4.5 Safety Requirements at the Logistics Module Level

The Gateway Logistics Services Requirements document, GLS-RQMT-001, provides more detailed examples of safety-related autonomy and control obligations.

Because this document concerns the Logistics Module, its requirements must not be generalized automatically to every Gateway module.

Nevertheless, it provides relevant evidence of how safety and autonomy responsibilities can be expressed at a more specific system level.

Examples include:

- L3-GLS-2001: control of critical hazards through the module or a combination of module-level and Gateway-level controls.
- L3-GLS-2004: autonomous operation of a system or subsystem when the loss of a function could lead to a catastrophic event.
- L3-GLS-2052: the crew's ability to override higher-level automatic control when the action does not produce a catastrophic event.
- L3-GLS-2071: rejection of commands that are out of sequence when their execution would be hazardous.
- L3-GLS-2075: verification of prerequisite conditions before executing hazardous commands.
- L3-GLS-2081: automatic detection and safing of critical and catastrophic hazards within the applicable hazard-effect timeframe.
- L3-GLS-2131: fault detection, isolation, and recovery.

These requirements demonstrate that autonomy and safety can be translated into explicit operational obligations.

They also show that safety-related behavior may involve several forms of control:

- Local autonomous response.
- Higher-level automatic control.
- Command validation and rejection.
- Crew override.
- Automated safing.
- Fault detection, isolation, and recovery.

The requirements therefore provide more specific evidence than a general architectural description.

However, they do not establish that every Gateway MSM implements an identical set of decision rules. Nor do they provide, within the reviewed material, a complete mapping from each requirement to a corresponding formal contract or verification property.

Their significance is that they demonstrate the existence of detailed safety and autonomy requirements at the module level, while leaving the broader traceability question open.

4.6 Safety Documentation and the Required Evidence Structure

The Gateway Logistics Services Safety Data Package, GLS-006 (2019), describes safety documentation expected during the development process.

The package includes evidence such as:

- Operational scenarios.
- Functional and control diagrams.
- Hazard analysis.
- Fault Tree Analysis (FTA).
- Failure Modes and Effects Analysis (FMEA).
- Critical Items List (CIL).
- Safety controls.
- Documentation of the independence of preventive measures and controls.
- System Safety Analysis Reports.
- Hazard Reports.

This documentation structure is relevant because it establishes that safety assurance is expected to be supported by engineering evidence rather than by general statements of compliance.

In particular, the inclusion of control diagrams, hazard analyses, and documentation of control independence provides a potential documentary basis for tracing safety obligations into system architecture.

However, the publicly reviewed material does not establish whether the resulting safety documentation contains a complete mapping to the operational decision and escalation rules of individual MSMs.

It therefore demonstrates a structured safety-assurance process without resolving the specific interface examined in this study.

4.7 Distributed Fault Management and Local Recovery

Gateway-related publications describe fault management as a distributed activity.

The paper Gateway at the Crossroads of Sustainable Lunar Exploration (2023) describes an approach in which fault management is distributed and faults are handled at the lowest practical level.

Under this approach:

- Module providers supply fault-detection capabilities.
- Module providers define responses and safing procedures.
- Local systems can perform corrective actions within their responsibilities.
- The VSM maintains an integrated vehicle-level perspective.
- The VSM can coordinate responses when faults affect multiple modules or vehicle-level resources.

This architecture is consistent with the principle that components should handle conditions within their own responsibility and delegate issues that exceed their scope.

A related example appears in the MAST work published in 2019.

The MAST approach describes local fault management in which components handle conditions within their purview and delegate problems that exceed their local responsibilities.

A power-distribution example illustrates this organization.

A local power-management cluster may detect a fault, generate recovery options, and attempt local recovery. If the problem affects another system or exceeds the local system's responsibility, higher-level coordination becomes necessary.

The described scenario includes a local recovery attempt involving an AMPS relay. When the attempt fails, the VSM intervenes by coordinating the response, including pausing an activity and directing a power-restoration sequence. Following recovery, the VSM can authorize the activity to resume.

This example illustrates an important architectural relationship:

Local autonomy does not necessarily imply unrestricted local authority. A component may be responsible for detecting and correcting a fault, while the VSM coordinates recovery when the condition affects broader vehicle operations.

The example also shows how local and vehicle-level actions can form a coordinated response sequence.

Nevertheless, the MAST work must be treated as evidence from its own architectural and research context. It cannot independently establish that every described behavior has been implemented in the operational Gateway system.

Similarly, Gateway risk-reduction activities provide evidence of intended management interactions without establishing the complete operational implementation of every decision rule.

4.8 Gateway Risk-Reduction Scenarios

Gateway risk-reduction documentation from 2022 provides additional examples of interactions between module-level and vehicle-level management.

One scenario describes an MSM detecting a failed task and reporting its status to the VSM at a specified reporting frequency. The VSM records the failure, updates the timeline, and determines whether corrective action is required.

Another scenario describes a module-level system diagnosing a problem, collecting evidence from other systems, and escalating the issue when the required response involves vehicle-level resources.

These scenarios are relevant because they demonstrate the existence of structured information exchange and escalation concepts.

They also illustrate that escalation is not necessarily triggered by the mere existence of a fault. The need for vehicle-level intervention depends on the scope and consequences of the problem.

However, these scenarios belong to risk-reduction work. They should not be treated as complete evidence of the operational implementation of all Gateway fault-management behaviors.

Their contribution is to demonstrate examples of intended coordination between local diagnosis and vehicle-level decision-making.

4.9 Formal Verification Through Assume-Guarantee Contracts

The paper Using Assume-Guarantee Contracts for Operational Verification of Autonomous Spacecraft (2023) describes the use of Assume-Guarantee Contracts in Gateway autonomous system verification.

An Assume-Guarantee Contract specifies expected behavior through two principal elements:

- Assumptions: conditions expected to hold at the system boundary or on its inputs.
- Guarantees: behavior the system is expected to provide when the assumptions are satisfied.

This structure allows the expected behavior of individual components and their interfaces to be represented in a form suitable for verification.

The paper distinguishes between internal VSM contracts and contracts associated with the MSM interface.

Internal VSM contracts are derived from software requirements and operational scenarios or use cases.

MSM contracts are documented through the MSM Interface Control Document (ICD).

The paper also describes a division of responsibility at the interface.

The MSM provider is primarily responsible for satisfying the relevant contract, while the VSM is expected to detect and respond to anomalies at the interface.

The contracts are represented using propositional logic and Mission-time Linear Temporal Logic.

For development-time verification, the work describes state-machine representations and formal analysis using methods and tools such as TLA+ and Promela, including model checking with TLC and Spin.

For operational verification, the work describes mechanisms including inline code and R2U2.

This approach establishes that Gateway verification is not limited to conventional testing of individual software functions. It includes formal representations of expected behavior and methods for evaluating those representations.

4.10 Contract Selection and the Role of Fault Management

An important methodological detail in the 2023 AGC work concerns the selection of behaviors to be represented as contracts.

The contract-selection process considers factors such as:

- Importance to mission or safety.
- The presence of relevant temporal behavior.
- Whether the behavior is already covered by Fault Management.

This last consideration is especially important for interpreting the available contract examples.

The absence of a specific behavior from published AGC examples cannot be treated as evidence that the behavior is absent from the broader assurance architecture.

A behavior may be addressed through an existing Fault Management mechanism rather than through a separately selected contract.

Therefore:

Because the contract-selection process excludes behaviors already covered by Fault Management, the set of published contract examples cannot be treated as a complete inventory of formally verified behaviors. The absence of a specific rule from published examples is therefore not evidence of its absence from the assurance architecture as a whole.

This qualification prevents an incomplete set of published contract examples from being interpreted as a complete description of Gateway verification coverage.

It also reinforces the importance of examining the relationship between contracts and fault-management mechanisms rather than treating them as mutually exclusive or exhaustive verification approaches.

4.11 Runtime Verification and R2U2

The Gateway verification work describes R2U2 as a runtime verification mechanism.

R2U2 evaluates monitored system behavior against specified properties and produces verdicts indicating whether monitored behavior satisfies or violates those properties.

Its role is distinct from that of the operational Fault Manager.

R2U2 provides verification results, while the Fault Manager receives relevant information and is responsible for the associated fault-management response.

This separation is important.

Runtime verification can detect that an observed behavior violates a specified property. However, detecting a violation and deciding what operational action should follow are different functions.

The operational response may involve containment, safing, recovery, escalation, or another action determined by the system's fault-management architecture.

Accordingly, R2U2 should not be described as independently holding the operational authority to decide the vehicle's response.

Its role is to provide verification information that can contribute to the larger fault-management process.

4.12 Gateway Timeline Verification Developments in 2026

The 2026 paper Implementation of a Stochastic Timeline Validation Tool Integrated With R2U2 describes further development of Gateway timeline verification.

The work addresses the complexity of timelines that may contain:

- State-machine behavior.
- Conditional branches.
- Parallel activities.
- Event-triggered transitions.
- Uncertain execution conditions.

The timelines are developed on the ground and can be uploaded to Gateway for autonomous or semi-autonomous execution.

The described approach uses Monte Carlo simulation to generate event sequences, which are subsequently evaluated using R2U2.

The work also describes automatic generation of Assume-Guarantee Contracts for timelines and the association of contract violations with the tasks responsible for producing them.

This development is relevant to the present investigation because it demonstrates a continuing effort to connect operational sequences with formal properties and runtime verification.

It also provides a mechanism for identifying which timeline activities are associated with a detected contract violation.

However, the reviewed publication does not provide a clear example of a contract specifically verifying a transition in Locus of Control or an MSM–VSM authority handoff.

This observation must be interpreted narrowly.

It does not establish that such transitions are unverified elsewhere. It indicates only that the specific relationship is not demonstrated in the reviewed publication.

4.13 Ground Authorization and Autonomous Task Execution

The 2024 paper Gateway to the Future: Lessons Learned in Development of the Refueling Systems for NASA’s First Lunar Space Station provides another relevant perspective on the relationship between ground authorization and autonomous execution.

The described refueling approach involves ground-authorized automated task execution through the VSM.

The process includes:

1. Ground authorization of an operation.
2. Coordination of a predefined task sequence by the VSM.
3. Transmission of commands to the relevant MSMs.
4. Execution through module-level systems and equipment.
5. Return of telemetry and operational information to the ground.
6. Suspension at the end of the authorized sequence while awaiting further authorization.

The publication also describes the VSM's role in integrated vehicle-level Fault Detection, Isolation, and Recovery (FDIR), together with cross-module virtual links.

These details demonstrate how ground authorization, vehicle-level coordination, and module-level execution can be combined within an autonomous operational process.

However, ground authorization of a predefined sequence should not be interpreted as evidence that every individual fault response requires a new ground decision.

The reviewed material does not fully establish whether each local fault response can proceed autonomously before reporting, or which specific fault conditions require renewed authorization.

The distinction is important because authorization to execute an operational sequence and authority to respond to an unexpected condition are separate questions.

The publication therefore provides evidence of coordinated autonomous task execution without resolving every local decision and escalation rule.

5. The Relationship Between Safety Assurance and Formal Verification

5.1 Two Documented Engineering Pathways

The findings establish that NASA Gateway has documented both a safety-assurance pathway and a formal-verification pathway.

The safety-assurance pathway includes:

1. Hazard identification.
2. Hazard analysis.
3. Definition of safety controls.
4. Allocation of safety-related functions.
5. Requirements for autonomous hazard control.
6. Documentation and verification of safety controls.

The formal-verification pathway includes:

1. Definition of software requirements and operational scenarios.
2. Construction of formal contracts.
3. Representation of assumptions and guarantees.
4. Formal modeling of expected behavior.
5. Development-time verification.
6. Runtime monitoring through mechanisms such as R2U2.
7. Integration of verification results with fault management.

Both pathways are therefore documented.

The central issue is not whether Gateway has safety assurance or formal verification. The issue is whether the available documentation establishes how safety-derived authority boundaries are systematically translated into the decision rules and verification properties governing the MSM–VSM interface.

5.2 The Unresolved Interface

The relationship between the two pathways can be represented conceptually as follows:

Safety-assurance pathway

Hazard identification
→ Hazard analysis
→ Safety requirements
→ Safety controls
→ Allocation of autonomous functions
→ Authority boundaries

Formal-verification pathway

Software requirements and operational scenarios
→ Formal contracts
→ Assumptions and guarantees
→ Formal models
→ Development-time verification
→ Runtime verification
→ Fault-management response

The two pathways address related aspects of system behavior.

Safety assurance establishes what must be protected and which safety obligations must be satisfied.

Formal verification establishes whether specified behaviors satisfy defined properties under the represented assumptions and conditions.

The unresolved question lies in the connection between the outputs of these pathways.

In particular, the reviewed public material does not establish a complete mapping showing how a specific hazard-derived authority boundary becomes:

- An explicit MSM decision rule.
- A defined condition for escalation to the VSM.
- A corresponding interface contract or fault-management property.
- A formally verified or runtime-monitored behavior.
- A documented response when the relevant property is violated.

The existence of requirements, contracts, and runtime verification mechanisms does not independently demonstrate this complete mapping.

Similarly, the existence of local autonomy and distributed fault management does not establish the formal verification coverage of every authority transition.

The unresolved interface is therefore a question of traceability rather than a demonstrated absence of technical capability.

5.3 Traceability as the Central Analytical Issue

For the purposes of this study, traceability refers to the ability to follow a documented relationship between an original safety obligation and the operational and verification artifacts intended to satisfy it.

A complete traceability chain for a particular autonomy boundary would ideally establish:

1. The original hazard or safety concern.
2. The safety requirement derived from that concern.
3. The system or subsystem assigned responsibility for controlling the hazard.
4. The operational authority boundary associated with that responsibility.
5. The decision rule governing local action or escalation.
6. The formal property, contract, or fault-management rule representing the expected behavior.
7. The verification evidence associated with that rule.
8. The operational response associated with a detected violation.

This sequence is an analytical model for evaluating documentary relationships.

It should not be confused with a claim that NASA currently lacks such a process.

The reviewed sources provide evidence for several elements of the sequence, but do not establish the complete relationship across all of them for the MSM–VSM interface.

The central finding can therefore be expressed as follows:

NASA Gateway publicly documents the existence of safety-derived autonomous operation requirements, distributed control responsibilities, formal contract-based verification, and runtime verification. However, the reviewed public documentation does not establish a complete traceability chain connecting hazard-derived autonomy boundaries to specific MSM decision and escalation rules and their corresponding verification properties.

6. Discussion

6.1 Local Autonomy Is a Safety Requirement, Not Merely an Operational Preference

One important result of this investigation is that local autonomy must be understood within the context of safety assurance.

Requirement L2-GW-0199 explicitly establishes that system and subsystem functions required for catastrophic hazard control must not depend on communication with Earth.

This means that local autonomous capability has a direct relationship with the system's ability to maintain safety under communication constraints.

The architecture must therefore provide sufficient local capability to control relevant hazards without assuming continuous ground availability.

This does not mean that every decision must be made locally. Nor does it imply that local systems have unrestricted authority.

Instead, the requirement establishes the need for autonomous safety-related functions, while the broader architecture determines how responsibilities are distributed and coordinated.

6.2 Distributed Autonomy Does Not Eliminate the Need for Escalation Rules

The distributed fault-management descriptions demonstrate that local recovery and vehicle-level coordination are complementary.

A local system may detect a fault and attempt recovery within its domain. When the condition affects other systems or requires vehicle-level resources, coordination by the VSM may become necessary.

This architecture provides a practical basis for hierarchical fault management.

However, the distinction between local and vehicle-level responsibility requires operational criteria.

Without examining the specific implementation documents, it is not possible to determine the complete decision logic governing every escalation condition.

The relevant research question is therefore not whether escalation exists as an architectural concept, but how its operational boundaries are defined, represented, and verified.

6.3 Formal Contracts and Fault Management Have Complementary Roles

The AGC work demonstrates that formal contracts can express expected behavior at system boundaries.

Fault Management, meanwhile, provides mechanisms for detecting and responding to abnormal conditions.

The contract-selection process itself recognizes that some behaviors may already be addressed through Fault Management.

This means that the verification architecture should not be evaluated by counting only the published contract examples.

A complete assessment would need to examine the combined coverage of:

- Formal contracts.
- Fault-management requirements.
- Software implementation.
- Runtime monitoring.
- Operational response procedures.

The available publications demonstrate the existence of these different mechanisms but do not provide a complete public inventory linking all safety-derived authority rules to their respective assurance mechanisms.

6.4 Runtime Detection and Operational Decision-Making Must Remain Distinct

The role of R2U2 illustrates another important distinction.

A runtime verification mechanism can evaluate observed behavior against specified properties and produce a verdict.

The operational decision that follows a violation belongs to the fault-management architecture.

This separation raises a further traceability consideration.

For a safety-relevant authority boundary, it is not sufficient to establish that a property can be monitored. The relationship between the monitored property and the resulting operational response must also be understood.

For example, a violation could require:

- A local corrective action.
- A request for higher-level coordination.
- A transition to a safe state.
- Suspension of a timeline.
- Another predefined fault-management response.

The reviewed material demonstrates the integration of runtime verification with fault management, but does not establish a complete mapping for every MSM–VSM authority condition.

6.5 The Importance of Documentary Boundaries

The findings also demonstrate why different documentary contexts must remain distinct.

The 2020 discussion of locus of control, the 2023 Gateway AGC work, the MAST research examples, the 2022 Gateway risk-reduction scenarios, and the 2024 refueling development paper do not necessarily describe identical system configurations or operational states.

They provide complementary evidence, but they cannot automatically be combined into a single description of a fully implemented operational architecture.

Likewise, requirements specific to Gateway Logistics Services should not be treated as universal requirements for every Gateway module.

A rigorous assessment must preserve these boundaries.

This study therefore uses each source according to the type of evidence it provides and avoids treating architectural principles, experimental scenarios, system requirements, and operational descriptions as interchangeable.

7. Research Limitations

This study is based on publicly available documentation and is subject to several limitations.

7.1 Access to Detailed Interface Documentation

The complete contents of certain documents relevant to the research question were not available in the reviewed public material.

These include:

- DSG-SPEC-VSM-003.
- The complete MSM Interface Control Document.
- DSG-RQMT-011, concerning Gateway Hazard Analysis Requirements.
- DSG-RPT-001, the System Safety Analysis Report for Gateway.

Their absence from the reviewed public material limits the ability to establish a complete requirement-to-implementation mapping.

It does not establish that the documents are unavailable through other channels or that the information they contain does not exist.

7.2 Difference Between Requirements and Implementation

System requirements establish obligations, but they do not independently demonstrate that a specific implementation satisfies those obligations.

Similarly, architecture descriptions establish intended responsibilities but do not necessarily provide the complete operational logic governing every system interaction.

The study therefore distinguishes between documented requirements, architectural descriptions, and evidence of implementation or verification.

7.3 Experimental and Risk-Reduction Evidence

MAST and Gateway risk-reduction publications provide useful examples of distributed fault management and escalation.

However, they are not treated as comprehensive proof of operational Gateway implementation.

Their contribution is limited to the architectural and experimental behavior explicitly described in the respective publications.

7.4 Module-Specific Requirements

Gateway Logistics Services requirements provide detailed examples of autonomy and safety obligations at the module level.

These requirements cannot be generalized automatically to other Gateway modules.

The study therefore uses them as specific evidence of requirement-level practices rather than as a universal specification for every MSM.

7.5 Incomplete Public Verification Coverage

The published AGC examples do not necessarily represent the complete set of Gateway verification properties.

Because the contract-selection process excludes some behaviors already covered by Fault Management, the available examples cannot be interpreted as an exhaustive inventory.

A complete evaluation would require access to the relevant contract definitions, fault-management specifications, interface requirements, and associated verification evidence.

8. Conclusion

This study examined the relationship between safety assurance and formal verification in NASA Gateway autonomous systems, focusing on the translation of safety-derived local autonomy boundaries into decision and escalation rules at the MSM–VSM interface.

The investigation established several findings.

First, Gateway architecture distributes autonomous management responsibilities across module-level and vehicle-level systems. The VSM provides integrated vehicle-level management, while module-level systems retain responsibilities within their respective domains.

Second, Gateway safety requirements establish that functions necessary for controlling catastrophic hazards must not depend on communication with Earth. Local autonomous capability is therefore connected directly to formal safety obligations.

Third, Gateway documentation describes a distributed fault-management approach in which local systems can perform corrective actions within their responsibilities, while the VSM coordinates conditions that exceed local capabilities or affect broader vehicle operations.

Fourth, Gateway verification publications document the use of Assume-Guarantee Contracts, formal specification methods, model checking, and runtime verification through R2U2. These mechanisms provide a formal basis for expressing and evaluating expected system behavior.

Fifth, the reviewed publications demonstrate that formal contracts and Fault Management have complementary roles. The absence of a particular behavior from published AGC examples cannot be interpreted as evidence that the behavior is absent from the wider assurance architecture.

The principal finding concerns the relationship between these established capabilities.

The reviewed public documentation does not establish a complete traceability chain connecting hazard-derived autonomy boundaries to specific MSM decision and escalation rules and their corresponding formal verification properties.

This finding must be interpreted precisely. It does not demonstrate that NASA lacks the relevant mechanisms, that the rules have not been implemented, or that the operational system is deficient.

It identifies a limitation in what can be established from the public documentary evidence examined in this study.

The distinction is important because the existence of safety requirements and formal verification mechanisms does not, by itself, demonstrate how safety-derived authority boundaries are translated into operational decision rules and verified at system interfaces.

The resulting research direction is therefore specific:

To establish whether the safety-assurance and formal-verification pathways are connected through a demonstrable requirement-to-decision-to-verification traceability relationship at the MSM–VSM interface.

This question provides a focused basis for further examination of Gateway interface specifications, safety analysis artifacts, fault-management definitions, formal contracts, and verification evidence.

The study concludes that the relevant architectural and engineering foundations are documented, while the complete relationship between them remains unresolved within the scope of the publicly reviewed material.

---

References

1. NASA. (2019). Gateway System Requirements. Document DSG-RQMT-001. Relevant requirements: L2-GW-0111, L2-GW-0112, L2-GW-0113, and L2-GW-0199.

2. NASA. Gateway Logistics Services Requirements. Document GLS-RQMT-001. Relevant requirements: L3-GLS-2001, L3-GLS-2004, L3-GLS-2052, L3-GLS-2071, L3-GLS-2075, L3-GLS-2081, and L3-GLS-2131.

3. NASA. (2019). Gateway Logistics Services Safety Data Package. Document GLS-006.

4. When the Eyes Don’t Have It: Autonomous Control of Deep Space Vehicles for Human Spaceflight. (2020).

5. Using Assume-Guarantee Contracts for Operational Verification of Autonomous Spacecraft. (2023).

6. NASA. (2023). Gateway at the Crossroads of Sustainable Lunar Exploration.

7. NASA. (2023). Trustworthy Autonomy for Gateway Vehicle System Manager. Technical presentation.

8. MAST. (2019). Technical publication describing distributed fault management, local self-correction, and vehicle-level coordination.

9. NASA. (2022). Gateway Risk-Reduction documentation. Use Cases 2 and 3.

10. Gateway to the Future: Lessons Learned in Development of the Refueling Systems for NASA’s First Lunar Space Station. (2024). NASA Technical Reports Server, NTRS 20240011961.

11. Implementation of a Stochastic Timeline Validation Tool Integrated With R2U2. (2026).

---

Author Information

Samir Baladi is an interdisciplinary researcher working on autonomous systems, AI, complex systems, and the engineering of decision and governance architectures.

Affiliation: Ronin Institute / Rite of Renaissance
Email: gitdeeper@gmail.com
ORCID: https://orcid.org/0009-0003-8903-0029

Project: NASA-GATEWAY
Project Website: https://nasa-gateway.netlify.app
Zenodo Project Record: https://doi.org/10.5281/zenodo.24559255