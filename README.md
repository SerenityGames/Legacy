# Legacy
[![Build Status](https://travis-ci.org/SerenityGames/Legacy.svg?branch=master)](https://travis-ci.org/SerenityGames/Legacy)

This site was created to replace the Serenity Games home page and to give members
a way to connect with each other. It is meant to be easily
maintainable, portable, and secure.

# Updating your page
Pages have what's called [front matter](https://jekyllrb.com/docs/frontmatter/). This defines who the user is and is where you can provide links for other members to find you on the web. Twitter, Steam, and Facebook will automatically add their respective icon (examples below). Only change your color code if it incorrectly matches your last known status on Serenity Games.

**Example:**
```
---
color: F55
links:
- handle: tjbenator
  name: twitter
- handle: tjbenator
  name: steam
- name: binarypenguin.net
  url: https://binarypenguin.net
username: tjbenator
---
My bio goes here.
```
