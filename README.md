# CMPM147Midterm

## Product

This is a generator that will create a graph of nodes represented in a line of columns, where each node connects to either one or two other nodes in an adjacent column. The number of nodes in each column will be determined on the parameters explained later and then randomly increased or decreased by one for the next column. The exceptions to this rule are the start and end nodes, which will always connect to every node in the adjacent column.

## Running the tool

You can run this generator by first downloading the GraphGenerator python file and opening it in terminal or through an IDE of your choice. Running the program will cause a Tkinter GUI to pop up and you will be able to change parameters and then press a generate button on the GUI screen to generate the graph. Once you are satisfied with the outcome, you may choose to save the graph (in adjacency matrix syntax of [Node0, Directed_Edges], [Node1, Directed_Edges] ... etc.) by pressing the Save Graph button when a graph is displayed. The saved file will return as "Saved_Graph_Output.JSON", AND IT WILL BE OVERRIDDEN BY SEQUENTIAL SAVES! 

## Parameters

This generator has three paramters which alter the shape of the graph: Maximum Depth, which determines how many columns the graph has (including the start and end nodes), Maximum Width, which determines the potential number of nodes that a column can hold, and Minimum Width, which determines both the starting number of nodes in the second column and the minimum number of nodes which can be present in a column. The Minimum Width cannot be higher than the Maximum Width.

## Example Outputs

Here is an example of the graph:


Here is the saved output of the graph in JSON:

## Limitations

This tool does not have a means of changing the connections in the graph, unless its algorithm was changed. Please do not generate graphs of a scale where Maximum Depth or Maximum/Minimum Width > 50, or where negative numbers are given. The outputs for the latter will not error, but they will be straight lines; as for the former, they will cause considerable strain on the Tkinter GUI for attempting such large renderings. When the parameters are larger than 10, the interface will begin to reach a size larger than the screen; the program will still save products of this size to JSON, but to prevent potential errors it is suggested that parameters with numbers larger than 50 are not to be saved. 
