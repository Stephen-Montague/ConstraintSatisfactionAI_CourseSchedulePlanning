#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stephen Montague
22 Feb 2020
Spring 2020 Term 1
AI - 1: Machine Problem 3 - CSP

Summary:

This program demos a Constraint Satisfaction Problem to provide a number of possible degree
plans, and a sample degree plan based on the data provided. The general approach is to set
variables to courses and domains to terms available. Each elective has a single domain term
greater than the full term range (1-14) to allow for non-enrollment.

By inference from the given end-date and number of courses required, only one term may be
skipped and still finish on time, so the skipped term was treated like a variable,
with a domain of all terms -1 from last term, however, seeing that Summer Term 2 only has
1 course offered, one year taking that course and the next year to skip, or vice-versa, is
inevitable, given the completion deadline and number of courses required.  This inference
allows us to reduce the domains of 2 variables and to allow treating one course as a core
course instead of as an elective.

This implementation could be more robust by importing data rather than encoding values,
although to complete on time (not having used Pandas before), I've implemented as below.
This implementation solves a specific CSP and won't generalize without modification, but
on the other hand, it seems simple, direct, and highly readable.

"""

from constraint import *


def prereqSatisfied(courseTerm, prereqTerm):
    # Course order is compared by domain term number,
    # where a higher term number means a later term.
    return courseTerm > prereqTerm


# INSTANTIATE CSP

problem = Problem()

# ADD VARIABLES & DOMAINS

# Variables added in the order of 'Course Rotation' sheet,
# Each course option is a variable, from A to S (19 total),
# that has a domain of term numbers, selected from 1 to 21,
# where terms 1 to 14 are enrolled (and > 14 are 'Not taken')
# so that order of enrollments are indicated by term number.

# For example, (Year 1 Fall 1) is 1, (Year 1 Fall 2) is 2, etc.
# where the last term of enrollment (Year 3 Fall 2) is 14.

# For exact variable to course-name map, see end 'courseNames'
# Course as variable & term as domain ensures 1 term / course.
problem.addVariable('A', [1, 2, 3, 5, 7, 8, 9, 11, 13, 14])  # Foundation & Core A - I
problem.addVariable('B', [1, 3, 5, 7, 9, 11, 13])
problem.addVariable('C', [2, 4, 8, 10, 14])
problem.addVariable('D', [4, 10])
problem.addVariable('E', [1, 5, 7, 11, 13])
problem.addVariable('F', [1, 3, 5, 7, 9, 11, 13])
problem.addVariable('G', [2, 5, 8, 11, 14])
problem.addVariable('H', [2, 3, 8, 9, 14])
problem.addVariable('I', [1, 5, 7, 11, 13])
problem.addVariable('J', [1, 3, 5, 7, 9, 11, 13, 15])  # Electives J - Q, each has 1 domain > 14 to allow non-enrollment
problem.addVariable('K', [2, 8, 14, 16])
problem.addVariable('L', [6, 12])  # Domain reduced by inference, along with 'S' is the only offering for Summer 2
problem.addVariable('M', [2, 8, 14, 17])
problem.addVariable('N', [1, 4, 7, 10, 13, 18])
problem.addVariable('O', [3, 9, 19])
problem.addVariable('P', [5, 11, 20])
problem.addVariable('Q', [4, 10, 21])
problem.addVariable('R', [2, 4, 5, 8, 10, 11, 14])  # Capstone
problem.addVariable('S', [6, 12])  # 'S' is a 'skip' term, so to finish on-time, can only occur once, opposite 'L'

# ADD CONSTRAINTS

# For each course assign a different term
problem.addConstraint(AllDifferentConstraint())

# Ensure all 14 domain terms are assigned, which guarantees elective enrollment
problem.addConstraint(SomeInSetConstraint({1}))
problem.addConstraint(SomeInSetConstraint({2}))
problem.addConstraint(SomeInSetConstraint({3}))
problem.addConstraint(SomeInSetConstraint({4}))
problem.addConstraint(SomeInSetConstraint({5}))
problem.addConstraint(SomeInSetConstraint({6}))
problem.addConstraint(SomeInSetConstraint({7}))
problem.addConstraint(SomeInSetConstraint({8}))
problem.addConstraint(SomeInSetConstraint({9}))
problem.addConstraint(SomeInSetConstraint({10}))
problem.addConstraint(SomeInSetConstraint({11}))
problem.addConstraint(SomeInSetConstraint({12}))
problem.addConstraint(SomeInSetConstraint({13}))
problem.addConstraint(SomeInSetConstraint({14}))

# Enforce prerequisites - given capstone 'R', prereq
problem.addConstraint(prereqSatisfied, ['R', 'A'])
problem.addConstraint(prereqSatisfied, ['R', 'B'])
problem.addConstraint(prereqSatisfied, ['R', 'C'])
problem.addConstraint(prereqSatisfied, ['R', 'D'])
problem.addConstraint(prereqSatisfied, ['R', 'E'])
problem.addConstraint(prereqSatisfied, ['R', 'F'])
problem.addConstraint(prereqSatisfied, ['R', 'G'])
problem.addConstraint(prereqSatisfied, ['R', 'H'])
problem.addConstraint(prereqSatisfied, ['R', 'I'])

# Enforce prerequisites - given course, prereq
problem.addConstraint(prereqSatisfied, ['F', 'A'])
problem.addConstraint(prereqSatisfied, ['E', 'A'])
problem.addConstraint(prereqSatisfied, ['G', 'A'])
problem.addConstraint(prereqSatisfied, ['H', 'A'])
problem.addConstraint(prereqSatisfied, ['I', 'A'])
problem.addConstraint(prereqSatisfied, ['K', 'A'])
problem.addConstraint(prereqSatisfied, ['M', 'A'])
problem.addConstraint(prereqSatisfied, ['N', 'A'])
problem.addConstraint(prereqSatisfied, ['O', 'A'])
problem.addConstraint(prereqSatisfied, ['P', 'O'])
problem.addConstraint(prereqSatisfied, ['Q', 'O'])
problem.addConstraint(prereqSatisfied, ['D', 'C'])

# SOLVE & PRINT

solution = sorted(problem.getSolution().items(), key=lambda kv: (kv[1], kv[0]))

# Map variable name (A-S) to course name or the 'skip' term option
courseNames = {'A': "CPSC-50100",
               'B': "MATH-51000",
               'C': "MATH-51100",
               'D': "MATH-51200",
               'E': "CPSC-51000",
               'F': "CPSC-51100",
               'G': "CPSC-53000",
               'H': "CPSC-54000",
               'I': "CPSC-55000",
               'J': "CPSC-50600",
               'K': "CPSC-51700",
               'L': "CPSC-52500",
               'M': "CPSC-55200",
               'N': "CPSC-55500",
               'O': "CPSC-57100",
               'P': "CPSC-57200",
               'Q': "CPSC-57400",
               'R': "CPSC-59000",
               'S': "Not taken"}  # Skip term

# Print Report
print("CLASS: Artificial Intelligence, Lewis University")
print("NAME: Stephen Montague")

print("\nSTART TERM = Year 1 Fall 1")
print("Number of Possible Degree Plans:", len(problem.getSolutions()))

print("\nSample Degree Plan: ")
print("Not Taken\t\t\t", courseNames[solution[14][0]])
print("Not Taken\t\t\t", courseNames[solution[15][0]])
print("Not Taken\t\t\t", courseNames[solution[16][0]])
print("Not Taken\t\t\t", courseNames[solution[17][0]])
print("Not Taken\t\t\t", courseNames[solution[18][0]])
print("Year 1 Fall 1\t\t", courseNames[solution[0][0]])
print("Year 1 Fall 2\t\t", courseNames[solution[1][0]])
print("Year 1 Spring 1\t\t", courseNames[solution[2][0]])
print("Year 1 Spring 2\t\t", courseNames[solution[3][0]])
print("Year 1 Summer 1\t\t", courseNames[solution[4][0]])

if courseNames[solution[5][0]] == "Not taken":
    print("Year 2 Fall 1\t\t", courseNames[solution[6][0]])  # Skip solution[5][0], means Term 6 not taken
    print("Year 2 Fall 2\t\t", courseNames[solution[7][0]])
    print("Year 2 Spring 1\t\t", courseNames[solution[8][0]])
    print("Year 2 Spring 2\t\t", courseNames[solution[9][0]])
    print("Year 2 Summer 1\t\t", courseNames[solution[10][0]])
    print("Year 2 Summer 2\t\t", courseNames[solution[11][0]])
    print("Year 3 Fall 1\t\t", courseNames[solution[12][0]])
    print("Year 3 Fall 2\t\t", courseNames[solution[13][0]])
else:
    print("Year 1 Summer 2\t\t", courseNames[solution[5][0]])
    print("Year 2 Fall 1\t\t", courseNames[solution[6][0]])
    print("Year 2 Fall 2\t\t", courseNames[solution[7][0]])
    print("Year 2 Spring 1\t\t", courseNames[solution[8][0]])
    print("Year 2 Spring 2\t\t", courseNames[solution[9][0]])
    print("Year 2 Summer 1\t\t", courseNames[solution[10][0]])  # Skip solution[11][0], means Term 12 not taken
    print("Year 3 Fall 1\t\t", courseNames[solution[12][0]])
    print("Year 3 Fall 2\t\t", courseNames[solution[13][0]])
