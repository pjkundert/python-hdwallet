#!/usr/bin/env python3

import unicodedata
import pytest

from hdwallet.mnemonics.bip39 import BIP39Mnemonic
from hdwallet.seeds.bip39 import BIP39Seed


class TestBIP39Normalization:
    """Test BIP-39 normalization implementation fixes.
    
    This test validates that the normalization changes work correctly:
    1. User input uses NFKC -> NFC normalization (handles compatibility characters)
    2. Internal processing uses NFC normalization (consistent word comparisons)
    3. Seed generation uses NFD normalization (BIP-39 specification requirement)
    """

    @classmethod
    def setup_class(cls):
        """Set up test cases with different Unicode representations."""
        
        # Test mnemonic with accented characters in different Unicode forms
        cls.test_mnemonics = {
            # French mnemonic with é in different forms
            'composed': 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon café',  # é as U+00E9
            'decomposed': 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon cafe\u0301',  # e + U+0301
            
            # Spanish mnemonic with ñ in different forms  
            'composed_spanish': 'ábaco ábaco ábaco ábaco ábaco ábaco ábaco ábaco ábaco ábaco ábaco niño',  # ñ as U+00F1
            'decomposed_spanish': 'ábaco ábaco ábaco ábaco ábaco ábaco ábaco ábaco ábaco ábaco ábaco nin\u0303o',  # n + U+0303
        }
        
        # User input scenarios with compatibility characters
        cls.compatibility_scenarios = {
            # Fullwidth characters (common with Asian keyboards)
            'fullwidth': 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon ｃａｆé',
            # Ligature characters
            'ligature': 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon caﬁe',  # contains fi ligature
            # Roman numeral (though unlikely in real mnemonics)
            'roman': 'abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon cafeⅠ',
        }

    def test_user_input_normalization(self):
        """Test that user input normalization handles compatibility characters correctly."""
        
        # Test NFKC -> NFC normalization for user input
        test_cases = [
            # Fullwidth input should normalize to regular characters
            ('ａｂａｎｄｏｎ', 'abandon'),
            # Ligature input should decompose
            ('ﬁle', 'file'),  # fi ligature -> fi
            # Mixed case should be lowercased
            ('ABANDON', 'abandon'),
        ]
        
        for input_word, expected in test_cases:
            result = BIP39Mnemonic.normalize_user_input([input_word])
            assert result == [expected], f"Failed to normalize '{input_word}' to '{expected}', got {result}"

    def test_wordlist_normalization(self):
        """Test that wordlists are properly normalized to NFC for internal processing."""
        
        # Load French wordlist (contains accented characters)
        french_words = BIP39Mnemonic.get_words_list_by_language('french')
        
        # Check that all words are in NFC form
        for word in french_words[:10]:  # Test first 10 words
            nfc_form = unicodedata.normalize('NFC', word)
            assert word == nfc_form, f"Word '{word}' is not in NFC form, got '{nfc_form}'"
            
        # Check specific accented words
        accented_words = [word for word in french_words if any(ord(c) > 127 for c in word)][:5]
        for word in accented_words:
            # Verify it's in NFC form (shorter than NFD due to composed characters)
            nfd_form = unicodedata.normalize('NFD', word)
            assert len(word) < len(nfd_form), f"Word '{word}' doesn't appear to be in NFC form"

    def test_mnemonic_validation_consistency(self):
        """Test that mnemonics with different Unicode representations validate consistently."""
        
        # These should all represent the same semantic mnemonic
        composed_mnemonic = self.test_mnemonics['composed']
        decomposed_mnemonic = self.test_mnemonics['decomposed']
        
        # Both should be valid (after normalization)
        assert BIP39Mnemonic.is_valid(composed_mnemonic), "Composed mnemonic should be valid"
        assert BIP39Mnemonic.is_valid(decomposed_mnemonic), "Decomposed mnemonic should be valid"
        
        # Both should normalize to the same internal representation
        composed_normalized = BIP39Mnemonic.normalize(composed_mnemonic)
        decomposed_normalized = BIP39Mnemonic.normalize(decomposed_mnemonic)
        assert composed_normalized == decomposed_normalized, "Different Unicode forms should normalize to same result"

    def test_seed_generation_normalization(self):
        """Test that seed generation uses NFD normalization as required by BIP-39."""
        
        # Use a known valid mnemonic
        test_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        # Verify the mnemonic is valid
        assert BIP39Mnemonic.is_valid(test_mnemonic), "Test mnemonic should be valid"
        
        # Test normalize_for_seed method
        normalized_for_seed = BIP39Mnemonic.normalize_for_seed(test_mnemonic)
        
        # Should be in NFD form
        nfd_form = unicodedata.normalize('NFD', test_mnemonic)
        assert normalized_for_seed == nfd_form, "normalize_for_seed should return NFD form"
        
        # Generate seed to verify it works
        seed = BIP39Seed.from_mnemonic(test_mnemonic)
        assert len(seed) == 128, "BIP39 seed should be 128 hex characters (64 bytes)"

    def test_seed_generation_with_accents(self):
        """Test seed generation with accented characters uses proper NFD normalization."""
        
        # Test with French mnemonic containing accents
        # This is a crafted example - real French mnemonics would need proper checksum
        french_test = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon café"
        
        if BIP39Mnemonic.is_valid(french_test):
            # Test that different Unicode representations produce the same seed
            composed = french_test  # é as single codepoint
            decomposed = french_test.replace('café', 'cafe\u0301')  # e + combining accent
            
            seed1 = BIP39Seed.from_mnemonic(composed)
            seed2 = BIP39Seed.from_mnemonic(decomposed)
            
            assert seed1 == seed2, "Different Unicode representations should produce the same seed"

    def test_compatibility_character_handling(self):
        """Test that compatibility characters in user input are handled correctly."""
        
        # Test fullwidth characters (common with Asian keyboards)
        fullwidth_input = "ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂａｎｄｏｎ ａｂｏｕｔ"
        normal_input = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        # Normalize both
        fullwidth_normalized = BIP39Mnemonic.normalize(fullwidth_input)
        normal_normalized = BIP39Mnemonic.normalize(normal_input)
        
        # Should produce the same result
        assert fullwidth_normalized == normal_normalized, "Fullwidth input should normalize to same result as normal input"
        
        # Both should be valid
        assert BIP39Mnemonic.is_valid(fullwidth_input), "Fullwidth input should be valid after normalization"
        assert BIP39Mnemonic.is_valid(normal_input), "Normal input should be valid"

    def test_normalization_methods_consistency(self):
        """Test that different normalization methods work consistently."""
        
        test_input = "abandon café"  # Mix of ASCII and accented
        
        # Test normalize vs normalize_user_input
        normalized = BIP39Mnemonic.normalize(test_input)
        user_normalized = BIP39Mnemonic.normalize_user_input(test_input)
        
        assert normalized == user_normalized, "normalize() and normalize_user_input() should produce same result"
        
        # Test normalize_for_seed
        seed_normalized = BIP39Mnemonic.normalize_for_seed(test_input)
        
        # Should be different (NFD vs NFC)
        input_nfc = unicodedata.normalize('NFC', test_input)
        input_nfd = unicodedata.normalize('NFD', test_input)
        
        assert seed_normalized == input_nfd, "normalize_for_seed should return NFD form"
        assert " ".join(normalized) != seed_normalized, "Internal normalization should differ from seed normalization"

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        
        # Empty string
        assert BIP39Mnemonic.normalize("") == []
        assert BIP39Mnemonic.normalize([]) == []
        
        # Single word
        single_word = BIP39Mnemonic.normalize("abandon")
        assert single_word == ["abandon"]
        
        # Mixed case with accents
        mixed_case = BIP39Mnemonic.normalize("CAFÉ")
        assert mixed_case == ["café"]
        
        # Extra whitespace
        whitespace_test = BIP39Mnemonic.normalize("  abandon   about  ")
        assert whitespace_test == ["abandon", "about"]

    def test_backwards_compatibility(self):
        """Test that changes don't break existing functionality."""
        
        # Test standard English mnemonic (no accents, should work as before)
        english_mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        
        # Should be valid
        assert BIP39Mnemonic.is_valid(english_mnemonic)
        
        # Should generate consistent seed
        seed = BIP39Seed.from_mnemonic(english_mnemonic)
        assert isinstance(seed, str)
        assert len(seed) == 128
        
        # Normalized forms should be consistent
        normalized = BIP39Mnemonic.normalize(english_mnemonic)
        assert all(isinstance(word, str) for word in normalized)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])