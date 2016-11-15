#!/usr/bin/env python3

#################################################
# Theseus Services automatic deployment script  #
#              (~ ACE3 8e9c275)                 #
# ============================================= #
# This is not meant to be run directly!         #
#################################################

import os
import sys
import shutil
import traceback
import subprocess as sp
from github import Github, InputGitAuthor


TRANSLATIONISSUE = 1
TRANSLATIONBODY = """**[Translation Guide](https://github.com/Theseus-Aegis/TheseusServices/wiki/Translation-Guide)**

{}
"""

REPOUSER = "Theseus-Aegis"
REPONAME = "TheseusServices"
REPOPATH = "{}/{}".format(REPOUSER,REPONAME)
REPONAME_WIKI = "TheseusServices.wiki"
REPOPATH_WIKI = "{}/{}".format(REPOUSER,REPONAME_WIKI)

WIKI_CLASSNAMES_FILE = "Class-Names.md"


def update_translations(repo):
    diag = sp.check_output(["python3", "tools/stringtablediag.py", "--markdown"])
    diag = str(diag, "utf-8")
    issue = repo.get_issue(TRANSLATIONISSUE)
    issue.edit(body=TRANSLATIONBODY.format(diag))

def update_classnames(repo_wiki):
    print("ls: {}".format(os.listdir()))

    classnames_new = sp.check_output(["python3", "tools/export_classnames.py", "--print"])
    classnames_new = str(classnames_new, "utf-8")
    print("classnames_new: {}".format(classnames_new))

    classnames_old = repo_wiki.get_contents(WIKI_CLASSNAMES_FILE).content
    print("classnames_old: {}".format(classnames_old))

    diff = sp.check_output(["git", "diff", "--name-only", WIKI_CLASSNAMES_FILE])
    diff = str(diff, "utf-8")
    print("diff: {}".format(diff))

    if diff != "":
        sha = repo_wiki.get_contents(WIKI_CLASSNAMES_FILE).sha
        print("sha: {}".format(sha))
        repo_wiki.update_file(
            path="/{}".format(WIKI_CLASSNAMES_FILE),
            message="Update Class Names\nAutomatically committed through Travis CI.\n\n[ci skip]",
            content=classnames_new, sha=sha, comitter=InputGitAuthor("Theseus-Aegis", "info@theseus-aegis.com")
        )
        print("Class Names wiki page successfully updated.")
    else:
        print("Class Names wiki page update skipped - no change.")


def main():
    print("Obtaining token ...")
    try:
        token = os.environ["GH_TOKEN"]
        repo = Github(token).get_repo(REPOPATH)
    except:
        print("Could not obtain token.")
        print(traceback.format_exc())
        return 1
    else:
        print("Token successfully obtained.")

    print("\nUpdating translation issue ...")
    try:
        update_translations(repo)
    except:
        print("Failed to update translation issue.")
        print(traceback.format_exc())
        return 1
    else:
        print("Translation issue successfully updated.")

    print("\nUpdating Class Names wiki page ...")
    try:
        repo_wiki = Github(token).get_repo(REPOPATH_WIKI)
        update_classnames(repo_wiki)
    except:
        print("Failed to update Class Names wiki page.")
        print(traceback.format_exc())

        os.chdir("..")
        print("ls: {}".format(os.listdir()))

        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
