# BorderDays social-pain evidence ledger

Research window: 2026-07-20 through 2026-08-19 (inclusive).

This ledger is the claim gate for public pages. A page claim is allowed only when
the row below cites a current, original, publicly readable social discussion whose
visible text supports the paraphrase. No topic reached the required minimum of
three usable recent first-party sources in this window, so no page claim is
currently approved.

| Pain | Source platform | Published | Original URL | Evidence paraphrase | Allowed page claim | Implementation boundary |
| --- | --- | --- | --- | --- | --- | --- |

## Omitted topics

| Topic | Reason omitted |
| --- | --- |
| Schengen 90/180 spreadsheet | Fewer than three usable current original social posts with visible dates and text validating the pain. |
| Schengen future trip calculator | Fewer than three usable current original social posts with visible dates and text validating the pain. |
| Tax residency day tracker spreadsheet | Fewer than three usable current original social posts with visible dates and text validating the pain. |
| Travel tracker privacy no account | Fewer than three usable current original social posts with visible dates and text validating the pain. |

## Implementation boundaries reviewed

The following product capabilities exist, but remain disallowed for public pain
claims until qualifying social evidence is recorded above:

- Explain a rolling 90/180 calculation - `SchengenRuleEngine.swift` and Rules Dashboard output.
- Plan a future stay before booking - Schengen simulation UI and engine tests.
- Keep one manual travel-day ledger - `LedgerStore.swift` and `FileLedgerRepository.swift`.
- Keep travel data on device - local repository and privacy manifest.
- Protect records with app lock - `AppLockStore.swift`.
- Attach proof and create encrypted backups - `AttachmentVault.swift` and `BackupArchiveService.swift`.
- Review US/UK presence rules - `USSubstantialPresenceEngine.swift` and `UKRuleEngines.swift`.
