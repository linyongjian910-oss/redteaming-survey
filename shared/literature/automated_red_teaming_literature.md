# Automated Red-Teaming Literature Map

Scope: automated red-teaming for generative models, including LLMs, VLMs/MLLMs, text-to-image and text-to-video models, retrieval-augmented applications, and tool-using agents.

Cutoff: 2026-07-11.

This is a structured research map rather than a claim that every paper containing the words ``safety'' or ``jailbreak'' belongs in the survey. The inclusion rule is that a paper contributes to at least one part of the automated red-teaming loop: risk specification, test generation, adversarial search, interaction, outcome judgment, benchmark design, failure triage, or mitigation using red-team traces.

## 1. Surveys and Field-Level Framing

- [Against The Achilles' Heel: A Survey on Red Teaming for Generative Models](https://doi.org/10.1613/jair.1.17654) (JAIR, 2025). The closest broad survey. Use it for the risk taxonomy, search-state/search-goal/search-operation decomposition, evaluation, safeguards, multimodal settings, and application-level red teaming.
- [Security and Privacy Challenges of Large Language Models: A Survey](https://doi.org/10.1145/3712001) (ACM Computing Surveys, 2025). Use it for lifecycle-based security and privacy threats, attack-defense comparisons, and the distinction between model risks and system risks.
- [Red Teaming Large Language Models: A Comprehensive Review and Critical Analysis](https://doi.org/10.1016/j.ipm.2025.104239) (Information Processing & Management, 2025). Use it for a critical comparison of attack types, evaluation methods, and benchmark limitations.
- [Building Safe GenAI Applications: An End-to-End Overview of Red Teaming for Large Language Models](https://aclanthology.org/2025.trustnlp-main.23/) (TrustNLP, 2025). Use it for the practical end-to-end decomposition into attack strategy, evaluator, metrics, infrastructure, and tools.
- [Safety of Multimodal Large Language Models on Images and Text](https://www.ijcai.org/proceedings/2024/0901) (IJCAI Survey Track, 2024). Use it for the evaluation--attack--defense organization in MLLM safety.
- [Red-Teaming for Generative AI: Silver Bullet or Security Theater?](https://www.sei.cmu.edu/library/red-teaming-generative-ai-silver-bullet-security-theater/) (FAccT, 2024). Use it for scope, threat-model, human-participation, and governance questions; it is especially useful for the limitations section.
- [From Attack Surfaces to Actual Operations: A Survey of Modern LLM Jailbreaks](https://aclanthology.org/2026.findings-acl.929/) (Findings of ACL, 2026). Use it as a recent jailbreak-focused complement, not as the main survey structure.
- [Survey on LLM Safety: Attacks, Defenses, Alignment, Metrics, and Guardrails](https://link.springer.com/article/10.1007/s10994-026-07060-8) (Machine Learning, 2026). Use it for recent coverage of threat models, guardrails, metrics, and deployment assumptions.

## 2. Foundational Automated Red-Teaming Systems

- [Red Teaming Language Models with Language Models](https://arxiv.org/abs/2202.03286) (EMNLP, 2022). Foundational LM-as-attacker work; introduces automatic test-case generation, classifier-based judging, diversity control, and multi-turn harm discovery.
- [ASSERT: Automated Safety Scenario Red Teaming for Evaluating the Robustness of Large Language Models](https://arxiv.org/abs/2310.09624) (EMNLP, 2023). Generates semantically aligned, related, and adversarial scenarios; useful for the coverage and robustness subsection.
- [AART: AI-Assisted Red-Teaming with Diverse Data Generation for New LLM-powered Applications](https://arxiv.org/abs/2311.08592) (EMNLP Industry, 2023). Application-conditioned adversarial data generation with explicit concept, cultural, geographic, and scenario diversity.
- [Red-Teaming Large Language Models using Chain of Utterances for Safety-Alignment](https://arxiv.org/abs/2308.09662) (2023). Useful for multi-turn and conversational red-teaming.
- [Holistic Automated Red Teaming for Large Language Models through Top-Down Test Case Generation and Multi-turn Interaction](https://arxiv.org/abs/2409.16783) (EMNLP, 2024). Introduces HARM; useful for top-down risk taxonomies, multi-turn interaction, and the distinction between attack rate and test-case coverage.
- [Learning Diverse Attacks on Large Language Models for Robust Red-Teaming and Safety Tuning](https://arxiv.org/abs/2405.18540) (ICLR, 2025). Uses GFlowNet-based attacker training to reduce attack diversity collapse and connects red-teaming to safety tuning.
- [Diversity Seeking Techniques for Red-Teaming Large Language Models](https://doi.org/10.1109/ICASSP49660.2025.10890844) (ICASSP, 2025). Directly relevant to diversity-aware attacker generation.
- [DiveR-CT: Diversity-enhanced Red Teaming Large Language Model Assistants with Relaxing Constraints](https://doi.org/10.1609/aaai.v39i24.34797) (AAAI, 2025). Useful for constrained red-team generation and diversity-oriented evaluation.
- [Auto-RT: Automatic Jailbreak Strategy Exploration for Red-Teaming Large Language Models](https://arxiv.org/abs/2501.01830) (2025). Relevant to automated discovery of attack strategies rather than only attack prompts.
- [Quality-Diversity Red-Teaming: Automated Generation of High-Quality and Diverse Attackers for Large Language Models](https://arxiv.org/abs/2506.07121) (2025). Relevant to quality-diversity search and attacker population construction.

## 3. Automated Jailbreak Generation and Search

- [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) (2023). Introduces GCG-style gradient-guided adversarial suffix optimization; essential for white-box and transferability discussions.
- [GPTFUZZER: Red Teaming Large Language Models with Auto-Generated Jailbreak Prompts](https://arxiv.org/abs/2309.10253) (2023). Seed selection, mutation operators, and a judgment model; essential for fuzzing-based red teaming.
- [Jailbreaking Black Box Large Language Models in Twenty Queries](https://arxiv.org/abs/2310.08419) (ICLR, 2024). Introduces PAIR, an attacker LLM that iteratively refines semantic jailbreaks under black-box access.
- [AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models](https://arxiv.org/abs/2310.04451) (ICLR, 2024). Hierarchical genetic search for semantically meaningful and stealthy jailbreak prompts.
- [Tree of Attacks: Jailbreaking Black-Box LLMs Automatically](https://arxiv.org/abs/2312.02119) (NeurIPS, 2024). Introduces TAP, a tree-search attacker with pruning and iterative black-box feedback.
- [DeepInception: Hypnotize Large Language Model to Be Jailbreaker](https://arxiv.org/abs/2311.03191) (2023). Relevant to nested, role-based, and multi-step jailbreak generation.
- [A StrongREJECT for Empty Jailbreaks](https://arxiv.org/abs/2402.10260) (NeurIPS Datasets and Benchmarks, 2024). Shows that weak evaluators can overestimate jailbreak effectiveness; essential for the evaluator-validity section.
- [SmoothLLM: Defending Large Language Models Against Jailbreaking Attacks](https://arxiv.org/abs/2310.03684) (TMLR, 2025). Useful as a defense case study and for discussing adaptive attacks against defenses.
- [Defending Large Language Models Against Jailbreaking Attacks Through Goal Prioritization](https://arxiv.org/abs/2311.09096) (ACL, 2024). Useful for linking red-team failures to training-time and inference-time mitigation.

## 4. Benchmarks, Judges, Metrics, and Protocols

- [HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal](https://arxiv.org/abs/2402.04249) (ICML, 2024). Core benchmark for comparing 18 red-teaming methods across 33 target models and defenses; use it as the anchor for standardized evaluation.
- [JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models](https://arxiv.org/abs/2404.01318) (2024). Defines an open artifact repository, 100 behaviors, threat-model metadata, scoring functions, and a leaderboard.
- [SORRY-Bench: Systematically Evaluating Large Language Model Safety Refusal Behaviors](https://arxiv.org/abs/2406.14598) (ICLR, 2025). Uses a fine-grained taxonomy, multilingual and formatting augmentations, human annotations, and judge meta-evaluation.
- [SafetyBench: Evaluating the Safety of Large Language Models](https://arxiv.org/abs/2309.07045) (2023). Broad bilingual safety benchmark; useful as a general safety-evaluation baseline, although it is less attack-search-oriented.
- [XSTest: A Test Suite for Identifying Exaggerated Safety Behaviours in Large Language Models](https://arxiv.org/abs/2308.01263) (NAACL, 2024). Essential for the helpfulness--harmlessness trade-off and false-refusal evaluation.
- [ALERT: A Comprehensive Benchmark for Assessing Large Language Models' Safety through Red Teaming](https://arxiv.org/abs/2404.08676) (2024). Useful for broad safety red-team coverage and risk-category comparison.
- [CoSafe: Evaluating Large Language Model Safety in Multi-Turn Dialogue Coreference](https://arxiv.org/abs/2406.17626) (EMNLP, 2024). Useful for stateful and multi-turn safety evaluation.
- [StrongREJECT](https://strong-reject.readthedocs.io/en/latest/) provides the benchmark implementation and evaluator documentation associated with the StrongREJECT paper.

## 5. Multimodal and Vision-Language Red Teaming

- [MM-SafetyBench: A Benchmark for Safety Evaluation of Multimodal Large Language Models](https://arxiv.org/abs/2311.17600) (2023). Image-based manipulation benchmark with 5,040 text--image pairs across 13 scenarios.
- [Arondight: Red Teaming Large Vision Language Models with Auto-generated Multi-modal Jailbreak Prompts](https://doi.org/10.1145/3664647.3681379) (ACM Multimedia, 2024). Directly relevant to auto-generated multimodal jailbreak prompts.
- [Safety of Multimodal Large Language Models on Images and Text](https://arxiv.org/abs/2402.00357) (IJCAI, 2024). Organizes MLLM safety into evaluation, attack, and defense; use it as the multimodal survey anchor.
- [Red Teaming Multimodal Language Models: Evaluating Harm Across Prompt Modalities and Models](https://arxiv.org/abs/2509.15478) (2025). Useful for comparing text-only and multimodal red-team prompts with human harmfulness judgments.
- [Adversarial Attacks on Multimodal Large Language Models: A Comprehensive Survey](https://arxiv.org/html/2603.27918) (2026). Emerging survey for attack-surface and attacker-objective taxonomies across modalities.

## 6. Text-to-Image, Text-to-Video, and Diffusion Models

- [Adversarial Nibbler: A Data-Centric Challenge for Improving the Safety of Text-to-Image Models](https://arxiv.org/abs/2305.14384) (2023). Early open red-teaming challenge for discovering long-tail and implicitly adversarial T2I harms.
- [Discovering Safety Issues in Text-to-Image Models: Insights from Red Teaming](https://aclanthology.org/2023.artofsafety-1.5/) (Art of Safety, 2023). Useful for human-discovered T2I failure modes and red-team taxonomies.
- [Adversarial Nibbler: An Open Red-Teaming Method for Identifying Diverse Harms in Text-to-Image Generation](https://arxiv.org/abs/2403.12075) (2024). Extends the challenge into a sustained, iterative, human-participatory red-teaming process.
- [ART: Automatic Red-teaming for Text-to-Image Models to Protect Benign Users](https://arxiv.org/abs/2405.19360) (NeurIPS, 2024). Directly relevant to automated T2I red teaming using LLMs, VLMs, and image-aware detection.
- [Automated Red Teaming for Text-to-Image Models](https://tianweiz07.github.io/Papers/25-iccv-1.pdf) (ICCV, 2025). Relevant to iterative automated T2I testing and prompt-level safety-filter evasion.
- [Red-Teaming for Generative AI: Silver Bullet or Security Theater?](https://arxiv.org/abs/2401.15897) (FAccT, 2024). Contains a useful cross-modal review of red teaming for LLMs, MLLMs, and T2I systems.

## 7. Agents, RAG, Tools, and Application-Level Red Teaming

- [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents](https://arxiv.org/abs/2403.02691) (2024). Benchmark for indirect prompt injection, tool use, user harm, and private-data exfiltration.
- [AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents](https://arxiv.org/abs/2406.13352) (NeurIPS, 2024). Dynamic environment with realistic tasks, security test cases, adaptive attacks, and defenses.
- [ToolEmu: Identifying and Mitigating Tool-Execution Risks in Large Language Model Agents](https://arxiv.org/abs/2309.15817) (2023). Useful for tool-use risk modeling and simulator-based agent evaluation.
- [Teams of LLM Agents Can Exploit Zero-Day Vulnerabilities](https://arxiv.org/abs/2406.01637) (2024). Relevant to autonomous attacker teams and the boundary between red teaming and cyber capability evaluation.
- [tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045) (2024). Not a pure red-team benchmark, but useful for realistic tool-agent interaction and policy adherence evaluation.

## 8. Human, Governance, and Responsible Red Teaming

- [Red-Teaming for Generative AI: Silver Bullet or Security Theater?](https://www.sei.cmu.edu/library/red-teaming-generative-ai-silver-bullet-security-theater/) (FAccT, 2024). Use for the distinction between red teaming and generic benchmarking, the role of humans, and operational recommendations.
- [Closing the AI Accountability Gap: Defining an End-to-End Framework for Internal Algorithmic Audit](https://arxiv.org/abs/2001.00973) (FAccT, 2020). Useful for placing automated red teaming in a broader audit lifecycle.
- [Adversarial Nibbler: A Data-Centric Challenge for Improving the Safety of Text-to-Image Models](https://research.google/pubs/adversarial-nibbler-a-data-centric-challenge-for-improving-the-safety-of-text-to-image-models/) (Google Research). Useful for community participation and diverse data collection.
- [Lessons from Red Teaming 100 Generative AI Products](https://download.microsoft.com/download/4/9/6/496deaed-0dab-4e1d-85eb-7489a0f242a6/Lessons%20From%20Red%20Teaming%20100%20Generative%20AI%20Products%20eBook.pdf) (Microsoft, 2025). Practitioner evidence for deployment-oriented red teaming, automation, and the continuing role of human experts.

## 9. Recommended Reading Order for This Survey

1. Read the JAIR survey and the FAccT paper to define scope, terminology, and limitations.
2. Read Perez et al., ASSERT, AART, HARM, and Learning Diverse Attacks to build the automated-red-teaming method taxonomy.
3. Read GCG, GPTFuzzer, PAIR, AutoDAN, and TAP to cover the main automated jailbreak search families.
4. Read HarmBench, JailbreakBench, StrongREJECT, SORRY-Bench, and XSTest to write the evaluation section.
5. Read MM-SafetyBench, Arondight, the IJCAI survey, ART, and Adversarial Nibbler for multimodal and T2I coverage.
6. Read InjecAgent, AgentDojo, and ToolEmu for application-level, RAG, tool, and agent settings.

## 10. Taxonomy to Use in the Manuscript

Each paper should be coded along the following fields:

- target: LLM, VLM/MLLM, T2I, T2V, agent, RAG application, or other generative model;
- risk: harmful compliance, privacy leakage, prompt injection, unsafe tool use, misinformation, bias, copyright, or over-refusal;
- access: black-box, gray-box, white-box, or application-level;
- generation: template, transformation, LLM proposer, fuzzing, evolutionary search, RL/GFlowNet, gradient/token optimization, or multi-agent search;
- interaction: single-turn, iterative, multi-turn, stateful, or long-horizon;
- feedback: lexical rule, classifier, reward model, LLM judge, VLM judge, human annotation, or environment success signal;
- evaluation: attack success, harm severity, coverage, diversity, novelty, transferability, query cost, latency, utility, or false refusal; and
- outcome: benchmark only, attack discovery, safety tuning, guardrail design, regression testing, or deployment audit.

This coding scheme should become the basis for the survey's comparison tables and for the final discussion of gaps. In particular, do not compare attack-success rates across papers unless their target behavior, judge, threat model, query budget, and benchmark are aligned.
