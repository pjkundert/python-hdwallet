from hdwallet.exceptions import MnemonicError
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

    # Ensure our prefix and whitespace handling works correctly
    assert SLIP39Mnemonic.NORMALIZE.match(
        "  Group 1 { word word"
    ).groups() == ("Group 1 {","word word")

    assert SLIP39Mnemonic.NORMALIZE.match(
        "  Group 1 { word word  "
    ).groups() == ("Group 1 {","word word")

    assert SLIP39Mnemonic.NORMALIZE.match(
        "            word word  "
    ).groups() == (None,"word word")

    assert SLIP39Mnemonic.NORMALIZE.match(
        "  Group 1 {   "
    ).groups() == ("Group 1 {",None)

    entropy = "ff"*(256//8)
    mnemonic = SLIP39Mnemonic.encode(entropy=entropy, language="")
    mnemonic_list = SLIP39Mnemonic.normalize(mnemonic)
    recovered = SLIP39Mnemonic.decode(mnemonic_list)
    assert recovered == entropy

    expected_entropy = "ff" * (512 // 8)  # 64 bytes of 0xFF

    slip39 = SLIP39Mnemonic(mnemonic)
    assert slip39._mnemonic == mnemonic_list
    assert slip39.mnemonic() == mnemonic

    for mnemonic in [
            "curly agency academic academic academic boring radar cluster domestic ticket fumes remove velvet fluff video crazy chest average script universe exhaust remind helpful lamp declare garlic repeat unknown bucket adorn sled adult triumph source divorce premium genre glimpse level listen ancestor wildlife writing document wrist judicial medical detect frost leaves language jerky increase glasses extra alto burden iris swing",
            "trend cleanup acrobat easy acid military timber boundary museum dictate argue always grasp bundle welcome silent campus exhaust snake magazine kitchen surface unfold theory adequate gasoline exotic counter fantasy magazine slow mailman metric thumb listen ruler elite mansion diet hybrid withdraw swing makeup repeat glasses density express ting estimate climate scholar loyalty unfold bumpy ecology briefing much fiscal mental\ntrend cleanup beard easy acne extra profile window craft custody owner plot inherit injury starting iris talent curious squeeze retreat density decision hush rainbow extra grumpy humidity income should spray elevator drove large source game pajamas sprinkle dining security class adapt credit therapy verify realize retailer scatter suitable stick hearing lecture mountain dragon talent medal decision equip cleanup aircraft",
             "salon email acrobat romp acid lunar rival view daughter exchange privacy pickup moisture forbid welcome amount estimate therapy sled theory says member scroll sister smell erode scene tension glance laden ting cricket apart senior legend transfer describe crowd exceed saver lilac episode cluster pipeline sniff window loyalty manual behavior raspy problem fraction story playoff scroll aunt benefit element execute\nsalon email beard romp acquire vocal plan aviation nervous package unhappy often goat forward closet material fortune fitness wireless terminal slap resident aunt artist source cover perfect grant military ruin taught depend criminal theater decision standard salary priority equation license prisoner rhyme indicate academic shaft express kernel airport tolerate market owner erode dance orange beaver distance smug plunge level\nsalon email ceramic roster academic spark starting says phantom tension saver erode ugly smoking crazy screw pumps display funding fortune mixture ancestor industry glad paces junk laden timber hunting secret program ruin gather clogs legal sugar adjust check crazy genuine predator national swimming twice admit desert system sidewalk check class spelling early morning liberty grief election antenna merchant adjust\nsalon email ceramic scared acid cultural object wildlife percent include wealthy geology capture lift evidence envy identify game guilt curly garbage reaction early scatter practice metric mild earth subject axis verdict juice sled dominant ranked blimp sympathy credit example typical float prisoner ting paces husband adequate amuse display worthy amuse depict civil learn modify lecture mother paid evil stadium\nsalon email ceramic shadow acquire critical ugly desire piece romp piece olympic benefit cargo forbid superior credit username library usher beyond include verify pipeline volume pistol ajar mild carbon acrobat receiver decrease champion calcium flea email picture funding tracks junior fishing thorn regret lily tofu decent romp hazard loud cards peaceful alien retreat single pregnant unfold trial wrist jury\nsalon email ceramic sister acne spirit parking aquatic phrase fact order racism tendency example disaster finance trip multiple ranked lobe tackle smirk regular auction satoshi elephant traveler estimate practice sprinkle true making manual adjust herald mama jacket fishing lecture volume phantom symbolic liberty usher moment alcohol born nervous flip desert element budget pink switch envy discuss laden check promise\nsalon email decision round acquire voting damage briefing emphasis parking airport nylon umbrella coding fake cylinder chubby bolt superior client shame museum reward domain briefing forget guilt group leaf teacher that remind blind judicial soul library dismiss guard provide smoking robin blue focus relate tricycle flexible meaning painting venture trip manager stay flexible rebuild group elephant papa dismiss activity\nsalon email decision scatter acid idle veteran knife thorn theory remember volume cluster writing drove process staff usual sprinkle observe sympathy says birthday lunar leaves salary belong license submit anxiety award spray body victim domestic solution decent geology huge preach human scared desktop email frost verify says predator debris peasant burden swing owner safari reaction broken glimpse jacket deal\nsalon email decision shaft academic breathe mental capital midst guest tracks bolt twin change usual rescue profile taxi paces penalty vitamins emphasis story acquire exhaust salt quantity junction shame midst saver peanut acquire trash duke spend remember predator miracle vintage rich multiple story inmate depend example together blimp coding depart acid diminish petition sister mountain explain thumb density kidney\nsalon email decision skin acne owner finance kernel deal crazy fortune kernel cause warn ordinary document forward alto mixed burning theater axis hybrid review squeeze force shelter owner minister jump darkness smith advance greatest stadium listen prune prisoner exceed medal hospital else race lying liquid tolerate preach capture therapy junction method demand glasses relate emerald blind club income exceed\nsalon email decision snake acne repair sidewalk window video knit resident alien window weapon chubby pacific segment artwork nuclear erode thorn replace wits snapshot founder shaped quiet spray sled depend decent cage income pecan estimate purchase frequent trash chew luxury glimpse category move pipeline scout snake source entrance laundry skunk gravity briefing ancestor hormone security husky snake nylon prospect\nsalon email decision spider academic dramatic axis overall finger early alive health decent ceiling explain capture deploy trip mother viral valid unwrap filter holiday saver fake sharp decorate mustang stay survive hybrid hybrid cowboy peanut that findings umbrella worthy venture quick various watch filter impact jury paid elevator retreat literary viral capacity skin bumpy blue criminal behavior surface legal",
    ]:
        assert SLIP39Mnemonic.is_valid(mnemonic)
        slip39 = SLIP39Mnemonic(mnemonic)
        assert slip39.words() == 59
        assert SLIP39Mnemonic.decode(slip39.mnemonic()) == expected_entropy

        # Let's make sure we can detect missing mnemonics reliably.  With random subsets, we should
        # either decode the Mnemonic, or get a MnemonicError detailing what was missing
        mnemonic_list = mnemonic.split('\n')
        import random

        # Start with full list size and decrease
        for subset_size in range(len(mnemonic_list), 0, -1):
            # Create random subset
            subset = random.sample(mnemonic_list, subset_size)

            try:
                result = SLIP39Mnemonic.decode( '\n'.join(subset) )

                # If decode succeeds, verify it returns expected entropy
                assert result == expected_entropy, (
                    f"Subset size {subset_size}: Expected entropy {expected_entropy}, "
                    f"got {result}"
                )
            except MnemonicError as e:
                # Verify it's the expected "Incomplete" error
                assert "Incomplete: found" in str(e), (
                    f"Subset size {subset_size}: Expected 'Incomplete; found' error, "
                    f"got: {str(e)}"
                )
            except Exception as e:
                # Unexpected error type
                pytest.fail(
                    f"Subset size {subset_size}: Unexpected error type {type(e)}: {e}"
                )
