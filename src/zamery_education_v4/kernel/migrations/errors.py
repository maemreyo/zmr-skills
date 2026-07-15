class MigrationError(ValueError):
    pass


class UnreportedMigrationLoss(MigrationError):
    pass
