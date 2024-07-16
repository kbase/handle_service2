# Description of PR purpose/changes

-   Please include a summary of the change and which issue is fixed. 
-   Please also include relevant motivation and context.
-   List any dependencies that are required for this change.

# Jira Ticket / Issue

e.g. <https://kbase-jira.atlassian.net/browse/DATAUP-X>

-   [ ] Added the Jira Ticket to the title of the PR e.g. (DATAUP-69 Adds a PR template)

# Testing Instructions

-   Details for how to test the PR: 
-   [ ] Tests pass in github actions and locally
-   [ ] After deployment of the PR on CI, the following code block passes
-   [ ] Jobs that contact hs2 still run correctly, such as `Assess Quality of Assemblies with Quast` or `Example HTML Report`
```
curl -X POST -H "Authorization: $KBASE_TOKEN_CI" -d '{"id":42,"method":"AbstractHandle.hids_to_handles","params":[["KBH_202520"]]}' https://ci.kbase.us/services/handle_service | python -m json.tool
```
which results in
```
{"result": [[{"hid": "KBH_202520", "id": "62d6832d-fb3d-4644-8a86-70d3ed9586da", "file_name": "GCF_002136375.1_ASM213637v1_genomic.gbff", "type": "shock", "url": "https://ci.kbase.us/services/shock-api", "remote_md5": "d4fc8341d0be816739d121cc17b0065e", "remote_sha1": null, "created_by": "qzhang", "creation_date": 1497101498.0}]], "id": 42}
```

# Dev Checklist:

-   [ ] My code follows the guidelines at <https://sites.google.com/truss.works/kbasetruss/development>
-   [ ] I have performed a self-review of my own code
-   [ ] I have commented my code, particularly in hard-to-understand areas
-   [ ] I have made corresponding changes to the documentation, including updating the README with app information changes
-   [ ] My changes generate no new warnings
-   [ ] I have added tests that prove my fix is effective or that my feature works
-   [ ] New and existing tests pass locally with my changes
-   [ ] Any dependent changes have been merged and published in downstream modules

# Updating Version and Release Notes (if applicable)

-   [ ] [Version has been bumped](https://semver.org/) in `kbase.yml`
-   [ ] [Release notes](/RELEASE_NOTES.md) have been updated for each release (and during the merge of feature branches)
