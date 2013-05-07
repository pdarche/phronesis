var app = app || {};

app.TriggersView = Backbone.View.extend({

    initialize : function() {

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/currentSpatialTriggers.handlebars', function(tmpl){
                // var currentSpatialTriggers = [
                //     {"trigger_distance" : .05, "trigger_location" : "ITP", "trigger_text" : "take the stairs"},
                //     {"trigger_distance" : .05, "trigger_location" : "Chipotle", "trigger_text" : "leave off the cheese"}
                // ]

                var recHabitId = $('.chosen-action').attr('id'),
                    url = '/v1/ref/traits/traitSpecifics/recommendedHabit/triggers?for_rec_habit_key__icontains=' + recHabitId

                $.when( $.getJSON(url) )
                 .done(function(data){
                    console.log("the trigger data is", data)

                    var marker = undefined
                    self.template = tmpl
                    self.render( data )
                    var accentClass = $('.active-adj').html() + "-accent"

                    $('#spatial_trigger_heading').addClass(accentClass)

                    var map = new L.Map('trigger_map');

                    // create the tile layer with correct attribution
                    var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
                    var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 20});       

                    // start the map in South-East England
                    map.setView(new L.LatLng(40.72944585471527,-73.99366021156311), 15);
                    // marker = L.marker([40.72944585471527, -73.99366021156311]).addTo(map),
                    var itp = L.circle([40.72944585471527, -73.99366021156311], 150, {
                        color: 'red',
                        fillColor: '#f03',
                        fillOpacity: 0.5
                    }).addTo(map);

                    var chipotle = L.circle([40.73112880602221, -73.9935314655304], 150, {
                        color: 'green',
                        fillColor: '#00ff00',
                        fillOpacity: 0.5
                    }).addTo(map);
                    map.addLayer(osm);

                 })



            })

        } else {

            console.log("gots the template")

        }

    },

    render : function( data ) {

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template({ "currentTriggers" : data }) );

    }

    // events : {

        // "click .nav-adjective" : "toggleActions"

    // }

    // toggleActions : function( ev ){

    //     var newAdj = $(ev.target).attr('class')

    // }

})