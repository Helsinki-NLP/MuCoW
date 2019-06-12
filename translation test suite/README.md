# MuCoW translation test suite

The MuCoW translation test suite comprises 9 language pairs, automatically harvested from different parallel corpora (books, eubooks, opensubs, tatoeba, ted).

We submit this variant to the participants of the Conference of Machine Translation (WMT) news translation task 2019, for the following language pairs: German->English (DE-EN), Finnish->English (FI-EN), Lithuanian->English (LT-EN), Russian->English (RU-EN), English->Czech (EN-CS), English->German (EN-DE), English->Finnish (EN-FI), English->Lithuanian (EN-LT) and English->Russian (EN-RU).

For more detailed statistics please refer to Section 4 of the reference paper.

We release a script, `evaluate.py`, to compute precision, recall and fscore as explained in Section 5 of the reference paper. The evaluation script defines three paths that have to be set per language pair, for the metadata files, the raw (detokenized) system outputs, and the lemmatized system outputs. The evaluation scripts writes its results in TSV format to standard output.
