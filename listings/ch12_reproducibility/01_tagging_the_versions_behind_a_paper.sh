git tag -a v1.0-submission -m "Code used for the initial journal submission"
git push origin v1.0-submission

# After revisions
git tag -a v1.1-accepted -m "Code used for the accepted version"
git push origin v1.1-accepted

# Anyone can later recover exactly that version
git checkout v1.0-submission
