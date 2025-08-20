from hdwallet.mnemonics.slip39.mnemonic import (
    SLIP39Mnemonic, language_parser, group_parser
)


def test_slip39_language():

    # Any name; no spec --> simplest 1/1 group encoding yielding single mnemonic
    spec = language_parser("english")
    assert spec == {
        ("english",(1,1)): {
            0: (1,1),
        },
    }

    # No name or secret spec, and a single group w/ default size based on group threshold
    group = group_parser("Name 3 / ", size_default=None)
    assert group == ("Name",(3,6))
    spec = language_parser(": Name 3 / ")
    assert spec == {
        ("",(1,1)): {
            "Name": (3,6),
        },
    }

    # A secret w/ threshold 3 required, of the default 4 groups of fibonacci required mnemonics
    for language in [
        " 3 / 4 ",
        " 3 / 4 [ ] ",
        " 3 / : ,,, ",
        " 3 / : 1/, 1, 4, 3/ ",
    ]:
        spec = language_parser(language)
        assert spec == {
            ("",(3,4)): {
                0: (1,1),
                1: (1,1),
                2: (2,4),
                3: (3,6),
            },
        }, f"Language {language} yielded incorrect encoding: {spec!r}"

    # If some group specs are provided, the rest are deduced in a fibonacci-ish sequence
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
    
def test_slip39_mnemonics():
    entropy = "ff"*(256//8)
    mnemonic = SLIP39Mnemonic.encode(entropy=entropy, language="")
    mnemonic_list = SLIP39Mnemonic.normalize(mnemonic)
    recovered = SLIP39Mnemonic.decode(mnemonic_list)
    assert recovered == entropy

    slip39 = SLIP39Mnemonic(mnemonic)
    assert slip39._mnemonic == mnemonic_list
    assert slip39.mnemonic() == mnemonic


