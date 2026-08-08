# KAG Mark Corpus Index (UNION — never replace)

Agents RAG over this list + graph. Ingest is additive.

| Role | File |
|------|------|
| kag_mark_doctrine | `agent_constitution.md` |
| kag_mark_doctrine | `CHANGELOG.md` |
| kag_mark_doctrine | `GOAL_LEARN_TO_LEARN.md` |
| kag_mark_doctrine | `GOAL_REASON_TEACHER.md` |
| kag_mark_doctrine | `GROK_CLI_KAG_EVOLVE_ALL_AGENTS.md` |
| kag_mark_doctrine | `GROK_CLI_ONE_PROMPT.md` |
| kag_mark_doctrine | `GROK_CLI_TEACHER3_STANDALONE.md` |
| kag_mark_doctrine | `logical_forms.md` |
| kag_mark_doctrine | `MERGE_AND_PRESERVE.md` |
| kag_mark_doctrine | `novel_indicator_protocol.md` |
| kag_mark_doctrine | `obs_feel_spec.md` |
| kag_mark_doctrine | `PRINCIPLES_LEARNING.md` |
| kag_mark_doctrine | `README.md` |
| kag_mark_doctrine | `SPACE_KAG_MODE.md` |
| kag_mark_doctrine | `teach_to_meta_rl.md` |
| kag_mark_doctrine | `schema.yaml` |
| kag_mark_doctrine | `seed_triples.jsonl` |
| basic_knowledge | `00_INDEX.md` |
| basic_knowledge | `pt1__basic_knowledge.txt` |
| basic_knowledge | `pt2__basic_knowledge.txt` |
| basic_knowledge | `pt3__basic_knowledge.txt` |
| basic_knowledge | `pt4__basic_knowledge.txt` |
| basic_knowledge | `pt5__basic_knowledge.txt` |
| basic_knowledge | `SOUL_FINGERPRINT.json` |
| basic_knowledge_root | `all llm's have to know this is the most basic knowledge - Copy.txt` |
| basic_knowledge_root | `all llm's have to know this is the most basic knowledge pt2 - Copy.txt` |
| basic_knowledge_root | `all llm's have to know this is the most basic knowledge pt3 - Copy.txt` |
| basic_knowledge_root | `all llm's have to know this is the most basic knowledge pt5 - Copy.txt` |

## Hook for OpenSPG/KAG

1. Load `kag_mark_doctrine/schema.yaml` (merge entity types, keep v1.0).
2. Ingest `seed_triples.jsonl` append-only (dedupe SPO).
3. Index markdown wiki + basic knowledge pt1–pt5.
4. Teacher agents query logical forms; emit `mark.teacher.lesson.v1`.
5. Student: BC + aux heads + shaped rewards (see `markos_core.kag_mark`).

**Graph store:** `C:/Users/user/OneDrive/Desktop/ARMY/01_SYSTEM/data/knowledge/army/KAG_GRAPH__mark_doctrine.json`
**Pack root:** `C:/Users/user/OneDrive/Desktop/ARMY/kag_mark_doctrine`

- **PLAYBOOK_50D_MARK_MATCH** � recreate 35/50 pack-safe learn-to-learn (kag_mark_doctrine/PLAYBOOK_50D_MARK_MATCH.md + pack_50d_bridge/RECREATE_50D__*)

