## Table of Contents
1. [Important Academic Dates & University Holidays](#important-academic-dates--university-holidays)
2. [Semester Assessment Roadmap](#semester-assessment-roadmap)
   - [Visual Assessment & Exam Options Timeline](#visual-assessment--exam-options-timeline)
   - [Curriculum & Module Map](#curriculum--module-map)
   - [Homework Lifecycle & Windows](#homework-lifecycle--windows)
   - [Midterm Exam Scheduling Options & Trade-Offs](#midterm-exam-scheduling-options--trade-offs)
   - [Complete Deliverables Master Table](#complete-deliverables-master-table)

---

## Important Academic Dates & University Holidays

| Date | Day | Event | Impact on Course Schedule |
| :--- | :--- | :--- | :--- |
| **Aug 24, 2026** | Monday | First Day of Classes | Semester begins; Week 1 Lab 0 meets |
| **Sep 07, 2026** | Monday | **Labor Day (No Classes)** | **No Monday Lab**; In-Class Quiz 1 held in Tue/Thu lecture |
| **Oct 12–13, 2026** | Mon–Tue | **Fall Break (No Classes)** | **No Monday Lab & No Tuesday Lecture**; Thursday Oct 15 class meets |
| **Nov 23–28, 2026** | Mon–Sat | **Thanksgiving Break (No Classes)** | **No Classes all week** (Recess between Week 13 and Week 14 content) |
| **Dec 08, 2026** | Tuesday | Last Day of Classes | Final lecture session & course retrospective |
| **Dec 09, 2026** | Wednesday | **Designated Monday** | **Follows Monday schedule**: Lab makeup session / review |
| **Dec 10–18, 2026** | Thu–Fri | Final Examinations | University-scheduled Final Exam date |

---

## Semester Assessment Roadmap

The course utilizes a balanced evaluation structure combining **6 lab quizzes (administered in Monday labs)**, **5 in-class quizzes (administered in lectures)**, **3 major programming/theory homework assignments**, and **2 major examinations** (1 Midterm Exam and 1 Final Exam).

### Visual Assessment & Exam Options Timeline

```
====================+=============================+=================+=======================+=================+=====+========
Course Module       |  Mod 1: Foundations & Trees |Mod 2: Hash/Graph| Mod 3: Opt & Sequences|Mod 4: Complexity|Rev. | Finals 
Assessment Track    | W01 | W02 | W03 | W04 | W05 | W06 | W07 | W08 | W09 | W10 | W11 | W12 | W13 | W14 | W15 | W16 | Finals 
Monday Date         |8/24 |8/31 |9/07 |9/14 |9/21 |9/28 |10/5 |10/12|10/19|10/26|11/2 |11/9 |11/16|11/23|11/30|12/7 | 12/10+ 
Academic Calendar   |     |     |Labor|     |     |     |     |Fall |     |     |     |     |     |Thnx-|     |     | Final  
                    |     |     | Day |     |     |     |     |Break|     |     |     |     |     |giv. |     |     | Period 
--------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+--------
Topic Focus (Area)  |Intro| D&C |Heaps| BST |B-Tre| Hash|Strng|Graph| MST |Flow |AdvDP| NLP |Local|Recss|Apprx|Rev. | All    
Topic Focus (Detail)|Big-O|Sort |Bcket| AVL |Splay|Tries|KMP  |BFS  |Dijk |DP 01|EditD|Viter|P vNP|Break|Randm|Synth| Topics 
--------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+--------
Lab Quizzes (Mon)   |     |     |     | LQ1 |     | LQ2 |     | LQ3*|     | LQ4 | LQ5 | LQ6 |     |  -  |     |     |        
In-Class Quizzes    |     |     | IC1 |     | IC2 |     | IC3 |     | IC4 |     |     |     | IC5 |  -  |     |     |        
--------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+--------
HW 1: Trees         |     |     |     |     |START|====>| DUE |     |     |     |     |     |     |  -  |     |     |        
HW 2: Graphs & MST  |     |     |     |     |     |     |     |START|====>| DUE |     |     |     |  -  |     |     |        
HW 3: Dynamic Prog. |     |     |     |     |     |     |     |     |     |     |START|====>| DUE |  -  |     |     |        
--------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+--------
Midterm: Option A   |     |     |     |     |     |     |*EXAM|     |     |     |     |     |     |  -  |     |     | (Oct 6 or 8)
Midterm: Option B   |     |     |     |     |     |     |     |*EXAM|     |     |     |     |     |  -  |     |     | (Oct 15)
--------------------+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+-----+--------
Final Examination   |     |     |     |     |     |     |     |     |     |     |     |     |     |  -  |     |     | *FINAL*
```
*\*Note: Week 8 Monday (Oct 12) is Fall Break. Lab Quiz 3 is administered during Thursday Oct 15 class or in Week 9 Lab.*

---

### Curriculum & Module Map

| Module | Week & Dates | Core Topics & Key Algorithms | Slides / Readings | Deliverables & Exams |
| :--- | :--- | :--- | :--- | :--- |
| **Module 1**<br>Core Foundations, Sorting & Tree Structures | **Wk 1** (Aug 24–28) | **Introduction, Efficiency & Code Profiling**<br>• Algorithmic thinking & problem-solving framework<br>• Asymptotic notation: Big-$O$, Big-$\Omega$, Big-$\Theta$<br>• Best-, worst-, and average-case complexity analysis | Slides: Aug 25 · Aug 27 | Course Orientation<br>[Lab 0](lab0/index.md) (Python/Git) |
| | **Wk 2** (Aug 31–Sep 04) | **Divide-and-Conquer & Comparison Sorting**<br>• Divide-and-conquer template<br>• Mergesort & Quicksort trace<br>• Master Theorem & recursion trees<br>• Information-theoretic lower bound ($\Omega(n \log n)$) | Slides: Sep 1 · Sep 3 | [Lab 1](lab1/lab1.md) (Memoization) |
| | **Wk 3** (Sep 07–11) | **Heaps, Heapsort & Linear-Time Sorting**<br>• Array binary tree indexing<br>• Max-Heaps and Min-Heaps<br>• Heapsort algorithm structure<br>• Breaking comparison barrier: Bucketsort / Radix Sort | Sep 08 · Sep 10 | **In-Class Quiz 1**<br>*(Mon: Labor Day Holiday)* |
| | **Wk 4** (Sep 14–18) | **Ordered Search & Balanced Binary Trees**<br>• Binary Search Tree (BST) insertion, search & deletion<br>• Structural imbalance & runtime degeneration<br>• Height balance invariants & AVL Tree rotations | Sep 15 · Sep 17 | **Lab Quiz 1**<br>[Lab 2](lab2/lab2.md) (Sorting / Trees) |
| | **Wk 5** (Sep 21–25) | **Advanced Search Structures: Multiway & Self-Adjusting Trees**<br>• Multiway search trees (B-Trees and B+ Trees)<br>• Self-adjusting trees (Splay Trees)<br>• Introduction to amortized analysis | Sep 22 · Sep 24 | **HW 1 Assigned**<br>**In-Class Quiz 2**<br>Lab 3 (AVL/Rotations) |
| **Module 2**<br>Hashing, Strings & Graph Algorithms | **Wk 6** (Sep 28–Oct 02) | **Key Lookup, Hashing & Tries**<br>• Direct addressing vs. hashing frameworks<br>• Hash functions & collision handling<br>• Digital search trees & Tries for prefix processing | Sep 29 · Oct 01 | **Lab Quiz 2**<br>Lab 4 (Multiway/Splay) |
| | **Wk 7** (Oct 05–09) | **Pattern Search & String Matching**<br>• Exact string search problem<br>• Rabin-Karp algorithm (polynomial rolling hashes)<br>• Knuth-Morris-Pratt (KMP) prefix function ($\pi$-table) | Oct 06 · Oct 08 | **HW 1 Due** (Thu Oct 8)<br>**In-Class Quiz 3**<br>*(Midterm Option A: Oct 6/8)* |
| | **Wk 8** (Oct 12–16) | **Graph Foundations & Traversals**<br>• Adjacency Matrices vs. Adjacency Lists<br>• Breadth-First Search (BFS) for shortest paths<br>• Depth-First Search (DFS) & edge classifications<br>• Topological Sorting on DAGs | Oct 15 | **HW 2 Assigned** (Thu Oct 15)<br>**Lab Quiz 3** (Thu Oct 15)<br>*(Mon–Tue: Fall Break)*<br>*(Midterm Option B: Oct 15)* |
| **Module 3**<br>Optimization & Sequence Modeling | **Wk 9** (Oct 19–23) | **Minimum Spanning Trees & Shortest Paths**<br>• Greedy algorithm design paradigm & greedy invariants<br>• Kruskal’s algorithm (Union-Find with path compression)<br>• Prim’s algorithm for MSTs<br>• Dijkstra’s single-source shortest paths on weighted graphs | Oct 20 · Oct 22 | **In-Class Quiz 4**<br>Lab 6 (Traversals/Topo) |
| | **Wk 10** (Oct 26–30) | **Network Flow & Dynamic Programming Foundations**<br>• Flow networks, cuts & Edmonds-Karp Max-Flow<br>• Dynamic Programming (DP) core principles<br>• Overlapping subproblems & optimal substructure<br>• Memoization vs. Tabulation (0-1 Knapsack) | Oct 27 · Oct 29 | **HW 2 Due** (Thu Oct 29)<br>**Lab Quiz 4**<br>Lab 7 (Kruskal/Dijkstra) |
| | **Wk 11** (Nov 02–06) | **Advanced Dynamic Programming & Sequence Alignment**<br>• Sequence similarity measurement using DP<br>• Longest Common Subsequence (LCS)<br>• Edit Distance (Levenshtein Distance)<br>• Floyd-Warshall all-pairs shortest paths | Nov 03 · Nov 05 | **HW 3 Assigned**<br>**Lab Quiz 5**<br>Lab 8 (Knapsack DP) |
| | **Wk 12** (Nov 09–13) | **Special Topic — Algorithms in NLP & Health Informatics**<br>• Parsing unstructured clinical notes & social media data<br>• Modeling token sequences & noisy data fields<br>• Optimal hidden state decoding via Viterbi Algorithm | Nov 10 · Nov 12 | **Lab Quiz 6**<br>Lab 9 (LCS / Floyd-W) |
| **Module 4**<br>Intractability & Advanced Paradigms | **Wk 13** (Nov 16–20) | **Solution Spaces, Local Search & Intro to Complexity**<br>• Exploring solution spaces when exact solutions take too long<br>• Local neighborhoods & randomized walks<br>• Greedy Local Search & Simulated Annealing<br>• Computational hardness: $\mathbf{P}$ vs. $\mathbf{NP}$ complexity classes | Nov 17 · Nov 19 | **HW 3 Due** (Thu Nov 19)<br>**In-Class Quiz 5**<br>Lab 10 (Viterbi Trellis) |
| | **Wk 14** (Nov 23–27) | **Thanksgiving Recess**<br>• No classes; university closed Nov 23–28 | — | *Thanksgiving Break* |
| | **Wk 15** (Nov 30–Dec 04) | **Approximation, Randomized Algorithms & Course Wrap-Up**<br>• Approximation algorithms with performance guarantees<br>• Las Vegas vs. Monte Carlo randomized algorithms<br>• Course synthesis & algorithmic paradigm selection matrix | Dec 01 · Dec 03 | Lab 11 (Optimization)<br>Review Materials |
| **Synthesis & Exams** | **Wk 16** (Dec 07–09) | **Course Review & Synthesis**<br>• Dec 07: Lab 12 Final Synthesis<br>• Dec 08: Last day of classes; course retrospective<br>• Dec 09: Designated Monday (makeup sessions / office hours) | Dec 08 | Lab 12 Synthesis<br>Designated Monday |
| | **Finals** (Dec 10–18) | **Comprehensive Final Examination**<br>• Cumulative coverage across Modules 1–4 | University Schedule | **FINAL EXAM** |

---

### Homework Lifecycle & Windows

Each homework assignment spans a **2-week working window**, aligned directly with the preceding lecture and lab topics:

| Assignment | Topic Focus | Assigned Date | Active Working Window | Submission Deadline |
| :--- | :--- | :--- | :--- | :--- |
| **Homework 1** | **Tree Structures**<br>BST operations, AVL rebalancing & rotations, Multiway/Splay concepts | **Week 5**<br>Mon, Sep 21, 2026 | Weeks 5 & 6<br>(17 days total) | **Week 7**<br>Thu, Oct 08, 2026 @ 23:59 |
| **Homework 2** | **Graphs & Shortest Paths**<br>BFS/DFS, Topological Sort, MST (Kruskal/Prim), Dijkstra | **Week 8**<br>Thu, Oct 15, 2026 | Weeks 8, 9 & 10<br>(14 days total) | **Week 10**<br>Thu, Oct 29, 2026 @ 23:59 |
| **Homework 3** | **Dynamic Programming**<br>0-1 Knapsack, LCS, Edit Distance, Floyd-Warshall | **Week 11**<br>Thu, Nov 05, 2026 | Weeks 11 & 12<br>(14 days total) | **Week 13**<br>Thu, Nov 19, 2026 @ 23:59 |

---

### Midterm Exam Scheduling Options & Trade-Offs

The course midterm is a single 75-minute in-class exam. Two distinct candidate placements are evaluated below:

| Option | Scheduled Date & Session | Placement Relative to Break & HW | Covered Curriculum | Key Advantages & Trade-Offs |
| :---: | :---: | :---: | :--- | :--- |
| **Option A**<br>*(Recommended)* | **Tue, Oct 06**<br>or<br>**Thu, Oct 08**<br>*(Week 7)* | **Pre-Fall Break**<br>• Held during Week 7 lecture<br>• HW 1 due Thu Oct 08 | • Module 1 (Weeks 1–5: Sorting, Heaps, BSTs, AVL, Multiway Trees)<br>• Module 2 Part 1 (Weeks 6–7: Hashing, Tries, String Matching) | **Pros:** Clean break before recess. Students take the exam while sorting, tree, and hashing concepts are completely fresh and enjoy the 4-day Fall Break (Oct 12–13) free of exam stress.<br>**Cons:** Covers 6.5 weeks of content in rapid succession; students balance HW 1 completion with exam prep. |
| **Option B** | **Thu, Oct 15**<br>*(Week 8)* | **Post-Fall Break**<br>• Mon Oct 12 & Tue Oct 13 are Fall Break holidays<br>• Thu Oct 15 is the *only* class meeting in Week 8 | • Module 1 (Weeks 1–5)<br>• Module 2 (Weeks 6–7: Hashing, Tries, String Matching) | **Pros:** Gives students the long Fall Break weekend to study without missing new lectures.<br>**Cons:** Thursday Oct 15 is the first day back from vacation; having an exam immediately upon return can feel high-stress. |

---

### Complete Deliverables Master Table

| Week | Target Date(s) | Assessment | Format | Topic Coverage |
| :---: | :---: | :--- | :--- | :--- |
| **Wk 3** | Sep 08 / 10 | **In-Class Quiz 1** | In-Class (Lecture) | Wks 1–2: Sorting, Asymptotics, Divide & Conquer |
| **Wk 4** | Sep 14 | **Lab Quiz 1** | In-Lab (Monday) | Wk 3: Heaps, Heapsort & Linear-Time Sorting |
| **Wk 5** | Sep 21 | **HW 1 Assigned** | Programming + Theory | Wks 4–5: Tree Implementations (BST, AVL, Splay) |
| **Wk 5** | Sep 22 / 24 | **In-Class Quiz 2** | In-Class (Lecture) | Wk 4: Ordered Search & Balanced Binary Trees |
| **Wk 6** | Sep 28 | **Lab Quiz 2** | In-Lab (Monday) | Wk 5: Multiway & Self-Adjusting Trees |
| **Wk 7** | Oct 06 / 08 | **In-Class Quiz 3** | In-Class (Lecture) | Wk 6: Key Lookup, Hashing & Tries |
| **Wk 7** | Oct 08 | **HW 1 Due** | Submission Deadline | HW 1 Submission (23:59) |
| **Wk 7/8** | *Oct 06, 08, or 15* | **MIDTERM EXAM** | In-Class Major Exam | Modules 1 & 2 (See Options A & B above) |
| **Wk 8** | Oct 15 | **HW 2 Assigned** | Programming + Theory | Wks 8–9: Graphs, Traversals & Shortest Paths |
| **Wk 8** | Oct 15 | **Lab Quiz 3** | In-Lab / Post-Break | Wk 7: Pattern Search & String Matching *(held Thu Oct 15 or Wk 9 Lab)* |
| **Wk 9** | Oct 20 / 22 | **In-Class Quiz 4** | In-Class (Lecture) | Wk 8: Graph Foundations & Traversals |
| **Wk 10** | Oct 26 | **Lab Quiz 4** | In-Lab (Monday) | Wk 9: Minimum Spanning Trees & Shortest Paths |
| **Wk 10** | Oct 29 | **HW 2 Due** | Submission Deadline | HW 2 Submission (23:59) |
| **Wk 11** | Nov 02 | **Lab Quiz 5** | In-Lab (Monday) | Wk 10: Network Flow & DP Foundations |
| **Wk 11** | Nov 05 | **HW 3 Assigned** | Programming + Theory | Wks 10–11: Dynamic Programming Foundations |
| **Wk 12** | Nov 09 | **Lab Quiz 6** | In-Lab (Monday) | Wk 11: Advanced DP & Sequence Alignment |
| **Wk 13** | Nov 17 / 19 | **In-Class Quiz 5** | In-Class (Lecture) | Wk 12: Algorithms in NLP & Health Informatics |
| **Wk 13** | Nov 19 | **HW 3 Due** | Submission Deadline | HW 3 Submission (23:59) |
| **Finals** | *TBA* | **FINAL EXAM** | Cumulative Exam | Comprehensive (Modules 1–4) |

