from __future__ import annotations

from ...protocol.manifest import CapabilityManifest


class CapabilityCatalog:
    def __init__(self, manifests: tuple[CapabilityManifest, ...] = ()) -> None:
        self._manifests = {manifest.capability_id: manifest for manifest in manifests}

    def get(self, capability_id: str) -> CapabilityManifest:
        try:
            return self._manifests[capability_id]
        except KeyError as exc:
            raise KeyError(f"missing capability manifest: {capability_id}") from exc

    def add(self, manifest: CapabilityManifest) -> None:
        if manifest.capability_id in self._manifests:
            raise ValueError(f"duplicate capability: {manifest.capability_id}")
        self._manifests[manifest.capability_id] = manifest
