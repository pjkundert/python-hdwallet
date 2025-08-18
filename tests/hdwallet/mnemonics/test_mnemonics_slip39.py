from hdwallet.mnemonics.slip39.mnemonic import (
    SLIP39Mnemonic, language_parser, group_parser
)


def test_slip39_language():
    spec = language_parser("")
    assert spec == {
        ("",(2,4)): {
            0: (1,1),
            1: (1,1),
            2: (2,4),
            3: (3,6),
        },
    }

    # default secret spec, and a single group w/ default size
    group = group_parser(" 3 / ", size_default=None)
    assert group == ("",(3,6))
    spec = language_parser(" 3 / ")
    assert spec == {
        ("",(1,1)): {
            0: (3,6),
        },
    }
    
    # A secret w/ threshold 3 required, of the default 4 groups of fibonacci required mnemonics
    spec = language_parser(" 3 / [ ] ")
    assert spec == {
        ("",(3,4)): {
            0: (1,1),
            1: (1,1),
            2: (2,4),
            3: (3,6),
        },
    }
    
    spec = language_parser("Satoshi Nakamoto 7 [ 2/3 ] ")
    assert spec == {
        ("Satoshi Nakamoto",(4,7)): {
            0: (2,3),
            1: (1,1),
            2: (3,6),
            3: (4,8),
            4: (7,14),
            5: (8,16),
            6: (8,16),
        },
    }
    
