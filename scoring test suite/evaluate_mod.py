#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a slightly modified version of the evaluator from the ContraWSD project: https://github.com/a-rios/ContraWSD

from __future__ import division, print_function, unicode_literals
import sys
reload(sys);
sys.setdefaultencoding("utf8")
import json
import argparse
from collections import defaultdict, OrderedDict
from operator import gt, lt
import scipy
import scipy.stats

# usage: python evaluate_mod.py -r json < scores > output
# by default, lower scores (closer to zero for log-prob) are better
      

def count_errors(reference, scores, maximize, verbose):
    """read in scores file and count number of correct decisions"""

    reference = json.load(reference)

    results = {'by_origin': defaultdict(lambda: defaultdict(int)),
               'by_category': defaultdict(lambda: defaultdict(int))
	       }

    if maximize:
        better = gt
    else:
        better = lt

    for sentence in reference:
        score = float(scores.readline())
        all_better = True
        category = sentence['ambig word'] + ":" + sentence['sense']
        origin = sentence['origin']
        results['by_category'][category]['total'] += 1
        results['by_origin'][origin]['total'] += 1
       
        for error in sentence['errors']:
            errorscore = float(scores.readline())
            if not better(score, errorscore):
                all_better = False


        if all_better:
            results['by_category'][category]['correct'] += 1
            results['by_origin'][origin]['correct'] += 1
            if verbose:    
	       print('\ncorrect:')
	       print('ambig. word: {0}'.format(sentence["ambig word"]))
	       print('original translation: {0}'.format(sentence["original translation"]))
	       print('source: {0}'.format(sentence["source"]))
	       print('reference: {0}'.format(sentence["reference"]))
	elif verbose:
	       print('\nwrong:')
	       print('ambig. word: {0}'.format(sentence["ambig word"]))
	       print('original translation: {0}'.format(sentence["original translation"]))
	       print('source: {0}'.format(sentence["source"]))
	       print('reference: {0}'.format(sentence["reference"]))

    return results 

def get_scores(category):
    correct = category['correct']
    total = category['total']
    if total:
        accuracy = correct/total
    else:
        accuracy = 0
    return correct, total, accuracy


def print_statistics(results):

    correct = sum([results['by_category'][category]['correct'] for category in results['by_category']])
    total = sum([results['by_category'][category]['total'] for category in results['by_category']])
    print('{0} : {1} {2} {3}'.format('total', correct, total, correct/total))


def print_statistics_by_category(results):

    for category in sorted(results['by_category']):
        correct, total, accuracy = get_scores(results['by_category'][category])
	if total:
            print('{0} : {1} {2} {3}'.format(category, correct, total, accuracy))

def print_statistics_by_origin(results):

    for category in sorted(results['by_origin']):
        correct, total, accuracy = get_scores(results['by_origin'][category])
	if total:
            print('{0} : {1} {2} {3}'.format(category, correct, total, accuracy))


def main(reference, scores, maximize, verbose ):

    results = count_errors(reference, scores, maximize, verbose)

    print_statistics(results)
    print()
    print('statistics by error origin')
    print_statistics_by_origin(results)
    print()
    print('statistics by error category, ambiguous word:sense')
    print_statistics_by_category(results)
    print()

   

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument( '--verbose', '-v', action="store_true", help="verbose mode (prints out all wrong classifications)")
    parser.add_argument('--maximize', action="store_true", help="Use for model where higher means better (probability; log-likelhood). By default, script assumes lower is better (negative log-likelihood).")
    parser.add_argument('--reference', '-r', type=argparse.FileType('r'),
                        required=True, metavar='PATH',
                        help="Reference JSON file")
    parser.add_argument('--scores', '-s', type=argparse.FileType('r'),
                        default=sys.stdin, metavar='PATH',
                        help="File with scores (one per line)")

    args = parser.parse_args()

    main(args.reference, args.scores, args.maximize, args.verbose)
