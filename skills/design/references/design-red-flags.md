# Design red flags

A red flag is a reason to revise or reject a shape. Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Prefer the design where a change that looks right from one file is right for the whole repo.

- **Shallow module.** A large interface hiding little. Callers coordinate several methods for one operation, or public options expose internal stages. A deep module concentrates capability behind a small surface; a deep call chain scatters it.
- **Information leakage.** Several modules depend on the same internal decision (a representation, policy, wire format), so changing it means coordinated edits. Re-exported transport or storage types are leakage.
- **Temporal decomposition.** Modules split by execution order (load, validate, transform, save) instead of by the knowledge they own, repeating one representation across stages.
- **Pass-through method.** Forwards the same arguments to another method of the same shape, adding a layer without hiding anything.
- **Split ownership.** More than one module writes the same state or keeps its own copy. Give each piece of state one owner.
- **Two ways to do one task.** An agent copies whichever it finds first, so both keep gaining callers. Keep one.
- **Importable internals.** Internals reachable from outside become interface. Make an outside import fail the build.
- **Hand-synced list.** The same items listed in several places. Keep one list and derive the rest, or make the build fail when they disagree.
- **Unguarded boundary.** External input reaching domain logic unparsed, an auth check living in the caller instead of the boundary, or a money or webhook path with no answer to "what if this runs twice".
