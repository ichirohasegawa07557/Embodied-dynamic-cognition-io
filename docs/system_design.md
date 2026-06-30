# System Design

## Concept

The system is a closed-loop input-output device.

```text
external space
→ sensor input
→ internal state estimation
→ action selection
→ actuator output
→ external response
→ new sensor input
```

The key point is that output is not the end of the process.  
Output changes the surrounding space, and that change returns as the next input.

## Modules

### Sensor Layer

Reads external state.

### State Estimator

Maintains internal memory:

```text
observed distance
estimated distance
predicted next distance
prediction error
target error
```

### Controller

Converts internal state into an action command.

### External Space

In simulation, the external space has inertia, disturbance, and actuator response.  
In hardware, the physical environment responds to servo/LED output.
