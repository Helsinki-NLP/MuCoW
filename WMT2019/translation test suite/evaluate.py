#! /usr/bin/env python3

import sys, glob, sacremoses

def processLanguagePair(lgpair, keyfile_prefix, rawtranslations_glob, lemtranslations_glob):
	# load sense keys from file
	sense_keys = []
	k = open(keyfile_prefix + ".key.txt", 'r', encoding='utf-8')
	for line in k:
		elements = line.strip().split("\t")
		t = (elements[0], elements[1], elements[2], tuple(elements[3].split(" ")), tuple(elements[4].split(" ")))
		sense_keys.append(t)
	k.close()
	
	# load domain keys from file
	indomain_keys = set()
	outdomain_keys = set()
	d = open(keyfile_prefix + ".domain.txt", 'r', encoding='utf-8')
	for line in d:
		elements = line.strip().split("\t")
		if elements[2] == "in":
			indomain_keys.add((elements[0], elements[1]))
		else:
			outdomain_keys.add((elements[0], elements[1]))
	d.close()
	
	# initialize tokenizer
	tokenizer = sacremoses.MosesTokenizer(lang=lgpair[-2:])
	
	# load and process submissions
	results = {}
	toksubmissions = sorted(glob.glob(rawtranslations_glob))
	lemsubmissions = sorted(glob.glob(lemtranslations_glob))
	for toksubmission, lemsubmission in zip(toksubmissions, lemsubmissions):
		
		if toksubmission.split("/")[-1] != lemsubmission.split("/")[-1].replace(".parsed.toklemma", ""):
			print("Mismatch in filenames")
			print(toksubmission)
			print(lemsubmission)
			return
	
		counts = {"pos_in": 0, "pos_out": 0, "neg_in": 0, "neg_out": 0, "unk_in": 0, "unk_out": 0}
		tokf = open(toksubmission, 'r', encoding='utf-8')
		lemf = open(lemsubmission, 'r', encoding='utf-8')
		
		for tokline, lemline, key in zip(tokf, lemf, sense_keys):
			if (key[2], " ".join(key[3])) in indomain_keys:
				suffix = "_in"
			elif (key[2], " ".join(key[3])) in outdomain_keys:
				suffix = "_out"
			else:
				print("Domain not found:", (key[2], " ".join(key[3])))
			
			# first look in tokenized data
			tokwords = [x.lower() for x in tokenizer.tokenize(tokline.strip(), escape=False)]
			posfound = any([posword in tokwords for posword in key[3]])
			negfound = any([negword in tokwords for negword in key[4]])
			
			# if not found, look in lemmatized data
			if (not posfound) and (not negfound):
				lemwords = lemline.strip().lower().split(" ")
				posfound = any([posword in lemwords for posword in key[3]])
				negfound = any([negword in lemwords for negword in key[4]])
			
			if posfound and not negfound:
				counts["pos"+suffix] += 1
			elif negfound:
				counts["neg"+suffix] += 1
			else:
				counts["unk"+suffix] += 1
		
		tokf.close()
		lemf.close()
		
		counts["cov_in"] = (counts["pos_in"] + counts["neg_in"]) / (counts["pos_in"] + counts["neg_in"] + counts["unk_in"])
		counts["cov_out"] = (counts["pos_out"] + counts["neg_out"]) / (counts["pos_out"] + counts["neg_out"] + counts["unk_out"])
		counts["cov_all"] = (counts["pos_in"] + counts["neg_in"] + counts["pos_out"] + counts["neg_out"]) / (counts["pos_in"] + counts["neg_in"] + counts["unk_in"] + counts["pos_out"] + counts["neg_out"] + counts["unk_out"])
		
		# Precision = pos / (pos+neg)
		counts["prec_in"] = 0 if counts["pos_in"] == 0 else counts["pos_in"] / (counts["pos_in"] + counts["neg_in"])
		counts["prec_out"] = 0 if counts["pos_out"] == 0 else counts["pos_out"] / (counts["pos_out"] + counts["neg_out"])
		counts["prec_all"] = 0 if (counts["pos_in"] + counts["pos_out"]) == 0 else (counts["pos_in"] + counts["pos_out"]) / (counts["pos_in"] + counts["neg_in"] + counts["pos_out"] + counts["neg_out"])
		
		# Recall = pos / (pos+unk)
		counts["rec_in"] = 0 if counts["pos_in"] == 0 else counts["pos_in"] / (counts["pos_in"] + counts["unk_in"])
		counts["rec_out"] = 0 if counts["pos_out"] == 0 else counts["pos_out"] / (counts["pos_out"] + counts["unk_out"])
		counts["rec_all"] = 0 if (counts["pos_in"] + counts["pos_out"]) == 0 else (counts["pos_in"] + counts["pos_out"]) / (counts["pos_in"] + counts["unk_in"] + counts["pos_out"] + counts["unk_out"])
		
		counts["f1_in"] = 0 if (counts["prec_in"] + counts["rec_in"]) == 0 else 2 * counts["prec_in"] * counts["rec_in"] / (counts["prec_in"] + counts["rec_in"])
		counts["f1_out"] = 0 if (counts["prec_out"] + counts["rec_out"]) == 0 else 2 * counts["prec_out"] * counts["rec_out"] / (counts["prec_out"] + counts["rec_out"])
		counts["f1_all"] = 0 if (counts["prec_all"] + counts["rec_all"]) == 0 else 2 * counts["prec_all"] * counts["rec_all"] / (counts["prec_all"] + counts["rec_all"])
		
		submissionName = toksubmission.split("/")[-1]
		results[submissionName] = counts
	
	print(lgpair.upper())
	print()
	print("Submission\t\tInPos\tInNeg\tInUnk\tInCoverage\tInPrecision\tInRecall\tInFscore\t\tOutPos\tOutNeg\tOutUnk\tOutCoverage\tOutPrecision\tOutRecall\tOutFscore\t\tAllPos\tAllNeg\tAllUnk\tAllCoverage\tAllPrecision\tAllRecall\tAllFscore")
	for submission, result in sorted(results.items(), key=lambda x: x[1]["f1_all"], reverse=True):
		s = submission
		s += "\t\t{}\t{}\t{}\t{:.2f}%\t{:.2f}%\t{:.2f}%\t{:.2f}%".format(result["pos_in"], result["neg_in"], result["unk_in"], 100*result["cov_in"], 100*result["prec_in"], 100*result["rec_in"], 100*result["f1_in"])
		s += "\t\t{}\t{}\t{}\t{:.2f}%\t{:.2f}%\t{:.2f}%\t{:.2f}%".format(result["pos_out"], result["neg_out"], result["unk_out"], 100*result["cov_out"], 100*result["prec_out"], 100*result["rec_out"], 100*result["f1_out"])
		s += "\t\t{}\t{}\t{}\t{:.2f}%\t{:.2f}%\t{:.2f}%\t{:.2f}%".format(result["pos_in"] + result["pos_out"], result["neg_in"] + result["neg_out"], result["unk_in"] + result["unk_out"], 100*result["cov_all"], 100*result["prec_all"], 100*result["rec_all"], 100*result["f1_all"])
		print(s)
	print()
	

if __name__ == "__main__":
	for lgpair in ("de-en", "fi-en", "lt-en", "ru-en", "en-de", "en-fi", "en-lt", "en-ru"):
		# path of the *.key.txt and *.domain.txt files
		keyfileprefix = "txt/{}".format(lgpair)
		# path of the detokenized translation output (one file per system)
		rawtranslations = "examples/{}/*".format(lgpair)
		# path of the lemmatized translation output (one file per system, same number of files and same ordering as detokenized files)
		lemtranslations = "examples/{}-lem/*.parsed.toklemma".format(lgpair)
		processLanguagePair(lgpair, keyfileprefix, rawtranslations, lemtranslations)
		
