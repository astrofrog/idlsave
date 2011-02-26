<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
   "http://www.w3.org/TR/html4/loose.dtd">

<html>
   <head>
      <link rel="stylesheet" href="style.css" type="text/css" media="screen" title="no title" charset="utf-8">
      <link rel="stylesheet" href="style_code.css" type="text/css" media="screen" title="no title" charset="utf-8">
   </head>
   <body>
      <div id="main">
         
         <div class='title'>IDLSave - a python module to read IDL 'save' files</div><br>
         
         <div class='subtitle'>News!</div><br>
         
         The IDLSave code is now in <b><code>scipy.io</code></b>! At the moment, it is only available through the svn version of SciPy, but it should be included in future stable releases (from 0.9.0 onwards). To use the version in <code>scipy.io</code>, you can use <b><code>from scipy.io.idl import readsav</code></b> and then use <b><code>readsav</code></b> as you would use <code>idlsave.read</code>.<br><br>
         
         At this time, the standalone <code>idlsave</code> package on this page will be maintained in parallel with the <code>scipy.io.idl</code> version.<br><br>
         
         <div class='subtitle'>Introduction</div><br>
         
         IDLSave is a pure python module to import variables
         from IDL 'save' files (e.g. .sav) into python, and does <b>not</b> require IDL to
         work. It has a very simple command-line interface, and converts all
         IDL variables to python types. Arrays are converted to Numpy arrays, and Structures are converted to Numpy record arrays.
         <br><br>
         
         <center>
         <a href="https://github.com/astrofrog/idlsave/archives/master">Download the latest version</a><br>(0.9.7, released 18 August 2010)
         </center>
         <br>

         This program is distributed with permission from ITT Visual Information Systems.         

         To report bugs and request features, please use the <a href="https://github.com/astrofrog/idlsave/issues">issue tracker</a>. To contact me directly, please use <b>thomas dot robitaille [at] gmail dot com</b>.<br><br>

         To follow the development and get a copy of the latest development code, visit the <a href="https://github.com/astrofrog/idlsave">GitHub</a> pages.
         
         <div class='subtitle'>Changes</div>
         
         <ul>
            <li>0.9.7: Code style changes to conform to scipy coding guidelines. This version is identical to the initial version committed to scipy.io.idl
            <li>0.9.6: Added unit tests. Results are now returned as a dictionary of variables. Variables can be added to an existing dictionary. Scalars are returned with correct Numpy type. Code re-released under MIT license.
            <li>0.9.5: Implemented reading in IDL .sav files written with the <code>/COMPRESS</code> option
            <li>0.9.4: Fixed bug with pre-defined IDL structures
            <li>0.9.3: Implemented reading in of IDL pointers
            <li>0.9.2: Fixed reading of byte values/arrays
            <li>0.9.1: Implemented reading in of IDL structures as record arrays
            <li>0.9.0: Initial release
         </ul>
         
         <div class='subtitle'>Installation</div><br>
         
         To install, simply run <code>python setup.py install</code> inside
         the <code>IDLSave-x.x.x directory</code>.
         Alternatively, IDLSave can be installed using <code>easy_install idlsave</code> if you have <code>setuptools</code> installed.<br><br>

         The only dependency for IDLSave is <a href="http://numpy.scipy.org/">Numpy</a> (1.3.0 or later)<br><br>
                  
         <div class='subtitle'>Quick start</div><br>
         
         The following example demonstrates how to read a <code>.sav</code> file into
         python. This is done using the <code>idlsave.read</code> method,
         which returns an <code>IDLSaveFile</code> instance. The variables
         are then accessible as attributes to the <code>IDLSaveFile</code>
         instance. Variable names are not case-sensitive. For structures (i.e. recarrays),
         variable names can be access either lower or upper case, but not
         mixed-case.<br>
         
         <div class='code'>
         <?php include('demo2.php');?>
         </div>
         
         <div class='copyright'>
             Many thanks to Craig Markwardt for publishing the <a href="http://www.physics.wisc.edu/~craigm/idl/savefmt/">Unofficial Format Specification</a> for IDL <code>.sav</code> files, without which this Python module would not exist. IDL&reg; is a registered trademark of ITT Visual Information Systems, Inc. for their Interactive Data Language software.
         </div>
         
      </div>
   </body>
</html>
