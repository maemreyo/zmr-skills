class ExecutionError(RuntimeError):
    pass


class SandboxViolation(ExecutionError):
    pass


class CapabilityTimeout(ExecutionError):
    pass


class OutputHashMismatch(ExecutionError):
    pass


class OutputValidationError(ExecutionError):
    pass
