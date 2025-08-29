#!/usr/bin/env python3

import os
import random
import unicodedata
from typing import List, Set

import pytest

from hdwallet.mnemonics.bip39 import BIP39Mnemonic


class TestBIP39CrossLanguage:
    """Test BIP39 mnemonics that work in both English and French languages.
    
    This test explores the theoretical possibility of mnemonics that can be validly
    decoded in multiple languages. About 2% (100/2048) of words are common between 
    the English and French BIP-39 wordlists.
    
    For randomly generated entropy uses only common words:
    - Probability for a 12-word mnemonic: (100/2048)^12*1/16  ≈ 1.15*10^-17
    - Probability for a 24-word mnemonic: (100/2048)^24*1/256 ≈ 1.32x10^-34
    
    Most wallets allow abbreviations; only the first few characters of the word need to be entered:
    the words are guaranteed to be unique after entering at least 4 letters (including the word end
    symbol; eg. 'run' 'runway, and 'sea' 'search' 'season' 'seat').

    If we include full words in one language that are abbreviations in the other, the probabilities
    increase:



    These probabilities are astronomically small, so naturally occurring mnemonics
    will essentially never be composed entirely of common words.
    
    This test deliberately constructs mnemonics using only common words,
    then tests what fraction pass checksum validation in both languages:
    - For 12-word mnemonics: ~1/16 (6.25%) due to 4-bit checksum
    - For 24-word mnemonics: ~1/256 (0.39%) due to 8-bit checksum
    
    This demonstrates the theoretical cross-language compatibility while showing
    why it's not a practical security concern for real-world usage.

    For details about BIP-39 word list selection for various languages, see:

    https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md

    Particularly interesting for abbreviations is the fact that any letter with an accent is
    considered equal to the same letter without the accent for entry and word selection.

    """

    @classmethod
    def _load_language_wordlist(cls, language: str) -> tuple[set, list]:
        """Load wordlist for a given language and compute abbreviations.
        
        Args:
            language: Language name (e.g., 'english', 'french'), NFKC normalized to combine characters and accents
            
        Returns:
            Tuple of (words_set, abbreviations_list)
        """
        wordlist_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            f"hdwallet/mnemonics/bip39/wordlist/{language}.txt"
        )
        with open(wordlist_path, "r", encoding="utf-8") as f:
            words = set(unicodedata.normalize("NFKC", word.strip()) for word in f.readlines() if word.strip())

        # All words are unique in 3 or 4 letters
        abbrevs = [
            w[:3] if (w[:3] in words or len(set(aw.startswith(w[:3]) for aw in words)) == 1) else w[:4]
            for w in words
        ]
        
        # Debug print for abbreviation conflicts
        conflicts = {
            ab: set(w for w in words if w.startswith(ab))
            for ab in abbrevs
            if ab not in words and len(set(w for w in words if w.startswith(ab))) > 1
        }
        if conflicts:
            print(f"{language.capitalize()} abbreviation conflicts: {conflicts}")
        
        assert all(ab in words or len(set(w for w in words if w.startswith(ab))) == 1 for ab in abbrevs)
        
        return words, abbrevs

    @classmethod
    def setup_class(cls, languages: list[str] = None):
        """Load wordlists and find common words between specified languages.
        
        Args:
            languages: List of language names to load (defaults to ['english', 'french'])
        """
        if languages is None:
            languages = ['english', 'french']
        
        if len(languages) < 2:
            raise ValueError("At least 2 languages are required for cross-language testing")
        
        # Load all specified languages
        language_data = {}
        for language, words, words_indices in BIP39Mnemonic.all_wordslist_indices():
            language_data[language] = {'words': words, 'abbrevs': words_indices}
            if language not in languages:
                continue
            
            # Set class attributes for backward compatibility
            setattr(cls, f"{lang}_words", language_data[language]['words'])
            setattr(cls, f"{lang}_abbrevs", language_data[language]['abbrevs'])
        
        # Find common words across all languages
        all_word_sets = [data['words'] for data in language_data.values()]
        all_abbrev_lists = [data['abbrevs'] for data in language_data.values()]
        
        cls.common_words = list(set.intersection(*all_word_sets))
        cls.common_abbrevs = list(set.intersection(*[set(abbrevs) for abbrevs in all_abbrev_lists]))
        
        # Print statistics
        for lang, data in language_data.items():
            print(f"{lang.capitalize()} words: {len(data['words'])}")
        
        print(f"Common words found: {len(cls.common_words)}")
        print(f"First 20 common words: {cls.common_words[:20]}")
        print(f"Common abbrevs found: {len(cls.common_abbrevs)}")
        print(f"First 20 common abbrevs: {cls.common_abbrevs[:20]}")

    def create_random_mnemonic_from_common_words(self, word_count: int) -> str:
        """Create a random mnemonic using only common words."""
        if len(self.common_words) < word_count:
            raise ValueError(f"Not enough common words ({len(self.common_words)}) to create {word_count}-word mnemonic")
        
        selected_words = random.choices(self.common_words, k=word_count)
        return selected_words
        return " ".join(selected_words)

    def test_common_words_exist(self):
        """Test that there are common words between English and French wordlists."""
        assert len(self.common_words) > 0, "No common words found between English and French wordlists"

    def dual_language_N_word_mnemonics(self, words=12, expected_rate=1/16, total_attempts=1000):
        """Test N-word mnemonics that work in both English and French."""
        successful_both_languages: List[List[str]] = []
        
        for _ in range(total_attempts):
            try:
                # Generate a random N-word mnemonic from common words
                mnemonic = self.create_random_mnemonic_from_common_words(words)
                
                # Try to decode as both English and French - both must succeed (pass checksum)
                # Note: We expect different entropy values since words have different indices
                entropy_english = BIP39Mnemonic.decode(mnemonic, words_list=self.english_words)
                entropy_french = BIP39Mnemonic.decode(mnemonic, words_list=self.french_words)
                
                # If both decode successfully, the mnemonic is valid in both languages
                successful_both_languages.append(mnemonic)
                print(f"{words}-word common mnemonics {' '.join(mnemonic)!r}")
            
            except Exception as exc:
                # Skip invalid mnemonics (e.g., checksum failures)
                continue
        
        success_rate = len(successful_both_languages) / total_attempts
        
        print(f"{words}-word mnemonics: {len(successful_both_languages)}/{total_attempts} successful ({success_rate:.4f})")
        print(f"Expected rate: ~{expected_rate:.4f}")
        
        # Assert we found at least some successful mnemonics
        assert success_rate > 0, f"No {words}-word mnemonics worked in both languages"

        # The success rate should be roughly around the expected rate, but due to
        # randomness and limited common words, we'll accept a broader range
        tolerance = 0.5  # 50% tolerance due to statistical variance
        assert expected_rate * (1 - tolerance) < success_rate < expected_rate * (1 + tolerance), \
            f"Success rate {success_rate:.4f} not in expected range around {expected_rate:.4f}"
        return successful_both_languages

    def test_cross_language_12_word_mnemonics(self):
        """Test 12-word mnemonics that work in both English and French."""
        candidates = self.dual_language_N_word_mnemonics(words=12, expected_rate=1/16, total_attempts=1000)

        

    def test_cross_language_24_word_mnemonics(self):
        """Test 24-word mnemonics that work in both English and French."""
        candidates = self.dual_language_N_word_mnemonics(words=24, expected_rate=1/256, total_attempts=5000)

    def test_wordlist_properties(self):
        """Test basic properties of the wordlists."""
        # Verify wordlist sizes
        assert len(self.english_words) == 2048, f"English wordlist should have 2048 words, got {len(self.english_words)}"
        assert len(self.french_words) == 2048, f"French wordlist should have 2048 words, got {len(self.french_words)}"
        
        # Verify no duplicates within each wordlist
        assert len(set(self.english_words)) == len(self.english_words), "English wordlist contains duplicates"
        assert len(set(self.french_words)) == len(self.french_words), "French wordlist contains duplicates"
        
        # Verify common words list properties
        assert len(self.common_words) > 0, "No common words found"
        assert len(set(self.common_words)) == len(self.common_words), "Common words list contains duplicates"


if __name__ == "__main__":
    pytest.main([__file__])
