+++
Title = "Why timing matters"
SequenceNumber = 10
+++

Time-locked averaging methods such as ERPs and ERFs rely on events being sampled
accurately. In a typical setup, your stimulus software sends markers ("triggers") that are
meant to coincide with the events you care about — but the stimulus itself arrives later,
and by a variable amount.

Many parts of the stack introduce **unknown and variable delays**:

- Stimulus software and the operating system
- Monitor refresh rate
- Graphics cards
- Sound cards

Existing solutions don't make this easy to measure. Dedicated commercial toolkits retail for
around **$2000–3000**, vendor-specific single-modality sensors run ~$300 and still require
calibration, and most of this hardware is **proprietary and closed-source** — making it hard
to replicate or compare results between labs.
