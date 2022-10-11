PowerArm Sizing Project

The PowerArm is an assistive device sold by CKD. While working there as a Mechanical Engineer I created a python based sizing tool to help specify the correct model of PowerArm, show load calculations, and generate a price. The protect the intellectual property of CKD the data included is only publicly available catalog data and sensitive pricing data is altered. 

The project is made in python with the Tkinter library. Numpy is used for calculations. Some other libraries are described below. It can be ran directly as a python file, but for production it was distributed as an executable program for windows 10. 

Installations required:

Tkinter: pip install tk
Numpy: pip install numpy
PyPDF4: pip install PyPDF4
pdf_annotate: pip install pdf-annotate
ReportLab: pip install reportlab
Fitz: pip install fitz

Using the application:

Input Information (Page 1)
-The first page is where you describe what is being picked up by the tool. Roughly descrie the shape of the workpiece as a rectangular or cylindrical prism and input the dimensions. This is followed with inputting the pressure you plan to operate the device at, as well as some radio boxes about optional features. 

End Effector (Page 2)
-The second page is where you input information about the tool at the end of the PowerArm that will pick up the work piece described on the first page. 

Application Information (Page 3)
-The third page is where you in put information regarding mass and reach required. After that you click Calculate Model Number and the application will choose the correct size, provide pricing, and display load calculations. After this the user should click "Create Order Form" in the bottom right

Create Order Form (Page 4) 
-The fourth and last page is where you input some information specific to the CKD ordering process such as environmental information, frequency of use, and customer information. After this you clikc "Generate PAW Order Form" and the application will fill out the PDF required to order a PowerArm. The filled PDF will be saved in the current working directory and the user can easily send the file to CKD to order. 
