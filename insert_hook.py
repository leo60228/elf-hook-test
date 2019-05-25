#!/usr/bin/env python3

# Description
# -----------
# Hook the 'clock' function from the standard math library (libc)

import lief

libc = lief.parse("/nix/store/681354n3k44r8z90m35hm8945vsp95h1-glibc-2.27/lib/libc.so.6")
hook = lief.parse("hook.o")

bss_idx = next((idx for idx, val in enumerate(hook.sections) if val.name == ".bss"))
bss = hook.sections[bss_idx]

bss_syms = [x for x in hook.symbols if x.shndx is bss_idx and x.type != lief.ELF.SYMBOL_TYPES.SECTION]

print(bss.size)
print([x.shndx for x in hook.symbols])
print([x.name for x in bss_syms])
print([x.type for x in bss_syms])

target_bss_idx = next((idx for idx, val in enumerate(libc.sections) if val.name == ".bss"))
target_bss = libc.sections[bss_idx]

for sym in bss_syms:
    print("injecting symbol", sym.name)
    sym.shndx = target_bss_idx
    if sym.is_static:
        libc.add_dynamic_symbol(sym)
    else:
        libc.add_static_symbol(sym)
    libc.export_symbol(sym) # FOR DEBUGGING, REMOVE LATER

libc.write("libc.so.6")

#libc = lief.parse("/nix/store/681354n3k44r8z90m35hm8945vsp95h1-glibc-2.27/lib/libc.so.6")
#hook = lief.parse("hook")
#
#hook_sym = hook.get_symbol("hook")
#
#hook_text = next(x for x in hook.segments if any(x.name == ".text" for x in x.sections))
#
#print(hook_text.virtual_address)
#print(hook_sym.value)
#
#segment_added = libc.add(hook_text)
#
#hook_addr = segment_added.virtual_address + hook_sym.value
#
#print("Hook inserted at VA: 0x{:06x}".format(segment_added.virtual_address))
#print("hook(void) = 0x{:06x}".format(hook_addr))
#
#libc.write("libc.so.6")
