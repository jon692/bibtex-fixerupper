# bibtex-fixerupper
Reads through a BibTex library text file and cleans it up with a variety of functions. Also writes a change and alert log.

Note that there is a test.txt file you can use to test. I've also included the output and log files for that test file.


Basic instructions:
1) Copy and paste your BibTex library into a text file. SaveAs with a txt extension. If you have special characters, it will warn you that you need to save it with a different encoding. That's fine. Use utf-16-le or utf-8. If there were others of interest, we could deal with them in the future. Save this file to your hard drive.

2) Before running the fixerupper python code on your BibTex text file, peruse the main function (at the bottom) and make sure you like what it's doing. I built it for my purposes. Right now, it:
  - changes non-ascii characters to a LaTeX form of those characters
  - deletes extra spaces on the left-hand side
  - cleans up the spacing (e.g., makes each field one single line [title = {Some Catchy Title},\n])
  - deletes the abstract field
  - comments out the note field
  - adds the DOI or URL code (whichever is missing)
  - formats the page field nicely
  It also creates a log of all the changes that it made, in addition to giving you some other comments such as:
  - gives a nice list of journals so you can see that they are all the same length format
  - gives you a nice list of titles so you can see if you need to fix any formatting issues (e.g., put molecule names in \ch{CH3NH3PbI3})
  - tells you if any entries are missing or have blank author, title, journal, year, or volume fields
  
3) Run the main function. main(r'path',textfilename.txt)
  
4) If there were any notifications printed, best wishes handling them.

5) Find the output file and the log file in the same directory as the BibTex file. I would suggest going through the log very closely to make sure you like the changes. Note that the original file was not touched.

6) Copy and paste the BibTeX from the output file back into your LaTeX project. Done!
