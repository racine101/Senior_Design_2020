# Senior_Design_2020

Problem Statement:

The current manual process of taking attendance in college is ineffective and inconvenient for both professors and  students. On average a professor spends between 5 to 10 minutes, sometimes even longer than that, taking class   attendance. In a 50 minute class session, that’s 10-20% of class time that's not going towards going over the class   material. Many times individual complained that they have not been recorded when they indeed were present.  

Objective:

The goal of this project is to use facial recognition with deep learning to take class attendance.  
This will reduce the time professors spend taking attendance, and increasing productivity of students and faculty.  

Prerequisites
For this lab, you should have a sound knowledge of these Linux commands:

cat
grep
cut
cat:

The cat command allows us to create single or multiple files, view the contents of a file, concatenate files, and redirect output in terminal or other files.

Syntax:

cat [file]
grep:

The grep command, which stands for "global regular expression print", processes text line-by-line and prints any lines that match a specified pattern.

Syntax:

grep [pattern] [file-directory]
Here, [file-directory] is the path to the directory/folder where you want to perform a search operation. The grep command is also used to search text and match a string or pattern within a file.

Syntax:

grep [pattern] [file-location]
cut:

The cut command extracts a given number of characters or columns from a file. A delimiter is a character or set of characters that separate text strings.

Syntax:

cut [options] [file]
For delimiter separated fields, the - d option is used. The -f option specifies the field, a set of fields, or a range of fields to be extracted.

Syntax:

cut -d [delimiter] -f [field number]
Linux I/O Redirection
Redirection is defined as switching standard streams of data from either a user-specified source or user-specified destination. Here are the following streams used in I/O redirection:

Redirection into a file using >

Append using >>

Redirection into a file
Each stream uses redirection commands. A single greater than sign (>) or a double greater than sign (>>) can be used to redirect standard output. If the target file doesn't exist, a new file with the same name will be created.

Commands with a single greater than sign (>) overwrite existing file content.

cat > [file]
Commands with a double greater than sign (>>) do not overwrite the existing file content, but it will append to it.

cat >> [file]
So, rather than creating a file, the >> command is used to append a word or string to the existing file.

