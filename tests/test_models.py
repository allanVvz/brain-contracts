from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from pydantic import ValidationError

from brain_contracts import (
    BuildHealth,
    ConversationObservation,
    InternalPrincipalClaims,
)


def test_internal_claims_are_strict_and_immutable():
    now = datetime.now(UTC)
    claims = InternalPrincipalClaims(
        subject=uuid4(), role="service", persona_ids=(), service="gateway",
        issued_at=now, expires_at=now + timedelta(seconds=60), nonce="n",
    )
    assert claims.contract_version == "1.1"
    with pytest.raises(ValidationError):
        InternalPrincipalClaims(**claims.model_dump(), injected=True)


def test_health_requires_full_source_sha():
    with pytest.raises(ValidationError):
        BuildHealth(status="ready", service="runtime", source_sha="short",
                    build_digest="sha256:test", schema_version=130,
                    required_schema_version=130)


def test_conversation_observation_11_is_additive_and_records_real_usage():
    observation = ConversationObservation(
        inbound_id="inbound-1",
        lead_ref="174",
        publication_id=uuid4(),
        finish_reason="length",
        output_truncated=True,
        provider_failure_class="length",
        asked_field_keys=("retail_need",),
        prompt_context_manifest={"retained_chunk_count": 8},
        prompt_tokens=8421,
        completion_tokens=1200,
        total_tokens=9621,
        removed_context=("recent_messages:2", "rag_chunks:2"),
        attempt=2,
    )

    assert observation.contract_version == "1.1"
    assert observation.total_tokens == 9621
    assert observation.asked_field_keys == ("retail_need",)


def test_conversation_observation_10_remains_readable_during_blue_green():
    observation = ConversationObservation(
        contract_version="1.0",
        inbound_id="inbound-old",
        lead_ref="175",
        publication_id=uuid4(),
    )

    assert observation.contract_version == "1.0"
    assert observation.attempt == 1
    assert observation.asked_field_keys == ()
