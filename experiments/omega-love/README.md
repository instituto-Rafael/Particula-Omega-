# Partícula Ômega · LOVE/PHONEME · experimental v0

**State:** DESIGN + toy text-only reference implementation. Not a dictionary, TTS/ASR engine, production translation model, or evidence of learning from one word alone.

## Claim boundary

- Initial *selected English token*: `love`. No Portuguese equivalent is supplied to the inducer.
- The provided parallel sentences are **weak cross-lingual supervision**, not two truly independent monolingual corpora.
- We rank Portuguese candidates by sentence-level Dice co-occurrence; this is an *association score*, **not** calibrated confidence or a verified translation.
- At most one selected English seed is queried; the source corpora include numerous words whose meanings are not preloaded.
- Synthetic authored toy text (12 pairs) demonstrates plumbing only. **No real-world generalization**, no massive Portuguese/English lexicon, no learned phonemes, and no audio have been tested.
- No corpus, recording, voice, copyright, consent or personal data is ingested by default. No automatic scrape, network, training, or public claim.

## Reproduce (Python stdlib)

```sh
python3 omega_love.py data/toy_sentence_pairs.jsonl
python3 -m unittest discover -s tests -v
```

Expected on the authored toy corpus: `amor` emerges first for `love` with association Dice 1.0, four co-occurrences. This is not a held-out test.

## Speech layer (DESIGN ONLY, not implemented)

Each observed spoken segment needs an explicit record:
`language, variety, text, IPA, syllable_or_mora, stress, F0/pitch_contour, duration, intensity, voice_quality, source, consent, phonetic_annotation_provenance, uncertainty`.
Never infer voice timbre, accent, emotion, tone or audio authenticity from written text alone. An unmeasured channel is **TOKEN_VAZIO**, not zero.

- Brazilian Portuguese `não` has a nasal diphthong for which American English has no direct phonemic counterpart.
- American English `love` /lʌv/ and Portuguese `amor` /aˈmoɾ/ are semantically related, but not acoustically equivalent.
- English `haircut` can be borrowed as Japanese katakana `ヘアカット` (hea-katto). Japanese `散髪` (sanpatsu) is a *semantic equivalent in kanji*, not a phonetic spelling of American English. Japanese has moraic /N/ and gemination /Q/; it is incorrect to claim Japanese cannot have internal consonant boundaries.
- English `wh` has dialect- and lexical-item-dependent pronunciations. Pronunciation variation must never be used to stereotype a nationality.

## Next falsifiers

1. Freeze independent train/test sentences; ensure word pairs in test labels are never used by induction.
2. Contrast correctly aligned with shuffled English/Portuguese sentences; measure Precision@1, MRR, coverage and abstention.
3. Compare against unigram and frequency-only baselines; evaluate morphologically related words separately.
4. Add opt-in, licensed audio with IPA reference annotations and speaker/session split; evaluate phoneme error rate and prosodic retention independently.
5. Introduce Japanese phonological loanword adaptation as a separate transduction task; test form, writing system and meaning separately.

## Research

- Søgaard et al., ACL 2018, limits of unsupervised bilingual dictionary induction: https://aclanthology.org/P18-1072/
- Vulić et al., EMNLP 2019, fully unsupervised cross-lingual embedding failure cases: https://aclanthology.org/D19-1449/
- alphaXiv prosody comparison: https://www.alphaxiv.org/abs/2608.27848
- alphaXiv phoneme-augmented speech translation: https://www.alphaxiv.org/abs/2505.24691
- IPA charts: https://www.internationalphoneticassociation.org/IPAcharts/IPA_charts_EI/IPA_charts_EI.html

## Security & rollback

This is an **isolated HOLD branch**; main untouched. No secrets, network access, audio, releases, CI workflows, or automations. Delete/close the draft branch/PR to abandon the experiment without affecting the source corpus. Promotion requires fixed-source dataset licenses, adversarial tests, exact-head evidence, and human review.
