package com.geospeed.partner.service;

import static org.assertj.core.api.Assertions.assertThat;

import com.geospeed.partner.dto.TriageIssueRequest;
import com.geospeed.partner.repository.PartnerRepository;
import org.junit.jupiter.api.Test;

class PartnerServiceTest {
    @Test
    void launchReadinessReflectsOpenBlockers() {
        PartnerService service = new PartnerService(new PartnerRepository());

        var readiness = service.launchReadiness();

        assertThat(readiness.launchReady()).isFalse();
        assertThat(readiness.openBlockerCount()).isEqualTo(1);
    }

    @Test
    void triageIssueUpdatesOwnerAndStatus() {
        PartnerService service = new PartnerService(new PartnerRepository());

        var updated = service.triageIssue("pi-001", new TriageIssueRequest("triage", "ADAS Integrations", "vehicle_signal_mapping"));

        assertThat(updated.status()).isEqualTo("triage");
        assertThat(updated.ownerTeam()).isEqualTo("ADAS Integrations");
    }
}

