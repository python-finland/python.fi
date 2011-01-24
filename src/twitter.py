"""

    Generate Twitter link list

"""

input = """@2gen
@EsaMatti
@Soft
@Teemu
@akaihola
@akhern
@ariflinkman
@ecyrd
@hagnas
@jlaurila
@kpuputti
@linjaaho
@mikharj
@moo9000
@nailor
@pyconfinland
@roxeteer
@saffe
@teelmo
@tkoola
@tsharju
@uninen
"""

print "<ul>"
for line in input.split("\n"):
    line = line.strip()
    line = line.strip("@")
    print '<li><a href="http://twitter.com/%s">%s</a></li>' % (line, line)
print "</ul>"
