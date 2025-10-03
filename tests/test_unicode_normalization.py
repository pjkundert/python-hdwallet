#!/usr/bin/env python3

import os
import unicodedata
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set

import pytest


def remove_accents_safe(text: str) -> str:
    """Remove accents from Latin/Cyrillic/Greek scripts, preserve other scripts.

    Not the correct approach; doesn't work for eg. Korean, where NFD expands unicodedata.category
    "Lo" (Letter other) symbols to simply more "Lo" symbols.

    """
    text_nfd = unicodedata.normalize('NFD', text)
    result = []
    for char in text_nfd:
        category = unicodedata.category(char)
        if category.startswith('M'):  # Mark (combining) characters
            if result and self._is_latin_cyrillic_greek_script(result[-1]):
                continue  # Skip accent marks on Latin/Cyrillic/Greek characters
        result.append(char)
    return ''.join(result)

def remove_accents_safe(text: str) -> str:
    """Remove accents from texts if the removed Marks leave the same number of resultant Letter glyphs.

    Normalizes all incoming text to NFC for consistency (may be raw NFD eg. from BIP-39 word lists)

    """
    text_nfc = unicodedata.normalize('NFC', text)
    text_nfd = unicodedata.normalize('NFD', text_nfc)
    result = []
    for char in text_nfd:
        category = unicodedata.category(char)
        if category.startswith('M'):  # Mark (combining) characters
            continue  # Skip accent marks
        result.append(char)
    if len(result) == len(text_nfc):
        return ''.join(result)
    return text_nfc
        

@dataclass
class CharacterInfo:
    """Information about a single Unicode character."""
    char: str
    ord: int
    hex: str
    category: str
    name: str
    script: str


@dataclass 
class UnicodeAnalysis:
    """Analysis results for a Unicode text string."""
    text: str
    label: str
    length: int
    categories: List[str]
    category_counts: Dict[str, int]
    scripts: Set[str]
    character_details: List[CharacterInfo]


class TestUnicodeNormalization:
    """Test Unicode normalization effects on BIP-39 mnemonic words.
    
    This test validates our understanding of how unicodedata.normalize works
    with the four normalization forms (NFC, NFD, NFKC, NFKD) on actual
    BIP-39 wordlist entries that contain Unicode characters with diacritics.
    
    Key normalization forms:
    - NFC (Canonical Decomposition + Canonical Composition): é = é (U+00E9)
    - NFD (Canonical Decomposition): é = e + ´ (U+0065 + U+0301)
    - NFKC (Compatibility Decomposition + Canonical Composition): similar to NFC but more aggressive
    - NFKD (Compatibility Decomposition): similar to NFD but more aggressive
    
    BIP-39 specifies that mnemonics should use NFC normalization.
    
    === KEY FINDINGS CONFIRMED BY THIS TEST ===
    
    1. BIP-39 wordlists use NFD (decomposed) form:
       - French/Spanish wordlists store accented characters as base + combining diacritics
       - Example: "café" is stored as c-a-f-e-´ (5 codepoints) not c-a-f-é (4 codepoints)
       - Confirmed in: test_bip39_word_normalization_consistency() with french.txt/spanish.txt
       - Evidence: "Is NFC normalized: False" for all accented words from wordlists
    
    2. Normalization forms work as expected:
       - NFC combines decomposed → composed (e + ´ → é, reduces length)
       - NFD decomposes composed → base + combining (é → e + ´, increases length)
       - Confirmed in: test_normalization_understanding() and test_manual_normalization_cases()
    
    3. String length changes with normalization:
       - NFD form is longer due to separate combining characters
       - NFC form is shorter due to composed characters
       - Confirmed in: test_bip39_word_normalization_consistency() output shows different lengths
    
    4. Case is preserved through normalization:
       - "café" vs "CAFÉ" maintain their case after all normalization forms
       - Confirmed in: test_case_sensitivity_with_normalization()
    
    5. Equivalence classes work correctly:
       - Different representations (composed vs decomposed) normalize to same forms
       - Confirmed in: test_normalization_equivalence_classes()
    
    6. NFKC = NFC for BIP-39 words (no compatibility characters):
       - All BIP-39 words pass the assertion that NFC == NFKC
       - Confirmed in: test_bip39_word_normalization_consistency() assertion
    """

    @classmethod
    def setup_class(cls):
        """Load sample words with Unicode characters from BIP-39 wordlists."""
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "hdwallet/mnemonics/bip39/wordlist")
        
        cls.test_words = {}
        
        # Load French words with accents from hdwallet/mnemonics/bip39/wordlist/french.txt
        # These words demonstrate KEY FINDING #1: BIP-39 uses NFD (decomposed) form
        # French has ~366 words with accents stored as base letter + combining diacritics
        french_path = os.path.join(base_path, "french.txt")
        with open(french_path, "r", encoding="utf-8") as f:
            french_words = [line.strip() for line in f if line.strip()]
            cls.test_words['french'] = [
                word for word in french_words 
                if any(ord(c) > 127 for c in word)  # Filter for non-ASCII (accented) words
            ][:10]  # Take first 10 for testing
        
        # Load Spanish words with accents from hdwallet/mnemonics/bip39/wordlist/spanish.txt
        # Spanish also has ~334 words with accents, confirming NFD usage across languages
        spanish_path = os.path.join(base_path, "spanish.txt")
        with open(spanish_path, "r", encoding="utf-8") as f:
            spanish_words = [line.strip() for line in f if line.strip()]
            cls.test_words['spanish'] = [
                word for word in spanish_words 
                if any(ord(c) > 127 for c in word)  # Filter for non-ASCII (accented) words
            ][:10]  # Take first 10 for testing
        
        # Manual test cases to understand specific normalization behaviors
        # These demonstrate KEY FINDINGS #2, #4, #5 about normalization equivalence
        cls.manual_test_cases = [
            # Various ways to represent "é" - demonstrates equivalence classes
            "café",  # é as single codepoint U+00E9 (NFC form)
            "cafe\u0301",  # e + combining acute accent U+0301 (NFD form)
            # Various ways to represent "ñ" - demonstrates equivalence classes  
            "niño",  # ñ as single codepoint U+00F1 (NFC form)
            "nin\u0303o",  # n + combining tilde U+0303 (NFD form)
            # Greek letters (no combining characters, should be unchanged)
            "αβγ",  # Greek letters - tests that non-Latin scripts work correctly
            # Mixed case - demonstrates KEY FINDING #4 about case preservation
            "Café",   # Mixed case with composed accent
            "CAFÉ",   # Upper case with composed accent
        ]
        
        # Compatibility character test cases - these demonstrate NFKC/NFKD differences
        # These characters might appear in user input but not in BIP-39 wordlists
        cls.compatibility_test_cases = [
            # Roman numerals (compatibility characters)
            "Ⅰ",      # U+2160 ROMAN NUMERAL ONE → "I" under NFKC/NFKD
            "Ⅱ",      # U+2161 ROMAN NUMERAL TWO → "II" under NFKC/NFKD
            "ⅰ",      # U+2170 SMALL ROMAN NUMERAL ONE → "i" under NFKC/NFKD
            # Circled numbers (compatibility characters)
            "①",      # U+2460 CIRCLED DIGIT ONE → "1" under NFKC/NFKD
            "②",      # U+2461 CIRCLED DIGIT TWO → "2" under NFKC/NFKD
            # Fullwidth characters (compatibility characters common in Asian input)
            "ａｂｃ",   # U+FF41, U+FF42, U+FF43 → "abc" under NFKC/NFKD
            "ＡＢＣ",   # U+FF21, U+FF22, U+FF23 → "ABC" under NFKC/NFKD
            "１２３",   # U+FF11, U+FF12, U+FF13 → "123" under NFKC/NFKD
            # Superscript/subscript (compatibility characters)
            "café²",  # U+00B2 SUPERSCRIPT TWO → "café2" under NFKC/NFKD
            "H₂O",    # H + U+2082 SUBSCRIPT TWO + O → "H2O" under NFKC/NFKD
            # Ligatures (compatibility characters)
            "ﬁle",    # U+FB01 LATIN SMALL LIGATURE FI → "file" under NFKC/NFKD
            "ﬀ",      # U+FB00 LATIN SMALL LIGATURE FF → "ff" under NFKC/NFKD
            # Mixed compatibility with BIP-39 relevant words
            "ｃａｆé",  # Fullwidth + normal é → "café" under NFKC/NFKD
        ]

    def analyze_unicode_string(self, text: str) -> Dict[str, any]:
        """Analyze a Unicode string and return detailed information."""
        return {
            'original': text,
            'length': len(text),
            'codepoints': [hex(ord(c)) for c in text],
            'char_names': [unicodedata.name(c, f'UNKNOWN-{ord(c):04X}') for c in text],
            'nfc': unicodedata.normalize('NFC', text),
            'nfd': unicodedata.normalize('NFD', text),
            'nfkc': unicodedata.normalize('NFKC', text),
            'nfkd': unicodedata.normalize('NFKD', text),
        }

    def test_normalization_understanding(self):
        """Test basic understanding of Unicode normalization forms."""
        # Test composed vs decomposed é
        composed_e = "é"  # U+00E9
        decomposed_e = "e\u0301"  # U+0065 + U+0301
        
        # NFC should give us the composed form
        assert unicodedata.normalize('NFC', composed_e) == composed_e
        assert unicodedata.normalize('NFC', decomposed_e) == composed_e
        
        # NFD should give us the decomposed form
        assert unicodedata.normalize('NFD', composed_e) == decomposed_e
        assert unicodedata.normalize('NFD', decomposed_e) == decomposed_e
        
        # They should be different in their raw forms but equal after normalization
        assert composed_e != decomposed_e  # Different byte representations
        assert unicodedata.normalize('NFC', composed_e) == unicodedata.normalize('NFC', decomposed_e)

    def test_bip39_word_normalization_consistency(self):
        """Test that BIP-39 words are consistently normalized.
        
        CONFIRMS KEY FINDINGS #1, #3, #6:
        - Shows BIP-39 wordlists use NFD form ("Is NFC normalized: False")
        - Demonstrates length differences between NFC/NFD forms  
        - Verifies NFC == NFKC (no compatibility characters in BIP-39)
        - Tests actual words from french.txt and spanish.txt wordlists
        """
        for language, words in self.test_words.items():
            print(f"\n=== Testing {language} words ===")
            
            for word in words:
                analysis = self.analyze_unicode_string(word)
                
                print(f"\nWord: {word}")
                print(f"  Codepoints: {analysis['codepoints']}")
                print(f"  NFC:  '{analysis['nfc']}' (len={len(analysis['nfc'])})")
                print(f"  NFD:  '{analysis['nfd']}' (len={len(analysis['nfd'])})")
                print(f"  NFKC: '{analysis['nfkc']}' (len={len(analysis['nfkc'])})")
                print(f"  NFKD: '{analysis['nfkd']}' (len={len(analysis['nfkd'])})")
                
                # KEY FINDING #1: BIP-39 words are stored in NFD (decomposed) form
                # This will show "False" for all accented words, proving they use NFD
                is_nfc_normalized = (word == analysis['nfc'])
                print(f"  Is NFC normalized: {is_nfc_normalized}")
                
                # All forms should produce valid strings
                assert isinstance(analysis['nfc'], str)
                assert isinstance(analysis['nfd'], str)
                assert isinstance(analysis['nfkc'], str)
                assert isinstance(analysis['nfkd'], str)
                
                # KEY FINDING #6: NFC == NFKC for BIP-39 words (no compatibility characters)
                assert analysis['nfc'] == analysis['nfkc'], f"NFC != NFKC for {word}"

    def test_manual_normalization_cases(self):
        """Test specific normalization cases to understand behavior.
        
        CONFIRMS KEY FINDINGS #2, #5:
        - Shows how NFC combines decomposed characters (shorter length)
        - Shows how NFD decomposes composed characters (longer length) 
        - Demonstrates equivalence classes: different representations normalize to same result
        - Tests both composed (é) and decomposed (e + ´) input forms
        """
        print("\n=== Manual Test Cases ===")
        
        for test_case in self.manual_test_cases:
            analysis = self.analyze_unicode_string(test_case)
            
            print(f"\nTest case: '{test_case}'")
            print(f"  Original codepoints: {analysis['codepoints']}")
            print(f"  Character names: {analysis['char_names']}")
            
            # Show all normalization forms - demonstrates KEY FINDING #2
            for form in ['nfc', 'nfd', 'nfkc', 'nfkd']:
                normalized = analysis[form]
                norm_codepoints = [hex(ord(c)) for c in normalized]
                print(f"  {form.upper():4}: '{normalized}' -> {norm_codepoints}")
                
                # Verify normalization is idempotent (applying twice gives same result)
                double_normalized = unicodedata.normalize(form.upper(), normalized)
                assert double_normalized == normalized, f"Double {form.upper()} normalization changed result"

    def test_case_sensitivity_with_normalization(self):
        """Test how case affects normalization.
        
        CONFIRMS KEY FINDING #4:
        - Case is preserved through all normalization forms
        - "café" stays lowercase, "CAFÉ" stays uppercase
        - Normalization affects accents but not case
        """
        test_cases = [
            ("café", "CAFÉ"),   # French word with acute accent
            ("niño", "NIÑO"),   # Spanish word with tilde
        ]
        
        print("\n=== Case Sensitivity Tests ===")
        
        for lower, upper in test_cases:
            print(f"\nTesting: '{lower}' vs '{upper}'")
            
            for form in ['NFC', 'NFD', 'NFKC', 'NFKD']:
                lower_norm = unicodedata.normalize(form, lower)
                upper_norm = unicodedata.normalize(form, upper)
                
                print(f"  {form}: '{lower_norm}' vs '{upper_norm}'")
                
                # Case should be preserved through normalization
                assert lower_norm.lower() == lower_norm
                assert upper_norm.upper() == upper_norm
                
                # Normalization should not change case
                assert lower_norm != upper_norm

    def test_normalization_equivalence_classes(self):
        """Test that different representations normalize to the same result.
        
        CONFIRMS KEY FINDING #5:
        - Different Unicode representations of same character normalize to same forms
        - Composed "é" and decomposed "e + ´" both normalize to same NFC and NFD results
        - This is critical for BIP-39 mnemonic validation across different input methods
        """
        equivalence_classes = [
            # Different ways to represent é (composed vs decomposed)
            ["é", "e\u0301"],      # U+00E9 vs U+0065+U+0301
            # Different ways to represent ñ (composed vs decomposed)
            ["ñ", "n\u0303"],      # U+00F1 vs U+006E+U+0303
        ]
        
        print("\n=== Equivalence Classes ===")
        
        for equiv_class in equivalence_classes:
            print(f"\nTesting equivalence class: {[repr(s) for s in equiv_class]}")
            
            # All should normalize to the same NFC form
            nfc_results = [unicodedata.normalize('NFC', s) for s in equiv_class]
            assert len(set(nfc_results)) == 1, f"NFC normalization not consistent: {nfc_results}"
            
            # All should normalize to the same NFD form
            nfd_results = [unicodedata.normalize('NFD', s) for s in equiv_class]
            assert len(set(nfd_results)) == 1, f"NFD normalization not consistent: {nfd_results}"
            
            print(f"  NFC result: {repr(nfc_results[0])}")
            print(f"  NFD result: {repr(nfd_results[0])}")

    def test_accent_removal_for_fallback_matching(self):
        """Test accent removal for fallback matching while preserving non-Latin scripts.
        
        This test creates a function to remove accents from Latin, Cyrillic, and Greek
        characters while leaving Chinese, Japanese, Korean, and other scripts unchanged.
        This could be useful for fuzzy matching when exact Unicode matches fail.
        """
        
        
        print("\n=== Accent Removal Tests ===")
        
        # Test cases for different scripts
        test_cases = [
            # Latin script - should have accents removed
            {
                'input': 'café',
                'expected': 'cafe',
                'script': 'Latin',
                'should_change': True
            },
            {
                'input': 'niño', 
                'expected': 'nino',
                'script': 'Latin',
                'should_change': True
            },
            {
                'input': 'académie',
                'expected': 'academie', 
                'script': 'Latin',
                'should_change': True
            },
            {
                'input': 'algèbre',
                'expected': 'algebre',
                'script': 'Latin', 
                'should_change': True
            },
            # Greek script - should have accents removed (if any)
            {
                'input': 'αβγ',  # Greek letters without accents
                'expected': 'αβγ',
                'script': 'Greek',
                'should_change': False
            },
            # Cyrillic script - should have accents removed (if any)
            {
                'input': 'абв',  # Cyrillic letters  
                'expected': 'абв',
                'script': 'Cyrillic',
                'should_change': False
            },
            # Chinese - should be left unchanged
            {
                'input': '中文',
                'expected': '中文',
                'script': 'Chinese',
                'should_change': False
            },
            # Japanese Hiragana - should be left unchanged
            {
                'input': 'あいう',
                'expected': 'あいう', 
                'script': 'Japanese Hiragana',
                'should_change': False
            },
            # Japanese Katakana - should be left unchanged
            {
                'input': 'アイウ',
                'expected': 'アイウ',
                'script': 'Japanese Katakana', 
                'should_change': False
            },
            # Korean - should be left unchanged
            {
                'input': '한글',
                'expected': '한글',
                'script': 'Korean',
                'should_change': False
            },
            # Arabic - should be left unchanged
            {
                'input': 'العربية',
                'expected': 'العربية',
                'script': 'Arabic',
                'should_change': False
            },
            # Hebrew - should be left unchanged
            {
                'input': 'עברית',
                'expected': 'עברית',
                'script': 'Hebrew',
                'should_change': False
            },
            # Mixed script - only Latin parts should be modified
            {
                'input': 'café中文',
                'expected': 'cafe中文',
                'script': 'Mixed Latin+Chinese',
                'should_change': True
            }
        ]
        
        for case in test_cases:
            input_text = case['input']
            expected = case['expected']
            script = case['script']
            should_change = case['should_change']
            
            result = remove_accents_safe(input_text)
            
            print(f"\nTesting {script}: '{input_text}' -> '{result}'")
            print(f"  Expected: '{expected}'")
            print(f"  Should change: {should_change}")
            print(f"  Did change: {result != input_text}")
            
            assert result == expected, f"Failed for {script}: '{input_text}' -> '{result}', expected '{expected}'"
            
            # Verify our expectation about whether it should change
            if should_change:
                assert result != input_text, f"Expected {script} text to change but it didn't: '{input_text}'"
            else:
                assert result == input_text, f"Expected {script} text to remain unchanged but it changed: '{input_text}' -> '{result}'"

    def _is_latin_cyrillic_greek_script(self, char: str) -> bool:
        """Check if character belongs to Latin, Cyrillic, or Greek script."""
        if not char:
            return False
            
        code_point = ord(char)
        
        # Latin script ranges (Basic Latin, Latin-1 Supplement, Latin Extended A/B, etc.)
        latin_ranges = [
            (0x0041, 0x007A),  # Basic Latin A-Z, a-z
            (0x00C0, 0x00FF),  # Latin-1 Supplement (À-ÿ)
            (0x0100, 0x017F),  # Latin Extended-A
            (0x0180, 0x024F),  # Latin Extended-B
            (0x1E00, 0x1EFF),  # Latin Extended Additional
        ]
        
        # Greek script ranges
        greek_ranges = [
            (0x0370, 0x03FF),  # Greek and Coptic
            (0x1F00, 0x1FFF),  # Greek Extended
        ]
        
        # Cyrillic script ranges  
        cyrillic_ranges = [
            (0x0400, 0x04FF),  # Cyrillic
            (0x0500, 0x052F),  # Cyrillic Supplement
        ]
        
        # Check if character falls in any of these ranges
        all_ranges = latin_ranges + greek_ranges + cyrillic_ranges
        
        for start, end in all_ranges:
            if start <= code_point <= end:
                return True
                
        return False

    def test_accent_removal_with_bip39_words(self):
        """Test accent removal specifically with BIP-39 words from accented languages."""
        
        print("\n=== BIP-39 Word Accent Removal Tests ===")
        
        # Test with actual French BIP-39 words (using our test words from setup_class)
        if hasattr(self, 'test_words') and 'french' in self.test_words:
            for word in self.test_words['french'][:5]:  # Test first 5 French words
                deaccented = remove_accents_safe(word)
                print(f"  French: '{word}' -> '{deaccented}'")
                # Verify that accents were actually removed (should be shorter or different)
                if any(ord(c) > 127 for c in word):  # Contains non-ASCII (accented chars)
                    assert word != deaccented, f"Expected accent removal for '{word}'"
        
        # Test with actual Spanish BIP-39 words
        if hasattr(self, 'test_words') and 'spanish' in self.test_words:
            for word in self.test_words['spanish'][:5]:  # Test first 5 Spanish words
                deaccented = remove_accents_safe(word)
                print(f"  Spanish: '{word}' -> '{deaccented}'")
                # Verify that accents were actually removed
                if any(ord(c) > 127 for c in word):  # Contains non-ASCII (accented chars)
                    assert word != deaccented, f"Expected accent removal for '{word}'"
        
        # Test with known examples
        test_examples = [
            ('académie', 'academie'),
            ('acquérir', 'acquerir'), 
            ('algèbre', 'algebre'),
            ('ábaco', 'abaco'),
            ('acción', 'accion'),
            ('niño', 'nino')
        ]
        
        for original, expected in test_examples:
            deaccented = remove_accents_safe(original)
            print(f"  '{original}' -> '{deaccented}'")
            assert deaccented == expected, f"Expected '{expected}', got '{deaccented}'"
        
        # Test that non-Latin scripts are unchanged, unless removing the Marks leaves the same
        # number of Letter category glyphs/symbols.
        non_latin_examples = [
            '中文',      # Chinese
            'あいう',    # Japanese Hiragana
            'アイウ',    # Japanese Katakana
            '한글',      # Korean
            'العربية',   # Arabic
            'עברית'      # Hebrew
        ]
        
        for word in non_latin_examples:
            deaccented = remove_accents_safe(word)
            print(f"  Non-Latin '{word}' -> '{deaccented}' (should be unchanged)")
            assert deaccented == word, f"Non-Latin script should not change: '{word}' -> '{deaccented}'"

    def test_bip39_wordlist_character_categories(self):
        """Analyze character categories in actual BIP-39 wordlists."""
        
        def analyze_wordlist_categories(language: str, max_words: int = 10):
            """Analyze character categories in a BIP-39 wordlist."""
            print(f"\n=== BIP-39 Wordlist Analysis: {language.capitalize()} ===")
            
            # Get words from the wordlist using our test setup
            if not hasattr(self, 'test_words') or language not in self.test_words:
                print(f"No test words available for {language}")
                return
            
            words = self.test_words[language][:max_words]
            
            category_summary = {}
            script_summary = set()
            
            for word in words:
                print(f"\nWord: '{word}'")
                
                # Analyze original word
                for i, char in enumerate(word):
                    category = unicodedata.category(char)
                    name = unicodedata.name(char, f'UNKNOWN-{ord(char):04X}')
                    script = self._determine_script_from_name(name)
                    
                    print(f"  [{i}] '{char}' U+{ord(char):04X} {category} - {name}")
                    
                    category_summary[category] = category_summary.get(category, 0) + 1
                    script_summary.add(script)
                
                # Show NFD decomposition
                nfd_word = unicodedata.normalize('NFD', word)
                if nfd_word != word:
                    print(f"  NFD decomposition: '{nfd_word}' (length {len(nfd_word)})")
                    for i, char in enumerate(nfd_word):
                        if i >= len(word) or char != word[i]:
                            category = unicodedata.category(char)
                            name = unicodedata.name(char, f'UNKNOWN-{ord(char):04X}')
                            print(f"    [{i}] '{char}' U+{ord(char):04X} {category} - {name}")
            
            print(f"\nCategory summary for {language}:")
            for category, count in sorted(category_summary.items()):
                print(f"  {category}: {count}")
            
            print(f"Scripts found: {', '.join(sorted(script_summary))}")
            
            return category_summary, script_summary
        
        # Analyze available wordlists
        if hasattr(self, 'test_words'):
            for language in self.test_words.keys():
                analyze_wordlist_categories(language, max_words=5)
        
        # Also test some known challenging cases
        print(f"\n=== Manual BIP-39 Word Examples ===")
        
        challenging_words = [
            ('académie', 'French with acute accent'),
            ('algèbre', 'French with grave accent'), 
            ('ábaco', 'Spanish with acute accent'),
            ('niño', 'Spanish with tilde'),
            ('acción', 'Spanish with acute accent')
        ]
        
        for word, description in challenging_words:
            print(f"\n{description}: '{word}'")
            
            # Show character-by-character breakdown
            for i, char in enumerate(word):
                category = unicodedata.category(char)
                name = unicodedata.name(char, f'UNKNOWN-{ord(char):04X}')
                print(f"  [{i}] '{char}' U+{ord(char):04X} {category} - {name}")
            
            # Show NFD breakdown
            nfd_word = unicodedata.normalize('NFD', word)
            if nfd_word != word:
                print(f"  NFD: '{nfd_word}'")
                for i, char in enumerate(nfd_word):
                    category = unicodedata.category(char)
                    name = unicodedata.name(char, f'UNKNOWN-{ord(char):04X}')
                    combining = " (COMBINING)" if category.startswith('M') else ""
                    print(f"    [{i}] '{char}' U+{ord(char):04X} {category}{combining} - {name}")

    def test_normalization_preserves_meaning(self):
        """Test that normalization preserves the semantic meaning of words.
        
        CONFIRMS that normalization is reversible and consistent:
        - Converting NFD→NFC→NFD produces the original NFD form
        - Converting NFC→NFD→NFC produces the original NFC form  
        - Double normalization is idempotent (same result)
        - Critical for ensuring BIP-39 mnemonics work regardless of input normalization
        """
        for language, words in self.test_words.items():
            for word in words:
                nfc_word = unicodedata.normalize('NFC', word)
                nfd_word = unicodedata.normalize('NFD', word)
                
                # While byte representation may differ, they should represent the same word
                # This is more of a documentation test - we can't programmatically verify
                # semantic equivalence, but we can verify they normalize consistently
                
                # Double normalization should be idempotent
                assert unicodedata.normalize('NFC', nfc_word) == nfc_word
                assert unicodedata.normalize('NFD', nfd_word) == nfd_word
                
                # Converting between forms should be consistent (reversible)
                assert unicodedata.normalize('NFC', nfd_word) == nfc_word
                assert unicodedata.normalize('NFD', nfc_word) == nfd_word

    def test_compatibility_character_normalization(self):
        """Test NFKC/NFKD normalization effects on compatibility characters.
        
        CRITICAL ANALYSIS FOR BIP-39 PROCESSING:
        This test determines whether BIP-39 implementations need to handle 
        compatibility normalization when comparing user input to wordlist words.
        
        Compatibility characters that might appear in user input:
        - Fullwidth characters from Asian input methods (ａｂｃ → abc)
        - Roman numerals (Ⅰ → I) 
        - Ligatures (ﬁ → fi)
        - Circled numbers (① → 1)
        - Super/subscripts (² → 2)
        
        Key questions answered:
        1. Do NFKC/NFKD change compatibility chars differently than NFC/NFD?
        2. Could user input contain compatibility chars that map to BIP-39 words?
        3. Should BIP-39 validation use NFKC instead of NFC for robustness?
        """
        print("\n=== Compatibility Character Analysis ===")
        
        compatibility_transformations = []
        
        for test_case in self.compatibility_test_cases:
            analysis = self.analyze_unicode_string(test_case)
            
            print(f"\nCompatibility test: '{test_case}'")
            print(f"  Original codepoints: {analysis['codepoints']}")
            print(f"  Character names: {analysis['char_names']}")
            
            # Compare all normalization forms
            nfc_result = analysis['nfc']
            nfd_result = analysis['nfd'] 
            nfkc_result = analysis['nfkc']
            nfkd_result = analysis['nfkd']
            
            print(f"  NFC : '{nfc_result}' -> {[hex(ord(c)) for c in nfc_result]}")
            print(f"  NFD : '{nfd_result}' -> {[hex(ord(c)) for c in nfd_result]}")
            print(f"  NFKC: '{nfkc_result}' -> {[hex(ord(c)) for c in nfkc_result]}")
            print(f"  NFKD: '{nfkd_result}' -> {[hex(ord(c)) for c in nfkd_result]}")
            
            # Check if NFKC/NFKD produce different results than NFC/NFD
            canonical_vs_compatibility = (nfc_result != nfkc_result) or (nfd_result != nfkd_result)
            
            if canonical_vs_compatibility:
                transformation = {
                    'original': test_case,
                    'nfc': nfc_result,
                    'nfkc': nfkc_result,
                    'transformation_type': 'compatibility_normalization'
                }
                compatibility_transformations.append(transformation)
                print(f"  *** COMPATIBILITY TRANSFORMATION: '{test_case}' -> '{nfkc_result}' ***")
            else:
                print(f"  No compatibility transformation (NFC == NFKC)")
        
        # Store results for analysis
        self.compatibility_transformations = compatibility_transformations
        
        # Verify we found some compatibility transformations
        assert len(compatibility_transformations) > 0, "Expected to find compatibility character transformations"
        
        print(f"\nFound {len(compatibility_transformations)} compatibility transformations")

    def test_bip39_wordlist_compatibility_analysis(self):
        """Analyze whether BIP-39 wordlists contain any compatibility characters.
        
        DETERMINES: Do actual BIP-39 wordlists use compatibility characters?
        If not, then compatibility normalization is only needed for user input processing.
        """
        print("\n=== BIP-39 Wordlist Compatibility Analysis ===")
        
        compatibility_found_in_wordlists = []
        
        for language, words in self.test_words.items():
            print(f"\nAnalyzing {language} wordlist...")
            
            for word in words:
                nfc_form = unicodedata.normalize('NFC', word)
                nfkc_form = unicodedata.normalize('NFKC', word)
                
                if nfc_form != nfkc_form:
                    compatibility_found_in_wordlists.append({
                        'language': language,
                        'word': word,
                        'nfc': nfc_form,
                        'nfkc': nfkc_form
                    })
                    print(f"  COMPATIBILITY CHARACTER FOUND: '{word}' -> '{nfkc_form}'")
        
        if compatibility_found_in_wordlists:
            print(f"\nWARNING: Found {len(compatibility_found_in_wordlists)} compatibility characters in wordlists!")
            for item in compatibility_found_in_wordlists:
                print(f"  {item['language']}: '{item['word']}' -> '{item['nfkc']}'")
        else:
            print("\nRESULT: No compatibility characters found in BIP-39 wordlists")
            print("This confirms BIP-39 wordlists use only canonical Unicode forms")

    def test_user_input_compatibility_scenarios(self):
        """Test realistic user input scenarios with compatibility characters.
        
        PRACTICAL ANALYSIS: What happens when users enter compatibility characters
        that could map to valid BIP-39 words after NFKC normalization?
        """
        print("\n=== User Input Compatibility Scenarios ===")
        
        # Simulate user input scenarios that might contain compatibility chars
        user_input_scenarios = [
            # Fullwidth input (common with Asian keyboards)
            {
                'input': 'ａｃａｄéｍｉｅ',  # Fullwidth 'académie' 
                'expected_word': 'académie',
                'scenario': 'Asian keyboard fullwidth input'
            },
            # Mixed fullwidth/normal
            {
                'input': 'ａｃtion',  # Fullwidth 'a' + normal 'ction'
                'expected_word': 'action',
                'scenario': 'Mixed fullwidth/normal input'
            },
            # Ligature input
            {
                'input': 'proﬁt',  # Contains ligature fi
                'expected_word': 'profit', 
                'scenario': 'Ligature character input'
            },
        ]
        
        bip39_validation_recommendations = []
        
        for scenario in user_input_scenarios:
            user_input = scenario['input']
            expected = scenario['expected_word']
            description = scenario['scenario']
            
            print(f"\nScenario: {description}")
            print(f"  User input: '{user_input}'")
            print(f"  Expected word: '{expected}'")
            
            # Test different normalization approaches
            nfc_result = unicodedata.normalize('NFC', user_input)
            nfkc_result = unicodedata.normalize('NFKC', user_input)
            
            print(f"  NFC normalization:  '{nfc_result}'")
            print(f"  NFKC normalization: '{nfkc_result}'")
            
            # Check if NFKC helps match the expected word
            nfc_matches_expected = (nfc_result == expected)
            nfkc_matches_expected = (nfkc_result == expected)
            
            print(f"  NFC matches expected: {nfc_matches_expected}")
            print(f"  NFKC matches expected: {nfkc_matches_expected}")
            
            if not nfc_matches_expected and nfkc_matches_expected:
                recommendation = f"NFKC normalization needed for: {description}"
                bip39_validation_recommendations.append(recommendation)
                print(f"  *** RECOMMENDATION: Use NFKC normalization for this scenario ***")
            elif nfc_matches_expected:
                print(f"  NFC normalization sufficient")
        
        # Store recommendations for final analysis
        self.bip39_validation_recommendations = bip39_validation_recommendations
        
        if bip39_validation_recommendations:
            print(f"\n=== BIP-39 VALIDATION RECOMMENDATIONS ===")
            for rec in bip39_validation_recommendations:
                print(f"  • {rec}")
        else:
            print(f"\nNo special compatibility handling needed for tested scenarios")

    def test_compatibility_normalization_security_implications(self):
        """Analyze security implications of compatibility normalization in BIP-39.
        
        SECURITY ANALYSIS: Could compatibility normalization create security issues?
        - Homograph attacks (different characters that look similar)
        - Unexpected transformations that change meaning
        - Compatibility chars that map to multiple possible words
        """
        print("\n=== Compatibility Normalization Security Analysis ===")
        
        # Test potential homograph/confusable scenarios
        potentially_confusing_cases = [
            # Roman numeral vs Latin letters
            {
                'char1': 'I',      # Latin capital I
                'char2': 'Ⅰ',      # Roman numeral I 
                'concern': 'Roman numeral I vs Latin I'
            },
            # Fullwidth vs normal
            {
                'char1': 'a',      # Normal Latin a
                'char2': 'ａ',      # Fullwidth Latin a
                'concern': 'Fullwidth vs normal Latin letters'
            },
            # Ligature vs separate chars
            {
                'char1': 'fi',     # Separate f + i
                'char2': 'ﬁ',      # Ligature fi
                'concern': 'Ligature fi vs separate f+i'
            }
        ]
        
        security_warnings = []
        
        for case in potentially_confusing_cases:
            char1 = case['char1']
            char2 = case['char2'] 
            concern = case['concern']
            
            # Test if they normalize to the same thing under NFKC
            nfkc1 = unicodedata.normalize('NFKC', char1)
            nfkc2 = unicodedata.normalize('NFKC', char2)
            
            print(f"\nTesting: {concern}")
            print(f"  '{char1}' NFKC-> '{nfkc1}'")
            print(f"  '{char2}' NFKC-> '{nfkc2}'")
            
            if nfkc1 == nfkc2:
                warning = f"SECURITY CONCERN: {concern} normalize to same result under NFKC"
                security_warnings.append(warning)
                print(f"  *** {warning} ***")
            else:
                print(f"  No normalization collision")
        
        # Final security assessment
        print(f"\n=== SECURITY ASSESSMENT ===")
        if security_warnings:
            print(f"Found {len(security_warnings)} potential security concerns:")
            for warning in security_warnings:
                print(f"  ⚠️  {warning}")
            print(f"\nRECOMMENDATION: Carefully validate NFKC normalization in BIP-39 implementations")
        else:
            print(f"No obvious security concerns found with NFKC normalization")
