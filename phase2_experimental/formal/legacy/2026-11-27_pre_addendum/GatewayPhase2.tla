----------------------------- MODULE GatewayPhase2 -----------------------------
(***************************************************************************)
(* Phase II — Research model of MSM–VSM interface.                         *)
(*                                                                           *)
(* NOT a model of NASA's operational Gateway. All parameters frozen at      *)
(* PREREGISTRATION freeze 2026-11-27.                                      *)
(***************************************************************************)
EXTENDS Naturals, Sequences, properties

CONSTANTS MaxCycle, MaxComponents

ASSUME MaxCycle = 20
ASSUME MaxComponents = 4

VARIABLES
    cycle, components_healthy, shared_healthy,
    local_containable, resolved_locally,
    shared_resource_affected, escalated,
    local_recovery_failed, constraint_conflict, local_action,
    comm_lost, safe_mode, consistency, fault_injected

vars == << cycle, components_healthy, shared_healthy, local_containable,
          resolved_locally, shared_resource_affected, escalated,
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
    /\ local_recovery_failed = FALSE
    /\ constraint_conflict = FALSE
    /\ local_action = FALSE
    /\ comm_lost = FALSE
    /\ safe_mode = FALSE
    /\ consistency = TRUE
    /\ fault_injected = FALSE

InjectFault ==
    /\ cycle = 3
    /\ ~fault_injected
    /\ components_healthy # {}
    /\ \E c \in components_healthy :
         components_healthy' = components_healthy \ {c}
    /\ fault_injected' = TRUE
    /\ UNCHANGED << shared_healthy, local_containable, resolved_locally,
                    shared_resource_affected, escalated,
                    local_recovery_failed, constraint_conflict,
                    local_action, comm_lost, safe_mode, consistency, cycle >>

ResolveLocal ==
    /\ fault_injected
    /\ components_healthy # 1..MaxComponents
    /\ local_containable
    /\ ~escalated
    /\ ~safe_mode
    /\ resolved_locally' = TRUE
    /\ components_healthy' = 1..MaxComponents
    /\ UNCHANGED << shared_healthy, local_containable, shared_resource_affected,
                    escalated, local_recovery_failed, constraint_conflict,
                    local_action, comm_lost, safe_mode, consistency,
                    cycle, fault_injected >>

Escalate ==
    /\ fault_injected
    /\ ~local_containable
    /\ ~escalated
    /\ ~safe_mode
    /\ escalated' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected,
                    local_recovery_failed, constraint_conflict,
                    local_action, comm_lost, safe_mode, consistency, fault_injected >>

VSMResolve ==
    /\ escalated
    /\ ~resolved_locally
    /\ shared_healthy' = TRUE
    /\ components_healthy' = 1..MaxComponents
    /\ resolved_locally' = TRUE
    /\ UNCHANGED << cycle, local_containable, shared_resource_affected,
                    escalated, local_recovery_failed, constraint_conflict,
                    local_action, comm_lost, safe_mode, consistency, fault_injected >>

CommLoss ==
    /\ fault_injected
    /\ ~comm_lost
    /\ comm_lost' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    local_recovery_failed, constraint_conflict, local_action,
                    safe_mode, consistency, fault_injected >>

EnterSafeMode ==
    /\ comm_lost
    /\ ~safe_mode
    /\ safe_mode' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    local_recovery_failed, constraint_conflict, local_action,
                    consistency, fault_injected >>

ConstraintConflict ==
    /\ fault_injected
    /\ ~constraint_conflict
    /\ constraint_conflict' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    local_recovery_failed, local_action, comm_lost,
                    safe_mode, consistency, fault_injected >>

KeepConsistent ==
    /\ consistency' = TRUE
    /\ UNCHANGED << cycle, components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    local_recovery_failed, constraint_conflict, local_action,
                    comm_lost, safe_mode, fault_injected >>

Tick ==
    /\ cycle < MaxCycle
    /\ cycle' = cycle + 1
    /\ UNCHANGED << components_healthy, shared_healthy, local_containable,
                    resolved_locally, shared_resource_affected, escalated,
                    local_recovery_failed, constraint_conflict, local_action,
                    comm_lost, safe_mode, consistency, fault_injected >>

Next ==
    \/ InjectFault \/ ResolveLocal \/ Escalate \/ VSMResolve
    \/ CommLoss \/ EnterSafeMode \/ ConstraintConflict
    \/ KeepConsistent \/ Tick

Spec == Init /\ [][Next]_vars

THEOREM Spec => R1
THEOREM Spec => R2
THEOREM Spec => R3
THEOREM Spec => R4
THEOREM Spec => R5
THEOREM Spec => H3_prop
THEOREM Spec => H4_prop

====
