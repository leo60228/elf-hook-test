#!/usr/bin/env python3

# Description
# -----------
# Hook the 'clock' function from the standard math library (libc)

import lief

libc = lief.parse("/nix/store/681354n3k44r8z90m35hm8945vsp95h1-glibc-2.27/lib/libc.so.6")
hook = lief.parse("hook")

hook_text = next(x for x in hook.segments if any(x.name == ".text" for x in x.sections))

segment_added = libc.add(hook_text)

print("Hook inserted at VA: 0x{:06x}".format(segment_added.virtual_address))

libc.write("libc.so.6")
