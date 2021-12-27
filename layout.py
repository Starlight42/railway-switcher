html_template = """<!doctype html>
<html>
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
html {
font-family: Arial;
display: inline-block;
margin: 0px auto;
text-align: center;
}
.button {
background-color: #ce1b0e;
border: none;
color: white;
padding: 16px 40px;
text-align: center;
text-decoration: none;
display: inline-block;
font-size: 16px;
margin: 4px 2px;
 cursor: pointer;
 }
.button1 {
background-color: #000000;
}
</style>
</head>
<body>
<h2>Railway Switcher Web Server</h2>
<p>Switcher 01 : </p>
<p>
<i style="color:#000000;"></i>
<a href=\"?switcher01\"><button class="button button1">Switch Railway 01</button></a>
</p>
<p>Switcher 02 : </p>
<p>
<i style="color:#000000;"></i>
<a href=\"?switcher02\"><button class="button button1">Switch Railway 02</button></a>
</p>
</body>
</html>"""


