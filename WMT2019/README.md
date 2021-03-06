# MuCoW test suite
MuCoW is a **mu**ltilingual **co**ntrastive **w**ord sense disambiguation test suite for machine translation that covers 16 language pairs with more than 200 thousand contrastive sentence pairs, automatically built from word-aligned parallel corpora and the wide-coverage multilingual sense inventory of BabelNet.


The MuCoW test suite is available in two variants: *"scoring test suite"* and *"translation test suite"*.
For a more detailed description of MuCoW please refer to Section 2 (Building MuCoW) and Section 4 (Translation test suites for WMT 2019) of the reference paper.


The first variant *"scoring test suite"* covers 11 language pairs with a total of almost 240 000 sentence pairs and relies on the ability of neural machine translation systems to score given translations: a sentence containing an ambiguous source word is paired with the correct reference translation and with a modified translation in which the ambiguous word has been replaced by a word of a different sense. A contrast is considered successfully detected if the reference translation obtains a higher score than an artificially modified translation. 


The second variant *"translation test suite"* covers 9 language pairs with a total of 15 600 sentences and relies on the translation output. After a system translates a sentence containing an ambiguous source word, we check whether any of the correct or incorrect target words (listed in a pre-compiled multilingual lexicon) can be identified in the translation output (recommended in tokenized and lowercased format).


------


If you use this work, please cite:

*Alessandro Raganato, Yves Scherrer and Jörg Tiedemann. 2019.
[The MuCoW test suite at WMT 2019: Automatically harvested multilingual contrastive word sense disambiguation test sets for machine translation.](https://www.aclweb.org/anthology/W19-5354) 
In Proceedings of the Fourth Conference on Machine Translation (WMT): Shared Task Papers. Florence, Italy.*

```
@inproceedings{raganato-etal-2019-mucow,
    title = "The {M}u{C}o{W} Test Suite at {WMT} 2019: Automatically Harvested Multilingual Contrastive Word Sense Disambiguation Test Sets for Machine Translation",
    author = {Raganato, Alessandro  and Scherrer, Yves  and Tiedemann, J{\"o}rg},
    booktitle = "Proceedings of the Fourth Conference on Machine Translation (Volume 2: Shared Task Papers, Day 1)",
    month = aug,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/W19-5354",
    doi = "10.18653/v1/W19-5354",
    pages = "470--480"
}
```
