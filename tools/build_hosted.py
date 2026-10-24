# Builds the shareable copy of the game for the claude.ai page from index.html.
# The page host wraps the file in its own doctype/head/body, so those tags go; its viewport meta replaces ours.
# MIDI devices can't be reached from the host's frame; the game hides those controls itself (midiPossible). .mid export works (downloads capability).
import re,sys,os
# usage: python3 tools/build_hosted.py <output.html>   (then publish that file to the claude.ai link)
src=open(os.path.join(os.path.dirname(__file__),'..','index.html')).read()
out=src
out=re.sub(r'<!doctype html>\s*','',out,flags=re.I)
out=re.sub(r'</?html[^>]*>\s*','',out)
out=re.sub(r'</?head>\s*','',out)
out=re.sub(r'</?body>\s*','',out)
out=re.sub(r'<meta charset="utf-8">\s*','',out)
out=re.sub(r'<meta name="viewport"[^>]*>\s*','',out)
extra=':root{color-scheme:dark}\n'   # MIDI: the game hides device controls itself where the frame blocks Web MIDI; .mid export goes through the downloads capability
out=out.replace('<style>\n','<style>\n'+extra,1)
assert out.lstrip().startswith('<title>'),out[:80]
open(sys.argv[1],'w').write(out)
print(len(out),'bytes; rev',re.search(r"const REV=(\d+)",out).group(1))
