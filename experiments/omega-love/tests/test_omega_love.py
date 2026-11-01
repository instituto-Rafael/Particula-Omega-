"""Falsifiers for Omega's tiny demonstrator, not a large-scale validation."""
import sys
from pathlib import Path
import unittest
import tempfile
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from omega_love import candidates, read_pairs, report, tokens, TOKEN_VAZIO

DATA = ROOT / "data" / "toy_sentence_pairs.jsonl"

class OmegaLoveTest(unittest.TestCase):
    def test_only_seed_has_no_inferable_translation(self):
        self.assertEqual(candidates([({"love"}, set())], "love"), [])

    def test_toy_seed_recovers_candidate_without_dictionary(self):
        pairs = read_pairs(DATA)
        ranked = candidates(pairs, "love")
        self.assertEqual(ranked[0]["pt_candidate"], "amor")
        self.assertEqual(ranked[0]["association_dice"], 1.0)
        self.assertEqual(ranked[0]["cooccurring_sentences"], 4)

    def test_unsupported_seed_is_unresolved(self):
        self.assertEqual(candidates(read_pairs(DATA), "moon"), [])

    def test_unicode_normalization(self):
        self.assertEqual(tokens("NÃO, AMOR!"), {"não", "amor"})

    def test_no_audio_or_japanese_claim_from_text(self):
        output = report(read_pairs(DATA), "love")
        for name in ["acoustic_signal", "phoneme_inventory", "prosody",
                     "voice_timbre", "japanese_transliteration"]:
            self.assertEqual(output[name], TOKEN_VAZIO)
        self.assertFalse(output["claims_allowed"])

    def test_no_parallel_lines_is_invalid(self):
        with tempfile.TemporaryDirectory() as d:
            empty = Path(d) / "empty.jsonl"
            empty.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_pairs(empty)

if __name__ == "__main__":
    unittest.main()
