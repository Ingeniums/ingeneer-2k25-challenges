import angr, claripy

# We see in main that the flag is derived from password:
#
# if ( derive_flag_from_password(password, flag) )
# {
#   printf(
#     "I can't believe you were able to figure out my password too! "
#     "There must be some trickery going on! "
#     "But fine, here is your reward\n");
#   printf(flag);
#   return 1;
# }
#
# We'll execute 'derive_flag_from_password' symbolically
# with the end constraint that it must return non-zero.
#
# The branches to avoid are places where 0 is returned.
# In assembly it's just 'xor eax, eax' followed by a jump to the return block.
# Addresses:
# .text:000000014000148F
# .text:00000001400013C9
# .text:000000014000124F
#

# Let's setup an Angr project with base address 0
opts = {"base_addr": 0}
project = angr.Project("./n", auto_load_libs=False, main_opts=opts)

# Define our entry state to start at the beginning of 'derive_flag_from_password'
s0 = project.factory.entry_state(addr=0x1420)
# Usual angr stuff to prevent warnings
s0.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY)
s0.options.add(angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS)

# Let's store a symbolic password of size 29 (because 'scanf(" %29[^\n]", password);')
# in an unused memory region.
symchars = [claripy.BVS("flag", 8) for _ in range(29)]
symdat = claripy.Concat(*symchars, claripy.BVV(b"\n"))
s0.memory.store(0x10000, symdat, symdat.size() // 8)

# Set rcx (first arg) to be the address of our symbolic password.
s0.regs.rcx = 0x10000
# Set rdx (second arg) to be the address of an unused memory region.
# Flag will be written there.
s0.regs.rdx = 0x20000

# Constrain our password characters in the printable range.
for sc in symchars:
    s0.solver.add(sc < 127)
    s0.solver.add(sc > 31)

# Let's get a simulation manager to explore from our state.
sm = project.factory.simulation_manager(s0)
# Explore until it reaches the return block of the function at 0x14FE
# while avoiding the places where it would return 0.
sm.explore(find=0x14FE, avoid=(0x148F, 0x13C9, 0x124F))

# It found a path, let's get the end state.
se = sm.found[0]

# Constraint the return value (rax) to be non-zero.
se.solver.add(se.regs.rax != 0)

# Solve and evaluate the memory pointed by our second argument.
# Load enough bytes since I don't want to bother looking at the malloc arg.
sol = se.solver.eval(se.memory.load(0x20000, 50), cast_to=bytes)

# R-Strip the 0s and display the flag.
print(sol.rstrip(b"\0").decode())