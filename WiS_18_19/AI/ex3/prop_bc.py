from logic import conjuncts

def prop_bc(kb, alpha):
    def bc(prop):
        if prop in bc_rule_cache.keys():
            return bc_rule_cache[prop]
        else:
            prove_bsbls = set()
            for clause in kb.clauses:
                if clause.op in ("==>", "<=>"):
                    if prop in conjuncts(clause.args[1]):
                        prove_bsbls.add(frozenset(conjuncts(clause.args[0])))
                if clause.op in ("<==", "<=>"):
                    if prop in conjuncts(clause.args[0]):
                        prove_bsbls.add(frozenset(conjuncts(clause.args[1])))
            prove_bsbls = frozenset(prove_bsbls)
            bc_rule_cache[prop] = prove_bsbls
            return prove_bsbls
    def bc_unprovable():
        bc_unbrovable_cache.add(bc_stack[-1][-1][-1])
        bc_stack[-1].pop()
    def bc_proven():
        kb.clauses.add(bc_stack[-1][-1].pop())
    def bc_clear_visited():
        bc_visited.remove(bc_stack[-1][-1][-1])

    bc_stack = [[[alpha]]]
    bc_rule_cache = {}
    bc_visited = set()
    bc_unbrovable_cache = set()

    while True:
        if len(bc_stack) == 0:
            return True
        elif len(bc_stack[-1]) == 0:
            bc_stack.pop()
            if len(bc_stack) == 0:
                return False
            bc_clear_visited()
            bc_unprovable()
            continue
        elif len(bc_stack[-1][-1]) == 0:
            bc_stack.pop()
            if len(bc_stack) == 0:
                return True
            bc_clear_visited()
            bc_proven()
            continue

        prop = bc_stack[-1][-1][-1]
        if prop in kb.clauses:
            bc_proven()
            continue
        if prop in bc_unbrovable_cache or prop in bc_visited:
            bc_unprovable()
            continue
        else:
            bc_visited.add(prop)
        bc_stack.append(sorted(map(list, bc(prop)), key=len))
