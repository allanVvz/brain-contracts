from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from pydantic import ValidationError

from brain_contracts import BuildHealth, InternalPrincipalClaims


def test_internal_claims_are_strict_and_immutable():
    now = datetime.now(UTC)
    claims = InternalPrincipalClaims(
        subject=uuid4(), role="service", persona_ids=(), service="gateway",
        issued_at=now, expires_at=now + timedelta(seconds=60), nonce="n",
    )
    assert claims.contract_version == "1.0"
    with pytest.raises(ValidationError):
        InternalPrincipalClaims(**claims.model_dump(), injected=True)


def test_health_requires_full_source_sha():
    with pytest.raises(ValidationError):
        BuildHealth(status="ready", service="runtime", source_sha="short",
                    build_digest="sha256:test", schema_version=130,
                    required_schema_version=130)
