var app = app || {};

app.TriggersView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/triggers.handlebars', function(tmpl){
                self.template = tmpl
                self.render()
                var accentClass = $('.active-adj').html() + "-accent"
                $('.action').eq(0).addClass(accentClass + ' chosen-action')

                console.log("adding this mother f'n map")

                var map = new L.Map('trigger_map');

                // create the tile layer with correct attribution
                var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
                var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 12});       

                // start the map in South-East England
                map.setView(new L.LatLng(51.3, 0.7),9);
                map.addLayer(osm);

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function() {

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.append( template );

    }

    // events : {

        // "click .nav-adjective" : "toggleActions"

    // }

    // toggleActions : function( ev ){

    //     var newAdj = $(ev.target).attr('class')

    // }

})