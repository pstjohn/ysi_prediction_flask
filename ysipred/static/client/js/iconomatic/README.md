Iconomatic
===============

Detect links to native files and append the proper icon image.


This is an update to the old script to include new AJAX detection, manual overrides, custom file types, and encapsulation using jQuery plugin design pattern.


## Quick Setup
Include the scripts
```html
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.1/jquery.js"></script>
<script src="jquery.iconomatic.js"></script>
```

Initialize the plugin
```js
$(document).ready( function() {
  $('body').iconomatic();
});
```
## Options
Default plugin options:
```js
var defaults = {
     ajax:      false        // if true: listen for DOM changes using the MutationObserver object
    ,dataMode:  false        // if true: check data attributes for manually tagged links (useful for redirected links)
    ,dataAttr:  'iconomatic' // the data attribute to check for (eg data-iconomatic="pdf")
    ,iconClass: 'fileIcon'   // the CSS class to apply to the icons
    ,filesObj:  fileTypes    // an object that lists the file types to label with icons (see structure below)
};
```
## Notes
By default, both ```ajax``` and ```dataMode``` are disabled.

The ```ajax``` option may not work in all browsers. MutationObserver is a DOM4 spec.
For support see: http://caniuse.com/mutationobserver

The ```dataMode / dataAttr``` options are useful for hyperlinks that have non-normative href attributes for their filetype, or are controlled by javascript.
For example, these links would not be labeled without ```dataMode:true```:
```html
<a data-iconomatic="pdf" href="http://bit.ly/12345">Some PDF</a>
<a data-iconomatic="pdf" href="#" onclick="downloadfunction()">Some PDF</a>
```

The default file types are:
```js
avi
doc
docx
gif
jpg
m3u
mov
mp3
mp4 
mpg
mpeg
pdf
ppt
pptx
txt
wmv
xls
xlsx
xlsm
zip
```

## Dependencies
jQuery (Tested with 1.7 and 1.11)
Font Awesome

## DEV Dependencies
Grunt
grunt-contrib-uglify
