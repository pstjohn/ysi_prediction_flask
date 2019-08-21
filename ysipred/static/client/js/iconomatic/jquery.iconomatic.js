;(function ( $, window, document, undefined ) {

    'use strict';

    // Default file types to label with icons
    var fileTypes = {
          'avi' : { 'class' : 'fa-file-video-o',      'type' : 'Video'}
        , 'doc' : { 'class' : 'fa-file-word-o',       'type' : 'Microsoft Word'}
        , 'docx': { 'class' : 'fa-file-word-o',       'type' : 'Microsoft Word'}
        , 'gif' : { 'class' : 'fa-file-image-o',      'type' : 'GIF'}
        , 'jpg' : { 'class' : 'fa-file-image-o',      'type' : 'JPG'}
        , 'm3u' : { 'class' : 'fa-file-audio-o',      'type' : 'Audio'}
        , 'mov' : { 'class' : 'fa-file-video-o',      'type' : 'Video'}
        , 'mp3' : { 'class' : 'fa-file-audio-o',      'type' : 'Audio'}
        , 'mp4' : { 'class' : 'fa-file-video-o',      'type' : 'Video'}
        , 'mpg' : { 'class' : 'fa-file-video-o',      'type' : 'Video'}
        , 'mpeg': { 'class' : 'fa-file-video-o',      'type' : 'Video'}
        , 'pdf' : { 'class' : 'fa-file-pdf-o',        'type' : 'PDF'}
        , 'ppt' : { 'class' : 'fa-file-powerpoint-o', 'type' : 'Microsoft PowerPoint'}
        , 'pptx': { 'class' : 'fa-file-powerpoint-o', 'type' : 'Microsoft PowerPoint'}
        , 'wmv' : { 'class' : 'fa-file-video-o',      'type' : 'Video'}
        , 'txt' : { 'class' : 'fa-file-text-o',       'type' : 'Text'}
        , 'xls' : { 'class' : 'fa-file-excel-o',      'type' : 'Microsoft Excel'}
        , 'xlsb': { 'class' : 'fa-file-excel-o',      'type' : 'Microsoft Excel'}
        , 'xlsx': { 'class' : 'fa-file-excel-o',      'type' : 'Microsoft Excel'}
        , 'xlsm': { 'class' : 'fa-file-excel-o',      'type' : 'Microsoft Excel'}
        , 'zip' : { 'class' : 'fa-file-archive-o',    'type' : 'ZIP Archive'}
    };


    var pluginName = 'iconomatic';

    // Plugin defaults
    var defaults = {
         ajax:      false
        ,dataMode:  false
        ,dataAttr:  'iconomatic'
        ,iconClass: 'fileIcon'
        ,filesObj:  fileTypes
    };

    // Constructor
    function Iconomatic( element, options ) {
        this.element = element;

        this.options = $.extend( {}, defaults, options );

        this._defaults = defaults;
        this._name = pluginName;

        this.init();
    }

    Iconomatic.prototype = {

        init: function() {
            var links,
                context;

            context = $('body');    // todo: move this into settings

            links = this.getLinks( context );
            this.addIcons( links );

            if( this.options.ajax ) {
                this.enableAjax();
            }
        },

        /*
         *  Inspect all <a> tags within our region
         *  Return the ones with relevant file extensions or data attributes
         *
         */
        getLinks: function( region ) {
            var opts,
                types,
                dataAttr,
                links;

            opts     = this.options;
            types    = opts.filesObj;
            dataAttr = 'data-' + opts.dataAttr;

            links = [];

            $(region).find('a').filter(function(){
                 return !$(this).attr('data-iconomatic-tagged'); // remove any previously tagged
            }).each( function( idx, link ){
                var href,
                    ext;


                href = $(link).attr('href');

                if( typeof href !== 'undefined' && href !== null && href !== '' ) {

                    ext = href.toLowerCase().split('.').splice( -1, 1 ).toString(); // this could be more elegant

                    if( ext in types ) {
                        $(link).attr('data-iconomatic-tagged', ext); // tag our valid links
                        links.push( link );
                    }
                }
                if( opts.dataMode ) {

                    // copy the users data attribute to our data attribute
                    if( $(link).attr(dataAttr) ) {

                        $(link).attr('data-iconomatic-tagged', function(){ // tag our valid links
                            return $(this).attr( dataAttr );
                        });

                        links.push( link );
                    }
                }
            });

            return links;
        },

        /*
         *  Use the mutation observer to watch for changes in our doc.
         *  Find the Links and add the icons in the changed region.
         *
         */
        enableAjax: function(){
            var links,
                MutationObserver,
                region,
                observer,
                self = this;

            if( window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver ) {
                MutationObserver = window.MutationObserver || window.WebKitMutationObserver || window.MozMutationObserver;
            } else {
                return true; // BAIL ON <IE11
            }

            region   = document.querySelector('body');
            observer = new MutationObserver( function(mutations) {

                mutations.forEach( function(mutation) {
                    if (mutation.type === 'childList') {
                        links = self.getLinks( mutation.target );
                        self.addIcons( links );
                    }
                });
            });

            observer.observe(region, {
                childList: true,
                subtree: true
            });
        },

        /*
         *  Append the icon image on the link
         *
         */
        addIcons: function( links ) {
            var opts = this.options;

            $(links).filter(function() {
                return $(this).has('img').length === 0; // don't label things link lightboxes
            }).each( function( idx, link ){
                var fileType,
                    theClass,
                    attrs;

                fileType = $(link).data('iconomatic-tagged');

                theClass  = ( typeof opts.filesObj[fileType] !== 'undefined' ) ?  opts.filesObj[fileType].class : false;

                if( theClass ) {

                    attrs = {
                        'class' : opts.iconClass + ' fa ' + theClass
                      , 'title' : opts.filesObj[fileType].type
                    };

                    $( '<i />', attrs ).appendTo(link); // finally do the work!
                }
            });
        }

    };

    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, 'plugin_' + pluginName)) {
                $.data(this, 'plugin_' + pluginName, new Iconomatic( this, options ));
            }
        });
    };


})( jQuery, window, document );
