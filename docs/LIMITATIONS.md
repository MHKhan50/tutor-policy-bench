# Limitations

1. The learner simulator encodes researcher-chosen assumptions about learning, misconception correction, and forgetting.
2. Delayed transfer accuracy is generated from latent simulated mastery; it is not a real post-test score.
3. The benchmark's action set is small and does not model natural-language explanation quality, curriculum alignment, affect, accessibility needs, or classroom context.
4. The rule-based multi-agent policy does not require multiple LLMs and should not be described as an LLM multi-agent system.
5. The optional Ollama policy may return invalid or inconsistent structured actions; the harness validates outputs but does not guarantee pedagogical quality.
6. ASSISTments 2009–2010 is an older dataset and does not contain full action-level hint sequences. Aggregate statistics can inform descriptive parameter ranges but cannot identify causal effects of tutor actions.
7. The benchmark does not establish effectiveness for Pakistani students or for Roman Urdu/Urdu-English code-switching.
8. Human educator review and controlled student studies are necessary for external validity.
9. This release is a general mathematics-tutoring policy benchmark, not a Pakistan-specific curriculum or language benchmark. Local validation would require educator-reviewed curriculum mapping and appropriately governed local learner data.
