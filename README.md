# pyschedge

pyschedge is a python wrapper for the [Schedge API](https://schedge.a1liu.com).

# Installation
Run `pip install pyschedge`

# Formatting
Run `black src` before committing to ensure codes are formatted.

# Development
1. Run `python3 -m venv env` for a virtual environment
2. Install all the dependencies `pip install -r requirements.txt`
3. Run `deactivate` to exit your virtual environment

# Issue and PR
Feel free to make an issue for any bugs or enhancement and PR!

# Docs
```
get_courses(school, subject, full=False)

get_section(registration_number, full=False)

get_non_online()

check_schedule(*argv)

search_course(query, school="", subject="", title_weight=2, description_weight=1, notes_weight=0, prereqs_weight=0, full=False, limit=50)
```