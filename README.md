# Course Network
The main purpose of this project is to visualize and then analyze the course curriculum network of SFU. However, due to limited resource, only the stem field courses will be analyzed.

## Weight of edges (optional)
The prerequisite binding—course A must be taken before course B—establishes a parent‐daughter, predecessor‐successor relationship between the courses, one that is readily modeled as a directed graph. Although one could specify B → A, where B is referencing information obtained previously in course A, I chose the alternate method that better represents the flow of information from A into B, the arc A → B. If more than one prerequisite was specified as mandatory, then equal and full weights were applied to each arc. For example, if both course A and B were required before one could take course C, then arcs A → C and B → C were both given a weight of 1.0. However, if prerequisite rules presented an option such that, for example, either course A or B (but not both) was required before C, then the total weight of 1.0 was distributed equally across arcs (e.g., A → C, 0.5; B → C, 0.5).

## Corequisites (optional)
A hard corequisite binding—coregistration in course X—establishes a symmetric relationship between courses, particularly if both courses reference the other as a corequisite. Here, it generally is assumed that a student will enrol for both courses A and B in the same term, as is typical of lecture/lab combinations in the sciences, or more broadly when a theory course is temporally bound to a practical applications course. We can represent this symmetric binding with a bidirectional arc between the courses in the CPN (A ← → B, Fig. 1), with equal weights in both directions (A → B, 1.0; B → A, 1.0). However, this bidirectional edge introduces a 2‐member cycle, and the CPN no longer can be treated as a directed acyclic graph (DAG).

A soft corequisite binding—credit or coregistration in course X—establishes a slightly asymmetric relationship between courses, particularly if only one course of the two names the other as a corequisite. Although most students likely will take A and B together, the option exists to take course A first and B later. This allowance of temporal priority also suggests a certain amount of conceptual priority. One might ask, if a student were to take the courses in different terms, which should come first? I expect most would agree that a lecture should precede a lab, not the other way around. By this argument, one might treat some corequisite courses as conceptually, if not temporally, prior in the curriculum.

In the Benedictine University catalogue, this was a reasonable interpretation since all corequisite pairings contained one course (A) that served as a “lecture” or “theory” course and the other (B) as a “laboratory” or “applied” course. Consequently, I elected to interpret all corequisite relationships as soft corequisite bindings, allowing their coding as prerequisites (A → B), thus preserving the DAG structure; this was not critical to the analyses performed in the present study. The hypothetical example in Fig. 1 shows two instances of corequisite bindings between a lecture and a lab, wherein a cycle is introduced if a bidirectional arc is used, whereas DAG structure is preserved if only the lab carries the co(pre)requisite.


### Installation
`pip install -r requirements.txt`

## Project Structure
`/course_network_analysis`
- `scraper.py`: used to scrape all course names and their prerequisites.
- `make_nx_graph.py`: used to make NetworkX graph, and we do analysis using NetworkX's built-in functions.
- `/courses` 
Each file is a json file. Each item in the list of json is a dictionary. <br>
Example: <br>
{<br>
    "label": "MATH 151", <br>
    "name": "Calculus I", <br>
    "prereq": ["MATH 100"],<br>
    "weight": [1]<br>
}