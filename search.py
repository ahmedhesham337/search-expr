# NOTE TO STUDENT: Please read the handout before continuing.

from tilegameproblem import TileGame
from dgraph import DGraph
from queue import Queue, LifoQueue, PriorityQueue

import matplotlib.pyplot as plt 
import networkx as nx 
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

from sys import argv
from time import sleep

class bfs():
    
    def __init__(self, problem, ns=20, sleeptime=1):
        self.problem = problem
        self.front   = Queue()
        self.reached = set()
        self.current = problem.get_start_state()
        self.prev    = {self.current: None}
        self.graph   = nx.Graph()
        self.tkRoot  = Tk()
        self.fig     = plt.figure(1, frameon=True, figsize=(5,1), dpi=100)
        self.canvas  = FigureCanvasTkAgg(self.fig, self.tkRoot)
        self.sol     = []
        self.solved  = False
        self.stop    = False
        self.ns      = ns
        self.sleept  = sleeptime
        self.lck     = True
        self.nsteps  = 0

        plt.gca().set_facecolor("grey")
        
        self.fig.set_facecolor("black")
        self.graph.add_node(TileGame.board_to_pretty_string(self.current))

        self.front.put(self.current)
        self.reached.add(self.current)

        self.tkRoot.title("BFS")

        self.redraw()

        if self.problem.is_goal_state(self.current):
            self.sol    = [self.current]
            self.solved = True
    
    def redraw(self, node_color=None):
        if node_color is None:
            cc = "green"
        else:
            cc = node_color
        plt.clf()
        nx.draw_networkx(self.graph, node_color=cc, pos=nx.spring_layout(self.graph, 25), alpha=1, node_size=1100, with_labels=True)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def next_step(self):

        if self.stop:
            return

        print(self.current)

        if self.lck:
            self.lck = False
            sleep(self.sleept)

        if self.solved:
            self.stop = True
            self.tkRoot.after(self.ns, self.next_step)
            print("steps: {}".format(self.nsteps))
            print("path length: {}".format(len(self.sol)))
            return

        self.current = self.front.get()
        
        if self.problem.is_goal_state(self.current):
            self.sol = []
            self.sol.append(self.current)
            while self.prev[self.current] is not None:
                self.sol.append(self.prev[self.current])
                self.current = self.prev[self.current]
            self.sol    = self.sol[::-1]
            self.solved = True
            
            color_map = []
            sol_str = []
            
            for node in self.sol:
                sol_str.append(TileGame.board_to_pretty_string(node))
            
            for node in self.graph:
                if node in sol_str:
                    if sol_str.index(node) == len(sol_str)-1:
                        color_map.append("green")
                    else:
                        color_map.append("blue")
                else:
                    color_map.append("red")
            
            color_map[0] = "yellow"
            self.redraw(node_color=color_map)
            self.tkRoot.after(self.ns, self.next_step)
            return
        
        successors = self.problem.get_successors(self.current)
        for state in successors:
            if not state in self.reached:
                self.graph.add_node(TileGame.board_to_pretty_string(state))
                self.reached.add(state)
                self.front.put(state)
                self.prev[state] = self.current
                self.graph.add_edge(TileGame.board_to_pretty_string(self.current), TileGame.board_to_pretty_string(state))
        self.redraw()
        self.nsteps += 1
        self.tkRoot.after(self.ns, self.next_step)

    def start(self):
        self.tkRoot.after(self.ns, self.next_step)
        #self.tkRoot.attributes("-zoomed", True)
        self.tkRoot.state("zoomed")
        self.tkRoot.mainloop()

class dfs():
    
    def __init__(self, problem, ns=20, sleeptime=1):
        self.problem = problem
        self.front   = LifoQueue()
        self.current = problem.get_start_state()
        self.prev    = {self.current: None}
        self.reached = set()
        self.graph   = nx.Graph()
        self.tkRoot  = Tk()
        self.fig     = plt.figure(1, frameon=True, figsize=(5,1), dpi=100)
        self.canvas  = FigureCanvasTkAgg(self.fig, self.tkRoot)
        self.sol     = []
        self.solved  = False
        self.stop    = False
        self.ns      = ns
        self.sleept  = sleeptime
        self.lck     = True
        self.nsteps  = 0

        plt.gca().set_facecolor("grey")
        
        self.fig.set_facecolor("black")
        self.graph.add_node(TileGame.board_to_pretty_string(self.current))

        self.front.put(self.current)
        self.reached.add(self.current)

        self.tkRoot.title("DFS")

        self.redraw()

        if self.problem.is_goal_state(self.current):
            self.sol    = [self.current]
            self.solved = True
    
    def redraw(self, node_color=None):
        if node_color is None:
            cc = "green"
        else:
            cc = node_color
        plt.clf()
        nx.draw_networkx(self.graph, node_color=cc, pos=nx.spring_layout(self.graph, 25), alpha=1, node_size=1100, with_labels=True)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def next_step(self):

        if self.stop:
            return

        print(self.current)
        #print(self.front)

        if self.lck:
            self.lck = False
            sleep(self.sleept)

        if self.solved:
            self.tkRoot.after(self.ns, self.next_step)
            print("steps: {}".format(self.nsteps))
            print("path length: {}".format(len(self.sol)))
            self.stop = True
            return

        self.current = self.front.get()
        
        if self.problem.is_goal_state(self.current):
            self.graph.add_node(TileGame.board_to_pretty_string(self.current))
            if self.prev[self.current] is not None:
                self.graph.add_edge(TileGame.board_to_pretty_string(self.current), TileGame.board_to_pretty_string(self.prev[self.current]))
            self.sol = []
            self.sol.append(self.current)
            while self.prev[self.current] is not None:
                self.sol.append(self.prev[self.current])
                self.current = self.prev[self.current]
            self.sol    = self.sol[::-1]
            self.solved = True
            
            color_map = []
            sol_str = []
            
            for node in self.sol:
                sol_str.append(TileGame.board_to_pretty_string(node))
            
            for node in self.graph:
                if node in sol_str:
                    if sol_str.index(node) == len(sol_str)-1:
                        color_map.append("green")
                    else:
                        color_map.append("blue")
                else:
                    color_map.append("red")
            
            color_map[0] = "yellow"
            self.redraw(node_color=color_map)
            self.tkRoot.after(self.ns, self.next_step)
            return
        
        self.graph.add_node(TileGame.board_to_pretty_string(self.current))
        if self.prev[self.current] is not None:
            self.graph.add_edge(TileGame.board_to_pretty_string(self.current), TileGame.board_to_pretty_string(self.prev[self.current]))
        successors = self.problem.get_successors(self.current)
        for state in successors:
            if not state in self.reached:
                self.front.put(state)
                self.reached.add(state)
                self.prev[state] = self.current
        self.redraw()
        self.nsteps += 1
        self.tkRoot.after(self.ns, self.next_step)

    def start(self):
        self.tkRoot.after(self.ns, self.next_step)
        #self.tkRoot.attributes("-zoomed", True)
        self.tkRoot.state("zoomed")
        self.tkRoot.mainloop()

class ids():
    
    def __init__(self, problem, limit=200, ns=20, sleeptime=1):
        self.problem = problem
        self.front   = LifoQueue()
        self.current = problem.get_start_state()
        self.prev    = {self.current: None}
        #self.reached = set()
        self.graph   = nx.Graph()
        self.tkRoot  = Tk()
        self.fig     = plt.figure(1, frameon=True, figsize=(5,1), dpi=100)
        self.canvas  = FigureCanvasTkAgg(self.fig, self.tkRoot)
        self.sol     = []
        self.solved  = False
        self.ns      = ns
        self.sleept  = sleeptime
        self.lck     = True
        self.nsteps  = 0
        self.limit   = limit
        self.counter = 0
        self.currdep = 1
        self.stop    = False

        plt.gca().set_facecolor("grey")
        
        self.fig.set_facecolor("black")
        self.graph.add_node(TileGame.board_to_pretty_string(self.current))

        self.front.put(self.current)
        #self.reached.add(self.current)

        self.tkRoot.title("IDS")

        self.redraw()

        if self.problem.is_goal_state(self.current):
            self.sol    = [self.current]
            self.solved = True
    
    def redraw(self, node_color=None):
        if node_color is None:
            cc = "green"
        else:
            cc = node_color
        plt.clf()
        nx.draw_networkx(self.graph, node_color=cc, pos=nx.spring_layout(self.graph, 25), alpha=1, node_size=1100, with_labels=True)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def is_cyclic(self, state, parent):
        cur = parent
        while cur is not None:
            if cur == state:
                return True
            cur = self.prev[cur]

        return False

    def depth(self, state):
        cur = state
        depth = 0
        while cur is not None:
            cur = self.prev[cur]
            depth += 1
        #print("depth")
        return depth

    def clear(self):
        
        if self.currdep > self.limit:
            print("no answer")
            self.solved = True
            self.redraw()
            self.stop = True
            return 
        
        self.front   = LifoQueue()
        self.current = self.problem.get_start_state()
        self.prev    = {self.current: None}
        #self.reached.clear()
        self.graph.clear()
        #self.counter = 0
        self.currdep += 1

        self.front.put(self.current)
        #self.reached.add(self.current)
        self.redraw()

    def next_step(self):

        if self.stop:
            return

        #print(self.prev)

        if self.solved:
            self.tkRoot.after(self.ns, self.next_step)
            self.stop = True
            print("steps: {}".format(self.nsteps))
            print("path length: {}".format(len(self.sol)))
            return

        if self.lck:
            self.lck = False
            sleep(self.sleept)

        if self.front.empty():
            print("reached dep {}".format(self.currdep))
            self.clear()
            self.tkRoot.after(self.ns, self.next_step)
            return

        self.current = self.front.get()
        print(self.current)
        
        if self.problem.is_goal_state(self.current):
            self.graph.add_node(TileGame.board_to_pretty_string(self.current))
            if self.prev[self.current] is not None:
                self.graph.add_edge(TileGame.board_to_pretty_string(self.current), TileGame.board_to_pretty_string(self.prev[self.current]))
            self.sol = []
            #print(self.prev)
            self.sol.append(self.current)
            while self.prev[self.current] is not None:
                self.sol.append(self.prev[self.current])
                self.current = self.prev[self.current]
            self.sol    = self.sol[::-1]
            self.solved = True
            
            color_map = []
            sol_str = []
            
            for node in self.sol:
                sol_str.append(TileGame.board_to_pretty_string(node))
            
            for node in self.graph:
                if node in sol_str:
                    if sol_str.index(node) == len(sol_str)-1:
                        color_map.append("green")
                    else:
                        color_map.append("blue")
                else:
                    color_map.append("red")
            
            color_map[0] = "yellow"
            self.redraw(node_color=color_map)
            self.tkRoot.after(self.ns, self.next_step)
            return

        if self.depth(self.current) > self.currdep:
            print("      - depth viol: {}".format(self.depth(self.current)))
            self.tkRoot.after(self.ns, self.next_step)
            return

        self.graph.add_node(TileGame.board_to_pretty_string(self.current))
        if self.prev[self.current] is not None:
            self.graph.add_edge(TileGame.board_to_pretty_string(self.current), TileGame.board_to_pretty_string(self.prev[self.current]))
        print("      - valid")
        successors = self.problem.get_successors(self.current)
        print(successors)
        for state in successors:
            if self.is_cyclic(state, self.current):
                #print("      - cyclic viol")
                continue
            self.front.put(state)
            self.prev[state] = self.current
        self.redraw()
        self.nsteps += 1
        self.tkRoot.after(self.ns, self.next_step)

    def start(self):
        self.tkRoot.after(self.ns, self.next_step)
        #self.tkRoot.attributes("-zoomed", True)
        self.tkRoot.state("zoomed")
        self.tkRoot.mainloop()

class astar():
    def __init__(self, problem, ns=20, sleeptime=1):
        self.problem = problem
        self.front   = PriorityQueue()
        self.current = problem.get_start_state()
        self.prev    = {self.current: None}
        self.reached = set()
        self.graph   = nx.Graph()
        self.tkRoot  = Tk()
        self.fig     = plt.figure(1, frameon=True, figsize=(5,1), dpi=100)
        self.canvas  = FigureCanvasTkAgg(self.fig, self.tkRoot)
        self.sol     = []
        self.solved  = False
        self.ns      = ns
        self.sleept  = sleeptime
        self.lck     = True
        self.nsteps  = 0
        self.stop    = False

        plt.gca().set_facecolor("grey")
        
        self.fig.set_facecolor("black")
        self.graph.add_node(TileGame.board_to_pretty_string(self.current))

        self.front.put((self.heuristic(self.current), self.current))
        self.reached.add(self.current)

        self.tkRoot.title("ASTAR")

        self.redraw()

        if self.problem.is_goal_state(self.current):
            self.sol    = [self.current]
            self.solved = True
        
    def heuristic(self, state):
        cnt = 1
        err = 0
        
        for tu in state:
            for n in tu:
                if n != cnt:
                    err += 1
                cnt += 1
        
        return err
    
    def redraw(self, node_color=None):
        if node_color is None:
            cc = "green"
        else:
            cc = node_color
        plt.clf()
        nx.draw_networkx(self.graph, node_color=cc, pos=nx.spring_layout(self.graph, 25), alpha=1, node_size=1100, with_labels=True)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)
    
    def next_step(self):

        if self.stop:
            return

        #print(self.front)

        if self.lck:
            self.lck = False
            sleep(self.sleept)

        if self.solved:
            self.tkRoot.after(self.ns, self.next_step)
            print("steps: {}".format(self.nsteps))
            print("path length: {}".format(len(self.sol)))
            self.stop = True
            return

        self.current = self.front.get()[1]
        print(self.current)
        
        if self.problem.is_goal_state(self.current):
            self.graph.add_node(TileGame.board_to_pretty_string(self.current))
            if self.prev[self.current] is not None:
                self.graph.add_edge(TileGame.board_to_pretty_string(self.current), TileGame.board_to_pretty_string(self.prev[self.current]))
            self.sol = []
            self.sol.append(self.current)
            while self.prev[self.current] is not None:
                self.sol.append(self.prev[self.current])
                self.current = self.prev[self.current]
            self.sol    = self.sol[::-1]
            self.solved = True
            
            color_map = []
            sol_str = []
            
            for node in self.sol:
                sol_str.append(TileGame.board_to_pretty_string(node))
            
            for node in self.graph:
                if node in sol_str:
                    if sol_str.index(node) == len(sol_str)-1:
                        color_map.append("green")
                    else:
                        color_map.append("blue")
                else:
                    color_map.append("red")
            
            color_map[0] = "yellow"
            self.redraw(node_color=color_map)
            self.tkRoot.after(self.ns, self.next_step)
            return
        
        self.graph.add_node(TileGame.board_to_pretty_string(self.current))
        if self.prev[self.current] is not None:
            self.graph.add_edge(TileGame.board_to_pretty_string(self.current), TileGame.board_to_pretty_string(self.prev[self.current]))
        
        successors = self.problem.get_successors(self.current)
        for state in successors:
            if not state in self.reached:
                heur = self.heuristic(state)
                self.front.put((heur, state))
                self.reached.add(state)
                self.prev[state] = self.current
        self.redraw()
        self.nsteps += 1
        self.tkRoot.after(self.ns, self.next_step)

    def start(self):
        self.tkRoot.after(self.ns, self.next_step)
        #self.tkRoot.attributes("-zoomed", True)
        self.tkRoot.state("zoomed")
        self.tkRoot.mainloop()


def main():
    if (len(argv) != 2):
        print("argument...")
        return
    
    #tg = TileGame(2, start_state=((2,4), (1,3)))
    #tg  = TileGame(2, start_state=((4,3), (2,1)))
    #tg = TileGame(2)
    tg  = TileGame(3)
    sleeptime = 1
    ns = 10
    if argv[1] == "--bfs":
        test = bfs(tg, sleeptime=sleeptime, ns=ns)
    elif argv[1] == "--dfs":
        test = dfs(tg, sleeptime=sleeptime, ns=ns)
    elif argv[1] == "--ids":
        test = ids(tg, sleeptime=sleeptime, ns=ns)
    elif argv[1] == "--astar":
        test = astar(tg, sleeptime=sleeptime, ns=ns)
    else:
        print("err...")
        return
    test.start()
    return

if __name__ == "__main__":
    main()
