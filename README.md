# MuCoW - **Mu**ltilingual **Co**ntrastive **W**ord sense disambiguation test suites for machine translation

## WMT 2019 Version

A first version of MuCoW was introduced at WMT 2019:

*Alessandro Raganato, Yves Scherrer and Jörg Tiedemann. 2019.
[The MuCoW test suite at WMT 2019: Automatically harvested multilingual contrastive word sense disambiguation test sets for machine translation.](https://www.aclweb.org/anthology/W19-5354) 
In Proceedings of the Fourth Conference on Machine Translation (WMT): Shared Task Papers. Florence, Italy.*

The relevant data for this version can be found in the **WMT2019** folder.

The same data was used again to evaluate the WMT 2020 systems:

*Yves Scherrer, Alessandro Raganato, Jörg Tiedemann. 2020
[The MUCOW word sense disambiguation test suite at WMT 2020.](https://www.aclweb.org/anthology/2020.wmt-1.40/) In Proceedings of the Fifth Conference on Machine Translation (WMT). Online.*

## LREC 2020 Version

An extended version of MuCoW including training data is presented at LREC 2020:

*Alessandro Raganato, Yves Scherrer and Jörg Tiedemann. 2020.
[An Evaluation Benchmark for Testing the Word Sense Disambiguation Capabilities of Machine Translation Systems.](https://www.aclweb.org/anthology/2020.lrec-1.452/)
In Proceedings of the 12th Language Resources and Evaluation Conference. Marseille, France.*

The relevant data for this version can be found in the **LREC2020** folder.

## A note on evaluation:

For both WMT and LREC versions, there is a mismatch between the definitions of recall given in the papers and those used to compute the results. The evaluation scripts have been updated to provide both variants: recallA corresponds to the one effectively used in the results tables, recallB corresponds to the definition in the papers.
