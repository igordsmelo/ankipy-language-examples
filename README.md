# AnkiPy - Language Examples

A simple library with the purpose of adding examples (in text and audio) to Anki cards.

It uses [Tatoeba](https://tatoeba.org)'s database text files as the source for the phrases to be added to your cards.


This script requires:
- [Anki](https://apps.ankiweb.net) open and running.
- [AnkiConnect](https://github.com/FooSoft/anki-connect) to be set up.
- [Tatoeba Sentence Pairs](https://tatoeba.org/en/downloads) in the desired language(s).

If this code is useful to you, consider contributing to Tatoeba.

# To-do
- [ ] Turn code into an Anki add-on
- [ ] Simplify workflow, make it suit for the default Anki deck.
  - [ ] Clear certain defaults to make code better suit for general use.
  - [ ] Check for existence of certain fields, and create them if needed.
  - [ ] Allow the user to change which fields certain data will be stored in.
- [ ] Allow the access of Tatoeba's database directly (if allowed by them, and if it's fast)