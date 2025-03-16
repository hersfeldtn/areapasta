# areapasta
A quick tool for finding true area of regions on an equirectangular map
Made 2025 by Nikolai Hersfeldt of Worldbuilding Pasta


Python version requires numpy, .exe version is standalone.

Input map should be a raster image file in Equirectangular projection (can be any aspect ratio though), global, and extend exactly to the edges of the map. It can be any map aspect (like Cassini), but should always be oriented with the long axis horizontal (corresponding to the equator in normal aspect). Each area you want to measure should be colored in a separate unique color.

Runs through command line, will prompt you for image filename and total surface area of the globe (Earth's is 510000000 km^2 for reference), which can be any unit, and you can input 0 to show only percentages; will then display a list of each color found by their RGB or greyscale code and their true area on the globe in terms of percantage of the total and amount in units based on your input total.

You can then choose to output that result to a text or .csv file, which will be called "area_counts"
