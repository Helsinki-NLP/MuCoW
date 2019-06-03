# MuCoW scoring test suite

The MUCOW scoring test suite comprises 11 language pairs having as target language English, automatically harvested from different parallel corpora (books, eubooks, europarl, multiun, newscomm, opensubs, tatoeba, ted).

We built this variant to all to-English translation directions that were part of the Conference of Machine Translation (WMT) news translation task over the last years, namely Czech-> English (CS-EN), German->English (DE-EN), Spanish->English (ES-EN), Estonian->English (ET-EN), Finnish->English (FI-EN), French->English (FR-EN), Lithuanian-> English (LT-EN), Latvian-> English (LV-EN), Romanian->English (RO-EN), Russian->English (RU-EN) and Turkish->English (TR-EN).

For a more detailed statistics please refer to Section 2.5 of the reference paper.


Following [contraWSD](https://github.com/a-rios/ContraWSD) project, we release two scripts, `json_to_plaintext.py` and `evaluate_mod.py`, to extract the source and contrastive translations from the json file and to compute the accuracy score respectively.


`json_to_plaintext.py` takes in input three arguments, the path of the json file and the path where to create the source and constrastive files. For example:

`python json_to_plaintext.py ./json/cs-en.mucow.json ./source.cs ./contrastive.en`

will create the files `source.cs` and `contrastive.en` containing the translations to score with a given machine translation system (Note that the sentences are in raw format, so you would need to apply a preprocessing pipeline before scoring).


After scoring the translations in the same order in which are listed, you can use the `evaluate_mod.py` script to compute the accuracy score on the test suite. 

`evaluate_mod.py` takes in input a file with a score per line and will print out the overall accuracy of a given model and some statistics, i.e., accuracy per corpus (books, eubooks, europarl, multiun, newscomm, opensubs, tatoeba, ted) and accuracy per word sense.


An example:

`python evaluate_mod.py -r ./json/cs-en.mucow.json < myscore.cs-en > myaccuracy.cs-en`


(By default, the script assumes lower scores are better, however you change the setting with the `--maximize` option which means the higher the better)

