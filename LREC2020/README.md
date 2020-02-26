# MuCoW - An evaluation benchmark for testing the Word Sense Disambiguation capabilities of Machine Translation systems

## Training data

We make available training data for 5 language pairs (i.e. 10 translation directions) in *Small* and *Big* conditions.

Links will be added here.

## Evaluation data and scripts

The test data is available in the folder `testdata`. The evaluation procedure is detailed below.

### 1. Translate the test set

The folder `testdata` contains a *.test.txt.gz file for each language pair and direction, with the following structure (from the de-en translation direction):

```
abfall  0       europarl        Allein dabei fällt eine riesige Menge an Abfall an .    This in itself generates a large amount of waste .      Abfall
abfall  0       europarl        Auch wurden meiner Auffassung nach gewaltige Anstrengungen unternommen , um eine vernünftige Materialverwertung und eine Reduzierung umweltschädlicher Abfälle zu erreichen sowie die technologische Innovation zu fördern .    I also think that a great effort has been made to arrive at intelligent recycling of materials , a reduction of polluting waste and the promotion of technological innovation . Abfälle
...
```

For translation, only the fourth column (*Allein...*) is relevant. Extract this column from the file and apply your preprocessing pipeline on it. Tokenization is already done, but you may want to apply truecasing and subword splitting. An example of this file is found in `example-de-en/src_segmented.txt`:

```
allein dabei fällt eine riesige Menge an Abfall an .
auch wurden meiner Auffassung nach gewaltige Anstrengungen unternommen , um eine vernünftige Material@@ ver@@ wertung und eine Reduzierung umwelt@@ schädlicher Abfälle zu erreichen sowie die technologische Innovation zu fördern .
...
```

Translate this file with your translation system. An example output (without any postprocessing such as subword merging or detokenization) is found in `example-de-en/out_segmented.txt`:

```
just that , a huge amount of waste is falling .
I also believe that huge efforts have been made to achieve sensible materials recycling and a reduction in environmentally harmful waste and to promote technological innovation .
...
```

Keep both the segmented source file and the segmented output file, both will be needed for evaluation.


### 2. Lemmatize the translated test set

Apply your postprocessing pipeline on the translation output. Then, parse the processed output to CoNLL-U format. (We use the Turku neural parser pipeline for this, but any other tool will do fine. MuCoW only requires lemmatization, all the other fields may remain empty.) The file `example-de-en/out_parsed.txt` shows an example:

```
# newdoc
# newpar
# sent_id = 1
# text = Just that, a huge amount of waste is falling.
1	Just	just	ADV	RB	_	2	advmod	_	_
2	that	that	PRON	DT	Number=Sing|PronType=Dem	10	advmod	_	SpaceAfter=No
3	,	,	PUNCT	,	_	10	punct	_	_
4	a	a	DET	DT	Definite=Ind|PronType=Art	6	det	_	_
5	huge	huge	ADJ	JJ	Degree=Pos	6	amod	_	_
6	amount	amount	NOUN	NN	Number=Sing	10	nsubj	_	_
7	of	of	ADP	IN	_	8	case	_	_
8	waste	waste	NOUN	NN	Number=Sing	6	nmod	_	_
9	is	be	AUX	VBZ	Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin	10	aux	_	_
10	falling	fall	VERB	VBG	Tense=Pres|VerbForm=Part	0	root	_	SpaceAfter=No
11	.	.	PUNCT	.	_	10	punct	_	SpacesAfter=\n

...
```

### 3. Run the evaluation script

The evaluation script `evaluate.py` takes six files as parameters:
- `--ref-testsuite`: the test file as defined by the test suite (in our example `testdata/de-en.test.txt.gz`)
- `--sense-file`: the sense definition file (in our example `testdata/senses.de-en.txt`)
- `--dist-file`: the file defining the distances between senses (in our example `testdata/distances.de-en.txt`)
- `--src-segmented`: the segmented input file, one sentence per line (in our example `example-de-en/src_segmented.txt`)
- `--tgt-segmented`: the segmented system output, one sentence per line (in our example `example-de-en/out_segmented.txt`)
- `--tgt-lemmatized`: the de-segmented, lemmatized system output, in CoNLL format (in our example `example-de-en/out_parsed.txt`)

The first three files remain identical for all systems, whereas the last three files vary according to different systems and segmentation strategies.

Running the command:
```
python3 evaluate.py \
	--ref-testsuite testdata/de-en.test.txt.gz \
	--sense-file testdata/senses.de-en.txt \
	--dist-file testdata/distances.de-en.txt \
	--src-segmented example-de-en/src_segmented.txt \
	--tgt-segmented example-de-en/out_segmented.txt \
	--tgt-lemmatized example-de-en/out_parsed.txt
```

gives the following result table:

| Category        | Pos     | WPos    | Neg     | Unk     | Total   | AvgDist | Precision       | Recall  | F1-Score  | WPrec   | WF1 |
| ---        | ---     | ---    | ---     | ---     | ---   | --- | ---       | ---  | ---  | ---   | --- |
|  all     | 12648   | 13550.8 | 3504    | 1551    | 17703   | 0.1610  | 0.7831  | 0.8908  | 0.8334  | 0.8390  | 0.8641  |
|  corp:EUbookshop | 382     | 510.4   | 467     | 163     | 1012    | 0.3988  | 0.4499  | 0.7009  | 0.5481  | 0.6012    | 0.6472  |
|  corp:books      | 782     | 821.7   | 162     | 163     | 1107    | 0.1296  | 0.8284  | 0.8275  | 0.8280  | 0.8704    | 0.8484  |
|  corp:commoncrawl        | 792     | 946.9   | 582     | 130     | 1504    | 0.3108  | 0.5764  | 0.8590  | 0.6899    | 0.6892  | 0.7648  |
|  corp:europarl   | 3074    | 3266.1  | 745     | 521     | 4340    | 0.1448  | 0.8049  | 0.8551  | 0.8292  | 0.8552    | 0.8551  |
|  corp:globalvoices       | 1091    | 1124.7  | 128     | 77      | 1296    | 0.0774  | 0.8950  | 0.9341  | 0.9141    | 0.9226  | 0.9283  |
|  corp:jw | 4024    | 4288.8  | 1058    | 356     | 5438    | 0.1561  | 0.7918  | 0.9187  | 0.8506  | 0.8439  0.8797 |
 | corp:multiun    | 13      | 17.8    | 17      | 13      | 43      | 0.4070  | 0.4333  | 0.5000  | 0.4643  | 0.5930    | 0.5425  |
|  corp:tatoeba    | 830     | 852.0   | 84      | 27      | 941     | 0.0678  | 0.9081  | 0.9685  | 0.9373  | 0.9322    | 0.9500  |
|  corp:ted        | 1660    | 1722.5  | 261     | 101     | 2022    | 0.1033  | 0.8641  | 0.9426  | 0.9017  | 0.8967    | 0.9191  |
|  datasrc:clean   | 11461   | 12075.7 | 2438    | 1245    | 15144   | 0.1312  | 0.8246  | 0.9020  | 0.8616  | 0.8688    | 0.8851  |
|  datasrc:clean:0-20      | 1377    | 1723.5  | 1406    | 344     | 3127    | 0.3807  | 0.4948  | 0.8001  | 0.6115    | 0.6193  | 0.6982  |
|  datasrc:noisy   | 1187    | 1475.1  | 1066    | 306     | 2559    | 0.3453  | 0.5269  | 0.7950  | 0.6337  | 0.6547    | 0.7181  |
|  datasrc:noisy:0-20      | 373     | 594.8   | 817     | 179     | 1369    | 0.5001  | 0.3134  | 0.6757  | 0.4282    | 0.4999  | 0.5746  |
|  dist:above_avg  | 6721    | 6998.0  | 1495    | 905     | 9121    | 0.1482  | 0.8180  | 0.8813  | 0.8485  | 0.8518    | 0.8663  |
|  dist:below_avg  | 5927    | 6552.8  | 2009    | 646     | 8582    | 0.1743  | 0.7468  | 0.9017  | 0.8170  | 0.8257    | 0.8620  |
|  freq:0-20       | 1750    | 2318.3  | 2223    | 523     | 4496    | 0.4165  | 0.4405  | 0.7699  | 0.5604  | 0.5835    | 0.6639  |
|  freq:20-40      | 1488    | 1659.2  | 648     | 239     | 2375    | 0.2232  | 0.6966  | 0.8616  | 0.7704  | 0.7768    | 0.8170  |
|  freq:40-60      | 1841    | 1939.6  | 367     | 193     | 2401    | 0.1215  | 0.8338  | 0.9051  | 0.8680  | 0.8785    | 0.8916  |
|  freq:45-55      | 1352    | 1410.0  | 224     | 121     | 1697    | 0.1053  | 0.8579  | 0.9179  | 0.8868  | 0.8947    | 0.9061  |
|  freq:60-80      | 2244    | 2282.9  | 149     | 208     | 2601    | 0.0460  | 0.9377  | 0.9152  | 0.9263  | 0.9540    | 0.9342  |
|  freq:80-100     | 5325    | 5350.7  | 117     | 388     | 5830    | 0.0168  | 0.9785  | 0.9321  | 0.9547  | 0.9832    | 0.9570  |
|  srcsplit:no     | 12411   | 13289.0 | 3432    | 1516    | 17359   | 0.1612  | 0.7834  | 0.8911  | 0.8338  | 0.8388    | 0.8642  |
|  srcsplit:yes    | 237     | 261.8   | 72      | 35      | 344     | 0.1528  | 0.7670  | 0.8713  | 0.8158  | 0.8472    | 0.8591  |
|  tgtsplit:no     | 11939   | 12774.8 | 3246    | 0       | 15185   | 0.1587  | 0.7862  | 0.0000  | 0.0000  | 0.8413    | 0.0000  |
|  tgtsplit:yes    | 709     | 776.0   | 258     | 0       | 967     | 0.1975  | 0.7332  | 0.0000  | 0.0000  | 0.8025    | 0.0000  |

The columns used in the paper are *Precision*, *Recall* and *F1-Score*. *WPrec* refers to the weighted precision proposed in Section 3.

Each row represents a subset of the dataset according to some criterion. *all* refers to the entire dataset. The *freq:* rows represent the different frequency bins as shown in Section 4.1. *srcsplit:* and *tgtsplit:* shows the segmentation effects described in Section 4.2. *datasrc:* (and *corp:* in a more detailed level) refers to the corpus effects described in Section 4.3.
