var app = app || {};

app.AddTriggerView = Backbone.View.extend({

    initialize : function() {

        this.$el.undelegate('click')

        var self = this

        if ( !($.isFunction(this.template)) ){

            $.get('/static/js/templates/addTrigger.handlebars', function(tmpl){

                marker = undefined
                self.template = tmpl
                self.render()
                var accentClass = $('.active-adj').html() + "-accent"

                $('#spatial_trigger_heading').addClass(accentClass)

                console.log("done rendering")
                console.log($('#add_trigger_map'))

                setTimeout(self.renderMap, 500)

                
                // var itp = L.circle([40.72944585471527, -73.99366021156311], 150, {
                //     color: 'red',
                //     fillColor: '#f03',
                //     fillOpacity: 0.5
                // }).addTo(map);

                // var chipotle = L.circle([40.73112880602221, -73.9935314655304], 150, {
                //     color: 'green',
                //     fillColor: '#00ff00',
                //     fillOpacity: 0.5
                // }).addTo(map);
                // map.addLayer(osm);

                $.when( $.getJSON('/v1/data/pdarche/body/location?source__icontains=foursquare'))
                 .done( function(data){
                    var locations = _.pluck(data, 'venue_name')
                    locations = _.uniq(locations)
                    $('#trigger_location input').autocomplete({
                        source : locations
                    })
                 })

            })

        } else {

            console.log("gots the template")

        }

    },

    render : function( data ) {

        var source = $(this.template).html();
        var template = Handlebars.compile( source );
        this.$el.html( template );

    },

    renderMap : function(){

        this.map = new L.Map('add_trigger_map_thing');
        // create the tile layer with correct attribution
        var osmUrl='http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
        var osm = new L.TileLayer(osmUrl, {minZoom: 8, maxZoom: 20});
        // // start the map in BROOKLYN
        this.map.setView(new L.LatLng(40.72944585471527,-73.99366021156311), 15);
        marker = L.marker([40.72944585471527, -73.99366021156311]).addTo(this.map)
    
    },

    events : {

        "click #new_trigger_submit" : "submitTrigger"

    },

    submitTrigger : function(){

        var trigger_distance = $('#trigger_distance input').val(),
            trigger_location = $('#trigger_location input').val(),
            trigger_text = $('#add_trigger_text textarea').val(),
            for_rec_habit_key = $('.chosen-action').attr('id'),
            data

        data = {
            "trigger_distance" : trigger_distance,
            "trigger_location" : trigger_location,
            "trigger_text" : trigger_text,
            "for_rec_habit_key" : for_rec_habit_key
        }

        console.log("firin this bitch?")

        $.ajax({
            url : '/v1/ref/traits/traitSpecifics/recommendedHabit/triggers',
            type : 'POST',
            data : data,
            success : function(){
                console.log("great success!")
            }
        })

    }

    // toggleActions : function( ev ){

    //     var newAdj = $(ev.target).attr('class')

    // }

})