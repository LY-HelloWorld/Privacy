# BorderDays social-pain evidence ledger

Preferred research window: 2026-07-20 through 2026-08-19 (inclusive).

This ledger is the claim gate for public pages. A page claim is allowed only when
the row below cites a current, original, publicly readable social discussion whose
visible text supports the paraphrase. Recent discussion is preferred, not
required. The retained Schengen rows below are older than the preferred window
because each is an accessible original post with visible source text that
directly substantiates the pain, and together they provide five independent
examples. Revisit them when newer evidence is available.

| Pain | Source platform | Published | Original URL | Evidence paraphrase | Allowed page claim | Implementation boundary |
| --- | --- | --- | --- | --- | --- | --- |
| Travelers can struggle to work out how earlier trips affect a proposed summer stay and need a reliable latest legal exit date. | Reddit | 2026-06-02 (older than preferred 30-day window) | https://www.reddit.com/r/SchengenVisa/comments/1tv6rfa/question_about_90180_days_schengen_visa_for_usa/ | A traveler compares a prior Spain trip with a planned July-to-September visit and asks for the last day their spouse may legally stay after conflicting calculator results. | Plan a future stay before booking | Schengen simulation UI and engine tests |
| Travelers need help interpreting a rolling 90/180 count when re-entry dates and remaining allowance are not intuitive. | Reddit | 2026-05-08 (older than preferred 30-day window) | https://www.reddit.com/r/SchengenVisa/comments/1t7g003/reminder_90_in_180_is_a_limit_not_a_guideline/ | The post says people repeatedly try to calculate their exact re-entry date; the discussion distinguishes a current allowance from a possible longer stay as older days leave the window. | Explain a rolling 90/180 calculation | `SchengenRuleEngine.swift` and Rules Dashboard output |
| Travelers can misread a calculator when earlier trips drop out of the rolling 180-day window during a future stay. | Reddit | 2025-11-13 (older than preferred 30-day window) | https://www.reddit.com/r/SchengenVisa/comments/1owbll8/official_schengen_calculator_seems_to_be_wrong/ | A traveler questions a result after two earlier 30-day trips; replies explain that days fall out of the rolling window as a planned stay progresses. | Explain a rolling 90/180 calculation | `SchengenRuleEngine.swift` and Rules Dashboard output |
| Travelers planning a return trip can be unsure whether a stay longer than the allowance shown on entry remains compliant as days are regained. | Reddit | 2026-04-17 (older than preferred 30-day window) | https://www.reddit.com/r/SchengenVisa/comments/1so7y6s/is_this_risky_at_border_control_90180_rule/ | A traveler asks whether to book and later change a return flight because the proposed stay exceeds the days they believe remain at entry. | Plan a future stay before booking | Schengen simulation UI and engine tests |
| Travelers can be confused when a border officer's remaining-day figure seems to conflict with a calculator after a previous Schengen stay. | Reddit | 2025-11-24 (older than preferred 30-day window) | https://www.reddit.com/r/SchengenVisa/comments/1p5h7br/90180_rule_help/ | A traveler asks why an airport showed 16 days rather than a new 90 after time outside Schengen; replies explain the rolling count and future drop-off of earlier days. | Explain a rolling 90/180 calculation | `SchengenRuleEngine.swift` and Rules Dashboard output |

## Omitted topics

| Topic | Reason omitted |
| --- | --- |
| Tax residency day tracker spreadsheet | Fewer than three usable current original social posts with visible dates and text validating the pain. |
| Travel tracker privacy no account | Fewer than three usable current original social posts with visible dates and text validating the pain. |

## Implementation boundaries reviewed

The following product capabilities exist. Only the two Schengen capabilities
represented by retained rows above are allowed for public pain claims; the rest
remain disallowed until qualifying social evidence is recorded above:

- Explain a rolling 90/180 calculation - `SchengenRuleEngine.swift` and Rules Dashboard output.
- Plan a future stay before booking - Schengen simulation UI and engine tests.
- Keep one manual travel-day ledger - `LedgerStore.swift` and `FileLedgerRepository.swift`.
- Keep travel data on device - local repository and privacy manifest.
- Protect records with app lock - `AppLockStore.swift`.
- Attach proof and create encrypted backups - `AttachmentVault.swift` and `BackupArchiveService.swift`.
- Review US/UK presence rules - `USSubstantialPresenceEngine.swift` and `UKRuleEngines.swift`.
