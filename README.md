# Arabic Morphological Search Engine

This project is a search and generation engine for Arabic morphology. It manages trilateral roots and applies morphological patterns to generate or verify derived words.

## Features

- **Root Management**: Add, search, and delete trilateral roots.
- **Pattern Management**: Store and manipulate morphological templates.
- **Morphological Generation**: Generate a word from a root and a pattern, or generate the entire morphological family.
- **Validation**: Check whether a word is derived from a specific root by identifying the matching pattern.
- **Multiple Interfaces**:
  - Interactive graphical user interface (GUI) built with **Flet**.
  - Command-line interface (CLI) for quick usage.

## Data Structures

The engine's efficiency relies on two core data structures:

1. **AVL Tree**: Used to store roots. This is a self-balancing binary search tree that guarantees optimal search performance ($O(\log n)$).
2. **Hash Table**: Used to index patterns. It uses a polynomial rolling hash function and handles collisions via chaining.

## Complexity Analysis

### Time Complexity

| Operation | Structure | Average Case | Worst Case |
| :--- | :--- | :--- | :--- |
| **Root Insertion** | AVL Tree | $O(\log n)$ | $O(\log n)$ |
| **Pattern Lookup** | Hash Table | $O(1)$ | $O(k)$ |
| **Generation** | Substitution | $O(L)$ | $O(L)$ |
| **Validation** | Exhaustive Search | $O(P \times L)$ | $O(P \times L)$ |

*Note: $n$ is the number of roots, $L$ is the pattern length, and $P$ is the number of patterns.*

### Space Complexity

- **AVL Tree**: $O(N)$ where $N$ is the number of stored roots.
- **Hash Table**: $O(S + P)$ where $S$ is the table size and $P$ is the number of patterns.

## Installation and Usage

### Prerequisites

- Python 3.9+
- Pip (package manager)

### Installation

1. Clone the repository or download the files.
2. Install the required dependencies:
```bash
   pip install -r requirements.txt
```

### Running the Application

#### Graphical Interface (GUI)

To launch the application with the visual interface:
```bash
python main.py
```

#### Terminal Interface (CLI)

To use the engine directly from your terminal:
```bash
python cli.py
```

#### Unit Tests

To verify the integrity of the system:
```bash
python -m unittest tests/test_morphology.py
```

## 📝 Technical Report

Full technical documentation is available in `rapport_technique.md`.
