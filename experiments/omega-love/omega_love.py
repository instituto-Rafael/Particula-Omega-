#!/usr/bin/env python3
"""OMEGA LOVE: experimental bilingual word hypotheses from sentence-aligned data.

Pure Python stdlib, no lexicon, no audio claims, no automatic scientific promotion.
The only initially selected English item is "love"; target word is NOT preloaded.
"""
import argparse
from collections import Counter
import json
import re
import unicodedata
from pathlib import Path

WORD = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)
TOKEN_VAZIO = "TOKEN_VAZIO"

def tokens(text):
    return set(WORD.findall(unicodedata.normalize("NFC", text).casefold()))

def read_pairs(path):
    pairs = []
    with open(path, encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            record = json.loads(line)
            if not isinstance(record.get("en"), str) or not isinstance(record.get("pt"), str):
                raise ValueError("line %d lacks en/pt text" % line_number)
            pairs.append((tokens(record["en"]), tokens(record["pt"])))
    if not pairs:
        raise ValueError("parallel sentences required; a word alone is not sufficient")
    return pairs

def candidates(pairs, source="love", minimum_joint=2):
    """Dice sentence co-occurrence, not an unconditional translation probability."""
    en_frequency, pt_frequency, joint = Counter(), Counter(), Counter()
    for english, portuguese in pairs:
        en_frequency.update(english)
        pt_frequency.update(portuguese)
        if source in english:
            joint.update(portuguese)
    ranked = []
    for target, overlap in joint.items():
        if overlap < minimum_joint:
            continue
        denominator = en_frequency[source] + pt_frequency[target]
        score = (2.0 * overlap / denominator) if denominator else 0.0
        ranked.append({"pt_candidate": target, "association_dice": round(score, 6),
                       "cooccurring_sentences": overlap, "en_sentences": en_frequency[source],
                       "pt_sentences": pt_frequency[target]})
    return sorted(ranked, key=lambda x: (-x["association_dice"],
                                         -x["cooccurring_sentences"],
                                         x["pt_candidate"]))

def report(pairs, seed):
    return {
        "status": "EXPERIMENTAL_CANDIDATES_NOT_VERIFIED_TRANSLATIONS",
        "seed_en": seed,
        "known_target_translation_at_start": TOKEN_VAZIO,
        "observed_parallel_sentence_pairs": len(pairs),
        "crosslingual_signal": "sentence_alignment_is_weak_supervision",
        "phoneme_inventory": TOKEN_VAZIO,
        "acoustic_signal": TOKEN_VAZIO,
        "prosody": TOKEN_VAZIO,
        "voice_timbre": TOKEN_VAZIO,
        "japanese_transliteration": TOKEN_VAZIO,
        "claims_allowed": False,
        "candidates": candidates(pairs, seed)
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parallel_jsonl", type=Path)
    parser.add_argument("--seed", default="love")
    args = parser.parse_args()
    print(json.dumps(report(read_pairs(args.parallel_jsonl), args.seed),
                     ensure_ascii=False, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
