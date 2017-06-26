# This program reads all images from the defined directory, then format them as latex images blocks and finally copy the resulting string into the clipboard.
# Before running, we must activate the virtual environment using:
    # source ~/Coding/venv/bin/activate

import os, sys
import pyperclip

directory = "../../output_good/real/"
directory2 = "../../output_good/clu_values/"
template = ""

# Go over all files ordered by name
for filename in sorted(os.listdir(directory)):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        print "Adding image: " + filename
        filename = filename.replace(".png", "")
        filename = filename.replace(".jpg", "")
        complete_filename = filename
        caption = filename
        caption = caption.replace("_","\_")
        # Concatenate template
        template = template + "\\subsubsection{" + caption + "}\n"
        template = template + "\\begin{figure}[H]\n\
  \centering\n\
  \includegraphics[width=1 \\textwidth]{{{\"" + directory + complete_filename + "\"}}}\n\
  \caption{" + caption + ", plot from all methods" + "}\n\
  \label{}\n\
\end{figure}\n"

        template = template + "\\begin{figure}[H]\n\
  \centering\n\
  \includegraphics[width=1 \\textwidth]{{{\"" + directory2 + filename + "_comm"  + "\"}}}\n\
  \caption{" + caption + ", community detection sample values" + "}\n\
  \label{}\n\
\end{figure}\n"

        template = template + "\\newpage\n\n"
        continue
    else:
        continue

# Copy template to clipboard
pyperclip.copy(template)
# print pyperclip.paste()
print "output created and copied to clipboard (Just paste text using Ctrl+V)"
