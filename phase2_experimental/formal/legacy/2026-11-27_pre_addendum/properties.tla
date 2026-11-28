----------------------------- MODULE properties -----------------------------
(***************************************************************************)
(* Phase II — Properties corresponding to H5 and the treatment rules.       *)
(*                                                                           *)
(* Each property is the TLA+ translation of a treatment_property in         *)
(* scenarios/S{1..5}.yaml. H5 is falsified if TLC finds any counterexample  *)
(* to any of them within the frozen state space (MAX_COMPONENTS=4,          *)
(* MAX_CYCLES=20, MAX_ESCALATION_DEPTH=2, MAX_MESSAGES_IN_FLIGHT=3).        *)
(*                                                                           *)
(* What H5 establishes: the MODEL satisfies these properties within the    *)
(* frozen bounds. What H5 does NOT establish: that any operational system  *)
(* satisfies them. See PREREGISTRATION.md §7.3 and §12.                    *)
(***************************************************************************)
EXTENDS Naturals, Sequences

VARIABLES
    cycle,
    local_containable,
    resolved_locally,
    shared_resource_affected,
    escalated,
    local_recovery_failed,
    constraint_conflict,
    local_action,
    comm_lost,
    safe_mode,
    consistency

vars == << cycle, local_containable, resolved_locally,
          shared_resource_affected, escalated,
          local_recovery_failed, constraint_conflict,
          local_action, comm_lost, safe_mode, consistency >>

(* R1: fault contained within MSM domain -> eventually resolved locally *)
R1 == [](local_containable => <>(resolved_locally))

(* R2: shared resource affected -> eventually escalated *)
R2 == [](shared_resource_affected => <>(escalated))

(* R3: repeated local recovery failures -> eventually escalated *)
R3 == [](local_recovery_failed => <>(escalated))

(* R4: constraint conflict -> never take the local action *)
R4 == [](constraint_conflict => ~(local_action))

(* R5: communication lost -> eventually safe mode *)
R5 == [](comm_lost => <>(safe_mode))

(* H3: consistency is preserved (no cycle where MSM and VSM disagree) *)
H3_prop == [](consistency)

(* H4 support: if comm is lost, no safety violation is possible. *)
H4_prop == [](comm_lost => ~(local_action))

(* Bounded liveness: every escalation eventually reaches the VSM. *)
BoundedEscalation == [](escalated => <>(~escalated))

====
