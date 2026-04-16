# Project Name & Description
Bible Verse Flashcards

A Python-based flashcard application that helps users memorize Bible verses (or other topics, depending on file provided) through progress tracking. The app presents verse references and requires users to type the full verse from memory, reinforcing learning through repetition. The app utilizes tkinter and pandas.

## Features

* Displays randomly chosen verse references for recall-based learning
* Provides optional hints (first 3 words of the verse)
* Tracks progress by removing correctly learned verses
* Saves progress using a CSV file so users can continue later
* Includes a practice mode for incorrect answers
* Automatically resets when all verses are learned

## Technologies

* Python
* Tkinter
* Pandas
* CSV Files

## How It Works
* The given verses are loaded from a CSV file
* A random verse reference is shown
* The user types the verse from memory (or chooses to receive a hint)
* If correct, the verse is removed from the learning set
* If incorrect, the user enters practice mode (they write the correct verse) and the verse is shuffled back into the learning set
* Progress is saved for future sessions
* The app automatically resets when all verses are learned

## How To Run
* Install pandas
* Edit bible_verses.csv as desired (or change to different flashcard topics)

