# How to make multi language code
## requirments
What do you need ?
- Gnu gettext (installed on linux)
- Python
- Linux terminal
## Instructions
First you run the command pygettext3
`pygettext3 -d base main.py game_classes.py main.kv`\
Than u move the base.pot file to the folder where you want this template to be placed.\
Than you copy the base.pot file to your language folder
`cp base.pot ./locales/LANGUAGE/LC_MESSAGES/base.po`\
The LANGUAGE changed to your wanted language. There you edit the file with your translation.\
When you are done translating you have ot make the .mo file using
`msgfmt -o base.mo base`\
Than you are done and you have made the translation files.
## Source
Theory and making of .po and .mo files taken form\
https://phraseapp.com/blog/posts/translate-python-gnu-gettext/\
Code taken form\
https://github.com/tito/kivy-gettext-example