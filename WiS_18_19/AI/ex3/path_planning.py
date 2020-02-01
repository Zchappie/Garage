from collections import deque
from utils import expr

class PathPlanner:
    def __init__(self, minefield, kb, stop_on_risk = False):
        self.kb = kb
        self.minefield = minefield

        self._visited_field_cache = [[False]*minefield.dim_y
                                     for x in range(minefield.dim_x)]
        self._free_field_cache = [[False]*minefield.dim_y
                                  for x in range(minefield.dim_x)]
        self._mined_field_cache = [[False]*minefield.dim_y
                                   for x in range(minefield.dim_x)]

        self.not_checked_pos = []
        for ptx in range(minefield.dim_x):
            for pty in range(minefield.dim_y):
                self.not_checked_pos.append((ptx,pty))
        
        self._possible_targets = set()

        self.target = None
        self.risky_target = False

        self._risky_alert = False
        self.stop_on_risk = stop_on_risk
    def _expand_possible_targets(self, ptx, pty):
        if (ptx, pty) in self._possible_targets:
            self._possible_targets.remove((ptx, pty))
        for sptx, spty in self.minefield.surrounding_positions(ptx, pty):
            if not self._visited_field_cache[sptx][spty] and not self._mined_field_cache[sptx][spty]:
                self._possible_targets.add((sptx, spty))
    def _update_target(self):
        def ask(prop):
            print("ask:", prop, end="")
            if self.kb.ask(prop):
                print(" ≡ True")
                return True
            else:
                print(" ≡ ?")
                return False
        
        if self.target not in self._possible_targets:
            self.target = None
        if self.target == None:
            for ptx, pty in sorted(set(self._possible_targets),
                                   key =
                                    lambda pt:
                                        abs(self.minefield.bot_pos[0]-pt[0])+\
                                        abs(self.minefield.bot_pos[1]-pt[1])+\
                                        abs(self.minefield.goal_pos[0]-pt[0]) +\
                                        abs(self.minefield.goal_pos[1]-pt[1])):
                assert not self._visited_field_cache[ptx][pty]
                assert not self._mined_field_cache[ptx][pty]
                if self._free_field_cache[ptx][pty]:
                    self.target = ptx, pty
                    self.risky_target = False
                    break
                elif ask(expr("~B%i%i" % (ptx,pty))):
                    self._free_field_cache[ptx][pty] = True
                    self.target = ptx, pty
                    self.risky_target = False
                    break
            if self.target != None:
                print("target field:", self.target,
                      "(this target is not proven safe)"*self.risky_target)
                print("inferring cells...")
                for i in range(len(self.not_checked_pos) - 1, -1, -1):
                    ptx, pty = self.not_checked_pos[i]
                    if self.kb.ask(expr("~B%i%i" % (ptx,pty))):
                        self.minefield.add_known_pos(ptx,pty)
                        del self.not_checked_pos[i]
                    elif self.kb.ask(expr("B%i%i" % (ptx,pty))):
                        self.minefield.add_known_pos(ptx,pty)
                        del self.not_checked_pos[i]
                print("done.")
        while self.target == None:
            if not self._risky_alert:
                self._risky_alert = True
                print("There is no target for the robot left to choose, which "+\
                      "can be proven mine free. So either your knowledge base "+\
                      "needs more rules to solve this minefield, or the"+\
                      " minefield is actually not solvable. (All provided "+\
                      "fields should be.)")
                if self.stop_on_risk: return
            if len(self._possible_targets) == 0:
                raise RuntimeError("there is apparently no solution")
            self.target = min(self._possible_targets,
                              key = lambda pt:
                                  abs(self.minefield.bot_pos[0]-pt[0])+\
                                  abs(self.minefield.bot_pos[1]-pt[1])+\
                                  abs(self.minefield.goal_pos[0]-pt[0]) +\
                                  abs(self.minefield.goal_pos[1]-pt[1]))
            if ask(expr("B%i%i" % self.target)):
                self._mined_field_cache[self.target[0]][self.target[1]] = True
                if self.target in self._possible_targets:
                    self._possible_targets.remove(self.target)
                self.target = None
                continue
            self.risky_target = True
            print("target field:", self.target,
                  "(this target is not proven safe)"*self.risky_target)

    def next_move(self):
        self._visited_field_cache[self.minefield.bot_pos[0]][self.minefield.bot_pos[1]] = True
        self._free_field_cache[self.minefield.bot_pos[0]][self.minefield.bot_pos[1]] =\
            self.minefield.state_in_view() != -1
        self._expand_possible_targets(*self.minefield.bot_pos)

        self._update_target()
        if self.target == None: return

        paths = deque([(None,self.minefield.bot_pos)])
        pvisited = {self.minefield.bot_pos,}
        while True:
            prev_path, akt_pos = paths.popleft()
            for tx, ty in self.minefield.surrounding_positions(*akt_pos):
                if self.target == (tx, ty):
                    best_path = (prev_path, akt_pos), (tx, ty)
                    break
                elif self._free_field_cache[tx][ty] and (tx, ty) not in pvisited:
                    paths.append(((prev_path, akt_pos), (tx, ty)))
                    pvisited.add((tx, ty))
            else: continue
            break

        while best_path[0][0] != None:
            best_path = best_path[0]

        return best_path[1][0] - best_path[0][1][0], best_path[1][1] - best_path[0][1][1]
