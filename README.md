# Traffic Simulation using Dijkstra and A* Algorithm

## Introduction

This project is based on shortest path finding between cities using Dijkstra and A* algorithms. It helps in finding the best route from source city to destination city by considering distance and traffic conditions.

A graphical user interface is created using Python Tkinter for easy interaction. The road network is shown as a graph where cities are nodes and roads are edges. :contentReference[oaicite:0]{index=0}

---

## Objective

- To implement Dijkstra Algorithm
- To implement A* Algorithm
- To compare both algorithms
- To find shortest route between cities
- To simulate traffic conditions

---

## Software Used

- Python
- Tkinter
- NetworkX
- Matplotlib

---

## Modules in Project

### 1. Graph Creation
Cities like Chennai, Bangalore, Salem, Mysore etc are connected using roads with distance values.

### 2. Traffic Conditions
Each road has traffic status:

- Low
- Medium
- Heavy

Based on traffic, extra cost is added.

### 3. Dijkstra Algorithm
Checks shortest path by selecting minimum cost node step by step.

### 4. A* Algorithm
Uses heuristic function to reach destination faster.

### 5. GUI Output
User selects:

- Source city
- Destination city
- Algorithm

Then result is displayed.

---

## Output Details

The program displays:

- Shortest Path
- Total Cost
- Number of Nodes Visited
- Execution Time
- Visited Order

Graph is also shown visually.

---

## How to Run

1. Install Python  
2. Install libraries:

```bash
pip install networkx matplotlib