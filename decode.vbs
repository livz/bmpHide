' Decode and dump a base64 encoded file
' Usage: cscript decode.vbs [inFile] [outFile]
' E.g.: cscript decode.vbs binary.txt binary.out

Dim inFile, outFile
inFile = WScript.Arguments(0)
outFile = WScript.Arguments(1)

Dim objFS, objTS
Set objFS = CreateObject("Scripting.FileSystemObject")
Set objTS = objFS.OpenTextFile(inFile, 1)

Dim base64Encoded, base64Decoded
base64Encoded = objTS.ReadAll
base64Decoded = decodeBase64(base64Encoded)

writeBytes outFile, base64Decoded

Private Function decodeBase64(base64)
	Dim DM, EL
	Set DM = CreateObject("Microsoft.XMLDOM")
    ' Create temporary node with Base64 data type
	Set EL = DM.createElement("tmp")
	EL.DataType = "bin.base64"
	' Set encoded String, get bytes
	EL.Text = base64
	decodeBase64 = EL.NodeTypedValue
End Function

Private Sub writeBytes(file, bytes)
	Dim binaryStream	
	Set binaryStream = CreateObject("ADODB.Stream")
	
	binaryStream.Type = 1	' adTypeBinary
	'Open the stream and write binary data
	binaryStream.Open
	binaryStream.Write bytes
	binaryStream.SaveToFile file, 2  ' adSaveCreateOverWrite
End Sub
