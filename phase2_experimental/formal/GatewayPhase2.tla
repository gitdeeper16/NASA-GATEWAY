----------------------------- MODULE GatewayPhase2 -----------------------------
(***************************************************************************)
(* Phase II — Research model of MSM–VSM interface.                         *)
(*                                                                           *)
(* NOT a model of NASA's operational Gateway. See PREREGISTRATION.md §12. *)
(*                                                                           *)
(* TECHNICAL CORRECTIONS (Addendum 001 §3.4):                              *)
(*  §3.4.1  Properties are temporal; declared PROPERTIES in .cfg.          *)
(*  §3.4.2  FailLocalRecovery and ConstraintConflict added as transitions  *)
(*          so R3 and R4 are not vacuously true.                          *)
(*  §3.4.3  TakeLocalAction added, guarded by ~constraint_conflict, so     *)
(*          H4_prop (comm_lost => ~local_action) is not vacuously true.   *)
(*  §3.4.4  EscalationCompletes replaces BoundedEscalation (in properties).*)
(*  §3.4.5  MaxEscalationDepth and MaxMessagesInFlight are CONSTANTS with *)
(*          ASSUME, and escalation depth is enforced in Next.            *)
(***************************************************************************)
EXTENDS Naturals, Sequences, properties

CONSTANTS MaxCycle, MaxComponents, MaxEscalationDepth, MaxMessagesInFlight

ASSUME MaxCycle = 20
ASSUME MaxComponents = 4
ASSUME MaxEscalationDepth = 2
ASSUME MaxMessagesInFlight = 3

VARIABLES
    cycle,
    components_healthy, shared_healthy,
    local_containable, resolved_locally,
    shared_resource_affected, escalated, escalation_resolved,
    escalation_depth,
    local_recovery_failed,
    constraint_conflict, local_action,
    comm_lost, safe_mode,
    consistency,
    fault_injected

vars == << cycle, components_healthy, shared_healthy,
          local_containable, resolved_locally,
          shared_resource_affected, escalated, escalation_resolved,
          escalation_depth,
          local_recovery_failed, constraint_conflict, local_action,
          comm_lost, safe_mode, consistency, fault_injected >>

Init ==
    /\ cycle = 0
    /\ components_healthy = 1..MaxComponents
    /\ shared_healthy = TRUE
    /\ local_containable = FALSE
    /\ resolved_locally = FALSE
    /\ shared_resource_affected = FALSE
    /\ escalated = FALSE
    /\ escalation_resolved = FALSE
    /\ escalation_depth = 0
    /\ local_recovery_failed = FALSE
    /\ constraint_conflict = FALSE
    /\ local_action = FALSE
    /\ comm_lost = FALSE
    /\ safe_mode = FALSE
    /\ consistency = TRUE
    /\ fault_injected = FALSE

(* --- Fault injection --- *)
InjectFault ==
    /\ cycle = 3
    /\ ~fault_injected
    /\ components_healthy # {}
    /\ \E c \in components_healthy :
         components_healthy' = components_healthy \ {c}
    /\ fault_injected' = TRUE
    /\ UNCHANGED << shared_healthy, local_containable, resolved_locally,
                    shared_resource_affected, escalated, escalation_resolved,
                    escalation_depth, local_recovery_failed, constraint_conflict,
                    local_action, comm_lost, safe_mode, consistency, cycle >>

(* --- R1 path: local resolution --- *)
ResolveLocal ==
    /\ fault_injected
    /\ components_healthy # 1..MaxComponents
    /\ local_containable
    /\ ~escalated
    /\ ~safe_mode
    /\ resolved_locally' = TRUE
    /\ components_healthy' = 1..MaxComponents
    /\ UNCHANGED << shared_healthy, local_containable, shared_resource_affected,
                    escalated, escalation_resolved, escalation_depth,
                    local_recovery_failed, constraint_conflict, local_action,
                    comm_lost, safe_mode, consistency, cycle, fault_injected >>

(* --- R2 path: escalation --- *)
Escalate ==
    /\ fault_injected
    /\ ~local_containable
    /\ ~escalated
    /\ ~safe_mode
    /\ escalation_depth < MaxEscalationDepth
    /\ escalated' = TRUE
    /\ escalation_depth' = escalation_depth + 1
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected,
                    escalation_resolved, local_recovery_failed,
                    constraint_conflict, local_action, comm_lost, safe_mode,
                    consistency, fault_injected >>

(* --- VSM resolution after escalation --- *)
VSMResolve ==
    /\ escalated
    /\ ~escalation_resolved
    /\ shared_healthy' = TRUE
    /\ components_healthy' = 1..MaxComponents
    /\ escalation_resolved' = TRUE
    /\ resolved_locally' = TRUE
    /\ UNCHANGED << cycle, local_containable, shared_resource_affected,
                    escalated, escalation_depth, local_recovery_failed,
                    constraint_conflict, local_action, comm_lost, safe_mode,
                    consistency, fault_injected >>

(* --- R3 path: local recovery failed (Addendum 001 §3.4.2) --- *)
FailLocalRecovery ==
    /\ fault_injected
    /\ ~local_containable
    /\ ~escalated
    /\ ~safe_mode
    /\ local_recovery_failed' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    escalation_resolved, escalation_depth, constraint_conflict,
                    local_action, comm_lost, safe_mode, consistency, fault_injected >>

(* --- R4 path: constraint conflict (Addendum 001 §3.4.2) --- *)
ConstraintConflict ==
    /\ fault_injected
    /\ ~constraint_conflict
    /\ constraint_conflict' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    escalation_resolved, escalation_depth, local_recovery_failed,
                    local_action, comm_lost, safe_mode, consistency, fault_injected >>

(* --- Local action (Addendum 001 §3.4.3): enabled ONLY when NOT in conflict --- *)
TakeLocalAction ==
    /\ constraint_conflict = FALSE
    /\ ~safe_mode
    /\ local_action' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    escalation_resolved, escalation_depth, local_recovery_failed,
                    constraint_conflict, comm_lost, consistency, fault_injected >>

(* --- R5 path: comm loss --- *)
CommLoss ==
    /\ fault_injected
    /\ ~comm_lost
    /\ comm_lost' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    escalation_resolved, escalation_depth, local_recovery_failed,
                    constraint_conflict, local_action, safe_mode, consistency,
                    fault_injected >>

EnterSafeMode ==
    /\ comm_lost
    /\ ~safe_mode
    /\ safe_mode' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    escalation_resolved, escalation_depth, local_recovery_failed,
                    constraint_conflict, local_action, consistency, fault_injected >>

KeepConsistent ==
    /\ consistency' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    escalation_resolved, escalation_depth, local_recovery_failed,
                    constraint_conflict, local_action, comm_lost, safe_mode,
                    fault_injected >>

Tick ==
    /\ cycle < MaxCycle
    /\ cycle' = cycle + 1
    /\ UNCHANGED << components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    escalation_resolved, escalation_depth, local_recovery_failed,
                    constraint_conflict, local_action, comm_lost, safe_mode,
                    consistency, fault_injected >>

Next ==
    \/ InjectFault \/ ResolveLocal \/ Escalate \/ VSMResolve
    \/ FailLocalRecovery \/ ConstraintConflict \/ TakeLocalAction
    \/ CommLoss \/ EnterSafeMode \/ KeepConsistent \/ Tick

Spec == Init /\ [][Next]_vars

THEOREM Spec => R1
THEOREM Spec => R2
THEOREM Spec => R3
THEOREM Spec => R4
THEOREM Spec => R5
THEOREM Spec => H3_prop
THEOREM Spec => H4_prop
THEOREM Spec => EscalationCompletes

====
