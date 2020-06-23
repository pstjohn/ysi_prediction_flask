'use strict';

/*
 *  moakley
 *  Set site-level variables (required)
 */
 $(document).ready( function(){

    window.nrel = $.extend({}, window.nrel); // Merge in page level variables if they are set
    window.nrel.pagevars = $.extend({}, window.nrel.pagevars); // (in case window.nrel isn't defined)

    window.nrel.pagevars.sitename = 'AppName';

    var $navlink,
        $navitem,
        slash,
        nrel,
        pv;

    // shorthand alias for our page variables
    nrel = window.nrel || {};
    pv = nrel.pagevars || {};


    pv.pagename = $('h1').text();
    slash = location.pathname.lastIndexOf('/') + 1;

    pv.pageurl  = location.pathname;                 //  /foo/bar/baz/boink.html
    pv.siteurl  = location.pathname.substr(0,slash); //  /foo/bar/baz/
    pv.filename = location.pathname.substr(slash) ;  //  boink.html

    // catch situations where the url ends in a slash, with index.html implied
    if( ! pv.filename.length) {
        pv.filename = 'index.html'; // this could be index.php or index.cfm, or ...
    }


    /*
     * Contact Us footer link
     * if the site doesn't defer to the globalwebmaster, use the local one
     */
    if( !pv.globalwebmaster && pv.sitename ) {
        $('#contact-link').attr( 'href', pv.siteurl + 'contacts.html' );
    } else {
        $('#contact-link').attr( 'href', '/webmaster.html' );
    }

});
